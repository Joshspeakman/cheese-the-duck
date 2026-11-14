# bed_king

## Work queue
- host: placed; family: bed; family_engine: None
- native_acts: rest inside (native residence)
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (home-workshop.mjs): bed_king:{w:100,h:49,bed:'fourposter',lining:'velvet',props:['pillow','quilt','canopy','curtains'],shelter:false}, cozy_bed:{w:86,h:43,bed:'round',lining:'wool',props:['pillow','quilt','book'],shelter:false}, }; const has=(p,key)=>p.props.includes(key),hash=s=>[...s].reduce((n,c)=>(Math.imul(n,31)+c.charCodeAt(0))>>>0,7); function plankWall(c,x,y,w,h,kind){ c.rect(x,y,w,h,'b',true); if(kind==='stone'){ for(let j
- bed_king - art source: {'construction': 'workshop-v1', 'family': 'bed', 'kind': 'comfort', 'blueprint': 'bed_king', 'material': 'fabric'}
- names taken by the drawing: ['entry', 'seat', 'rim', 'capacity']
- drawing anchors: 0=entry(0.51,0.77) 1=seat(0.51,0.71)

## Drawn parts (y fraction, px above the standing line)
- finial '(o)' on each post top at y 0.06, px 289 (?)
- canopy/tester top rail '=====' at y 0.10, px 272, full width (too high for perch)
- posts '|:|' both sides, y 0.12-0.88 (fourposter posts, carved ':', ?)
- mattress top '=====' at y 0.40, px 153, full width (top of the bed)
- quilt panels '|  |' with '(o)' tufts at y 0.42-0.48, px 119-145 (props quilt)
- pillow '(  .--.  )' at y 0.56-0.60, px 68-85 (props pillow, ?); blanket '~' at y 0.58 px 77 (?)
- bed rail/skirt '(-----)' at y 0.62-0.67, px 43-60 (rail top, ?)
- frame boards and studs '|---|' at y 0.67-0.85, px -34 to 43; legs '|::|' feet at y 0.92-0.96, px -60 to -77
- seat anchor (0.51,0.71) px ~34 region; entry (0.51,0.77) px ~15 (?)

## Low parts (at or below 63 px)
- frame skirt px 43-51; frame boards px -34 to 43; feet below the line; entry near px 15

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none flat (the frame boards sit below the mattress)
- adult <=70: skirt/rail top px ~43-51 (?) = the only candidate; it is a hanging skirt, low confidence

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- native: rest inside; shelters.py HOMES bed_king (False, 'hatchling') = no roof; comfort 8 (shelters.py line 67)
- home-rooms.json: room 'bed', capacity 2, elevated False; no routine keyed to it in animation JSON

## Siblings (same family field in the work queue)
- family 'bed': bed_small, cozy_bed
