"""Saved hat and accessory materials and care, without equipping or granting."""
import copy,json,math
from pathlib import Path
from engine.excursions import clamp,finite
BLUEPRINTS=json.loads((Path(__file__).parent/'client/animation/headwear.json').read_text())
CARE=json.loads((Path(__file__).parent/'client/animation/headwear-care.json').read_text())
ACCESSORIES=json.loads((Path(__file__).parent/'client/animation/accessories.json').read_text())
ACCESSORY_CARE=json.loads((Path(__file__).parent/'client/animation/accessory-care.json').read_text())
SLOTS=json.loads((Path(__file__).parent/'client/animation/wearable-slots.json').read_text())
PROFILES={**BLUEPRINTS,**ACCESSORIES}

def care_for(item):return ACCESSORY_CARE if item in ACCESSORIES else CARE

def selected_items(game):
    from engine.scene import equipped_wearables
    if game.duck.growth_stage=='egg':return []
    slots={}
    for item in equipped_wearables(game).values():
        if item in SLOTS:slots[SLOTS[item]]=item
    available=owned(game)
    return [item for item in slots.values() if item in PROFILES and item in available]

def owned(game):
    wardrobe=getattr(getattr(game,'seasonal_clothing',None),'wardrobe',None)
    return set(getattr(getattr(game,'habitat',None),'owned_items',[]))|set(getattr(getattr(game,'outfits',None),'owned_items',[]))|set(getattr(wardrobe,'owned_items',[]))

def selected(game):
    return next((item for item in selected_items(game) if item in BLUEPRINTS),None)

def state(pond,item):
    records=pond.state.setdefault('apparel',{})
    if not isinstance(records.get(item),dict):records[item]={}
    s=records[item]
    for key in ('wet','snow','fog','wind'):s[key]=clamp(s.get(key))
    if item in ACCESSORIES:
        for key in ('soil','slack'):s[key]=clamp(s.get(key))
    s['phase']=finite(s.get('phase'))%math.tau
    return s

def sheltered(pond):
    from engine import shelters
    plan=pond.state.get('plan') or {};r=plan.get('residence')
    return bool(r and r.get('roof') and shelters.still_placed(pond,r) and plan.get('phase') in ('act','settle'))

def update(pond,dt,weather,intensity,temperature,wind,offline=False):
    if not pond.game:return
    dt=max(0,finite(dt));active=selected_items(pond.game);outside=not offline and not sheltered(pond)
    # No fitted wardrobe exists while unhatched. A stored accessory dries
    # quietly; it cannot collect weather from a different wearer or location.
    wet='rainbow' not in weather and any(x in weather for x in ('rain','storm','drizzle','shower','sleet'))
    snow=any(x in weather for x in ('snow','blizzard'))
    for item in owned(pond.game)&PROFILES.keys():
        s=state(pond,item);wearing=item in active and not offline;p=PROFILES[item]
        exposure=wearing and outside
        target=clamp(intensity)*p['absorbency'] if exposure and wet else 0
        s['wet']=target+(s['wet']-target)*math.exp(-dt/(90 if exposure and wet else 600))
        target=clamp(intensity) if exposure and snow else 0
        s['snow']=target+(s['snow']-target)*math.exp(-dt/(120 if exposure and snow else 360 if temperature<0 else 90))
        target=.8 if wearing and (p['shape']=='helmet' or p.get('fog')) and temperature<8 else 0
        s['fog']=target+(s['fog']-target)*math.exp(-dt/40)
        s['wind']=clamp(wind) if exposure else 0
        if wearing:s['phase']=(s['phase']+dt*(.9+s['wind']*2))%math.tau
        if item in ACCESSORIES and wearing:
            action=pond.game.renderer.duck_pos.get_state()
            moving=any(x in action for x in ('walk','waddle','hop','danc','flap'))
            s['slack']=clamp(s['slack']+dt*((.00045 if moving else 0)+s['wind']*.00012))
            messy=pond.game.duck.current_action in ('feed','play') or action in ('eating','playing','digging')
            s['soil']=clamp(s['soil']+dt*(.0007 if messy else .00006 if exposure and s['wind']>.55 and not wet else 0))

