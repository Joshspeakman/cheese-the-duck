# aurora

## Work queue
- host: placed; family: aurora; family_engine: wonders.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 6 - family_routines 0 = 42); repertoire_routines: 0; family_routines: 0; wonder_routines: 6; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (object-footprints.json): "aurora": { "width": 35.7, "height": 26.65, "floor": false, "construction": "wonder-v1" }
- aurora - art source: {'construction': 'wonder-v1', 'family': 'aurora', 'kind': 'wonder', 'blueprint': 'aurora', 'material': 'glass'}
- names taken by the drawing: ['entry', 'contact', 'switch', 'dial', 'lens']
- drawing anchors: 0=contact(0.51,0.87) 1=dial(0.68,0.89) 2=entry(0.51,1.00) 3=lens(0.51,0.65) 4=switch(0.31,0.89)

## Drawn parts (y fraction, px above the standing line)
- halo of ribbons: '(' arcs and lens rings, y 0.51-0.64 (px 137-106), hub '(-)' at y 0.58 (px 116)
- lens cap '+---3---+' at y 0.65-0.67 (px 96-91), anchor lens (0.51,0.65)
- cone body '/ | \' from y 0.69 to 0.87 (px 86-35), tripod-like
- base ring '+-----0-----+' at y 0.87 (px 35), full width
- control box: dial '(*1.)' and switch '--+-4-+' at y 0.89-0.93 (px 30-25), anchors dial (0.68,0.89) and switch (0.31,0.89)
- box base '+-----+' at y 0.95 (px 15); entry px 0

## Low parts (at or below 63 px)
- base ring px 35 (cone foot)
- control box px 15-30
- entry px 0

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: base ring top px 35 (flat, full width) (?)
- adult <=70: base ring px 35 (flat) and control box top px 30 (?)

## Existing behaviour (family_engine: wonders.json)
- wonders.json: fields power, hue, ribbons, glow, drift; effects on, off, hue, ribbon, dim
- wonder-routines.json: aurora_switch_on, aurora_tune_colour, aurora_add_ribbon, aurora_lie_and_watch, aurora_bedtime_dim, aurora_switch_off (6)
- labels: 'Flicking on the aurora lamp...', 'Turning the brass dial through greens and violets', 'Lying back on the grass to watch...'

## Siblings (same family field in the work queue)
- none (family 'aurora' has only this object). Its 6 routines already cover switching, colour, ribbons and lying down
