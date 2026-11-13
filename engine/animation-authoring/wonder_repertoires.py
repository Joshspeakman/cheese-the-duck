"""Emit honest per-object repertoire records for the wonders (no acceptance claims).

Stages: implemented = runs end to end in the real game under check_wonders.py;
liveRenderSampled marks routines also rendered from a captured native frame by
wonders-check.cjs (not indexed evidence, so no 'replayed' stage is claimed).
verifiedSequences stays 0: no wonder has 48 accepted sequences, visitor roles,
egg observation, all-age/guest bindings or a semantic review yet.
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
ITEMS = json.loads((ROOT / 'client/animation/wonders.json').read_text())
ROUTINES = json.loads((ROOT / 'client/animation/wonder-routines.json').read_text())
native = json.loads((ROOT / 'artifacts/animation-milestone/wonder-native.json').read_text())
render = json.loads((ROOT / 'artifacts/animation-milestone/wonders-render.json').read_text())
frames = json.loads((ROOT / 'artifacts/animation-milestone/wonder-frames.json').read_text())
REACH = json.loads((ROOT / 'client/animation/wonder-reach.json').read_text())['routines']
replayed = {str(f.get('review')).split('-')[0] for f in frames} if render.get('replay', {}).get('workers') == len(frames) else set()
assert native['result'] == 'PASS' and native['routines'] == len(ROUTINES)
out = ROOT / 'overhaul/animation-milestone/repertoires'
for oid in ITEMS:
    seqs = []
    for key, r in ROUTINES.items():
        if r['item'] != oid:
            continue
        parts = sorted({k for _, q in r['track'] for k in q if k not in ('x', 'y', 'b', 'w', 'l', 'r', 'reach', 'contact', 'eye', 'mark', 'anchor')})
        seqs.append(dict(id=key, status='implemented', liveRenderSampled=key in replayed, verified=False, label=r['label'], duration_seconds=r['duration'],
                         source=dict(path='engine/client/animation/wonder-routines.json', json_pointer='/' + key),
                         production_entry=dict(command=dict(type='pond', action='wonder_action', target=oid, instance='<existing-owned-placed-instance>', text=key),
                                               autonomous='living_world.decide -> wonders.best (context appeal)'),
                         contacts=[name for _, name in r['events']], anchors=sorted({q['anchor'] for _, q in r['track'] if q.get('anchor')}), parts_moved=parts,
                         tool=r['tool'], when=r['when'], prefer=r['prefer'], ages=r['ages'] or 'all hatched ages', reachableAges=REACH[key]['reachableAges'], contactHeightPx=REACH[key]['contactHeight'],
                         evidence_note='engine/check_wonders.py (native, disposable save)' + ('; wonders-check.cjs live render' if key in replayed else '')))
    doc = dict(schemaVersion=1, objectId=oid, status='implemented_not_accepted', requiredSequences=48, authoredSequences=len(seqs), verifiedSequences=0,
               nativeCheck=dict(command='.venv/bin/python engine/check_wonders.py', result=native['result'], checks=native['checks'], routineAgeRuns=native.get('routineAgeRuns')),
               missing=['48-sequence target: ' + str(48 - len(seqs)) + ' more meaningful sequences',
                        'visitor company roles (guests joining, watching, taking turns)', 'egg-age observation role',
                        'per-age and per-guest bindings beyond the authored age gates', 'semantic distinctness review by a person',
                        'rendered evidence for every routine (only sampled routines replayed)'],
               sequences=seqs)
    (out / (oid + '.json')).write_text(json.dumps(doc, indent=1) + '\n')
print(len(ITEMS), 'repertoire records', sum(1 for k in ROUTINES if k in replayed), 'replayed')
