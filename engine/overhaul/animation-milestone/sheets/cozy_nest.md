# cozy_nest

## Work queue
- host: placed; family: nest; family_engine: None
- native_acts: rest inside (native residence)
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (home-workshop.mjs): cozy_nest:{w:76,h:35,nest:'braid',lining:'wool',props:['pillow','quilt','leaf'],shelter:false}, deluxe_nest:{w:84,h:43,nest:'willow',lining:'quilt',props:['canopy','pillow','quilt','lantern'],shelter:true}, nest_premium:{w:88,h:44,nest:'wicker',lining:'velvet',props:['canopy','pillow','quilt','curtains'],shelter:true}, golden_nest:{w:90,h:44,nest:'gold',lining:'velvet',props:['canopy','pillow','quilt','jewels'],sh
- cozy_nest - art source: {'construction': 'workshop-v1', 'family': 'nest', 'kind': 'comfort', 'blueprint': 'cozy_nest', 'material': 'fabric'}
- names taken by the drawing: ['entry', 'seat', 'rim', 'workLeft', 'workRight', 'capacity']
- drawing anchors: 0=entry(0.51,0.71) 1=seat(0.51,0.79) 2=workLeft(0.21,0.83) 3=workRight(0.80,0.83)

## Drawn parts (y fraction, px above the standing line)
- rim/wool lining: y 0.58-0.62, px 29-41 (the top band of the bowl, ~38 chars wide)
- braided bowl (braid): y 0.62-0.85, px -41 to 23, with '><' pillow-stuffing marks at px -6 to -52 (?)
- quilt/box (props quilt): '+-----+' at y 0.83, px -35, centre (?)
- leaf (props) '/;  /' and '(.:)' at the right, y 0.60-0.66, px 17-35 (?)
- entry anchor (0.51,0.71) px 0; seat (0.51,0.79) px -23; workLeft (0.21,0.83) px -35; workRight (0.80,0.83) px -35

## Low parts (at or below 63 px)
- all parts (the nest is low); rim px 29-41 is the highest flat-ish part

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none (rim curved, starts at px 29-41)
- adult <=70: rim top px 41 curved lip; not a flat perch

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- native: rest inside; shelters.py HOMES cozy_nest (False, 'hatchling') = no roof; comfort 8 (shelters.py line 67)
- home-rooms.json: room 'nest', capacity 2, elevated False; no routine keyed to it in animation JSON

## Siblings (same family field in the work queue)
- family 'nest': basic_nest, deluxe_nest, golden_nest, nest_premium
