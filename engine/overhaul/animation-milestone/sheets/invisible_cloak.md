# invisible_cloak

## Work queue
- host: placed; family: cape; family_engine: wonders.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 4 - family_routines 0 = 44); repertoire_routines: 0; family_routines: 0; wonder_routines: 4; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (object-footprints.json): "invisible_cloak": { "width": 22.42, "height": 22.1, "floor": false, "construction": "wonder-v1" }
- invisible_cloak - art source: {'construction': 'wonder-v1', 'family': 'cape', 'kind': 'wonder', 'blueprint': 'invisible_cloak', 'material': 'cloth'}
- names taken by the drawing: ['entry', 'contact', 'hem', 'mid', 'shoulder', 'hook']
- drawing anchors: 0=contact(0.51,0.81) 1=entry(0.51,1.00) 2=hem(0.51,0.83) 3=hook(0.51,0.08) 4=mid(0.51,0.68) 5=shoulder(0.51,0.24)

## Drawn parts (y fraction, px above the standing line)
- hanger hook '_/3~~\_' at y 0.08 (px 212), anchor hook (0.51,0.08)
- shoulders at y 0.19-0.29 (px 189-165), anchor shoulder (0.51,0.24)
- cloak body with shimmer texture ':.~' tapering from y 0.29 to 0.85 (px 165-35), anchor mid (0.51,0.68)
- hem at y 0.83 (px 39), anchor hem (0.51,0.83), ragged (no flat top)
- stand bar '=====' at y 0.97 (px 8), feet '/____\' at y 0.98 (px 4)

## Low parts (at or below 63 px)
- stand bar px 8
- feet px 0-4

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: stand bar px 8 (flat, about 19 cols) (?)
- adult <=70: none flat under 70 (hem is ragged)

## Existing behaviour (family_engine: wonders.json)
- wonders.json: fields shimmer, folded, hidden, dust; effects shake, fold, hang, hide, peek
- wonder-routines.json: cloak_shake_out, cloak_hide_under, cloak_fold, cloak_hang_up (4)
- labels: 'Shaking the cloak out so it shimmers...', 'Hiding under the cloak and sneaking a look out', 'Folding the cloak neatly over the stand'

## Siblings (same family field in the work queue)
- family 'cape': cape and cape_superhero are garments (garments.json, wearable-slots.json); not in this batch
