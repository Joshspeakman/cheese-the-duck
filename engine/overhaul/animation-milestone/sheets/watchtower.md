# watchtower

## Work queue
- host: placed; family: tower; family_engine: None
- native_acts: None
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: curio-v1 (review)

## Blueprint and art source (rep.py printout)
- blueprint (curios.json): "watchtower": { "type": "prop", "w": 180, "h": 240, "scale": 1.64, "grid": 3 }, "butterfly_wing": { "type": "prop", "w": 52, "h": 48, "scale": 0.9, "grid": 2 }, "mud_sculpture": { "type": "prop", "w": 48, "h": 40, "scale": 0.85, "grid": 2 }, "mystery_gift": { "type": "prop", "w": 48, "h": 44, "scale": 0.85, "grid": 2 }, "parade_flag": { "type": "prop", "w": 56, "h
- watchtower - art source: {'construction': 'curio-v1', 'family': 'tower', 'kind': 'structure', 'blueprint': 'watchtower', 'material': 'wood'}
- names taken by the drawing: ['entry', 'contact', 'ladder', 'window', 'flag', 'platform']
- drawing anchors: 0=contact(0.51,0.94) 1=entry(0.51,1.00) 2=flag(0.58,0.05) 3=ladder(0.83,0.89) 4=platform(0.51,0.48) 5=window(0.51,0.37)

## Drawn parts (y fraction, px above the standing line)
- flag on a pole: pole top y 0.04 px 869; flag '~~~2~~' at y 0.05-0.08 px 835-858 (anchor flag 0.58,0.05)
- pointed shingle roof: y 0.13-0.29, px 641-789 (the '=-=-' shingle rows)
- lookout rail/platform: '+----+' top at y 0.29 px 641; platform anchor (0.51,0.48) px ~480
- window/porthole '(##)': y 0.35-0.37, px 572-583 (anchor window 0.51,0.37)
- ladder (?): rung boxes '|---|' down the right side, x ~0.73-0.85, y 0.56-0.90, px 92-366; anchor ladder (0.83,0.89) px 103
- cross braces '\\//' across the lower body, y 0.51-0.92, px 69-446 (architecture-routines 'watchtower_braces')
- legs: tower walls '|' down to the base frame, y 0.43-0.92
- base frame: y 0.94-0.99 px 11-57, with seven '[__]' blocks at y 0.96 px 34 (?)
- contact anchor (0.51,0.94) px 57 (feet); entry (0.51,1.00) px 0

## Low parts (at or below 63 px)
- base frame top px 57 (contact); '[__]' blocks px 23-34 (?); entry px 0

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: the '[__]' blocks top px ~34 are only ~4 chars wide each (too narrow, ?)
- adult <=70: base frame top px 57, flat ~47 chars wide = candidate; nothing else flat under 70

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- native_acts in the queue is None, but architecture-routines.json already has watchtower_braces (follow the cross braces to their bolted feet) and watchtower_roof (look up through the lookout rails to the shingle roof); check before authoring
- architecture.json has a 'watchtower' entry (type watchtower); curios.json has the prop size (180x240, scale 1.64)
- shelters.py HOMES: not listed; living_world.py: nothing by name

## Siblings (same family field in the work queue)
- family 'tower': castle_tower, sand_castle, tower
