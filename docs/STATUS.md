# Game status list

Mango Port shows a tested status for games: **Works**, **Playable with issues**,
**Currently not playable** and **Can't run on iPhone**. The list lives in
[`status/games.json`](../status/games.json) on `main`, so it changes without a new build:
every copy of Mango Port reads it when it opens, and on pull-to-refresh in **Game status**.
The app keeps a copy for offline starts, and ships a built-in list for a first start with
no connection.

## Editing it from the app (owner only)

Only someone holding a GitHub token that can write this repo can change the list.

1. On GitHub: **Settings → Developer settings → Personal access tokens → Fine-grained tokens
   → Generate new token**.
   - Repository access: **Only select repositories → FarCry-4-But-Mango**
   - Permissions → Repository permissions → **Contents: Read and write** (nothing else)
   - Expiration: up to a year; make a new one when it runs out.
2. In Mango Port open **Game status** (the button beside the greeting, or Settings), and
   **long-press the text at the top** of the page for about a second.
3. Paste the token as the **Owner key** and tap **Save**. It is kept in this iPhone's
   Keychain only.

Then: **+** adds a game (pick one of your installed Steam games, or type its Steam App ID
and name), a **tap** on a game changes its status or note, and a **swipe** removes it. Each
change is a commit to `status/games.json`; other phones see it on their next refresh (GitHub
can take up to five minutes to serve the new file).

## Editing it by hand

Edit `status/games.json` on GitHub. Each game:

```json
{ "appID": 377160, "name": "Fallout 4", "status": "works", "note": "Plays well.", "updated": "2026-11-12" }
```

`status` is `works`, `issues`, `notYet` or `cantRun`. Only `cantRun` blocks Install and Play.

A game's modes that Steam sells as separate apps (Zombies, Multiplayer) go on its card, each
with its own status; leave `modes` out when there are none:

```json
{ "appID": 202970, "name": "Call of Duty: Black Ops II", "status": "works", "note": "", "updated": "2026-11-13",
  "modes": [ { "appID": 212910, "name": "Zombies", "status": "works", "note": "" } ] }
```
`scripts/check-status-list.py` (run by `scripts/test.sh` and CI) checks the file.
