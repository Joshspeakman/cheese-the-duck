# carousel

## Work queue
- host: placed; family: carousel; family_engine: excursions.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (excursions.json): "carousel": {"type":"carousel","w":148,"h":128,"scale":0.66,"material":"wood","motion":"motor"}
- carousel - art source: {'construction': 'excursion-v1', 'family': 'carousel', 'kind': 'toy', 'blueprint': 'carousel', 'material': 'paint'}
- names taken by the drawing: ['entry', 'contact', 'seat', 'pole', 'rides', 'fronts', 'roof', 'route']
- drawing anchors: 0=contact(0.82,0.91) 1=entry(0.82,0.99) 2=pole(0.50,0.61) 3=seat(0.50,0.78)

## Drawn parts (y fraction, px above the standing line)
- peaked roof with striped '+:' canopy at y 0.09-0.31 (px 525-401), finial '<*>' at y 0.01 (px 575)
- scalloped awning '(  (' at y 0.33-0.38 (px 387-359), anchor pole (0.50,0.61)
- horse seats 'o' in a row at y 0.38 (px 359)
- central pole '|:|' at x 0.50, y 0.40-0.78 (px 345-124)
- platform: stands '| |' and ornaments '~' at y 0.83-0.91 (px 97-46)
- base rim '______' at y 0.91 (px 46, flat, full width), skirt '=====' px 14-28

## Low parts (at or below 63 px)
- base rim px 46
- skirt px 14-28

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: lower skirt bar px 18 (flat) (?)
- adult <=70: base rim px 46 (flat, full width)

## Existing behaviour (family_engine: excursions.json)
- excursions.json entry: type carousel, w 148 h 128, motion motor
- carnival-routines.json: carousel_first, carousel_parade, carousel_trot, carousel_shy, carousel_quiet, carousel_glow (6)
- labels: 'Find a gentle carousel rhythm', 'Lead a very important parade', 'Count the wooden duck trot', 'Circle beneath the evening bulbs'

## Siblings (same family field in the work queue)
- none (family 'carousel' has only this object)
