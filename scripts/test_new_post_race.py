#!/usr/bin/env python3
"""WP-560 Ф12: reservation verification and real-process scaffold race tests.

Run: python3 scripts/test_new_post_race.py
All GitHub responses are served by a local fake gh executable. No live
reservation, publication, network request or authentication store is used.
"""

import base64
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
import sys

fixture_dir = pathlib.Path(os.environ["GH_FIXTURE_DIR"])
fixture = json.loads((fixture_dir / "responses.json").read_text())
with (fixture_dir / "calls.jsonl").open("a") as calls:
    calls.write(json.dumps(sys.argv[1:]) + "\\n")
if fixture.get("error"):
    print("sensitive-auth-sentinel", file=sys.stderr)
    raise SystemExit(1)
response = fixture[sys.argv[-1]]
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
            f"{REPOSITORY}/commits/main": {"sha": SNAPSHOT},
            f"{REPOSITORY}/contents/docs/_allocator-log.jsonl?ref={SNAPSHOT}": {
                "type": "file", "encoding": "base64",
                "content": base64.b64encode(log.encode()).decode(),
            },
        }
        self.save_responses()

    def save_responses(self):
        (self.tmp / "responses.json").write_text(json.dumps(self.responses), encoding="utf-8")

    def start_post(self, *, draft_id=DRAFT_ID, number=233, slug="test-post", extra=()):
        cmd = [sys.executable, str(self.root / "scripts" / "new-post.py"),
               "--date", "2026-09-25", "--slug", slug, "--title", "Test post",
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

    def test_entire_ledger_must_be_valid_and_unambiguous(self):
        bad_entries = [None, [], {}, {**reservation(OTHER_ID, 234), "artifact_type": "note"},
                       {**reservation(OTHER_ID, 234), "draft_id": "invalid"},
                       {**reservation(OTHER_ID, 234), "timestamp": "invalid"},
                       {**reservation(OTHER_ID, 234), "timestamp": "2026-09-25"},
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
