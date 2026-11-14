# garden_bench

## Work queue
- host: placed; family: bench; family_engine: furniture.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (furniture.json): "garden_bench":{"type":"bench","style":"ironwood","w":118,"h":61,"scale":0.97,"capacity":2,"seat":true}
- garden_bench - art source: {'construction': 'furniture-v1', 'family': 'bench', 'kind': 'comfort', 'blueprint': 'garden_bench', 'material': 'fabric'}
- names taken by the drawing: ['seat', 'slots', 'seatWidth', 'entry', 'front', 'back', 'arm']
- drawing anchors: 0=arm(0.91,0.53) 1=back(0.50,0.33) 2=entry(0.50,0.97) 3=seat(0.50,0.68)

## Drawn parts (y fraction, px above the standing line)
- back: top rail y 0.20-0.22 (px 341-334), ornamented back boards '(=)' and 'o' at y 0.23-0.52 (px 327-200)
- seat cushion '+|----' at y 0.67-0.77 (px 134-89), anchor seat (0.50,0.68)
- arm at (0.91,0.53)
- splayed legs '\' and '//' at y 0.90-0.97 (px 30-0), feet '[__]' at px 0

## Low parts (at or below 63 px)
- legs px 0-30
- feet px 0

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none (no flat top under 36)
- adult <=70: none under 70: seat top px 89 is just above the limit

## Existing behaviour (family_engine: furniture.json)
- furniture.json entry: type bench, style ironwood, capacity 2, seat true, w 118 h 61
- seating-routines.json: autumn_brush (when bench:true, autumn) and bench_gossip (shared); these key on the bench flag, not on this id
- no routine rows keyed to 'garden_bench' itself

## Siblings (same family field in the work queue)
- none (family 'bench' has only this object)
