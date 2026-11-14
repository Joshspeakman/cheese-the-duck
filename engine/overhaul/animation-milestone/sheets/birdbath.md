# birdbath

## Work queue
- host: placed; family: birdbath; family_engine: waterworks.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (object-footprints.json): "birdbath": { "width": 44.05, "height": 27.9, "floor": false, "construction": "waterworks-v1" }
- birdbath - art source: {'construction': 'waterworks-v1', 'family': 'birdbath', 'kind': 'water', 'blueprint': 'birdbath', 'material': 'stone'}
- names taken by the drawing: ['seat', 'entry', 'contact', 'water', 'rim', 'swimRadius']
- drawing anchors: 0=contact(0.23,0.33) 1=entry(0.20,0.94) 2=seat(0.51,0.35) 3=water(0.24,0.27)

## Drawn parts (y fraction, px above the standing line)
- rim '=======|======' at y 0.19-0.23 (px 212-207)
- water '~~~' at y 0.35-0.40 (px 173-156)
- bowl walls '(' ring at y 0.29-0.79 (px 190-45)
- fluted pedestal '| | {o}| |' at y 0.52-0.65 (px 123-84)
- flared plinth '+-------------+' at y 0.81 (px 39), skirt '(' px 34-6
- base ground px 0

## Low parts (at or below 63 px)
- plinth px 39
- skirt px 6-34

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none flat under 36 (skirt is curved)
- adult <=70: plinth top px 39 (flat, about 13 cols wide) (?)

## Existing behaviour (family_engine: waterworks.json)
- waterworks.json entry: type bath, style fluted, shallow true, w 76 h 53
- no routine rows in any animation JSON

## Siblings (same family field in the work queue)
- family 'birdbath': bird_bath and birdbath_garden (both in this batch)
