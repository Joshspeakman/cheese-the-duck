# bonsai

## Work queue
- host: placed; family: bonsai; family_engine: botanical.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (botanical.json): "bonsai": { "type": "tree", "shape": "bonsai", "w": 98, "h": 71, "scale": 0.8, "rooted": true, "container": "dish" }
- bonsai - art source: {'construction': 'botanical-v1', 'family': 'bonsai', 'kind': 'plant', 'blueprint': 'bonsai', 'material': 'leaf'}
- names taken by the drawing: ['contact', 'flower', 'soil', 'entry', 'leaf', 'rim']
- drawing anchors: 0=contact(0.58,0.59) 1=entry(0.51,0.97) 2=flower(0.45,0.16) 3=leaf(0.58,0.59) 4=rim(0.42,0.87) 5=soil(0.51,0.76)

## Drawn parts (y fraction, px above the standing line)
- canopy of fronds '/\ | /' over y 0.03-0.80 (px 368-67)
- trunk and branch band '////////' at y 0.70 (px 106), anchor contact (0.58,0.59) (?)
- soil line '_ _' at y 0.89 (px 33) (?)
- dish rim '\-----(' at y 0.87 (px 39)
- dish body '\' and '/' from y 0.90 to 0.96 (px 28-6), rim '====' at y 0.94 (px 11)
- ground '[__]' at y 0.97 (px 0)

## Low parts (at or below 63 px)
- dish px 0-28
- soil line px 33

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: dish top edge px 11 (flat, wide) (?)
  - soil line px 33 (?)
- adult <=70: dish rim px 39 (flat)
  - soil ring px 61 (?)

## Existing behaviour (family_engine: botanical.json)
- botanical.json entry: type tree, shape bonsai, rooted true, container dish, w 98 h 71
- no routine rows in any animation JSON

## Siblings (same family field in the work queue)
- none (family 'bonsai' has only this object)
