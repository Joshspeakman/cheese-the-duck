# potted_cactus

## Work queue
- host: placed; family: cactus; family_engine: botanical.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (botanical.json): "potted_cactus": { "type": "succulent", "shape": "barrel", "w": 74, "h": 65, "scale": 0.76, "rooted": true, "container": "pot", "color": "gold" }
- potted_cactus - art source: {'construction': 'botanical-v1', 'family': 'cactus', 'kind': 'plant', 'blueprint': 'potted_cactus', 'material': 'leaf'}
- names taken by the drawing: ['contact', 'flower', 'soil', 'entry', 'leaf', 'rim']
- drawing anchors: 0=contact(0.16,0.62) 1=entry(0.51,0.97) 2=flower(0.51,0.11) 3=leaf(0.16,0.62) 4=rim(0.40,0.77) 5=soil(0.51,0.70)

## Drawn parts (y fraction, px above the standing line)
- upper crown with flower 'o o' at y 0.14 (px 281), anchor flower (0.51,0.11)
- ribs '|' columns at y 0.19-0.70 (px 265-90), arms '(' and ')' at y 0.23-0.66
- soil band '~~~~~~~' at y 0.70-0.72 (px 90-85)
- pot rim '==========4=====' at y 0.77 (px 69), full width (flat)
- pot body '\ ... /' with '|  |' ribs at y 0.78-0.91 (px 64-21)
- pot base '\___________/' at y 0.91 (px 21)

## Low parts (at or below 63 px)
- pot base px 21
- lower rim px 58 (?)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: pot foot px 21 (?)
- adult <=70: pot rim px 69 (flat, full width)
  - lower body edge px 58 (?)

## Existing behaviour (family_engine: botanical.json)
- botanical.json entry: type succulent, shape barrel, rooted true, container pot, color gold, w 74 h 65
- no separate routine rows keyed to this id; cactus_drops (when succulent) can apply

## Siblings (same family field in the work queue)
- family 'cactus': cactus (both in this batch)
