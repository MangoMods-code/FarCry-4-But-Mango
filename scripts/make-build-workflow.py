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
    # Pushing to the release branch builds and publishes the newest version in docs/CHANGELOG.md.
    branches: [release]

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
# Diagnostics: this session can read check-run annotations but not job logs, so every
# run step tees its output to $RUNNER_TEMP/step.log, and a failed job posts the last
# 60 lines of its failing step as an error annotation.
def wrap_runs(text):
    lines = text.split('\n'); out = []; i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(\s+)run: (.*)$', line)
        if not m:
            out.append(line); i += 1; continue
        ind, val = m.groups()
        if val == '|':
            body = []; i += 1
            body_ind = None
            while i < len(lines) and (lines[i].strip() == '' or len(lines[i]) - len(lines[i].lstrip()) > len(ind)):
                if lines[i].strip():
                    body_ind = body_ind if body_ind is not None else len(lines[i]) - len(lines[i].lstrip())
                body.append(lines[i]); i += 1
            while body and not body[-1].strip(): body.pop()
            inner = [b[body_ind:] if b.strip() else '' for b in body]
        else:
            inner = [val]; i += 1
            body_ind = len(ind) + 2
        pad = ' ' * body_ind
        # A step that only runs after a failure appends, so the failing step's output stays.
        after_failure = any('failure()' in o for o in out[-3:])
        out.append(f'{ind}run: |')
        out.append(f'{pad}set -o pipefail')
        if not after_failure:
            out.append(f'{pad}: > "$RUNNER_TEMP/step.log"')
        out.append(f'{pad}(')
        out.extend((pad + '  ' + b) if b else '' for b in inner)
        out.append(f'{pad}) 2>&1 | tee -a "$RUNNER_TEMP/step.log"')
    return '\n'.join(out)

head2, jobs2 = s.split('\njobs:\n', 1)
jobs2 = wrap_runs(jobs2)
# A last step in every job: on failure, post the failing step's tail as an annotation.
report = '''      - name: Report the failing step
        if: failure()
        working-directory: .
        shell: bash
        run: |
          f="$RUNNER_TEMP/step.log"
          [ -s "$f" ] || exit 0
          msg=$(tr '\\r' '\\n' < "$f" | sed -e 's/\\x1b\\[[0-9;]*m//g' | grep -v '^[[:space:]]*$' | tail -60 | cut -c1-400 | sed -e 's/%/%25/g' | awk 'BEGIN{ORS="%0A"} {print}')
          echo "::error title=${GITHUB_JOB} failed (last 60 lines)::${msg}"
'''
blocks = re.split(r'(?m)^(?=  [a-z0-9-]+:\n)', jobs2)
jobs2 = ''.join(b.rstrip('\n') + '\n' + report + ('\n' if b.endswith('\n\n') else '') if re.match(r'  [a-z0-9-]+:\n', b) else b for b in blocks)
s = head2 + '\njobs:\n' + jobs2

# Release: on a v* tag, attach the IPA to a GitHub Release with that version's notes from
# docs/CHANGELOG.md (an ubuntu job, so it costs no macOS minutes).
s = s.rstrip('\n') + '''

  release:
    needs: [reuse, app]
    if: always() && (startsWith(github.ref, 'refs/tags/v') || github.ref == 'refs/heads/release') && (needs.app.result == 'success' || needs.reuse.result == 'success')
    runs-on: ubuntu-latest
    permissions:
      contents: write
    defaults:
      run:
        working-directory: .
    steps:
      - uses: actions/checkout@v4
      - uses: actions/download-artifact@v4
        with:
          name: MangoPort-ipa
          path: dist
      - name: Publish the release
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          # A tag build uses its tag; a release-branch build uses the newest '## vX.Y.Z' in the changelog.
          if [ "${GITHUB_REF_TYPE}" = tag ]; then TAG="${GITHUB_REF_NAME}"
          else TAG=$(awk '/^## v/ {print $2; exit}' docs/CHANGELOG.md); fi
          test -n "$TAG"
          mv dist/Madeira.ipa "dist/MangoPort-$TAG.ipa"
          awk -v tag="## $TAG" '$0 == tag {on=1; next} /^## / {on=0} on' docs/CHANGELOG.md > notes.md
          test -s notes.md || echo "Mango Port $TAG" > notes.md
          gh release create "$TAG" "dist/MangoPort-$TAG.ipa" --title "Mango Port $TAG" --notes-file notes.md --target "$GITHUB_SHA"
'''
open(dst, 'w').write(s)
