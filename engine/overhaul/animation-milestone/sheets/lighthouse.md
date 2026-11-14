# lighthouse

## Work queue
- host: placed; family: lighthouse; family_engine: None
- native_acts: rest inside (native residence)
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (home-workshop.mjs): lighthouse:{w:76,h:80,roof:'beacon',wall:'tower',door:[26,56,23,20],windows:[[27,36,19,12]],props:['beacon','stairs','rope'],roofInk:'#a6aeb1',shelter:true}, basic_nest:{w:66,h:29,nest:'twig',lining:'grass',props:['feather','leaf'],shelter:false}, cozy_nest:{w:76,h:35,nest:'braid',lining:'wool',props:['pillow','quilt','leaf'],shelter:false}, deluxe_nest:{w:84,h:43,nest:'willow',lining:'quilt',props:['canopy','pill
- lighthouse - art source: {'construction': 'workshop-v1', 'family': 'lighthouse', 'kind': 'structure', 'blueprint': 'lighthouse', 'material': 'wood'}
- names taken by the drawing: ['entry', 'seat', 'opening', 'capacity']
- drawing anchors: 0=entry(0.50,0.96) 1=opening(0.35,0.71) 2=seat(0.50,0.94)

## Drawn parts (y fraction, px above the standing line)
- roof/beacon cap, cone with finial: y 0.04-0.15, px 596-680 (roof ink #a6aeb1)
- gallery rail: y 0.16-0.18, px 578-587, full width
- lantern housing: y 0.19-0.28, px 503-568; round port '(o)' at 0.22 px 550 (?)
- tower wall with ledges every ~0.07 (px 475, 419, 363, 307, 252, 196, 140, 84, 28)
- window, framed and mullioned: y 0.44-0.61, px 261-382 (blueprint windows [27,36,19,12])
- door (?): lower centre, y 0.70-0.95, px ~9-196, panelled grid (blueprint door [26,56,23,20]); opening anchor (0.35,0.71) px 186
- stairs (props): dotted rung rows across the left column at y 0.35-0.66, px 233-447 (?)
- rope (props): loops and '~' hanging on the right exterior, y 0.85-0.93, px 19-84 (?)
- base platform: y 0.94-0.96, px 0-19; seat anchor (0.50,0.94) px 19, entry anchor (0.50,0.96) px 0

## Low parts (at or below 63 px)
- base platform px 19 and entry px 0; rope tail px 19-56 (?); tower ledge at px 28 (the '__|____' sill, ?)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: base platform top px 19 (flat, full width) = candidate; ledge px 28 (?)
- adult <=70: px 19 and px 28 (?); nothing else flat under 70 (next ledge px 84)

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- shelters.py HOMES: lighthouse (True, 'juvenile') = roof, youngest juvenile; resting inside is native
- home-rooms.json: room 'watch', capacity 2, elevated True. No routine keyed to it in animation JSON
- shelters.py line 11 also lists treehouse; living_world.py has no entry by name

## Siblings (same family field in the work queue)
- family 'lighthouse' has only this object
