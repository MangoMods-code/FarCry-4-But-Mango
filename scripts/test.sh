#!/usr/bin/env bash
# Run the Madeira host checks Mango's patches touch. Needs the patches applied
# (scripts/apply-mango.sh --shallow is enough). On macOS, pass --require-swift so
# the Swift fixture that compiles GameRecommendations.swift must run too.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/madeira"
python3 -I tests/host/check-game-recommendations.py "$@"
python3 -I tests/host/check-jit-method.py
echo "Mango Port checks: PASS"
