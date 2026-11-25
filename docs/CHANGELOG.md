# Changelog

## v0.18.2
Moon Sweepers money without the stuck step, and fixes from Madeira Nightly 0.2.101.

- **Moon Sweepers money:** after **Find my money**, the path to your money is saved in about a second, with no lag. Mango Port reads it from how Unity games are built (your money's object knows its class, and the class knows where it's kept) instead of searching all of the game's memory six times. Next launch it finds your money at once
- Scans skip memory iOS has compressed: faster, and they can't push Mango Port over iOS's memory limit (the reset you saw)
- Scans run gentler (3 cores, lower priority), so the game keeps running while they do
- **From Madeira Nightly 0.2.101** (camhawk):
  - Left 4 Dead 2: downloaded Workshop add-ons are copied to where the game looks for them, before it starts
  - Madeira Dock: a game with no .exe launch option uses the best Windows option outside beta branches (tModLoader)
  - Fix for the Visual C++ installer failing in some Unreal games

## v0.18.1
Much faster scans.

- **Find my money** and every Cheats scan are about 10x faster: numbers are checked with a quick range test instead of decoding every type at every spot, and the scan runs on several CPU cores at once
- Saving where your money lives (the pointer scan) also uses several cores
- Scans show a percentage

## v0.18.0
A real Moon Sweepers money mod, and a smarter cheat engine.

