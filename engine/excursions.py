"""Simulation-owned resting mechanisms for carnival and travel belongings.

These are the existing owned objects, with no passengers or invented journeys.
Native weather/daylight drive empty rides, tethered fabric and indicator lamps.
The original item action remains responsible for every gameplay reward.
"""
import json,math
from pathlib import Path
ITEMS=json.loads((Path(__file__).parent/'client/animation/excursions.json').read_text())
TAU=math.pi*2
def finite(v,d=0.):return float(v) if isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) else d
def clamp(v,a=0.,b=1.):return max(a,min(b,finite(v)))
def state(item,obj):
    if not isinstance(obj.get('excursion'),dict):obj['excursion']={}
    s=obj['excursion'];s['phase']=finite(s.get('phase'))%TAU;s['wind_phase']=finite(s.get('wind_phase'))%TAU
    for k,d in (('speed',0.),('wind',0.),('cover',0.),('inflation',1.),('lights',0.)):
        s[k]=clamp(s.get(k,d))
    s['running']=s.get('running') is True
    if item in ('bounce_house','magic_carpet'):
        if not isinstance(s.get('surface'),dict):s['surface']={}
        floor=s['surface']
        for role in ('a','b'):
            if not isinstance(floor.get(role),dict):floor[role]={}
            for k,lo,hi in (('jump',0,18),('press',0,1),('u',-1,1),('v',-1,1),('impact',0,1)):floor[role][k]=clamp(floor[role].get(k),lo,hi)
        for k,lo,hi in (('lift',0,18),('tilt',-.65,.65),('gate',0,1)):floor[k]=clamp(floor.get(k),lo,hi)
        floor['active']=floor.get('active') is True
    return s
def adverse(weather):
    weather=str(weather or '').lower()
    return weather!='rainbow' and any(k in weather for k in ('rain','storm','snow','blizzard','drizzle','shower','hail','sleet','tornado','hurricane','gale','freezing'))
def update(item,obj,dt,outdoors,weather,wind,hour,reserved=False):
    if item not in ITEMS:return
    s=state(item,obj);dt=max(0.,finite(dt));kind=ITEMS[item]['motion']
    if not outdoors:
        s.update(running=False,speed=0.,wind=0.,lights=0.);return
    hour=finite(hour,12.)%24
    wet=adverse(weather);night=hour<7 or hour>=20;wind=clamp(wind)
    live=not wet and not night and wind<.8 and finite(obj.get('condition'),1.)>.2
    # Exponential approach is frame-rate independent; a long offline update
    # advances the mechanism without emitting a backlog of activity events.
    target=.12 if live and kind=='motor' else .16 if live and kind=='scanner' else 0.
    if not reserved:
        old=s['speed'];decay=math.exp(-dt*1.4);s['speed']=target+(old-target)*decay
        s['phase']=(s['phase']+target*dt+(old-target)*(1-decay)/1.4)%TAU
        s['running']=target>0
    elif reserved=='hold':s.update(speed=0.,running=False)
    s['wind']=wind;s['wind_phase']=(s['wind_phase']+dt*(.4+wind*.7))%TAU
    s['lights']=float(not wet and (hour<6 or hour>=18))
    cover=1. if wet else 0.
    surface_owned=bool(reserved and item in ('bounce_house','magic_carpet'))
    if item in ('bounce_house','magic_carpet') and not reserved:
        floor=s['surface'];floor['active']=False
        for role in ('a','b'):
            for k in floor[role]:floor[role][k]*=math.exp(-dt*3)
        for k in ('lift','tilt','gate'):floor[k]*=math.exp(-dt*3)
    if not surface_owned and kind in ('envelope','inflation','cloth'):s['cover']+= (cover-s['cover'])*(1-math.exp(-dt*.12))
    if not surface_owned and kind in ('envelope','inflation'):
        target_inflation=.35 if wet or night or wind>=.8 else 1.
        s['inflation']+=(target_inflation-s['inflation'])*(1-math.exp(-dt*.08))
