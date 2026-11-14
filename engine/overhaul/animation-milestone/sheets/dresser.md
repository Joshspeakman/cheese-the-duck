# dresser

## Work queue
- host: placed; family: cabinet; family_engine: furniture.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (furniture.json): "dresser":{"type":"cabinet","style":"drawers","w":94,"h":62,"scale":0.87}
- dresser - art source: {'construction': 'furniture-v1', 'family': 'cabinet', 'kind': 'storage', 'blueprint': 'dresser', 'material': 'wood'}
- names taken by the drawing: ['contact', 'entry']
- drawing anchors: 0=contact(0.51,0.51) 1=entry(0.51,0.97)

## Drawn parts (y fraction, px above the standing line)
- top y 0.10-0.11 (px 353-346)
- drawer rows '(=)' at y 0.13-0.28 (px 339-280) with '|' fronts
- drawer fronts y 0.28-0.67 (px 280-120), wavy seams '~~~' at px 160 and 73, handles 'o' at px 240 and 200
- plinth '+------+' at y 0.84-0.89 (px 53-40)
- feet '(===)' at y 0.89 (px 33) and '[___]' at px 7

## Low parts (at or below 63 px)
- feet px 7-33
- plinth px 40-53

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: feet top px 33 (?)
- adult <=70: plinth top px 40 (flat, full width) (?)
  - plinth lower edge px 53 (?)

## Existing behaviour (family_engine: furniture.json)
- furniture.json entry: type cabinet, style drawers, w 94 h 62
- no routine rows in any animation JSON

## Siblings (same family field in the work queue)
- family 'cabinet': cabinet and wardrobe (both in this batch)
