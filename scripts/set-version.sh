#!/usr/bin/env bash
# Mango Port: stamp the app with this repo's release number, so Settings and sideloaders
# show e.g. 0.1.3 instead of Madeira's own version. The number is the first "## vX.Y.Z" in
# docs/CHANGELOG.md, the same one the release job tags. The build number is derived from it
# (0.1.3 -> 103) so every release counts up.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PBX="$ROOT/madeira/app/Madeira.xcodeproj/project.pbxproj"
v=$(grep -m1 -oE '^## v[0-9]+\.[0-9]+\.[0-9]+' "$ROOT/docs/CHANGELOG.md" | cut -c5-)
[ -n "$v" ] || { echo "no '## vX.Y.Z' heading in docs/CHANGELOG.md" >&2; exit 1; }
IFS=. read -r ma mi pa <<<"$v"
build=$(( ma * 10000 + mi * 100 + pa ))
sed -i.bak -E "s/MARKETING_VERSION = [^;]+;/MARKETING_VERSION = $v;/; s/CURRENT_PROJECT_VERSION = [^;]+;/CURRENT_PROJECT_VERSION = $build;/" "$PBX"
rm -f "$PBX.bak"
echo "app version $v (build $build)"
