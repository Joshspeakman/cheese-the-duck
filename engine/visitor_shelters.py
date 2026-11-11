"""Real visitor shelter reservations, arrivals, shared waits and departures.

Occupancy is transient; completed experiences belong to the persistent brains.
No guest inherits a reservation from a previous visit or a loaded save.
"""
import copy
import math
from datetime import datetime
from engine import shelters
from world.guest_cast import guest_profile

def distance(a,b):return math.hypot(a[0]-b[0],(a[1]-b[1])*2)

def departing(minds,key):
    g=minds.game;visit=g.friends.current_visit
    if visit and visit.friend_id==key:
        from world.friends import visitor_animator
        return visitor_animator._is_leaving
    rare=g.atmosphere.current_visitor
    if rare and rare[0].id==key:
        try:return rare[0].stay_duration_hours*3600-(datetime.now()-datetime.fromisoformat(rare[1])).total_seconds()<=6
        except (ValueError,TypeError):return False
    return False

def profile(minds,key):
    resident=minds.model.residents[key]
    p=guest_profile(resident['cast']) or {}
    species='duckling' if key=='story:pip' else p.get('species','duck')
    return ('duckling' if species=='duckling' else 'adult'),species

def release(minds,key,completed=False):
    r=minds.housing.pop(key,None)
    if not r:return
    if completed and r.get('waited',0)>=8:
        note='Waited out '+r['weather'].replace('_',' ')+' in the '+r['id'].replace('_',' ')+'.'
        minds.model.learn(key,'rest',r['context'],.3,minds.now,note)
        minds.model.remember(key,'shelter',note,minds.now,.55)
    minds.pond._cache=None

def tick(minds,dt):
    p=minds.pond;bad=shelters.adverse(p.weather_type)
    for key,r in list(minds.housing.items()):
        if key not in minds.present or r['token']!=minds.presence_tokens.get(key) or r['location']!=p.location or departing(minds,key):
            release(minds,key);continue
        if not shelters.still_placed(p,r):
            release(minds,key);minds.shelter_retry[key]=minds.now+2;continue
        if not bad and r['phase']=='approach':
            release(minds,key);continue
        where=minds.present[key]
        if r['phase']=='approach':
            if minds.now-r['started']>90:
                release(minds,key);minds.shelter_retry[key]=minds.now+20;continue
            if distance(where,r['destination'])<=.8:
                r.update(phase='enter',elapsed=0.)
        elif r['phase']=='enter':
            if distance(where,r['destination'])>3:
                r.update(phase='approach',elapsed=0.);continue
            r['elapsed']+=dt
            if r['elapsed']>=3:r.update(phase='inside',elapsed=0.)
        elif r['phase']=='inside':
            if distance(where,r['destination'])>3:
                release(minds,key);minds.shelter_retry[key]=minds.now+2;continue
            r['waited']+=dt;r['elapsed']+=dt
            resident=minds.model.residents[key]
            gain=min(.08-r['recovered'],dt*.0005)
            if gain>0:resident['energy']=min(1.,resident['energy']+gain);r['recovered']+=gain
            if not bad:r.update(phase='exit',elapsed=0.)
        elif r['phase']=='exit':
            r['elapsed']+=dt
            if r['elapsed']>=3:
                release(minds,key,completed=True);minds.shelter_retry[key]=minds.now+15
    if not bad or p.location!='Home Pond':return
    # A new reservation consumes its slot immediately, before the next resident
    # chooses. Actors keep their own destination even if Cheese walks elsewhere.
    for key in sorted(minds.present):
        if key=='cheese' or key in minds.housing or minds.now<minds.shelter_retry.get(key,0) or departing(minds,key):continue
        stage,species=profile(minds,key)
        choices=shelters.candidates(p,actor=key,stage=stage,position_at=minds.present[key],species=species)
        if not choices:
            minds.shelter_retry[key]=minds.now+5;continue
        chosen=choices[0]
        minds.cancel_encounter(key)
        minds.housing[key]={**chosen,'actor':key,'token':minds.presence_tokens[key],
            'location':p.location,'phase':'approach','elapsed':0.,'waited':0.,'recovered':0.,
            'started':minds.now,'context':minds.context(key)}
        minds.pond._cache=None
    for key in list(minds.shelter_retry):
        if key not in minds.present:minds.shelter_retry.pop(key)

def motion(minds,key):
    r=minds.housing.get(key)
    if not r:return None
    from engine.shelter_company import for_actor
    gesture='walking' if r['phase'] in ('enter','exit') else 'sleeping' if r['phase']=='inside' and not for_actor(minds,key) else 'idle'
    facing=r['slot']==0 if r['phase']!='enter' else r['slot']>=(r['capacity']-1)/2
    return {'target':list(r['destination']), 'facing':facing,'phase':r['phase'],'gesture':gesture}

def snapshot(minds):
    return [{k:copy.deepcopy(r.get(k)) for k in ('actor','id','instance','destination','slot','capacity','phase','elapsed','waited')}
            for r in minds.housing.values()]