- **Moon Sweepers money** card at the top of Cheats (in-game menu) while Moon Sweepers runs: **Find my money** once (it starts from your last save's amount), then **+1,000 / +10,000 / +100,000**, **Set** any amount, or **Lock** it
- It works like a PC trainer: after finding your money it runs a **pointer scan** from the game's code (GameAssembly.dll) and saves the path, so next launch your money shows up at once, with no scanning
- Finds money however the game keeps it: double, float, cents, or **hidden by anti-cheat** (XOR-scrambled values)
- Cheats: new **Hidden number (anti-cheat)** type for any single-player game
- Safer scans: only memory that's actually in use is read, so big games can't run Mango Port out of memory during a scan

## v0.17.0
Quality-of-life update: the best of Madeira's latest nightly, Heat guard, and cleanup.

- **From Madeira Nightly 0.2.100** (camhawk's test builds):
  - Steam games started as **The game** now get your **Launch arguments** too (they used to be ignored)
  - First-start installs: the DirectX setup that always failed is skipped (Wine has its own), and PhysX and other shared installers are found in every Steam library, including external drives (Batman Arkham fix)
  - A controller that's already connected counts as player 1 from the start, so games that only look once (Sonic Generations) see it
  - Recommended settings for 13 more games: Cyberpunk 2077, Dying Light 2, Detroit: Become Human, Hades II, L.A. Noire, Portal, Metaphor: ReFantazio, The Forest, Grounded, Satisfactory, Blue Prince, Sonic Generations and Football Manager 27
- New **Heat guard** in the in-game menu: shows how hot your iPhone is, and when it gets hot it drops the FPS limit (and turns on Eco mode when it's very hot), then puts things back once it cools down
- **Cheats:** Undo for Set all, Mango colors, and everything clears when the game closes
- Moon Sweepers: the save-file money test is gone (it never worked); the Mods page points to Cheats for money instead

## v0.16.0
A real cheat engine, built in.

- New **Cheats** page in the in-game menu (tap the menu button while a game runs). It scans the running game's memory, like Cheat Engine on PC, no save editing
- **Scan** for the number the game shows (money, ammo, health). Change it in the game, type the new number and tap **Next scan** until only a few results are left. Went up, Went down, Changed and Didn't change work without a number
- **Set all** changes every result at once; **Keep** a result to name it, **Set** it or **Freeze** it so the game can't change it
- Any number (whole and decimal together), or just whole numbers, floats, doubles or 64-bit numbers
- For single-player games. Nothing stays frozen after the game closes

## v0.15.0
A mod menu for Moon Sweepers.

- New **Mods** page and **Launch with mods** switch on Moon Sweepers' details page, off by default. With it on, Mango Port changes one save slot (you pick which, slot 2 by default) right before the game starts; every other slot stays legit
- **Suit upgrades:** set Payout (tested: more money per load), Belt, Lamp and Clean width to any level from 1 to 10
- **Money changer (experimental):** a first test at changing your money
- **Copy slot 1 into another slot**, so your modded slot starts from your real progress
- Every modded launch backs the slot up first (Files › Mango Port › Mango Mod Backups, newest five kept), and **Restore** puts the last one back
- The page shows the slot's money and upgrade levels as they are now

## v0.14.0
No more save tug-of-war, and your Mango Port hours.

- New **Always keep this iPhone's saves**, per game, on its Steam Cloud page. For games you only play here: when Steam Cloud and your iPhone disagree, your iPhone's saves win automatically instead of blocking Play (the cloud's copies are backed up first)
- Each game's card now shows how long you've played it **on Mango Port**, under its Steam hours. It starts counting from this version

## v0.13.0
Games on your Home Screen.

- New **Make Home Screen app** on a game's Library details page: Mango Port makes a small app with the game's name and its Steam art (with a little mango) as the icon, and opens the share sheet. Send it to Mango Signer to sign and install it; tapping it opens the game in Mango Port
- The game itself still runs in Mango Port, so keep Mango Port installed (and JIT on, as usual). Each Home Screen app uses one app on your certificate

## v0.12.1
Smoother in-game video and audio.

- Updated to the latest Madeira, which brings FFmpeg 7.1.5 (the part that plays in-game videos and audio) with its bug fixes

## v0.12.0
Only the stores you use, and quick Steam account switching.

- New **Settings › Game stores**: switch GOG, Epic Games, the EA app and itch.io off. Their library sections, sign-ins and settings go away; Steam is always on
- **Switch Steam accounts in one tap**: every account you sign in to is saved on this iPhone, and Settings › Steam lists the others with **Switch**. **Add another account** signs in a new one without losing the first; swipe an account to forget it, and Sign out forgets the one you're on
- Each account shows its own Steam library; downloads pause while switching

## v0.11.0
Uninstall in one step, and a clearer Can't run list.

- **Long-press** a Steam game's card to uninstall it, without opening its pages. A game that isn't downloaded offers **Download** there instead
- Uninstalling Black Ops II this way also removes its Zombies and Multiplayer, which share its folder (the app tells you first), so nothing is left listed without its files
- Game status: 117 Steam games with Easy Anti-Cheat that blocks Wine (Rust, Apex Legends, SCUM and more) are now marked **Can't run on iPhone**, so nobody wastes a download on them. Games whose offline or story modes may still play were left off

## v0.10.0
Game modes as add-ons, and cards that open from anywhere.

- Games whose modes are separate Steam apps (Black Ops II's **Zombies** and **Multiplayer**, Black Ops, Modern Warfare 2 and 3 Multiplayer) now show as one game. Their modes are listed under **Add-ons** on the game's page and download sheet: switch one on to download it, off to remove it, and tap **Open** to play it
- A mode installed into the same folder as its main game can't be removed on its own (that would delete the main game too); the app tells you instead
- Game status: a game's card can now list its modes, each with its own status and note. Owners add them from the game's edit sheet under **Modes**
- Fixed: tapping a game's artwork on the main screen and in the Steam library didn't open it; the whole card opens it now
- Fixed: the Live Activity while pairing said "Pairing with Madeira"; it now says **Pairing with Mango Port**

## v0.9.2
Game status keeps your changes.

- Fixed: games you added or changed on Game status seemed to go back to how they were when you reopened the page. Your changes were saved; the page was reading an older copy of the list. It now reads the newest one

## v0.9.1
Easier JIT setup.

- New **Paste pairing file**: copy your pairing file's text and paste it in, for when the file picker won't open (Settings › JIT › JIT setup, or first-run setup)
- Pairing on the phone now shows **Pair with Mango Port** in iOS Settings

## v0.9.0
Game status, live.

- New **Game status** page: every game we've tested, grouped into Works, Playable with issues, Currently not playable and Can't run on iPhone, with notes and test dates. Open it from the button beside the greeting, or from Settings
- Statuses now come from an online list, so they update without a new version of the app; pull down on Game status to refresh
- Search the list, and see each game's cover art

## v0.8.0
Know what works, and a livelier library.

- Tested games now carry a badge on their card, Steam page and details page: **Works** (green), **Playable with issues** (gold), **Currently not playable** (orange) and **Can't run on iPhone** (red)
- Skyrim and Fallout 4: Works. MX vs ATV Legends: Playable with issues. Black Ops: Currently not playable, waiting on a fix in Madeira (you can still try it)
- A greeting for the time of day above Continue playing, with how many games you have ready and the hours you've played
- Continue playing shows the game's badge, and its button glows gently
- Play and Continue give a little tap of haptic feedback

## v0.7.1
Less to set up by hand.

- Black Ops, Black Ops II, Borderlands 2 and other older Activision and 2K games no longer hang on "Steam is preparing this game's executable": Mango Port now makes the two Windows folders that step needs, by itself
- The DirectX installer's "exit -9" during one-time installs is expected and harmless; games run without it

## v0.7.0
Know before you download.

- Games we've tested that can't run on iPhone now show a red "Can't run on iPhone" label, and their Steam page explains why instead of offering Install
- First on the list: Hood Warfare 2, whose Easy Anti-Cheat only runs on Windows and Linux

## v0.6.3
A smoother Settings tab.

- Fixed the Mango Port title smearing into a glass bubble when you open or leave a Settings page: the title now shows on the Library tab only, and Settings opens its pages cleanly

## v0.6.2
A smoother top bar.

- Fixed the title smearing into a glass bubble when you open or leave a page in Settings or the library
- The bolt beside the title still enables JIT with a tap

## v0.6.1
One-tap JIT.

- Tap the grey bolt beside the Mango Port title to enable JIT straight from your library; it turns green once JIT is on

## v0.6.0
New logo, and the mango look everywhere.

- New app icon: the mango with its orbit ring
- The same mango beside the title, on the launch screen and on the welcome page (the title's mango was missing in v0.4 and v0.5)
- Mango orange is now the accent colour everywhere, and the launch screen has its night background
- The game-start screen: a gold spinner, a bolder title and a mango glow around the cover
- Every Game details page (Display, Controls, Launch and the rest) and every Settings page now uses the night theme

## v0.5.0
Mango Port: not just Far Cry 4.

- New name: **Mango Port**, because it plays Fallout 4, Skyrim, Black Ops and more, powered by Madeira
- New icon: just the mango
- "powered by Madeira" under the title, and a Mango Port section in Settings › Credits above Madeira's own credits
- Game details page: the night theme, a rounder cover and a mango Play button
- Settings now uses the night theme too
- The welcome screen shows the mango

## v0.4.1
Fixes for the new main screen.

- The F4 Mango Port title now fits beside the library's buttons, which no longer fold into a menu
- JIT is a bolt beside the title: green when JIT is on
- Tabs, links and switches are mango orange instead of blue
- The Continue playing card's text stands out on bright artwork

## v0.4.0
The main screen, mango style.

- New night theme in F4 Mango Port's colours, with mango orange buttons, switches and links throughout the app
- The title is now the mango and F4 Mango Port, with a JIT pill that turns green when JIT is on
- Continue playing: the game you played last sits at the top of your library, one tap from its details and Play
- Store tabs are now mango pills, and game cards are rounder with a soft edge
- Liquid metal buttons and tab bar shine in mango, gold and leaf green
- A new launch screen with the mango

## v0.3.0
Same app as v0.1.2, renumbered so updates are detected.

- Builds before v0.1.2 reported Madeira's version number, 0.2.0, so sideloaders saw v0.1.2 as older than what was installed. From now on F4 Mango Port's versions start above it.
- Includes everything in v0.1.2: the mango icon, F4 Mango Port on every screen, Mango Dock, and the Madeira credit in About

## v0.1.2
F4 Mango Port, inside and out.

- New mango app icon
- Every screen now says F4 Mango Port instead of Madeira, and Madeira Dock is now Mango Dock
- About credits Madeira by Will Faust, which F4 Mango Port is built on
- Same bundle ID, so it installs over the previous version and keeps your games and settings

## v0.1.1
Renamed to F4 Mango Port.

- The app's name on your Home Screen is now **F4 Mango Port**
- Same bundle ID as v0.1.0, so it installs over the old version and keeps your games and settings

## v0.1.0
First test build of F4 Mango Port.

- Runs Windows PC games on your iPhone, with Far Cry 4 set up out of the box
- Recognises Far Cry 4 from Steam or the Ubisoft Store and applies tuned settings automatically
- Ubisoft Connect support for signing in and launching the game
- Extra memory headroom on iPhones with less than 12 GB of RAM
- 30 FPS cap by default for steadier play

**Needs:** iOS 26 or later, JIT enabled, and your own copy of Far Cry 4. No game files are included.

**Heads-up:** this is an early test build. Far Cry 4 hasn't been confirmed working on a device yet.
