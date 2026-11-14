# hot_air_balloon

## Work queue
- host: placed; family: balloon; family_engine: excursions.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (excursions.json): "hot_air_balloon": {"type":"balloon","w":128,"h":154,"scale":0.62,"material":"fabric","motion":"envelope"}
- hot_air_balloon - art source: {'construction': 'excursion-v1', 'family': 'balloon', 'kind': 'toy', 'blueprint': 'hot_air_balloon', 'material': 'paint'}
- names taken by the drawing: ['entry', 'contact', 'basket', 'burner', 'tether']
- drawing anchors: 0=basket(0.50,0.82) 1=burner(0.50,0.63) 2=contact(0.65,0.85) 3=entry(0.78,0.99) 4=tether(0.90,0.97)

## Drawn parts (y fraction, px above the standing line)
- envelope: big balloon, y 0.01-0.44 (px 649-340), equator stripe '::::' at y 0.33 (px 432)
- rigging: rope lines '/ \' from the envelope to the basket, y 0.40-0.90 (both sides)
- burner: '(____)' and '=' flame box at y 0.63-0.75 (px 238-160)
- basket: wicker box with '[]' weave rows and 'BREAD AERONAUTICS' label, y 0.63-0.97 (px 238-13)
- basket top band '| ==  =|' rows at y 0.82-0.97 (px 108-22) (?)
- ground stand '_[|]_' at y 0.97 (px 9)

## Low parts (at or below 63 px)
- basket floor '+----+' at px 13
- ground stand px 9

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: basket floor px 13 (flat, full width) (?)
- adult <=70: basket floor px 13 (?)
  - weave band px 61-65 (? not flat)

## Existing behaviour (family_engine: excursions.json)
- excursions.json entry: type balloon, w 128, h 154, motion 'envelope'
- no routine rows found in any animation JSON for this id; no family routines (queue family None)

## Siblings (same family field in the work queue)
- none (family 'balloon' has only this object)
