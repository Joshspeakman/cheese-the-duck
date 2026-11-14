# chair_wood

## Work queue
- host: placed; family: chair; family_engine: furniture.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (furniture.json): "chair_wood":{"type":"chair","style":"ladder","w":66,"h":59,"scale":0.76,"capacity":1,"seat":true}
- chair_wood - art source: {'construction': 'furniture-v1', 'family': 'chair', 'kind': 'comfort', 'blueprint': 'chair_wood', 'material': 'fabric'}
- names taken by the drawing: ['seat', 'slots', 'seatWidth', 'entry', 'front', 'back', 'arm']
- drawing anchors: 0=arm(0.80,0.55) 1=back(0.51,0.45) 2=entry(0.51,0.97) 3=seat(0.51,0.69)

## Drawn parts (y fraction, px above the standing line)
- back top rails '+---+' at y 0.14-0.17 (px 279-267)
- back slats '~~~' and rungs at y 0.22-0.33 (px 250-215)
- back posts '|' at x 0.10 and 0.90, y 0.14-0.64 (px 279-110)
- seat frame '+---+' at y 0.59-0.74 (px 128-76), anchor seat (0.51,0.69)
- lower rung '========' at y 0.83 (px 47, flat, full width)
- legs '|' at y 0.74-0.97 (px 76-0), feet '[___]' at px 6

## Low parts (at or below 63 px)
- lower rung px 47
- legs px 0-76
- feet px 6

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none flat under 36 (feet are at px 6)
- adult <=70: lower rung px 47 (flat, full width) (?)

## Existing behaviour (family_engine: furniture.json)
- furniture.json entry: type chair, style ladder, capacity 1, seat true, w 66 h 59
- no routine rows in any animation JSON; furniture.json 'chair_throne' is a different family (throne)

## Siblings (same family field in the work queue)
- none (family 'chair' has only this object)
