"""Saved material state for the real wardrobe, without equipping or granting."""
import copy,json,math
from pathlib import Path
from engine.excursions import clamp,finite
BLUEPRINTS=json.loads((Path(__file__).parent/'client/animation/headwear.json').read_text())
CARE=json.loads((Path(__file__).parent/'client/animation/headwear-care.json').read_text())

def owned(game):
    wardrobe=getattr(getattr(game,'seasonal_clothing',None),'wardrobe',None)
    return set(getattr(getattr(game,'habitat',None),'owned_items',[]))|set(getattr(getattr(game,'outfits',None),'owned_items',[]))|set(getattr(wardrobe,'owned_items',[]))

def selected(game):
    from engine.scene import equipped_wearables
    available=owned(game)
    choices=[i for i in equipped_wearables(game).values() if i in BLUEPRINTS and i in available]
    return choices[-1] if choices and game.duck.growth_stage!='egg' else None

def state(pond,item):
    records=pond.state.setdefault('apparel',{})
    if not isinstance(records.get(item),dict):records[item]={}
    s=records[item]
    for key in ('wet','snow','fog','wind'):s[key]=clamp(s.get(key))
    s['phase']=finite(s.get('phase'))%math.tau
    return s

def sheltered(pond):
    from engine import shelters
    plan=pond.state.get('plan') or {};r=plan.get('residence')
    return bool(r and r.get('roof') and shelters.still_placed(pond,r) and plan.get('phase') in ('act','settle'))

def update(pond,dt,weather,intensity,temperature,wind,offline=False):
    if not pond.game:return
    dt=max(0,finite(dt));active=selected(pond.game);outside=not offline and not sheltered(pond)
    # No cosmetic head exists while unhatched. A stored or unequipped hat dries
    # quietly; it cannot collect weather from a different wearer or location.
    wet='rainbow' not in weather and any(x in weather for x in ('rain','storm','drizzle','shower','sleet'))
    snow=any(x in weather for x in ('snow','blizzard'))
    for item in owned(pond.game)&BLUEPRINTS.keys():
        s=state(pond,item);wearing=active==item and not offline;p=BLUEPRINTS[item]
        exposure=wearing and outside
        target=clamp(intensity)*p['absorbency'] if exposure and wet else 0
        s['wet']=target+(s['wet']-target)*math.exp(-dt/(90 if exposure and wet else 600))
        target=clamp(intensity) if exposure and snow else 0
        s['snow']=target+(s['snow']-target)*math.exp(-dt/(120 if exposure and snow else 360 if temperature<0 else 90))
        target=.8 if wearing and p['shape']=='helmet' and temperature<8 else 0
        s['fog']=target+(s['fog']-target)*math.exp(-dt/40)
        s['wind']=clamp(wind) if exposure else 0
        if wearing:s['phase']=(s['phase']+dt*(.9+s['wind']*2))%math.tau

def snapshot(pond):
    # A renderer has no authority to advance material or instantiate ownership.
    if not pond or not pond.game:return {}
    available=owned(pond.game)
    return {i:copy.deepcopy(s) for i,s in pond.state.get('apparel',{}).items() if i in available and i in BLUEPRINTS}

def suited(item,action):
    p=BLUEPRINTS.get(item,{})
    if not p or action not in CARE:return False
    spec=CARE[action]
    return (('materials' not in spec or p['material'] in spec['materials']) and
            ('shapes' not in spec or p['shape'] in spec['shapes']) and p['shape'] not in spec.get('excludeShapes',[]))

def free(pond):
    g=pond.game
    return bool(g and pond.available() and not pond.state.get('plan') and not pond.minds.encounter_for('cheese')
                and g.duck.current_action in (None,'idle') and not getattr(g,'_pending_talk_future',None)
                and g.duck.needs.energy>=12 and g.duck.needs.hunger>=12)

