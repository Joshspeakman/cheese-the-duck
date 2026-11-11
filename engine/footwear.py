"""Per-foot material state and grounded, interruptible two-foot care."""
import json,math
from pathlib import Path
from engine.excursions import clamp,finite
from engine.terrain import water_at
DATA=Path(__file__).parent/'client/animation'
BLUEPRINTS=json.loads((DATA/'footwear.json').read_text())
CARE=json.loads((DATA/'footwear-care.json').read_text())
FIELDS=('wet','snow','soil','slack')

def normalize(s):
    for key in FIELDS:
        for side in ('left','right'):s[key+'_'+side]=clamp(s.get(key+'_'+side,s.get(key)))
    summarize(s)

def summarize(s):
    for key in FIELDS:s[key]=max(s[key+'_left'],s[key+'_right'])

def solid_footing(pond):
    pos=pond.game.renderer.duck_pos
    return not water_at(pond.location,pos.x,pos.y,pond.biome) and not any(x in pos.get_state() for x in ('swim','sleep','div','float','hop','jump','flap'))

def update(pond,item,s,dt,wearing,exposure,rain,snow,intensity,temperature):
    p=BLUEPRINTS[item];pos=pond.game.renderer.duck_pos;action=pos.get_state()
    submerged=wearing and any(x in action for x in ('swim','div','float')) and water_at(pond.location,pos.x,pos.y,pond.biome)
    walking=wearing and any(x in action for x in ('walk','waddle'))
    muddy=walking and solid_footing(pond) and exposure and rain
    dusty=walking and solid_footing(pond) and exposure and not rain and not snow
    for side in ('left','right'):
        wet=clamp(intensity)*p['absorbency'] if exposure and rain else 0
        if submerged:wet=1
        key='wet_'+side;s[key]=wet+(s[key]-wet)*math.exp(-dt/(40 if submerged else 90 if exposure and rain else 600))
        target=clamp(intensity) if exposure and snow and not submerged else 0
        key='snow_'+side;s[key]=target+(s[key]-target)*math.exp(-dt/(120 if exposure and snow else 360 if temperature<0 else 90))
        s['soil_'+side]=clamp(s['soil_'+side]+dt*(.002 if muddy else .00025 if dusty else 0))
        s['slack_'+side]=clamp(s['slack_'+side]+dt*(.0006 if walking else 0))
    summarize(s)

def contact(s,spec,index):
    key=spec['material']+('_left' if index==0 else '_right')
    s[key]*=spec['retained'];summarize(s)
