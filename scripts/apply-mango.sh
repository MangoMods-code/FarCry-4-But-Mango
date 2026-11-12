#!/usr/bin/env bash
# Mango Port: fetch Madeira at the pinned commit and apply Mango's patches on top.
#
#   scripts/apply-mango.sh            fetch submodules (recursive) and apply patches
#   scripts/apply-mango.sh --shallow  only the top-level Madeira checkout (no Wine/FEX/DXMT);
#                                     enough for the host tests and CI, not for a build
#   scripts/apply-mango.sh --check    report whether the patches apply, change nothing
#
# Safe to re-run: a patch that is already applied is skipped.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MADEIRA="$ROOT/madeira"
PATCHES="$ROOT/mango/patches"
MODE="${1:-full}"

cd "$ROOT"
if [ "$MODE" = "--shallow" ] || [ "$MODE" = "--check" ]; then
  git submodule update --init madeira
else
  git submodule update --init --recursive madeira
fi

status=0
for patch in "$PATCHES"/*.patch; do
  name="$(basename "$patch")"
  if git -C "$MADEIRA" apply --reverse --check "$patch" 2>/dev/null; then
    echo "already applied: $name"
  elif git -C "$MADEIRA" apply --check "$patch" 2>/dev/null; then
    if [ "$MODE" = "--check" ]; then
      echo "applies cleanly: $name"
    else
      git -C "$MADEIRA" apply "$patch"
      echo "applied: $name"
    fi
  else
    echo "DOES NOT APPLY: $name (Madeira moved? rebase the patch on the pinned commit)" >&2
    status=1
    [ "$MODE" = "--check" ] || exit 1
  fi
done
exit $status
