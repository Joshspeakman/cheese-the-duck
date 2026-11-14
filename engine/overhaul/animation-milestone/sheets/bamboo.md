# bamboo

## Work queue
- host: placed; family: bamboo; family_engine: botanical.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (botanical.json): "bamboo": { "type": "bamboo", "shape": "grove", "w": 108, "h": 99, "scale": 0.88, "rooted": true, "container": "none" }
- bamboo - art source: {'construction': 'botanical-v1', 'family': 'bamboo', 'kind': 'plant', 'blueprint': 'bamboo', 'material': 'leaf'}
- names taken by the drawing: ['contact', 'flower', 'soil', 'entry', 'leaf', 'rim']
- drawing anchors: 0=contact(0.50,0.79) 1=entry(0.50,0.98) 2=flower(0.50,0.30) 3=leaf(0.14,0.60) 4=rim(0.43,0.94) 5=soil(0.50,0.94)

## Drawn parts (y fraction, px above the standing line)
- leaf sprays at top, y 0.08-0.13 (px 540-509)
- flower head anchor at (0.50,0.30) (px 436)
- grove stalks with nodes '|:|' and leaf whorls '\//\', y 0.22-0.62 (px 454-215)
- bare lower nodes '|:|' at y 0.71-0.84 (px 160-86)
- pot rim '[=]|' segments at y 0.88 (px 61)
- pot body '_/|\_' with soil at y 0.94 (px 25)
- ground px 0

## Low parts (at or below 63 px)
- pot body and soil px 25
- rim px 61 is the low edge of the pot (?)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: pot rim / soil line px 25 (?)
- adult <=70: pot rim px 61 (segmented, roughly flat) (?)

## Existing behaviour (family_engine: botanical.json)
- botanical.json entry: type bamboo, shape grove, rooted true, container none, w 108 h 99
- no routine rows in any animation JSON; no family routines

## Siblings (same family field in the work queue)
- none (family 'bamboo' has only this object)
