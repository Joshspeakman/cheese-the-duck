# toy_blocks

## Work queue
- host: placed; family: blocks; family_engine: None
- native_acts: None
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: reconstructed_review_in_progress

## Blueprint and art source (rep.py printout)
- blueprint (playground-workshop.mjs): toy_blocks:{type:'blocks',w:76,h:49,scale:.72}, toy_trampoline:{type:'trampoline',w:88,h:51,scale:.87,net:true},trampoline:{type:'trampoline',w:74,h:40,scale:.8,net:false}, toy_slide:{type:'slide',w:100,h:72,scale:.95,style:'wood'},water_slide:{type:'slide',w:108,h:75,scale:.95,style:'pool'},water_slide_mega:{type:'slide',w:116,h:82,scale:1,style:'cascade'},rainbow_slide:{type:'slide',w:110,h:76,scale:.98,style:'ra
- toy_blocks - art source: {'construction': 'playground-v1', 'family': 'blocks', 'kind': 'toy', 'blueprint': 'toy_blocks', 'material': 'paint'}
- names taken by the drawing: ['contact', 'top']
- drawing anchors: 0=contact(0.52,0.31) 1=top(0.52,0.06)

## Drawn parts (y fraction, px above the standing line)
- stack of three levels of blocks, faces with glyphs (letters or shapes, ?)
- top block: y 0.06-0.27, px 204-262 (top anchor (0.52,0.06) px 262)
- middle pair: y 0.29-0.58, px 117-198
- bottom row of three: y 0.60-0.92, px 23-111 (top face px 111, bottom px 23)
- contact anchor (0.52,0.31) px 191 (ledge between the top and middle levels, ?)

## Low parts (at or below 63 px)
- bottom row bottom edge px 23-29; nothing lower

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none
- adult <=70: none; lowest block top face is at px ~111

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- no routine keyed to toy_blocks found in animation JSON or engine/*.py (only footprints, item_profiles.py, playground-workshop.mjs)
- playdates TOYS does not include blocks; shelters.py HOMES: not listed

## Siblings (same family field in the work queue)
- family 'blocks' has only this object
