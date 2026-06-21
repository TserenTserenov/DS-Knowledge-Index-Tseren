#!/usr/bin/env bash
# Install repo git hooks from scripts/hooks/ into .git/hooks/.
# Git hooks are not versioned, so run this once after cloning:
#   bash scripts/install-hooks.sh
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
src="$repo_root/scripts/hooks"
dst="$repo_root/.git/hooks"

if [ ! -d "$src" ]; then
  echo "❌ Нет каталога с хуками: $src" >&2
  exit 1
fi

for hook in "$src"/*; do
  [ -e "$hook" ] || continue
  name="$(basename "$hook")"
  cp "$hook" "$dst/$name"
  chmod +x "$dst/$name"
  echo "✅ установлен хук: $name"
done

echo "Готово. Проверка имён публикаций активна на pre-commit."
