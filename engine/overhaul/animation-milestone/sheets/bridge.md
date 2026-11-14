# bridge

## Work queue
- host: placed; family: bridge; family_engine: architecture.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 7 = 41); repertoire_routines: 0; family_routines: 7; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (architecture.json): "bridge": { "type": "bridge", "w": 216, "h": 104, "scale": 0.6, "material": "wood", "skill": "observation", "verb": "Cross" }
- bridge - art source: {'construction': 'architecture-v1', 'family': 'bridge', 'kind': 'study', 'blueprint': 'bridge', 'material': 'wood'}
- names taken by the drawing: ['entry', 'contact', 'company']
- drawing anchors: 0=company(0.92,0.91) 1=contact(0.11,0.74) 2=entry(0.08,0.83)

## Drawn parts (y fraction, px above the standing line)
- deck: plank band '=' arching from the left landing up to y 0.35-0.37 (px 205-197) and down to the right landing
- tower piers '| |' at x 0.17-0.24 (y 0.43-0.83, px 172-13) and x 0.42-0.60 (y 0.54-0.80, px 121-17)
- rail columns '|||:' at x 0.30-0.67 (y 0.57-0.82)
- left landing '_____' at px 4-13 (x 0.13-0.20)
- right landing '==========' at px 25-29 (x 0.80-0.97)
- ground px 0

## Low parts (at or below 63 px)
- left landing px 4-21
- right landing px 25-33
- ground px 0

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: right landing top px 29 (flat, about 10 cols) (?)
  - left landing top px 8 (?)
- adult <=70: right landing px 29 and px 33 (?)
  - deck rail row px 54 (?)

## Existing behaviour (family_engine: architecture.json)
- architecture.json entry: type bridge, w 216 h 104, verb 'Cross'
- architecture-company.json: bridge_spotter ('Wait at the far landing and welcome Cheese across'), bridge_echo ('Tap three times on the far landing stone') (2 routines)

## Siblings (same family field in the work queue)
- none (family 'bridge' has only this object; the queue's family_routines 7 were not located in the files checked)
