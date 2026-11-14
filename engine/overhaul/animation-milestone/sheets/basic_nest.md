# basic_nest

## Work queue
- host: placed; family: nest; family_engine: None
- native_acts: rest inside (native residence)
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (home-workshop.mjs): basic_nest:{w:66,h:29,nest:'twig',lining:'grass',props:['feather','leaf'],shelter:false}, cozy_nest:{w:76,h:35,nest:'braid',lining:'wool',props:['pillow','quilt','leaf'],shelter:false}, deluxe_nest:{w:84,h:43,nest:'willow',lining:'quilt',props:['canopy','pillow','quilt','lantern'],shelter:true}, nest_premium:{w:88,h:44,nest:'wicker',lining:'velvet',props:['canopy','pillow','quilt','curtains'],shelter:true}, golde
- basic_nest - art source: {'construction': 'workshop-v1', 'family': 'nest', 'kind': 'comfort', 'blueprint': 'basic_nest', 'material': 'fabric'}
- names taken by the drawing: ['entry', 'seat', 'rim', 'workLeft', 'workRight', 'capacity']
- drawing anchors: 0=entry(0.51,0.67) 1=seat(0.51,0.76) 2=workLeft(0.23,0.80) 3=workRight(0.79,0.80)

## Drawn parts (y fraction, px above the standing line)
- rim/lining top (grass): y 0.54-0.61, px 17-35; feather prop '/' at the top right (?)
- bowl wall (twig): y 0.61-0.79, px -23 to 17, with leaf props '\|/' at px 0-6 (?)
- entry anchor (0.51,0.67) px 0 (the mouth, at the standing line)
- seat anchor (0.51,0.76) px -17 (inside the bowl, below the standing line)
- workLeft (0.23,0.80) px -29; workRight (0.79,0.80) px -29 (side work points)
- bowl floor and lower twig weave: px -23 to -82

## Low parts (at or below 63 px)
- the whole nest is at or below px 35; rim px 23-35; entry px 0

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: rim px 23-35 is a curved lip, not a flat perch
- adult <=70: same rim; it is a bowl to sit in, not a perch (no candidate)

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- native: rest inside (native residence); shelters.py HOMES basic_nest (False, 'hatchling') = no roof
- home-rooms.json: room 'nest', capacity 1, elevated False; shelters.py line 67 gives comfort 8 for nest/bed keys
- no routine keyed to basic_nest in animation JSON; living_world.py has no entry by name

## Siblings (same family field in the work queue)
- family 'nest': cozy_nest, deluxe_nest, golden_nest, nest_premium
