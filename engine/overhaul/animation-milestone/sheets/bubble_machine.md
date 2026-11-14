# bubble_machine

## Work queue
- host: placed; family: bubbles; family_engine: playkit.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (object-footprints.json): "bubble_machine": { "width": 52.29, "height": 40.37, "floor": false, "construction": "playkit-v1" }
- bubble_machine - art source: {'construction': 'playkit-v1', 'family': 'bubbles', 'kind': 'toy', 'blueprint': 'bubble_machine', 'material': 'metal'}
- names taken by the drawing: ['entry', 'contact', 'mouth', 'partner']
- drawing anchors: 0=contact(0.24,0.96) 1=entry(0.13,0.98) 2=mouth(0.50,0.64) 3=partner(0.60,0.91)

## Drawn parts (y fraction, px above the standing line)
- bubble wheel: '(' drum with 'o' bubbles at y 0.52-0.77 (px 203-94), anchor mouth (0.50,0.64), partner (0.60,0.91)
- feed tube '~~~~' at y 0.43-0.45 (px 243-236)
- casing top '+------+' at y 0.50 (px 214)
- sign 'BUBBLE / CO.' at y 0.82 (px 73), 'NO. 08' at y 0.86
- front tray ':::' at y 0.83 (px 69) and mouth lid '+---+' at y 0.85 (px 58)
- chassis base '+-----+' at y 0.91 (px 33), feet 'O' and '[O]' at px 0-11

## Low parts (at or below 63 px)
- feet px 0-11
- chassis base px 33

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: chassis base top px 33 (?)
- adult <=70: front tray px 69 (?)
  - mouth lid px 58 (?)

## Existing behaviour (family_engine: playkit.json)
- playkit.json entry: type bubbler, w 136 h 122, verb 'Make bubbles', portable false
- playkit-company.json: bubbler_drift ('Watch the wheel start and follow the first drifting bubbles'), bubbler_clean ('Wipe the far casing while Cheese tends the front switch') (2 routines)

## Siblings (same family field in the work queue)
- family 'bubbles': bubble_wand and frog_spawn (not in this batch)