def options(pond,item):
    material=pond.state.get('apparel',{}).get(item,{})
    waits=pond.state.get('apparel_care',{}).get('waits',{})
    if not isinstance(waits,dict):waits={}
    now=pond.state['elapsed'];active=pond.state.get('apparel_care',{}).get('active')
    result=[]
    for action,spec in CARE.items():
        if not suited(item,action):continue
        enough=finite(material.get(spec['material']))>=spec['threshold']
        ready=now>=finite(waits.get(item+':'+action))
        reason='Let Cheese finish what he is doing.' if active or not free(pond) else 'Give him a moment before repeating that.' if not ready else 'There is no '+{'wet':'water','snow':'snow','fog':'mist','wind':'strong gust'}[spec['material']]+' to tend.' if not enough else ''
        result.append(dict(id=action,label=spec['label'],enabled=not reason,reason=reason))
    return result

def request(pond,item,action,automatic=False):
    if item!=selected(pond.game):return False,'Equip that hat on Cheese first.'
    option=next((o for o in options(pond,item) if o['id']==action),None)
    if not option:return False,'That care does not suit this hat.'
    if not option['enabled']:return False,option['reason']
    spec=CARE[action];pos=pond.game.renderer.duck_pos
    pos.cancel_movement();pos.set_state_by_name('thinking',spec['duration']+1)
    pond.state.setdefault('apparel_care',{})['active']=dict(item=item,id=action,elapsed=0.,applied=False,
        location=pond.location,x=pos.x,y=pos.y,automatic=automatic)
    return True,spec['label']+'.'

def cancel(pond):
    record=pond.state.setdefault('apparel_care',{})
    if record.pop('active',None):
        pos=pond.game.renderer.duck_pos
        if pos.get_state()=='thinking':pos.set_state_by_name('idle',1)

def care_step(pond,dt,offline=False):
    if not pond.game:return
    dt=max(0,finite(dt));record=pond.state.setdefault('apparel_care',{});active=record.get('active')
    if offline:
        cancel(pond);return
    if active:
        pos=pond.game.renderer.duck_pos;action=active.get('id');item=active.get('item')
        if (not suited(item,action) or selected(pond.game)!=item or not free(pond) or active.get('location')!=pond.location
            or abs(pos.x-finite(active.get('x')))+abs(pos.y-finite(active.get('y')))>1):
            cancel(pond);return
        spec=CARE[action];active['elapsed']=min(spec['duration'],finite(active.get('elapsed'))+dt)
        if active['elapsed']>=spec['contact'] and not active.get('applied'):
            active['applied']=True;s=state(pond,item)
            if 'retained' in spec:s[spec['material']]*=spec['retained']
            # Holding the brim restrains its cloth, never the actual weather.
            if action=='wipe_visor':s['wet']*=.5
            if not isinstance(record.get('waits'),dict):record['waits']={}
            record['waits'][item+':'+action]=pond.state['elapsed']+spec['cooldown']
        if active['elapsed']>=spec['duration']:cancel(pond)
        return
    if not pond.state.get('auto') or not free(pond) or pond.state['elapsed']<finite(record.get('next')):return
    record['next']=pond.state['elapsed']+12
    item=selected(pond.game)
    if not item:return
    # Stop at the current spot for a short physical response. Snow/mist take
    # precedence; a hat is never shaken merely because its animation is due.
    choices={o['id']:o for o in options(pond,item)}
    for action in ('brush_snow','wipe_visor','steady_brim','shed_rain','dab_brim'):
        if choices.get(action,{}).get('enabled'):
            request(pond,item,action,True);break

def care_snapshot(pond):
    if not pond or not pond.game:return {}
    item=selected(pond.game)
    active=pond.state.get('apparel_care',{}).get('active')
    active=copy.deepcopy(active) if active and active.get('item')==item and suited(item,active.get('id')) and free(pond) else None
    if active:active['label']=CARE[active['id']]['label']
    return dict(equipped=item,active=active,options=options(pond,item) if item else [])
