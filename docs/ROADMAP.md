# Roadmap

## Milestone 1 — Profiles on Madeira ✅ (this commit)
- Madeira pinned as a submodule; Mango changes kept as patches
- Far Cry 4, Ubisoft Connect and its installer recognised and given recommended settings
- App renamed Mango Port (`com.mangomods.mangoport`)
- Madeira's host checks updated and passing; CI runs them on Linux and macOS

## Milestone 2 — First device run (needs a Mac + iPhone)
The big unknown is **Ubisoft Connect**, not the game. Order of work:
1. Build the IPA (`madeira/BUILDING.md`), sideload through Mango Signer, enable JIT.
2. Run the Ubisoft Connect installer, then Ubisoft Connect. Get to a signed-in window.
3. Install or point it at Far Cry 4, launch, reach the main menu.
4. Log every run in `docs/FAR_CRY_4.md` with the Madeira log number; raise the profile's `version` with each working change.

If Ubisoft Connect fails the way the Rockstar launcher first did (CEF pool exhaustion, PartitionAlloc reservations), the Rockstar notes in `GameRecommendations.swift` are the playbook — e.g. try `env.MADEIRA_SC_PA_POOLS = 2`.

## Milestone 3 — Five Star–style front end
- A single-game home screen: "Import Far Cry 4" → checks → Play
- Import checks: `bin\FarCry4.exe` present, enough free space, Ubisoft Connect installed
- A Far Cry 4 touch layout (Madeira's `TouchControlPresets.swift`), with controller auto-detect
- Per-device presets (iPhone 15 Pro / 16 Pro / 17 Pro / 18 Pro): resolution, MetalFX upscale, FPS cap

## Milestone 4 — Ship
- GitHub Actions job that builds the IPA on a macOS runner
- Release IPA into the Mango Signer library
- Public source for every release (GPL)
