# birdbath_garden

## Work queue
- host: placed; family: birdbath; family_engine: waterworks.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (object-footprints.json): "birdbath_garden": { "width": 53.88, "height": 34.49, "floor": false, "construction": "waterworks-v1" }
- birdbath_garden - art source: {'construction': 'waterworks-v1', 'family': 'birdbath', 'kind': 'water', 'blueprint': 'birdbath_garden', 'material': 'stone'}
- names taken by the drawing: ['seat', 'entry', 'contact', 'water', 'rim', 'swimRadius']
- drawing anchors: 0=contact(0.20,0.28) 1=entry(0.18,0.95) 2=seat(0.51,0.30) 3=water(0.21,0.23)

## Drawn parts (y fraction, px above the standing line)
- ornament bird on rim at y 0.10-0.13 (px 308-296) (?)
- rim '========|=======' at y 0.18 (px 278)
- water and leaves '~' at y 0.23-0.28 (px 260-242)
- vine basin walls '( (' at y 0.33-0.48 (px 224-169)
- hollow column '| |' at y 0.43-0.80 (px 187-54), inner '(*)~' fitting at px 73
- plinth '+-------------+' at y 0.83 (px 42), skirt '(' px 36-6

## Low parts (at or below 63 px)
- plinth px 42
- skirt px 6-36

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none flat under 36 (skirt is curved)
- adult <=70: plinth top px 42 (flat, about 13 cols wide) (?)

## Existing behaviour (family_engine: waterworks.json)
- waterworks.json entry: type bath, style vine, shallow true, w 86 h 61
- no routine rows in any animation JSON

## Siblings (same family field in the work queue)
- family 'birdbath': bird_bath and birdbath (both in this batch)
