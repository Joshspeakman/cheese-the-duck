# cosmic_arch

## Work queue
- host: placed; family: arch; family_engine: wonders.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 5 - family_routines 7 = 36); repertoire_routines: 0; family_routines: 7; wonder_routines: 5; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (object-footprints.json): "cosmic_arch": { "width": 45.29, "height": 34.37, "floor": false, "construction": "wonder-v1" }
- cosmic_arch - art source: {'construction': 'wonder-v1', 'family': 'arch', 'kind': 'wonder', 'blueprint': 'cosmic_arch', 'material': 'stone'}
- names taken by the drawing: ['entry', 'contact', 'wheel', 'dial_low', 'keystone', 'stars_l', 'stars_r', 'stars_low_a', 'stars_low_b', 'stars_low_c', 'pillar_l', 'pillar_r']
- drawing anchors: 0=contact(0.50,0.76) 1=dial_low(0.19,0.76) 2=entry(0.50,0.99) 3=keystone(0.50,0.09) 4=pillar_l(0.19,0.82) 5=pillar_r(0.82,0.82) 6=stars_l(0.23,0.23) 7=stars_low_a(0.79,0.73) 8=stars_low_b(0.85,0.75) 9=stars_low_c(0.81,0.84) 0=stars_r(0.78,0.23) 1=wheel(0.50,0.17)

## Drawn parts (y fraction, px above the standing line)
- star crown: arc of '=' dots from y 0.08 to 0.32 (px 343-252), keystone '[##]' at y 0.09 (px 337)
- keystone dial: '( *  @  * )' wheel at y 0.14-0.18 (px 320-303), centre x 0.50
- left pillar: '|' column at x 0.12, y 0.32-0.82 (px 252-63), with '=[]=[]=' brackets at px 217, 149, 80, 57 (?)
- low star dial '(  )' at x 0.19, y 0.76-0.82 (px 89-63) (?)
- right-side stars 'O' at x 0.79-0.85, y 0.73-0.84 (px 77-89) (?)
- open space under the arch at x 0.30-0.70 (sitting spot, contact px ~83)

## Low parts (at or below 63 px)
- base rim '+---+' at px 9 (?), entry px 0
- pillar bracket ledges px 34, 57, 63 (?)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: '=[]=[]=' bracket ledge at px 34 (?)
  - base plinth top px 9 (?)
- adult <=70: bracket ledges px 34, 57 (?)
  - no other flat top under 70

## Existing behaviour (family_engine: wonders.json)
- wonders.json: fields align, starlight, traced, moss; effects turn, trace, scrub, wish; physics starlight decay by night/clear
- wonder-routines.json: arch_turn_starwheel, arch_trace_constellation, arch_sit_beneath, arch_scrub_moss, arch_make_wish (5)
- labels: 'Turning the low star dial...', 'Tracing the little constellation...', 'Sitting under the arch and counting stars', 'Scrubbing moss...', 'Making a wish under the keystone'

## Siblings (same family field in the work queue)
- family 'arch': archway (architecture.json, 7 family routines; its acts are walk-beneath and night-watch). Keep cosmic_arch's acts on the star dial and carvings
