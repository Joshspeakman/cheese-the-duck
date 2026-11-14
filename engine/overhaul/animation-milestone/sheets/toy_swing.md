# toy_swing

## Work queue
- host: placed; family: swing; family_engine: None
- native_acts: ride / explore (native playground)
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (playground-workshop.mjs): toy_swing:{type:'swing',w:102,h:75,scale:.95},tire_swing:{type:'tire',w:82,h:75,scale:.9}, toy_seesaw:{type:'seesaw',w:100,h:43,scale:.9},toy_sandbox:{type:'sandbox',w:96,h:42,scale:.9}, toy_skateboard:{type:'skateboard',w:70,h:30,scale:.65,style:'fish'},skateboard:{type:'skateboard',w:64,h:29,scale:.6,style:'lightning'}, toy_car:{type:'car',w:66,h:39,scale:.6},rocking_horse:{type:'horse',w:84,h:62,scale:.82}, ru
- toy_swing - art source: {'construction': 'playground-v1', 'family': 'swing', 'kind': 'toy', 'blueprint': 'toy_swing', 'material': 'paint'}
- names taken by the drawing: ['seat', 'entry', 'pivot']
- drawing anchors: 0=entry(0.50,0.96) 1=pivot(0.50,0.12) 2=seat(0.50,0.78)

## Drawn parts (y fraction, px above the standing line)
- top beam: frame '+----+' at y 0.08-0.12, px 477-500, full width; pivot anchor (0.50,0.12) px 477
- hanger chains: vertical '|' pairs at x ~0.35 and ~0.57 from px 477 down to the seat, with bolt rings 'o' (?)
- zigzag side pieces '/\/\' at y 0.14-0.23, px 423-469, outer x 0.08-0.20 (?)
- A-frame legs '/ /  \ \' both sides, y 0.24-0.96, px 0-408; feet at ground px 0
- seat: '+---2---+' box at y 0.78-0.82, px 77-100 (seat anchor (0.50,0.78) px 92)
- entry anchor (0.50,0.96) px 0

## Low parts (at or below 63 px)
- A-frame feet px 0-63 (outer legs); entry px 0; nothing flat

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none
- adult <=70: none; seat bottom is at px 77, just above the 70 limit

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- work-queue native_acts says 'ride / explore (native playground)', but no routine keyed to toy_swing found in engine/client/animation/*.json or engine/*.py; treat as unverified
- shelters.py HOMES: not listed

## Siblings (same family field in the work queue)
- family 'swing': tire_swing
