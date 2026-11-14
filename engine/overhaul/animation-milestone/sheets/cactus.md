# cactus

## Work queue
- host: placed; family: cactus; family_engine: botanical.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (botanical.json): "cactus": { "type": "succulent", "shape": "saguaro", "w": 82, "h": 79, "scale": 0.81, "rooted": true, "container": "bed" }
- cactus - art source: {'construction': 'botanical-v1', 'family': 'cactus', 'kind': 'plant', 'blueprint': 'cactus', 'material': 'leaf'}
- names taken by the drawing: ['contact', 'flower', 'soil', 'entry', 'leaf', 'rim']
- drawing anchors: 0=contact(0.33,0.86) 1=entry(0.51,0.97) 2=flower(0.51,0.21) 3=leaf(0.33,0.86) 4=rim(0.41,0.92) 5=soil(0.51,0.92)

## Drawn parts (y fraction, px above the standing line)
- saguaro trunk '|' columns at x 0.25-0.80, y 0.41-0.95 (px 249-34)
- left arm '(|  |  )' at y 0.33-0.56 (px 282-181) and right arm '|   |' at y 0.41-0.69 (px 249-130)
- flower anchor at (0.51,0.21) (px 333)
- pot: rounded body '( )' at y 0.82-0.97 (px 68-0), rim '(  4  )' at px 23
- soil line '~~~~~~' at y 0.88-0.92 (px 40-23)
- anchor contact (0.33,0.86) px ~ 61

## Low parts (at or below 63 px)
- pot body px 0-23
- pot rim px 23 (?)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: soil line px 34 (flat '~~~~|~~~~|~~~') (?)
- adult <=70: soil line px 34 (?)
  - no other flat top under 70

## Existing behaviour (family_engine: botanical.json)
- botanical.json entry: type succulent, shape saguaro, rooted true, container bed, w 82 h 79
- botanical-routines.json: cactus_drops (mode water, tool can, anchor soil, when succulent true) and other succulent rows; label 'Counting a few drops for the cactus'

## Siblings (same family field in the work queue)
- family 'cactus': potted_cactus (both in this batch)
