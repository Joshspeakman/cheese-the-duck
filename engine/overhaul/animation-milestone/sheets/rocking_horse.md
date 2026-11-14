# rocking_horse

## Work queue
- host: placed; family: horse; family_engine: None
- native_acts: ride / explore (native playground)
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (playground-workshop.mjs): rocking_horse:{type:'horse',w:84,h:62,scale:.82}, rubber_duck:{type:'duck',w:52,h:38,scale:.5,style:'rubber'},squeaky_toy:{type:'duck',w:48,h:36,scale:.48,style:'squeaker'}, wind_up_duck:{type:'duck',w:60,h:42,scale:.53,style:'clockwork'},duck_toy:{type:'duck',w:56,h:40,scale:.52,style:'carved'}, plushie:{type:'plush',w:62,h:48,scale:.6}, }; function wheel(c,x,y,r,turn,tone='k'){ c.ellipse(x,y,r,r*.55,'=','s',tru
- rocking_horse - art source: {'construction': 'playground-v1', 'family': 'horse', 'kind': 'keepsake', 'blueprint': 'rocking_horse', 'material': 'ceramic'}
- names taken by the drawing: ['seat', 'entry', 'contact']
- drawing anchors: 0=contact(0.69,0.41) 1=entry(0.35,0.89) 2=seat(0.42,0.44)

## Drawn parts (y fraction, px above the standing line)
- head with ears '/\ /\' at y 0.11, px 312; eye 'O' at y 0.16 px 292; head y 0.13-0.28, px 246-306
- mane/neck strands '///' and '~': y 0.28-0.41, px 193-246 (?)
- saddle: y 0.44-0.48, px 166-179; seat anchor (0.42,0.44) px 179 (in the '.--2--.' box)
- barrel body with blanket '(~)' pattern: y 0.46-0.66, px 80-173 (?)
- tail '~~~' at right, y 0.46-0.52, px 146-173 (?)
- rockers: long curved runners from y 0.48 (px 166) down to y 0.89 (px 0); runner ends '[___]' at y 0.84 px ~20
- runner bottoms '____' at y 0.87-0.92, px -13 to 7; entry anchor (0.35,0.89) px 0; contact (0.69,0.41) px 193

## Low parts (at or below 63 px)
- rocker curves px 0-63 (the curve crosses 63 near y 0.75); '[___]' feet px ~20; runner bottoms px -13 to 7

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: '[___]' rocker feet px ~20 are ~5 chars wide (too narrow, ?); no flat top
- adult <=70: none; rocker runners are curves

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- work-queue native_acts says 'ride / explore (native playground)', but I found no routine keyed to rocking_horse in engine/client/animation/*.json or engine/*.py (only object-footprints.json, item-catalog.mjs, playground-workshop.mjs, item_profiles.py); treat as unverified
- shelters.py HOMES: not listed

## Siblings (same family field in the work queue)
- family 'horse' has only this object
