# bounce_house

## Work queue
- host: placed; family: bouncehouse; family_engine: excursions.json
- native_acts: none set in queue
- need: not set (rep.py default 48 - wonder_routines 0 - family_routines 0 = 48); repertoire_routines: 0; family_routines: 0; wonder_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (excursions.json): "bounce_house": {"type":"inflatable","w":180,"h":150,"scale":0.66,"material":"fabric","motion":"inflation"}
- bounce_house - art source: {'construction': 'excursion-v1', 'family': 'bouncehouse', 'kind': 'toy', 'blueprint': 'bounce_house', 'material': 'paint'}
- names taken by the drawing: ['entry', 'contact', 'surface', 'slots', 'controls', 'front', 'route', 'blower', 'mesh']
- drawing anchors: 0=blower(0.97,0.89) 1=contact(0.97,0.89) 2=entry(0.50,0.98) 3=mesh(0.24,0.47)

## Drawn parts (y fraction, px above the standing line)
- inflated top, ribbed arches '///' at y 0.06-0.25 (px 631-506)
- mesh walls with ':' panels at x 0.04-0.44 and posts '|', y 0.26-0.79 (px 493-134)
- floor ring '(------(' at y 0.79-0.81 (px 134-120)
- hose '~' along the left, y 0.81-0.96 (px 120-0)
- blower unit at right, x 0.85-0.97, y 0.83-0.97 (px 106-14), anchor blower (0.97,0.89)
- feet '[+]' at y 0.96 (px 14) and '[=]' at px 28

## Low parts (at or below 63 px)
- blower and feet px 0-28
- hose base px 0-14

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: blower top rail '[::]' px 28 (?)
  - feet '[=]' px 28 (?)
- adult <=70: floor seam '+-------_-----' at px 46 (flat, full width) (?)
  - floor top px 51 (?)

## Existing behaviour (family_engine: excursions.json)
- excursions.json entry: type inflatable, motion inflation, w 180 h 150
- surface-routines.json (bounce_first, bounce_echo, bounce_together, ... bounce_quiet) plus castle-care.json and castle-controls.json: 72 routine rows with item bounce_house (labels such as 'Find a first little bounce', 'Meet in the air')
- queue repertoire_routines 0 vs the 72 rows: check which count the queue uses before writing more

## Siblings (same family field in the work queue)
- none (family 'bouncehouse' has only this object)
