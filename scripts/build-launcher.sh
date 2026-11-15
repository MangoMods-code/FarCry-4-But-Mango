#!/usr/bin/env bash
# Builds Mango Port's Home Screen launcher (mango/launcher/MangoLauncher.swift) for iOS and
# writes it, base64-encoded, to the path given (inside Madeira.app, so it is not a second
# executable for signers to handle). Needs Xcode; run by tools/build/package-ipa.sh (patch 0018).
#   scripts/build-launcher.sh /path/to/Madeira.app/MangoLauncher.b64
set -euo pipefail
OUT=${1:?usage: build-launcher.sh <output .b64>}
HERE=$(cd "$(dirname "$0")/.." && pwd)
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT
xcrun -sdk iphoneos swiftc -parse-as-library -O \
  -target arm64-apple-ios16.0 -module-name MangoLauncher \
  "$HERE/mango/launcher/MangoLauncher.swift" -o "$WORK/MangoLauncher"
codesign --force --sign - "$WORK/MangoLauncher"
base64 < "$WORK/MangoLauncher" | tr -d '\n' > "$OUT"
echo "launcher: $(wc -c < "$WORK/MangoLauncher" | tr -d ' ') bytes -> $OUT"
