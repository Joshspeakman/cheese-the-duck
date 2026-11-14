# skateboard

## Work queue
- host: placed; family: skateboard; family_engine: None
- native_acts: None
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (playground-workshop.mjs): skateboard:{type:'skateboard',w:64,h:29,scale:.6,style:'lightning'}, toy_car:{type:'car',w:66,h:39,scale:.6},rocking_horse:{type:'horse',w:84,h:62,scale:.82}, rubber_duck:{type:'duck',w:52,h:38,scale:.5,style:'rubber'},squeaky_toy:{type:'duck',w:48,h:36,scale:.48,style:'squeaker'}, wind_up_duck:{type:'duck',w:60,h:42,scale:.53,style:'clockwork'},duck_toy:{type:'duck',w:56,h:40,scale:.52,style:'carved'}, plushie:{
- skateboard - art source: {'construction': 'playground-v1', 'family': 'skateboard', 'kind': 'toy', 'blueprint': 'skateboard', 'material': 'paint'}
- names taken by the drawing: ['seat', 'entry']
- drawing anchors: 0=entry(0.51,0.89) 1=seat(0.51,0.50)

## Drawn parts (y fraction, px above the standing line)
- deck top: '= ====' edge at y 0.79, px 15-19, ~32 chars wide (flat, the perch surface)
- lightning-style arcs '( (' and ':' stripes above the deck, y 0.39-0.75, px 19-68 (decoration, not solid, ?)
- seat anchor (0.51,0.50) px 53 = centre of the arcs, 34 px above the deck
- wheel pairs '( (  ) )' at y 0.82-0.89, px 0-10, at x 0.2-0.4 and 0.65-0.85 (?)
- bottom lip '=' at y 0.93 px -5; entry anchor (0.51,0.89) px 0

## Low parts (at or below 63 px)
- deck top px 15-19; wheels px -5 to 10; arcs start at px 19 (decor)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: deck top px 15-19 = candidate (about one duck wide)
- adult <=70: same deck top; arcs are not solid

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- native_acts is None in the queue; no routine keyed to skateboard in animation JSON or engine/*.py (only footprints, item_profiles.py, playground-workshop.mjs)
- playdates TOYS does not include skateboards; shelters.py HOMES: not listed

## Siblings (same family field in the work queue)
- family 'skateboard': toy_skateboard
