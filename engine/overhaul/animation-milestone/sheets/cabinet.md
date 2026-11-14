# cabinet

## Work queue
- host: placed; family: cabinet; family_engine: furniture.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (furniture.json): "cabinet":{"type":"cabinet","style":"glass","w":100,"h":77,"scale":0.92}
- cabinet - art source: {'construction': 'furniture-v1', 'family': 'cabinet', 'kind': 'storage', 'blueprint': 'cabinet', 'material': 'wood'}
- names taken by the drawing: ['contact', 'entry']
- drawing anchors: 0=contact(0.51,0.51) 1=entry(0.51,0.97)

## Drawn parts (y fraction, px above the standing line)
- cornice y 0.08-0.11 (px 479-465)
- glass top grid '(=)' rows at y 0.11-0.22 (px 465-422), anchor contact (0.51,0.51)
- door panels y 0.30-0.78 (px 359-106) with handles '[*=]' at px 317 and '[o=]' at px 169
- kick plinth '+------+' at y 0.84-0.89 (px 70-42)
- feet '(===)' at y 0.91 (px 35) and '[___]' at px 7

## Low parts (at or below 63 px)
- feet px 0-35
- plinth px 42 (flat, full width)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: feet top px 35 (?)
- adult <=70: plinth top px 42 (flat, full width)
  - plinth inner line px 56 (?)

## Existing behaviour (family_engine: furniture.json)
- furniture.json entry: type cabinet, style glass, w 100 h 77
- repertoire-reach.json: displaySlots cabinet
- no routine rows in any animation JSON

## Siblings (same family field in the work queue)
- family 'cabinet': dresser and wardrobe (both in this batch)
