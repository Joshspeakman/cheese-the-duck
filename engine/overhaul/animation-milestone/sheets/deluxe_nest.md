# deluxe_nest

## Work queue
- host: placed; family: nest; family_engine: None
- native_acts: rest inside (native residence)
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (home-workshop.mjs): deluxe_nest:{w:84,h:43,nest:'willow',lining:'quilt',props:['canopy','pillow','quilt','lantern'],shelter:true}, nest_premium:{w:88,h:44,nest:'wicker',lining:'velvet',props:['canopy','pillow','quilt','curtains'],shelter:true}, golden_nest:{w:90,h:44,nest:'gold',lining:'velvet',props:['canopy','pillow','quilt','jewels'],shelter:true}, bed_small:{w:78,h:40,bed:'pine',lining:'patchwork',props:['pillow','quilt','carving
- deluxe_nest - art source: {'construction': 'workshop-v1', 'family': 'nest', 'kind': 'comfort', 'blueprint': 'deluxe_nest', 'material': 'fabric'}
- names taken by the drawing: ['entry', 'seat', 'rim', 'workLeft', 'workRight', 'capacity']
- drawing anchors: 0=entry(0.51,0.75) 1=seat(0.51,0.82) 2=workLeft(0.20,0.85) 3=workRight(0.81,0.85)

## Drawn parts (y fraction, px above the standing line)
- canopy top '=====' at y 0.35-0.38, px 117-140 (flat top, above adult perch range)
- canopy valance '~~~' fringe at y 0.38-0.47, px 99-128
- canopy posts '|' at x ~0.17 and ~0.82 from px 6 to 128 (?)
- lantern hanging '_/o\|' right side at y 0.48-0.53, px 76-93 (prop lantern, ?)
- bowl rim '\'---'' at y 0.63-0.65, px 35-47; pillow/quilt '(  :  )' inside the rim
- willow bowl: y 0.65-0.85, px -29 to 23; seat (0.51,0.82) px -29; entry (0.51,0.75) px 0; workLeft (0.20,0.85) px -35; workRight (0.81,0.85) px -35

## Low parts (at or below 63 px)
- rim px 35-47 (partly above 36); entry px 0; post feet near px 6 (?)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none flat (rim is curved)
- adult <=70: none flat; canopy top (px 117-140) is far above 70

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- native: rest inside, with shelter (canopy); shelters.py HOMES deluxe_nest (True, 'hatchling'); shelters.py line 67 comfort 8
- home-rooms.json: room 'nest', capacity 2, elevated False; no routine keyed to it in animation JSON

## Siblings (same family field in the work queue)
- family 'nest': basic_nest, cozy_nest, golden_nest, nest_premium
