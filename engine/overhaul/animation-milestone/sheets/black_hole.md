# black_hole

## Work queue
- host: placed; family: blackhole; family_engine: wonders.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 5 - family_routines 0 = 43); repertoire_routines: 0; family_routines: 0; wonder_routines: 5; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (object-footprints.json): "black_hole": { "width": 27.75, "height": 24.37, "floor": false, "construction": "wonder-v1" }
- black_hole - art source: {'construction': 'wonder-v1', 'family': 'blackhole', 'kind': 'wonder', 'blueprint': 'black_hole', 'material': 'void'}
- names taken by the drawing: ['entry', 'contact', 'glass_low', 'port', 'rim', 'bolt_l', 'bolt_r', 'gauge', 'glass']
- drawing anchors: 0=bolt_l(0.24,0.54) 1=bolt_r(0.78,0.54) 2=contact(0.51,0.70) 3=entry(0.51,1.00) 4=gauge(0.51,0.82) 5=glass(0.65,0.21) 6=glass_low(0.51,0.61) 7=port(0.51,0.63) 8=rim(0.51,0.23)

## Drawn parts (y fraction, px above the standing line)
- glass dome of dust and void '( . ~*- ... )' at y 0.25-0.56 (px 193-112)
- port '((  4  ))' and eye 'O' at y 0.81-0.86 (px 49-36), anchor gauge (0.51,0.82)
- bolt flanges '+-+' at y 0.56 (px 112), anchors bolt_l (0.24,0.54), bolt_r (0.78,0.54)
- base frame '+-----+' at y 0.74-0.98 (px 67-4), anchor contact (0.51,0.70)
- 'HORIZON OK' gauge panel at y 0.93 (px 18)
- feet '[__________]' at y 0.98 (px 4)

## Low parts (at or below 63 px)
- base frame px 4-63
- feet px 4

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: feet / base plate px 4 (?)
  - HORIZON panel px 18 (?)
- adult <=70: frame top px 63 (flat, full width)
  - inner lid px 54 (?)

## Existing behaviour (family_engine: wonders.json)
- wonders.json: fields mass, containment, spin, fed, hum; effects feed, tighten, gauge, tap; physics spin wrap, containment decay
- wonder-routines.json: blackhole_feed_leaf, blackhole_tighten_ring, blackhole_read_gauge, blackhole_stare, blackhole_flick (5)
- labels: 'Dropping a fallen leaf into the intake port', 'Tightening the containment ring bolts', 'Staring into the void'

## Siblings (same family field in the work queue)
- none (family 'blackhole' has only this object)
