#!/usr/bin/env python3
"""status/games.json, the tested-games list the app reads (MangoStatusStore): valid JSON in
the shape the app decodes, known statuses, unique App IDs (modes included), a name for every
game and mode. A game's optional `modes` are its Zombies/Multiplayer apps, each with a status."""
import json, re, sys
from pathlib import Path
data = json.loads((Path(__file__).resolve().parent.parent / 'status' / 'games.json').read_text())
assert data.get('version') == 1, 'version must be 1'
ids = set()
for g in data['games']:
    assert set(g) - {'modes'} == {'appID', 'name', 'status', 'note', 'updated'}, f'fields: {sorted(g)}'
    for m in [g] + g.get('modes', []):
        if m is not g:
            assert set(m) == {'appID', 'name', 'status', 'note'}, f'mode fields: {sorted(m)}'
        assert isinstance(m['appID'], int) and m['appID'] > 0 and m['appID'] not in ids, f"App ID {m['appID']}"
        ids.add(m['appID'])
        assert m['status'] in ('works', 'issues', 'notYet', 'cantRun'), f"status {m['status']}"
        assert isinstance(m['note'], str) and m['name'].strip(), 'every game and mode needs a name'
    assert isinstance(g.get('modes', []), list) and g.get('modes') != [], 'modes: leave the key out when there are none'
    assert g['updated'] == '' or re.fullmatch(r'\d{4}-\d{2}-\d{2}', g['updated']), f"date {g['updated']}"
print(f'check-status-list: PASS ({len(data["games"])} games, {len(ids) - len(data["games"])} modes)')