def snapshot(pond):
    # A renderer has no authority to advance material or instantiate ownership.
    if not pond or not pond.game:return {}
    available=owned(pond.game)
    return {i:copy.deepcopy(s) for i,s in pond.state.get('apparel',{}).items() if i in available and i in PROFILES}

def suited(item,action):
    p=PROFILES.get(item,{})
    if not p or action not in care_for(item):return False
    spec=care_for(item)[action]
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
    for action,spec in care_for(item).items():
        if not suited(item,action):continue
        enough=finite(material.get(spec['material']))>=spec['threshold']
        ready=now>=finite(waits.get(item+':'+action))
        reason='Let Cheese finish what he is doing.' if active or not free(pond) else 'Give him a moment before repeating that.' if not ready else 'There is no '+{'wet':'water','snow':'snow','fog':'mist','wind':'strong gust','soil':'grime','slack':'looseness'}[spec['material']]+' to tend.' if not enough else ''
        result.append(dict(id=action,label=spec['label'],enabled=not reason,reason=reason))
    return result

def request(pond,item,action,automatic=False):
    if item not in selected_items(pond.game):return False,'Equip that accessory on Cheese first.'
    option=next((o for o in options(pond,item) if o['id']==action),None)
    if not option:return False,'That care does not suit this accessory.'
    if not option['enabled']:return False,option['reason']
    spec=care_for(item)[action];pos=pond.game.renderer.duck_pos
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
        if (not suited(item,action) or item not in selected_items(pond.game) or not free(pond) or active.get('location')!=pond.location
            or abs(pos.x-finite(active.get('x')))+abs(pos.y-finite(active.get('y')))>1):
            cancel(pond);return
        spec=care_for(item)[action];active['elapsed']=min(spec['duration'],finite(active.get('elapsed'))+dt)
        if active['elapsed']>=spec['contact'] and not active.get('applied'):
            active['applied']=True;s=state(pond,item)
            if 'retained' in spec:s[spec['material']]*=spec['retained']
            # Holding the brim restrains its cloth, never the actual weather.
            if action=='wipe_visor':s['wet']*=.5
            if action=='wipe_lenses':s['wet']*=.5;s['soil']*=.6
            if not isinstance(record.get('waits'),dict):record['waits']={}
            record['waits'][item+':'+action]=pond.state['elapsed']+spec['cooldown']
        if active['elapsed']>=spec['duration']:cancel(pond)
        return
    if not pond.state.get('auto') or not free(pond) or pond.state['elapsed']<finite(record.get('next')):return
    record['next']=pond.state['elapsed']+12
    # Stop at the current spot for a short physical response. Snow/mist take
    # precedence; care is never performed merely because an animation is due.
    priorities=('brush_snow','wipe_visor','steady_brim','wipe_lenses','brush_collar_snow','wring_scarf','dry_frames','dab_earpads','shed_rain','dab_brim','dab_bow','settle_frames','retie_bow','settle_headband','settle_pendant','clean_frames','clean_pendant')
    for action in priorities:
        for item in selected_items(pond.game):
            option=next((o for o in options(pond,item) if o['id']==action and o['enabled']),None)
            if option:request(pond,item,action,True);return

def care_snapshot(pond):
    if not pond or not pond.game:return {}
    wearing=selected_items(pond.game)
    active=pond.state.get('apparel_care',{}).get('active')
    active=copy.deepcopy(active) if active and active.get('item') in wearing and suited(active.get('item'),active.get('id')) and free(pond) else None
    item=active['item'] if active else selected(pond.game) or (wearing[0] if wearing else None)
    if active:active['label']=care_for(item)[active['id']]['label']
    return dict(equipped=item,active=active,options=options(pond,item) if item else [],items=[dict(id=i,options=options(pond,i)) for i in wearing])
