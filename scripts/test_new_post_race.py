#!/usr/bin/env python3
"""WP-560 Ф12: reservation verification and real-process scaffold race tests.

Run: python3 scripts/test_new_post_race.py
All GitHub responses are served by a local fake gh executable. No live
reservation, publication, network request or authentication store is used.
"""

import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from uuid import UUID

REPO_ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "repos/example/posts"
SNAPSHOT = "a" * 40
TREE = "b" * 40
DRAFT_ID = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
OTHER_ID = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"


def reservation(draft_id=DRAFT_ID, number=233):
    return {"draft_id": draft_id, "artifact_type": "post", "post_number": number,
            "timestamp": "2026-09-25T12:00:00.000Z"}


def tree_snapshot(root):
    return {str(path.relative_to(root)): path.read_bytes() if path.is_file() else None
            for path in root.rglob("*")}


class NewPostReservationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="new-post-reservation-")
        self.addCleanup(self.temp.cleanup)
        self.tmp = Path(self.temp.name)
        self.root = self.tmp / "repo"
        (self.root / "scripts").mkdir(parents=True)
        for name in ("new-post.py", "_publish_convention.py"):
            shutil.copy2(REPO_ROOT / "scripts" / name, self.root / "scripts" / name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(["git", "-C", str(self.root), "remote", "add", "origin",
                        "https://github.com/example/posts.git"], check=True)
        self.bin = self.tmp / "bin"
        self.bin.mkdir()
        (self.bin / "git").symlink_to(shutil.which("git"))
        self.gh = self.bin / "gh"
        self.gh.write_text(f"#!{sys.executable}\n" + '''import json
import os
import pathlib
import re
import sys

fixture_dir = pathlib.Path(os.environ["GH_FIXTURE_DIR"])
fixture = json.loads((fixture_dir / "responses.json").read_text())
with (fixture_dir / "calls.jsonl").open("a") as calls:
    calls.write(json.dumps(sys.argv[1:]) + "\\n")
if fixture.get("error"):
    print("sensitive-auth-sentinel", file=sys.stderr)
    raise SystemExit(1)
endpoint = sys.argv[-1]
if endpoint == "graphql" and endpoint not in fixture:
    query = next(arg[6:] for arg in sys.argv if arg.startswith("query="))
    fields = re.findall(r'b([0-9]+):object[(]oid:"([a-f0-9]+)"[)]', query)
    response = {"data": {"repository": {"b" + alias: fixture["_blobs"].get(oid)
                                       for alias, oid in fields}}}
else:
    response = fixture[endpoint]
print(response if isinstance(response, str) else json.dumps(response))
''', encoding="utf-8")
        self.gh.chmod(0o755)
        self.env = {**os.environ, "PATH": str(self.bin), "GH_FIXTURE_DIR": str(self.tmp)}
        self.env.pop("PYTHONDONTWRITEBYTECODE", None)
        self.set_log([reservation()])

    def set_log(self, entries):
        log = entries if isinstance(entries, str) else "\n".join(map(json.dumps, entries)) + "\n"
        self.responses = {
            REPOSITORY: {"default_branch": "main"},
            f"{REPOSITORY}/commits/main": {"sha": SNAPSHOT, "commit": {"tree": {"sha": TREE}}},
            f"{REPOSITORY}/contents/docs/_allocator-log.jsonl?ref={SNAPSHOT}": {
                "type": "file", "encoding": "base64",
                "content": base64.b64encode(log.encode()).decode(),
            },
            f"{REPOSITORY}/git/trees/{TREE}?recursive=1": {
                "sha": TREE, "truncated": False, "tree": [],
            },
        }
        self.save_responses()

    def save_responses(self):
        (self.tmp / "responses.json").write_text(json.dumps(self.responses), encoding="utf-8")

    def set_history(self, files):
        entries = []
        blobs = {}
        for path, text in files.items():
            content = text.encode("utf-8")
            oid = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
            entries.append({"path": path, "mode": "100644", "type": "blob",
                            "sha": oid, "size": len(content)})
            blobs[oid] = {"oid": oid, "byteSize": len(content), "isBinary": False,
                          "isTruncated": False, "text": text}
        self.responses[f"{REPOSITORY}/git/trees/{TREE}?recursive=1"]["tree"] = entries
        self.responses["_blobs"] = blobs
        self.save_responses()

    def start_post(self, *, draft_id=DRAFT_ID, number=233, slug="test-post", title="Test post",
                   extra=(), python_flags=()):
        cmd = [sys.executable, *python_flags, str(self.root / "scripts" / "new-post.py"),
               "--date", "2026-09-25", "--slug", slug, "--title", title,
               "--channels", "club,telegram"]
        if draft_id is not None:
            cmd += ["--draft-id", draft_id]
        if number is not None:
            cmd += ["--post-number", str(number)]
        return subprocess.Popen(cmd + list(extra), env=self.env, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)

    def run_post(self, **kwargs):
        process = self.start_post(**kwargs)
        stdout, stderr = process.communicate(timeout=15)
        return process.returncode, stdout, stderr

    def assert_rejected_without_writes(self, **kwargs):
        before = tree_snapshot(self.root)
        code, stdout, stderr = self.run_post(**kwargs)
        self.assertNotEqual(code, 0, stdout)
        self.assertEqual(before, tree_snapshot(self.root), stderr)
        self.assertNotIn("sensitive-auth-sentinel", stdout + stderr)
        self.assertNotIn("Traceback", stderr)
        return stderr

    def add_local_post(self, number=232, draft_id=None):
        path = self.root / "docs" / "2026" / "legacy-1-club-2026-09-01.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        content = f"---\npost_number: {number}\n"
        if draft_id:
            content += f"draft_id: {draft_id}\n"
        path.write_text(content + "---\nExisting body must survive.\n", encoding="utf-8")
        return path

    def test_missing_or_invalid_arguments_never_write(self):
        for kwargs in ({"draft_id": None}, {"number": None}, {"draft_id": "not-a-uuid"},
                       {"number": 0}, {"number": -1}, {"number": 2**53}):
            with self.subTest(kwargs=kwargs):
                self.assert_rejected_without_writes(**kwargs)
        self.assertFalse((self.tmp / "calls.jsonl").exists())

    def test_gh_unavailable_never_writes(self):
        self.gh.unlink()
        self.assert_rejected_without_writes()

    def test_unauthenticated_gh_never_writes_or_exposes_diagnostics(self):
        self.responses = {"error": True}
        self.save_responses()
        self.assert_rejected_without_writes()

    def test_missing_or_mismatched_reservation_never_writes(self):
        for entries in ([], [reservation(OTHER_ID)], [reservation(number=234)]):
            with self.subTest(entries=entries):
                self.set_log(entries)
                self.assert_rejected_without_writes()

    def test_stale_local_max_cannot_claim_another_drafts_remote_number(self):
        self.add_local_post(232)
        self.set_log([reservation(OTHER_ID, 233)])
        self.assert_rejected_without_writes()
        self.assert_rejected_without_writes(draft_id=None, number=None)

    def test_old_valid_reservation_cannot_reuse_remote_legacy_number_missing_locally(self):
        self.set_log([reservation(number=1)])
        path = "docs/2025/001-1-club-2025-01-01.md"
        self.set_history({path: "# Historic post without frontmatter\n"})
        error = self.assert_rejected_without_writes(number=1)
        self.assertIn(path, error)

    def test_remote_same_uuid_is_never_overwritten_even_with_a_different_number(self):
        path = "docs/2026/01-09-1-club-2026-09-01.md"
        self.set_history({path: f"---\npost_number: 232\ndraft_id: '{DRAFT_ID.upper()}'\n---\nBody\n"})
        error = self.assert_rejected_without_writes()
        self.assertIn(path, error)

    def test_monthly_prefix_and_body_citations_are_not_global_number_or_ownership(self):
        self.set_log([reservation(number=1)])
        citation = f"\n```yaml\npost_number: 1\ndraft_id: {DRAFT_ID}\n```\n"
        files = {
            "docs/2026/01-09-1-club-2026-09-01.md": "# Monthly folder prefix only\n",
            "docs/2026/02-09-1-club-2026-09-02.md": "---\npost_number: 232\n---\n" + citation,
            "docs/2026/03-09-1-club-2026-09-03.md": '---\ntitle: "Example\npost_number: 1\n"\n---\n',
        }
        self.set_history(files)
        local = self.add_local_post(232)
        local.write_text(local.read_text() + citation)
        code, stdout, stderr = self.run_post(number=1)
        self.assertEqual(code, 0, stdout + stderr)
        self.assertEqual(len(list((self.root / "docs").glob("**/*-1-club-*.md"))), 2)

    def test_quoted_yaml_number_keys_and_values_are_checked(self):
        path = "docs/2026/01-09-1-club-2026-09-01.md"
        self.set_history({path: '---\n"post_number": "233" # comment\n---\n'})
        self.assertIn(path, self.assert_rejected_without_writes())

    def test_yaml_null_is_absent_number_and_only_legacy_names_supply_fallback(self):
        for scalar in ("null", "", "~", "NULL"):
            with self.subTest(scalar=scalar):
                monthly = "docs/2026/01-09-1-club-2026-09-01.md"
                legacy = "docs/2026/233-1-club-2026-09-01.md"
                self.set_history({monthly: f"---\npost_number: {scalar}\n---\n"})
                code, stdout, stderr = self.run_post(slug=f"null-{len(scalar)}")
                self.assertEqual(code, 0, stdout + stderr)
                shutil.rmtree(self.root / "docs")
                self.set_history({legacy: f"---\npost_number: {scalar}\n---\n"})
                error = self.assert_rejected_without_writes()
                self.assertIn(legacy, error)

    def test_null_number_with_uuid_and_no_legacy_fallback_is_ambiguous(self):
        path = "docs/2026/01-09-1-club-2026-09-01.md"
        self.set_history({path: f"---\npost_number: null\ndraft_id: {OTHER_ID}\n---\n"})
        error = self.assert_rejected_without_writes()
        self.assertIn("не связан с глобальным номером", error)

    def test_ambiguous_or_malformed_yaml_stops_before_writes(self):
        path = "docs/2026/01-09-1-club-2026-09-01.md"
        headers = [
            'post_number: 232\n"post_number": 231',
            f'draft_id: {OTHER_ID}\n"draft_id": {DRAFT_ID}',
            'defaults: &base {post_number: 232}\n<<: *base',
            "post_number: [232]", "post_number: 0", "post_number: true",
            'post_number: "null"', "post_number: !!null 233",
            "post_number: " + "1" * 5000,
            "number: &number 232\npost_number: *number",
            "post_number: |-\n  232",
            "post_number: 232\ndraft_id: 123", "post_number: 232\ndraft_id: invalid",
            'title: "unclosed', "[232]",
        ]
        for header in headers:
            with self.subTest(header=header):
                self.set_history({path: f"---\n{header}\n---\nBody\n"})
                self.assert_rejected_without_writes()
        self.set_history({path: "---\npost_number: 232\n"})
        self.assert_rejected_without_writes()

    def test_missing_yaml_dependency_is_actionable_and_never_writes(self):
        error = self.assert_rejected_without_writes(python_flags=["-S"])
        self.assertIn("PyYAML", error)
        self.assertFalse((self.tmp / "calls.jsonl").exists())

    def test_incomplete_graphql_or_wrong_blob_metadata_stops_before_writes(self):
        path = "docs/2026/01-09-1-club-2026-09-01.md"
        for response in ({"errors": [{"message": "sensitive-auth-sentinel"}]}, {},
                         {"data": {"repository": None}},
                         {"data": {"repository": {}}},
                         {"data": {"repository": {"b0": None}}}):
            with self.subTest(response=response):
                self.set_history({path: "---\npost_number: 232\n---\n"})
                self.responses["graphql"] = response
                self.save_responses()
                self.assert_rejected_without_writes()
        self.responses.pop("graphql")
        for change in ({"isBinary": True}, {"isTruncated": True}, {"oid": "c" * 40},
                       {"text": None}, {"byteSize": 1}, {"byteSize": True}):
            with self.subTest(change=change):
                self.set_history({path: "---\npost_number: 232\n---\n"})
                blob = next(iter(self.responses["_blobs"].values()))
                blob.update(change)
                self.save_responses()
                self.assert_rejected_without_writes()

    def test_incomplete_or_oversized_tree_stops_before_writes(self):
        endpoint = f"{REPOSITORY}/git/trees/{TREE}?recursive=1"
        for change in ({"truncated": True}, {"sha": "c" * 40}, {"tree": None},
                       {"tree": [{"type": "blob"}]}):
            with self.subTest(change=change):
                self.set_log([reservation()])
                self.responses[endpoint].update(change)
                self.save_responses()
                self.assert_rejected_without_writes()
        for change in ({"size": 1024 * 1024 + 1}, {"size": None}, {"mode": "120000"},
                       {"sha": "invalid"}, {"type": "tree"}):
            with self.subTest(change=change):
                self.set_log([reservation()])
                self.set_history({"docs/232-1-club-2026-09-01.md": "Existing post\n"})
                self.responses[endpoint]["tree"][0].update(change)
                self.save_responses()
                self.assert_rejected_without_writes()

    def test_graphql_batches_read_immutable_blobs_with_a_maximum_of_40(self):
        files = {f"docs/2026/{index:03d}-1-club-2026-09-01.md": f"# История {index}\n"
                 for index in range(1, 82)}
        self.set_history(files)
        code, stdout, stderr = self.run_post()
        self.assertEqual(code, 0, stdout + stderr)
        calls = [json.loads(line) for line in (self.tmp / "calls.jsonl").read_text().splitlines()]
        graphql = [call for call in calls if call[-1] == "graphql"]
        self.assertEqual(len(graphql), 3)
        queried_oids = []
        for call, expected_size in zip(graphql, [40, 40, 1]):
            self.assertEqual(call[call.index("--method") + 1], "POST")
            query = next(arg[6:] for arg in call if arg.startswith("query="))
            self.assertTrue(query.startswith("query {"))
            self.assertNotIn("mutation", query)
            self.assertEqual(query.count("object(oid:"), expected_size)
            queried_oids.extend(oid for oid in self.responses["_blobs"] if oid in query)
        self.assertCountEqual(queried_oids, self.responses["_blobs"])

    def test_entire_ledger_must_be_valid_and_unambiguous(self):
        bad_entries = [None, [], {}, {**reservation(OTHER_ID, 234), "artifact_type": "note"},
                       {**reservation(OTHER_ID, 234), "extra": "unexpected"},
                       {**reservation(OTHER_ID, 234), "draft_id": "invalid"},
                       {**reservation(OTHER_ID, 234), "timestamp": "invalid"},
                       {**reservation(OTHER_ID, 234), "timestamp": "2026-09-25"},
                       {**reservation(OTHER_ID, 234), "timestamp": "2026-09-25T12:00Z"},
                       {**reservation(OTHER_ID, 234), "timestamp": "2026-W39-5T12:00:00Z"},
                       {**reservation(OTHER_ID, 234), "post_number": True},
                       {**reservation(OTHER_ID, 234), "post_number": 234.0},
                       reservation(OTHER_ID, 0), reservation(OTHER_ID, 2**53),
                       reservation(OTHER_ID, 233), reservation(DRAFT_ID.upper(), 234),
                       reservation()]
        for bad in bad_entries:
            with self.subTest(bad=bad):
                self.set_log([reservation(), bad])
                self.assert_rejected_without_writes()
        for tail in ("{malformed}", '{"draft_id":"first","draft_id":"second"}'):
            with self.subTest(tail=tail):
                self.set_log(json.dumps(reservation()) + "\n" + tail)
                self.assert_rejected_without_writes()

    def test_unusable_remote_responses_never_write(self):
        for endpoint, response in (
            (REPOSITORY, "not json"),
            (REPOSITORY, []),
            (REPOSITORY, {}),
            (f"{REPOSITORY}/commits/main", {"sha": "main"}),
            (f"{REPOSITORY}/contents/docs/_allocator-log.jsonl?ref={SNAPSHOT}", {}),
            (f"{REPOSITORY}/contents/docs/_allocator-log.jsonl?ref={SNAPSHOT}",
             {"type": "file", "encoding": "base64", "content": "bad base64!"}),
        ):
            with self.subTest(endpoint=endpoint, response=response):
                self.set_log([reservation()])
                self.responses[endpoint] = response
                self.save_responses()
                self.assert_rejected_without_writes()

    def test_valid_pair_uses_immutable_remote_snapshot_and_records_ownership(self):
        self.add_local_post(500)
        self.set_log("\n" + json.dumps(reservation(DRAFT_ID.upper())) + "\n\n")
        code, stdout, stderr = self.run_post(draft_id=DRAFT_ID.upper())
        self.assertEqual(code, 0, stderr)
        files = list((self.root / "docs").glob("**/01-09-*.md"))
        self.assertEqual(len(files), 2, stdout)
        for path in files:
            self.assertIn("post_number: 233\n", path.read_text())
            self.assertIn(f"draft_id: {DRAFT_ID}\n", path.read_text())
        calls = [json.loads(line) for line in (self.tmp / "calls.jsonl").read_text().splitlines()]
        self.assertEqual([call[-1] for call in calls], list(self.responses))
        for call in calls:
            self.assertEqual(call[call.index("--method") + 1], "GET")
            self.assertEqual(call[call.index("--hostname") + 1], "github.com")

    def test_same_draft_replay_preserves_existing_body_and_points_to_file(self):
        code, _, stderr = self.run_post()
        self.assertEqual(code, 0, stderr)
        club = next((self.root / "docs").glob("**/*-1-club-*.md"))
        club.write_text(club.read_text() + "Handwritten content.\n", encoding="utf-8")
        error = self.assert_rejected_without_writes(slug="retry-changed-slug")
        self.assertIn(str(club.relative_to(self.root)), error)

    def test_telegram_only_request_keeps_canonical_club_and_blocks_replay(self):
        code, stdout, stderr = self.run_post(extra=["--channels", "telegram"])
        self.assertEqual(code, 0, stdout + stderr)
        club_files = list((self.root / "docs").glob("**/*-1-club-*.md"))
        self.assertEqual(len(club_files), 1)
        self.assertEqual(len(list((self.root / "docs").glob("**/*.md"))), 2)
        error = self.assert_rejected_without_writes(
            slug="telegram-retry", extra=["--channels", "telegram"])
        self.assertIn(str(club_files[0].relative_to(self.root)), error)

    def test_free_text_stays_one_yaml_value_and_cannot_inject_ownership(self):
        import yaml

        title = 'Он сказал "да"\npost_number: 999\u2028---\u2029draft_id: ' + OTHER_ID
        source = 'Pack "цитата"\npost_number: 999'
        plan = 'План "на завтра"\nrelated_wp: 999'
        code, stdout, stderr = self.run_post(
            title=title, extra=["--source-knowledge", source, "--content-plan", plan])
        self.assertEqual(code, 0, stdout + stderr)
        files = list((self.root / "docs").glob("**/*.md"))
        self.assertEqual(len(files), 2)
        for path in files:
            header = path.read_text().split("\n---\n", 1)[0].removeprefix("---\n")
            fields = yaml.safe_load(header)
            self.assertEqual(fields["title"], title)
            self.assertEqual(fields["source_knowledge"], source)
            self.assertEqual(fields["content_plan"], plan)
            self.assertEqual(fields["post_number"], 233)
            self.assertEqual(fields["draft_id"], DRAFT_ID)
            self.assertNotIn("related_wp", fields)
        # The real ownership parser must still see the original club on replay.
        self.assert_rejected_without_writes(slug="quoted-title-retry")

    def test_existing_number_or_uuid_cannot_be_reused(self):
        for number, draft_id in ((233, None), (232, DRAFT_ID)):
            with self.subTest(number=number, draft_id=draft_id):
                path = self.add_local_post(number, draft_id)
                # A valid reservation can open the coordination lock, never docs.
                (self.root / "scripts" / ".new-post.lock").touch()
                error = self.assert_rejected_without_writes()
                self.assertIn(str(path.relative_to(self.root)), error)

    def test_dry_run_is_explicitly_unverified_and_does_not_write_or_call_gh(self):
        before = tree_snapshot(self.root)
        code, stdout, stderr = self.run_post(draft_id=None, extra=["--dry-run"])
        self.assertEqual(code, 0, stderr)
        self.assertIn("резервация не проверена", stdout)
        self.assertEqual(before, tree_snapshot(self.root))
        self.assertFalse((self.tmp / "calls.jsonl").exists())
        self.assert_rejected_without_writes(number=None, extra=["--dry-run"])

    def test_concurrent_distinct_reservations_keep_unique_monthly_folders(self):
        entries = [reservation(str(UUID(int=index)), 233 + index) for index in range(1, 13)]
        self.set_log(entries)
        processes = [self.start_post(draft_id=entry["draft_id"], number=entry["post_number"],
                                     slug=f"race-{index}")
                     for index, entry in enumerate(entries)]
        for process in processes:
            stdout, stderr = process.communicate(timeout=30)
            self.assertEqual(process.returncode, 0, stdout + stderr)
        clubs = list((self.root / "docs").glob("**/*-1-club-*.md"))
        self.assertEqual(len(clubs), 12)
        self.assertEqual(sorted(int(path.name.split("-")[0]) for path in clubs), list(range(1, 13)))
        contents = "".join(path.read_text() for path in clubs)
        for entry in entries:
            self.assertEqual(contents.count(f'post_number: {entry["post_number"]}\n'), 1)

    def test_concurrent_same_reservation_has_exactly_one_writer(self):
        processes = [self.start_post(slug=f"collision-{index}") for index in range(6)]
        codes = []
        for process in processes:
            process.communicate(timeout=30)
            codes.append(process.returncode)
        self.assertEqual(sorted(codes), [0, 1, 1, 1, 1, 1])
        clubs = list((self.root / "docs").glob("**/*-1-club-*.md"))
        self.assertEqual(len(clubs), 1)
        self.assertIn("post_number: 233\n", clubs[0].read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
