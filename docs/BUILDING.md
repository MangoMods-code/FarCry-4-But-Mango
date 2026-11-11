# Building the Mango Port IPA

## On GitHub (no Mac needed)

**Actions → Build Mango Port IPA → Run workflow.** When it finishes, download the
`MangoPort-ipa` artifact. It contains `Madeira.ipa`, which is the Mango Port app.
The IPA is ad-hoc signed with the increased-memory entitlement, so re-sign it with
Mango Signer or your usual sideloader.

The workflow is Madeira's own build (`madeira/.github/workflows/build.yml`), adapted by
`scripts/make-build-workflow.py`:

- runs from this repo, with Madeira at `madeira/`, and applies `mango/patches` first
- runs only when started by hand or when a `v*` tag is pushed, because builds are expensive
- includes the Mango patches in the IPA cache key, so a profile change gives a new IPA

After bumping the Madeira submodule, regenerate the workflow:

```bash
python3 scripts/make-build-workflow.py madeira/.github/workflows/build.yml .github/workflows/build-ipa.yml
```

### Runner and Xcode
Madeira builds on a runner labelled `xcode-27`, because it needs the **iOS 27 SDK**.
This workflow uses GitHub's `macos-26` image and selects the newest `Xcode_27*` on it.
If that image doesn't have Xcode 27 yet, the build fails early at the SDK step.
To use a different runner, such as a self-hosted Mac or a larger runner, set the
repository variable `MANGO_MAC_RUNNER` to its label.

### Cost — read before the first run
- A **cold build takes several hours** and runs about 10 macOS jobs in parallel: LLVM, FEX,
  the 32-bit DLLs, 7 runtime components and the app. Later runs reuse caches and finish
  much faster.
- **Private repo:** macOS minutes count 10× against your plan's included minutes and are
  billed after that. One cold build can use up a free or Pro allowance and then cost real money.
  Set a spending limit in your GitHub billing settings first.
- **Public repo:** standard GitHub-hosted runners are free. Mango Port has to be public anyway
  once you share the IPA (GPL-3.0), so making it public before building is the cheap option.

## On a Mac

```bash
scripts/apply-mango.sh
cd madeira && tools/build-ipa.sh      # see madeira/BUILDING.md for prerequisites
```
