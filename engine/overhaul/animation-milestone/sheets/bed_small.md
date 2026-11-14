# bed_small

## Work queue
- host: placed; family: bed; family_engine: None
- native_acts: rest inside (native residence)
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (home-workshop.mjs): bed_small:{w:78,h:40,bed:'pine',lining:'patchwork',props:['pillow','quilt','carving'],shelter:false}, bed_king:{w:100,h:49,bed:'fourposter',lining:'velvet',props:['pillow','quilt','canopy','curtains'],shelter:false}, cozy_bed:{w:86,h:43,bed:'round',lining:'wool',props:['pillow','quilt','book'],shelter:false}, }; const has=(p,key)=>p.props.includes(key),hash=s=>[...s].reduce((n,c)=>(Math.imul(n,31)+c.charCodeAt(0))>
- bed_small - art source: {'construction': 'workshop-v1', 'family': 'bed', 'kind': 'comfort', 'blueprint': 'bed_small', 'material': 'fabric'}
- names taken by the drawing: ['entry', 'seat', 'rim', 'capacity']
- drawing anchors: 0=entry(0.51,0.72) 1=seat(0.51,0.64)

## Drawn parts (y fraction, px above the standing line)
- headboard top '+------+' at y 0.21, px 138 (top edge)
- mattress top '=====' at y 0.26, px 124 (flat, above adult perch)
- pillows '(o)' row at y 0.33, px 103; '<~ o ~>' pillow pattern at y 0.31 px 110 (?)
- quilt panels '|  |' at y 0.36-0.46, px 76-96; '<><>' pattern at y 0.41 px 83
- carved footboard panel '(.-----.)' at y 0.46-0.51, px 55-69 (prop carving, ?)
- skirt rail '+-----+' at y 0.56, px 41; skirt '(~~~~)' at y 0.59, px 34 (?)
- quilt hem '<>' fringe at y 0.62-0.74, px -14 to 28; feet '|::|' at y 0.90-0.92, px -48 to -55
- entry anchor (0.51,0.72) px 0; seat anchor (0.51,0.64) px 21 (in the quilt hem)

## Low parts (at or below 63 px)
- skirt/rail px 34-41; quilt hem px -14 to 28; entry px 0; feet below the line

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: skirt top px ~34 (curved '(~~~~)' band, ?) = weak candidate
- adult <=70: same skirt top px 34-41 (?); nothing else flat under 70

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- native: rest inside; shelters.py HOMES bed_small (False, 'hatchling') = no roof; comfort 8 (shelters.py line 67)
- home-rooms.json: room 'bed', capacity 1, elevated False; no routine keyed to it in animation JSON

## Siblings (same family field in the work queue)
- family 'bed': bed_king, cozy_bed
