# candelabra

## Work queue
- host: placed; family: chandelier; family_engine: lighting.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (lighting.json): "candelabra":{"type":"candles","style":"silver","w":112,"h":100,"scale":0.78,"color":"#efd49b","radius":15,"power":0.52,"control":"wick","exposed":true,"material":"metal"}
- candelabra - art source: {'construction': 'lighting-v1', 'family': 'chandelier', 'kind': 'light', 'blueprint': 'candelabra', 'material': 'metal'}
- names taken by the drawing: ['control', 'contact', 'entry']
- drawing anchors: 0=contact(0.50,0.81) 1=control(0.68,0.83) 2=entry(0.50,0.98)

## Drawn parts (y fraction, px above the standing line)
- flames and wick tips '\' '/' at y 0.13-0.27 (px 457-381)
- candle cups 'vvv' and arms '(  )' at y 0.21-0.36 (px 413-332)
- candle stems '|' columns at y 0.39-0.67 (px 316-169) with '-' rings
- control box '| I 1 |' at y 0.83-0.86 (px 82-65), anchor control (0.68,0.83)
- plinth '|\/ |' and box top '+-----+' at y 0.79-0.90 (px 103-44)
- base rings '(  (' and '((' at y 0.91-0.97 (px 38-5), anchor contact (0.50,0.81) (?)

## Low parts (at or below 63 px)
- base rings px 5-38
- control box px 65-82

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: plinth ring top px 33 (?)
- adult <=70: control box top px 65 (flat) (?)
  - plinth top px 65 (?)

## Existing behaviour (family_engine: lighting.json)
- lighting.json entry: type candles, style silver, w 112 h 100, control wick, exposed true, power 0.52
- no routine rows in any animation JSON; the 'chandelier' sibling is in the same file

## Siblings (same family field in the work queue)
- family 'chandelier': chandelier (lighting.json; not in this batch)
