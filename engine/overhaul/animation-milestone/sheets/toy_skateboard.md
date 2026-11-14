# toy_skateboard

## Work queue
- host: placed; family: skateboard; family_engine: None
- native_acts: None
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (playground-workshop.mjs): toy_skateboard:{type:'skateboard',w:70,h:30,scale:.65,style:'fish'},skateboard:{type:'skateboard',w:64,h:29,scale:.6,style:'lightning'}, toy_car:{type:'car',w:66,h:39,scale:.6},rocking_horse:{type:'horse',w:84,h:62,scale:.82}, rubber_duck:{type:'duck',w:52,h:38,scale:.5,style:'rubber'},squeaky_toy:{type:'duck',w:48,h:36,scale:.48,style:'squeaker'}, wind_up_duck:{type:'duck',w:60,h:42,scale:.53,style:'clockwork'},d
- toy_skateboard - art source: {'construction': 'playground-v1', 'family': 'skateboard', 'kind': 'toy', 'blueprint': 'toy_skateboard', 'material': 'paint'}
- names taken by the drawing: ['seat', 'entry']
- drawing anchors: 0=entry(0.51,0.90) 1=seat(0.51,0.52)

## Drawn parts (y fraction, px above the standing line)
- deck top: '= ====' edge at y 0.79, px 16, ~34 chars wide (flat, the perch surface)
- fish-style decal '><((o)>' on the deck at y 0.59, px 47 (decoration above the deck, ?)
- fish-scale arcs '( (' and ':' rows, y 0.41-0.76, px 21-74 (decoration, not solid, ?)
- seat anchor (0.51,0.52) px 58 (above the deck)
- wheel pairs at y 0.83-0.93, px -5 to 11 (?); entry anchor (0.51,0.90) px 0

## Low parts (at or below 63 px)
- deck top px 16; wheels px -5 to 11; fish decal px 47 (above deck)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: deck top px 16 = candidate (about one duck wide)
- adult <=70: same deck top; arcs and fish are not solid

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- native_acts is None in the queue; no routine keyed to toy_skateboard in animation JSON or engine/*.py
- playdates TOYS does not include it; shelters.py HOMES: not listed

## Siblings (same family field in the work queue)
- family 'skateboard': skateboard
