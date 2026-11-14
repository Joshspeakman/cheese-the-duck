# wardrobe

## Work queue
- host: placed; family: cabinet; family_engine: furniture.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (furniture.json): "wardrobe":{"type":"cabinet","style":"wardrobe","w":108,"h":87,"scale":0.96}
- wardrobe - art source: {'construction': 'furniture-v1', 'family': 'cabinet', 'kind': 'storage', 'blueprint': 'wardrobe', 'material': 'wood'}
- names taken by the drawing: ['contact', 'entry']
- drawing anchors: 0=contact(0.50,0.51) 1=entry(0.50,0.98)

## Drawn parts (y fraction, px above the standing line)
- cornice y 0.07-0.09 (px 573-558)
- upper door glazing '(=)' rows y 0.09-0.23 (px 558-470) with 'o' knobs
- door seams '||' at x 0.25-0.75, y 0.23-0.86 (px 470-73), handles '0' at px 294
- lower glazing '(=)' at y 0.86 (px 73)
- kick plinth y 0.88-0.92 (px 59-37), feet '(===)' at px 37 and '[___]' at px 7

## Low parts (at or below 63 px)
- feet px 0-37
- plinth px 37-59

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: feet top px 37 (just above the 36 limit) (?)
- adult <=70: plinth top px 44 (flat, full width) (?)
  - lower band px 59 (?)

## Existing behaviour (family_engine: furniture.json)
- furniture.json entry: type cabinet, style wardrobe, w 108 h 87
- no routine rows in any animation JSON

## Siblings (same family field in the work queue)
- family 'cabinet': cabinet and dresser (both in this batch)
