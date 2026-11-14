# toy_ball

## Work queue
- host: placed; family: ball; family_engine: None
- native_acts: None
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (playground-workshop.mjs): toy_ball:{type:'ball',w:48,h:38,scale:.43,pattern:'panels'},ball:{type:'ball',w:48,h:38,scale:.43,pattern:'stripes'},snowball:{type:'ball',w:44,h:34,scale:.4,pattern:'snow'}, toy_blocks:{type:'blocks',w:76,h:49,scale:.72}, toy_trampoline:{type:'trampoline',w:88,h:51,scale:.87,net:true},trampoline:{type:'trampoline',w:74,h:40,scale:.8,net:false}, toy_slide:{type:'slide',w:100,h:72,scale:.95,style:'wood'},water_slid
- toy_ball - art source: {'construction': 'playground-v1', 'family': 'ball', 'kind': 'toy', 'blueprint': 'toy_ball', 'material': 'paint'}
- names taken by the drawing: ['contact', 'top']
- drawing anchors: 0=contact(0.87,0.62) 1=top(0.51,0.32)

## Drawn parts (y fraction, px above the standing line)
- ball sphere with panel pattern '.': y 0.32-0.92, px 14-87
- top anchor (0.51,0.32) px 87 (top rim, flat '_______' 15 chars wide at px ~84)
- hub/valve '(o)' at centre-front, y 0.76, px 31 (?)
- contact anchor (0.87,0.62) px 49 (right edge, bounce contact, ?)
- bottom edge '_' at y 0.89-0.92, px 10-14

## Low parts (at or below 63 px)
- lower half of the sphere, px 14-63 (curved, not flat)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none (curved sphere)
- adult <=70: none (the flat top rim is at px ~84, above 70)

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- playdates.py TOYS maps toy_ball and ball to family 'ball'; playdates.json has ball_pass (28 s) and ball_bounce (26 s) acts; native_acts in the queue is None
- shelters.py HOMES: not listed

## Siblings (same family field in the work queue)
- family 'ball': ball, frozen_dewdrop, snowball
