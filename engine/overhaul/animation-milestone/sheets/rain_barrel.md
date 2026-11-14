# rain_barrel

## Work queue
- host: placed; family: barrel; family_engine: keepsakes.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (keepsakes.json): "rain_barrel": { "type": "barrel", "style": "oak", "w": 112, "h": 108, "scale": 0.6, "material": "wood", "skill": "stewardship", "verb": "Check water", "portable": false, "capacity": 60 }
- rain_barrel - art source: {'construction': 'keepsake-v1', 'family': 'barrel', 'kind': 'study', 'blueprint': 'rain_barrel', 'material': 'wood'}
- names taken by the drawing: ['contact', 'lid', 'gauge', 'tap', 'inside', 'entry']
- drawing anchors: 0=contact(0.21,0.31) 1=entry(0.50,0.99) 2=gauge(0.41,0.52) 3=inside(0.41,0.25) 4=lid(0.41,0.22) 5=tap(0.62,0.73)

## Drawn parts (y fraction, px above the standing line)
- lid dome at y 0.18-0.22 (px 364-343)
- barrel staves '|' columns from y 0.36 to 0.84 (px 280-84), hoops '(~)' at px 268 and 92
- water gauge window '00L' at y 0.62-0.70 (px 167-130)
- brass tap '===5===' at y 0.73 (px 117), anchor tap (0.62,0.73)
- stand legs '(+----+' at y 0.84-0.89 (px 67-46)
- base plinth '+------+' at y 0.93-0.96 (px 29-13)
- ground px 0

## Low parts (at or below 63 px)
- plinth px 13-29
- legs px 46-67 (?)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: plinth top px 29 (flat, full width) (?)
- adult <=70: plinth top px 29
  - stand top '+----+' px 67 (?)

## Existing behaviour (family_engine: keepsakes.json)
- keepsakes.json entry: type barrel, style oak, w 112 h 108, capacity 60, skill stewardship, verb 'Check water'
- no routine rows in any animation JSON

## Siblings (same family field in the work queue)
- none (family 'barrel' has only this object)
