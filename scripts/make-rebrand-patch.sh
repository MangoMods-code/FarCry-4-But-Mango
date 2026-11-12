#!/usr/bin/env bash
# F4 Mango Port: regenerate mango/patches/0004-on-screen-rebrand.patch with scripts/rebrand.py.
# Run after bumping the Madeira submodule (and after rebasing patches 0001-0003), or after
# changing rebrand.py or the icon. Needs a clean Madeira checkout with no 0004 applied.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
M="$ROOT/madeira"
OUT="$ROOT/mango/patches/0004-on-screen-rebrand.patch"

git -C "$M" reset -q --hard          # Madeira at the pinned commit, nothing applied
for p in "$ROOT"/mango/patches/000[1-3]-*.patch; do git -C "$M" apply "$p"; done
git -C "$M" add -A                       # the index holds Madeira plus patches 0001-0003
python3 "$ROOT/scripts/rebrand.py" "$M"
git -C "$M" diff --binary > "$OUT"       # only what the rebrand changed
git -C "$M" reset -q
echo "wrote $OUT ($(grep -c '^diff --git' "$OUT") files)"
