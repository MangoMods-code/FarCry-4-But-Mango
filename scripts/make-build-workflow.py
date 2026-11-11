#!/usr/bin/env python3
# Usage: python3 scripts/make-build-workflow.py madeira/.github/workflows/build.yml .github/workflows/build-ipa.yml
"""Adapt Madeira's build.yml so it runs from the Mango Port repo (Madeira as a submodule at madeira/)."""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src).read()

# Header: name, manual trigger only, run steps inside madeira/.
head, jobs = s.split('\njobs:\n', 1)
head = '''# Generated from madeira/.github/workflows/build.yml by Mango Port (see docs/BUILDING.md).
# Differences: runs from this repo with Madeira at madeira/, applies mango/patches first,
# GitHub-hosted macOS runner (override with the MANGO_MAC_RUNNER repository variable),
# manual runs only, and the IPA cache key includes the Mango patches.
name: Build Mango Port IPA

on:
  workflow_dispatch:
  push:
    tags: ['v*']

permissions:
  contents: read

concurrency:
  group: mango-ipa-${{ github.ref }}
  cancel-in-progress: true

defaults:
  run:
    working-directory: madeira
'''
s = head + '\njobs:\n' + jobs

# Runner label.
s = s.replace('runs-on: xcode-27', "runs-on: ${{ vars.MANGO_MAC_RUNNER || 'macos-26' }}")

# Checkout steps: this repo, then Madeira + Mango patches, then pick the newest Xcode.
def checkout(full):
    mode = '' if full else ' --shallow'
    return f'''      - uses: actions/checkout@v4
      - name: Fetch Madeira and apply Mango patches
        working-directory: .
        run: scripts/apply-mango.sh{mode}
      - name: Select the newest Xcode
        working-directory: .
        run: |
          x=$(ls -d /Applications/Xcode_27*.app 2>/dev/null | sort -V | tail -1 || true)
          if [ -n "$x" ]; then sudo xcode-select -s "$x"; fi
          xcodebuild -version
'''
s = s.replace('      - uses: actions/checkout@v4\n        with:\n          submodules: recursive\n', '@@FULL@@\n')
s = s.replace('      - uses: actions/checkout@v4\n', checkout(False))
s = s.replace('@@FULL@@\n', checkout(True))

# Paths for cache/artifact actions are relative to the workspace, not working-directory.
out, in_path = [], False
for line in s.split('\n'):
    m = re.match(r'^(\s+)path: (.*)$', line)
    if m:
        ind, val = m.groups()
        if val == '|':
            in_path, path_ind = True, None
            out.append(line); continue
        neg = val.startswith('!')
        out.append(f'{ind}path: {"!" if neg else ""}madeira/{val.lstrip("!")}')
        in_path = False; continue
    if in_path:
        m2 = re.match(r'^(\s+)(\S.*)$', line)
        if m2 and (path_ind is None or len(m2.group(1)) == path_ind) and not re.match(r'^\s+[a-z-]+:', line):
            path_ind = len(m2.group(1))
            v = m2.group(2); neg = v.startswith('!')
            out.append(f'{m2.group(1)}{"!" if neg else ""}madeira/{v.lstrip("!")}'); continue
        in_path = False
    out.append(line)
s = '\n'.join(out)

# hashFiles() patterns are workspace-relative too.
def fix_hash(m):
    args = re.sub(r"'([^']+)'", lambda a: f"'madeira/{a.group(1)}'", m.group(1))
    return f'hashFiles({args})'
s = re.sub(r'hashFiles\(([^)]*)\)', fix_hash, s)

# The IPA cache key must change when Mango's patches change (Madeira's tree hash does not).
old = 'echo "ipa=ipa-v1-'
assert s.count(old) == 1
s = s.replace(old, 'echo "ipa=mango-ipa-v1-${{ hashFiles(\'mango/patches/**\') }}-')

# Artifact name.
s = s.replace('name: Madeira-ipa', 'name: MangoPort-ipa')
open(dst, 'w').write(s)
