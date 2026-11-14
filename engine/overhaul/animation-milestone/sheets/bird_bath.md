# bird_bath

## Work queue
- host: placed; family: birdbath; family_engine: waterworks.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (object-footprints.json): "bird_bath": { "width": 48.58, "height": 24.2, "floor": false, "construction": "waterworks-v1" }
- bird_bath - art source: {'construction': 'waterworks-v1', 'family': 'birdbath', 'kind': 'water', 'blueprint': 'bird_bath', 'material': 'stone'}
- names taken by the drawing: ['seat', 'entry', 'contact', 'water', 'rim', 'swimRadius']
- drawing anchors: 0=contact(0.21,0.33) 1=entry(0.19,0.93) 2=seat(0.51,0.36) 3=water(0.22,0.26)

## Drawn parts (y fraction, px above the standing line)
- rim '=======|=======' at y 0.17-0.19 (px 188-183)
- water surface '~~~' at y 0.57-0.76 (px 88-41)
- bowl walls '(  (' rings at y 0.29-0.83 (px 159-24)
- bird-perch or ornament '._.' at y 0.36 (px 141) (?)
- foot slab '_______-----' at y 0.81 (px 29), with '_' at px 24

## Low parts (at or below 63 px)
- foot slab px 24-29
- ground px 0

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: foot slab top px 29 (flat, about 0.15-0.85 wide) (?)
- adult <=70: foot slab px 29 (?)

## Existing behaviour (family_engine: waterworks.json)
- waterworks.json entry: type bath, style log, shallow true, w 82 h 43
- no routine rows in any animation JSON

## Siblings (same family field in the work queue)
- family 'birdbath': birdbath and birdbath_garden (both in this batch)
