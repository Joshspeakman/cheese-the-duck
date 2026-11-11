"""Snow in sealed miniatures and readings of the actual queued weather front."""
import math
from world.atmosphere import WeatherType

TYPES={'globe','oracle'}
WEATHER={w.value for w in WeatherType}
def finite(v,default=0.):return v if isinstance(v,(int,float)) and math.isfinite(v) else default
def clamp(v):return max(0.,min(1.,finite(v)))
def wet(pond):return pond.weather_type in {'rain','rainy','heavy_rain','drizzle','spring_showers','stormy','thunderstorm','summer_storm','sleet','hail','ice_storm'}
def state(s):
    if not isinstance(s.get('glass'),dict):s['glass']={}
    v=s['glass']
    for key in ('energy','focus'):v[key]=clamp(v.get(key))
    for key in ('phase','azimuth'):v[key]=finite(v.get(key))%(math.pi*2)
    for key in ('pumps','readings'):v[key]=max(0,min(9999,int(finite(v.get(key)))))
    vision=v.get('vision')
    if not isinstance(vision,dict) or vision.get('weather') not in WEATHER:v['vision']=None
    else:
        v['vision']={k:vision[k] for k in ('weather','biome','at','read_at') if k in vision}
        v['vision'].update(biome=str(vision.get('biome','pond'))[:64],at=max(0.,finite(vision.get('at'))),read_at=max(0.,finite(vision.get('read_at'))))
    return v
def update(s,dt):
    v=state(s);dt=max(0.,finite(dt));decay=math.exp(-dt/18)
    v['phase']=(v['phase']+v['energy']*18*(1-decay)*.65)%(math.pi*2)
    v['energy']*=decay;v['focus']*=math.exp(-dt/100)
def choose(pond,p,obj):
    v=state(obj['keepsake']);age=pond.game.duck.growth_stage
    if wet(pond):return 'glass_raindrops'
    if p['type']=='oracle':
        if age in ('hatchling','duckling'):return 'oracle_young'
        return 'oracle_focus' if not v['vision'] or obj['uses']%3==0 else 'oracle_compare' if obj['uses']%3==1 else 'oracle_rim'
    if age in ('hatchling','duckling'):return 'globe_low'
    if age in ('mature','elder','legendary') or pond.game.duck.needs.energy<40:return 'globe_slow'
    if pond.hour<6 or pond.hour>=19:return 'globe_night'
    if obj.get('dirt',0)>.35:return 'globe_polish'
    if v['energy']>.25:return 'globe_follow'
    return ('globe_pump','globe_scene','globe_polish')[obj['uses']%3]
def contact(pond,s,event):
    v=state(s)
    if event=='flurry':v.update(energy=min(1.,v['energy']+.42),pumps=min(9999,v['pumps']+1))
    elif event=='rotate':v['azimuth']=(v['azimuth']+math.pi/3)%(math.pi*2)
    elif event=='vision':
        front=pond.state['weather'].get(pond.biome,{})
        forecast=front.get('forecast',[])
        if forecast and forecast[0].get('type') in WEATHER:
            v.update(focus=1.,readings=min(9999,v['readings']+1),vision=dict(weather=forecast[0]['type'],biome=pond.biome,at=front['until'],read_at=pond.state['elapsed']))
def facts(pond,p,s):
    v=state(s)
    if p['type']=='globe':return dict(miniature=p['scene'],snow='swirling upward' if v['energy']>.5 else 'gently settling' if v['energy']>.03 else 'settled on the tiny landscape',pump_strokes=v['pumps'],visible_words=p['caption'])
    result=dict(visible_words=p['caption'],readings=v['readings'])
    if not v['vision']:result['vision']='No weather reading has appeared yet.';return result
    vision=v['vision'];front=pond.state['weather'].get(vision['biome'],{});queue=front.get('forecast',[])
    due=vision['at']-pond.state['elapsed']
    status='past reading' if due<=0 else 'forecast changed since reading' if front.get('until')!=vision['at'] or not queue or queue[0]['type']!=vision['weather'] else 'currently expected next front'
    result['weather_reading']={**vision,'status':status,'seconds_until':max(0,round(due)), 'certainty':'A reading of the queued weather when touched. It may change; no event is guaranteed.'}
    return result
