# spring_wreath

## Work queue
- host: placed; family: wreath; family_engine: None
- native_acts: None
- need: not set (rep.py default 48 - wonder_routines 0 = 48); repertoire_routines: 0; art: curio-v1 (review)

## Blueprint and art source (rep.py printout)
- blueprint (curio-workshop.mjs): spring_wreath:{kinds:['tulip','blossom','blossom','tulip'],tones:['q','f','l','y','w','q'],mids:['y','y','a','f','y','a'],ribbon:'w',eggs:1}, }; function wreath(c,W,H,s,f,t,id){ const cx=W/2,cy=H/2-1,rx=15,ry=9; for(let i=0;i<60;i++){const a=i/60*TAU;const x=cx+Math.cos(a)*rx,y=cy+Math.sin(a)*ry;c.put(x,y,';:"\''[i%4],i%3?'h':'m');c.put(cx+Math.cos(a)*(rx-2),cy+Math.sin(a)*(ry-1.4),'"~'[i%2],'h');} for(let i=0;i<1
- spring_wreath - art source: {'construction': 'curio-v1', 'family': 'wreath', 'kind': 'keepsake', 'blueprint': 'spring_wreath', 'material': 'ceramic'}
- names taken by the drawing: ['entry', 'contact', 'rim', 'emblem', 'ribbon']
- drawing anchors: 0=contact(0.51,0.87) 1=emblem(0.51,0.48) 2=entry(0.51,1.00) 3=ribbon(0.51,0.87) 4=rim(0.51,0.09)

## Drawn parts (y fraction, px above the standing line)
- wreath ring of flowers and leaves: y 0.13-0.87, px 17-117; tulips and blossoms '@*@' around the ring
- top rim anchor (0.51,0.09) px 117; flowers '\\|/' at the top, y 0.04-0.13, px 112-123
- centre emblem (0.51,0.48) px 73; hollow centre (the wreath is open)
- ribbon bow: '(\\/')' at y 0.91 px 11; contact/ribbon anchor (0.51,0.87) px 17
- ribbon tails '~~~' at y 0.96 px 6; entry anchor (0.51,1.00) px 0

## Low parts (at or below 63 px)
- bow px 11-17, tails px 6, lower flowers '@*@' at y 0.78 px ~28 (x 0.1-0.3 and 0.7-0.9)

## Perch candidates (hatchling <=36 px, adult <=70 px)
- hatchling <=36: none flat (bow is a shape, ring is hollow)
- adult <=70: none flat

## Existing behaviour (grep: shelters.py HOMES, animation JSON, engine .py)
- curios.json has spring_wreath (type wreath, 76x48, scale 0.8); native_acts None in the queue
- shelters.py HOMES: not listed; living_world.py: nothing by name

## Siblings (same family field in the work queue)
- family 'wreath': flower_wreath, flower_crown
