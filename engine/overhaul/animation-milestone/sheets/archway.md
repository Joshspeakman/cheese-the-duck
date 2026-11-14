# archway

## Work queue
- host: placed; family: arch; family_engine: architecture.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 7 = 41); repertoire_routines: 0; family_routines: 7; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (architecture.json): "archway": { "type": "arch", "w": 176, "h": 140, "scale": 0.57, "material": "metal", "skill": "observation", "verb": "Walk beneath" }
- archway - art source: {'construction': 'architecture-v1', 'family': 'arch', 'kind': 'study', 'blueprint': 'archway', 'material': 'metal'}
- names taken by the drawing: ['entry', 'contact', 'company']
- drawing anchors: 0=company(0.87,0.91) 1=contact(0.20,0.83) 2=entry(0.50,0.99)

## Drawn parts (y fraction, px above the standing line)
- crown hoop: arch of metal bands, top at y 0.06-0.22 (px 513-425), '(o.o)' ornament on the crown at px 505-513
- legs: two stacked-bracket posts, left x 0.22-0.32 and right x 0.78-0.84, from y 0.30 to 0.91 (px 378-44), vine ornaments '<;;>' at px 366, 294, 223, 187 (?)
- inner arc: the hoop curves down to the legs at y 0.30-0.45 (px 378-298)
- small figure '(o/o)' on the left leg at y 0.57-0.59 (px 231-227) (?)
- base slab: flat block between the legs, y 0.91-0.97 (px 40-8), panelled '|  |' inside

## Low parts (at or below 63 px)
- base slab top px 40 and its panel rows px 8-40
- entry anchor px 0

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none under 36 (slab top is px 40)
- adult <=70: base slab top px 40 (flat, between the legs, about 0.2-0.8 of the width)

## Existing behaviour (family_engine: architecture.json)
- architecture.json entry: type arch, verb 'Walk beneath', skill observation
- architecture-company.json: arch_frame, arch_light, night_watch (3 routines, labels: 'Stand inside the arch and frame the pond', 'Turn between the arch shadow and its bright rim', 'Watch the silhouette together')
- queue family_routines 7 (family arch); only the 3 company rows above were located in this pass

## Siblings (same family field in the work queue)
- family 'arch': cosmic_arch (wonders.json, wonder_routines 5). Avoid the 'night watch' and 'frame' acts already used by the family
