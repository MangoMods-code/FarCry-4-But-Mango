#!/usr/bin/env python3
"""status/games.json, the tested-games list the app reads (MangoStatusStore): valid JSON in
the shape the app decodes, known statuses, unique App IDs, a name for every game."""
import json, re, sys
from pathlib import Path
data = json.loads((Path(__file__).resolve().parent.parent / 'status' / 'games.json').read_text())
assert data.get('version') == 1, 'version must be 1'
ids = set()
for g in data['games']:
    assert set(g) == {'appID', 'name', 'status', 'note', 'updated'}, f'fields: {sorted(g)}'
    assert isinstance(g['appID'], int) and g['appID'] > 0 and g['appID'] not in ids, f"App ID {g['appID']}"
    ids.add(g['appID'])
    assert g['status'] in ('works', 'issues', 'notYet', 'cantRun'), f"status {g['status']}"
    assert g['name'].strip(), 'every game needs a name'
    assert g['updated'] == '' or re.fullmatch(r'\d{4}-\d{2}-\d{2}', g['updated']), f"date {g['updated']}"
print(f'check-status-list: PASS ({len(ids)} games)')
