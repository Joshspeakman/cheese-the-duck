# treehouse

## Work queue
- host: placed; family: treehouse; family_engine: None
- native_acts: rest inside (native residence)
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (home-workshop.mjs): treehouse:{w:104,h:71,roof:'shingle',wall:'timber',door:[40,30,22,21],windows:[[18,31,15,12],[70,31,14,12]],props:['branches','ladder','rope'],roofInk:'#a9ad72',shelter:true}, birdhouse:{w:62,h:54,roof:'shingle',wall:'plank',door:[23,25,16,12],windows:[],props:['pole','perch'],roofInk:'#a9b77a',shelter:true,maxStage:'duckling'}, lighthouse:{w:76,h:80,roof:'beacon',wall:'tower',door:[26,56,23,20],windows:[[27,36,19,
- treehouse - art source: {'construction': 'workshop-v1', 'family': 'treehouse', 'kind': 'structure', 'blueprint': 'treehouse', 'material': 'wood'}
- names taken by the drawing: ['entry', 'seat', 'opening', 'capacity']
- drawing anchors: 0=entry(0.50,0.73) 1=opening(0.39,0.43) 2=seat(0.50,0.70)

## Drawn parts (y fraction, px above the standing line)
- shingle roof: y 0.10-0.37, px 419-587 (roof ink #a9ad72, apex px 587)
- upper deck/eave line: '=====' at y 0.39-0.40, px 391-401, full width
- walls, timber: y 0.41-0.73, px 177-382
- door (?): centre, blueprint door [40,30,22,21] = y 0.42-0.72; entry anchor (0.50,0.73) px 177 = the deck-level doorway
- windows: left [18,31,15,12] at x 0.17-0.32, right [70,31,14,12] at x 0.67-0.80, y 0.44-0.61 (px 242-373), mullioned
- opening anchor (0.39,0.43) px 373; seat anchor (0.50,0.70) px 186 (?)
- deck/platform: '=====' at y 0.63 px 242 and y 0.74 px 168 (floor, ?)
- ladder or rope (props): vertical posts/'(=)' at x ~0.10-0.20 and 0.85-0.92, y 0.41-0.76 (?)
- branches (props): diagonals from y 0.77 down to the ground at both sides, px 9-149; leaves '(  ~  )' at x 0.86-0.93, px 37-102 (?)

## Low parts (at or below 63 px)
- branch tips reaching the ground, px 9-37 (thin diagonals, not flat); nothing else under 63 (deck is at px 168)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none flat (branches are thin diagonals)
- adult <=70: none flat; deck px 168 is far above

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- shelters.py HOMES: treehouse (True, 'juvenile') = roof, youngest juvenile; resting inside is native
- home-rooms.json: room 'lookout', capacity 2, elevated True; rep.py ground for treehouse = bottom art row (birdhouse, treehouse special case)
- no routine keyed to it in animation JSON; living_world.py: nothing by name

## Siblings (same family field in the work queue)
- family 'treehouse' has only this object
