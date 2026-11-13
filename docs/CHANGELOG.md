# Changelog

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
