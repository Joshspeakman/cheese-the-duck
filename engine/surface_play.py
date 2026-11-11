"""Native spring-floor play and weight-responsive magic-carpet hovering.

Arrival and visitor reservations are shared with carnival.py. This module owns
physical height, pressure, flight/landing events and a finite landing/exit path.
"""
import copy,json,math
from pathlib import Path
from engine import excursions
from engine.visitor_shelters import profile
ROUTINES=json.loads((Path(__file__).parent/'client/animation/surface-routines.json').read_text())
ITEMS={'bounce_house','magic_carpet'}
POSE=dict(x=0.,y=0.,b=0.,w=0.,l=0.,r=0.,u=0.,v=0.,press=0.,seated=0.,eye=None,mark='')
finite=excursions.finite;clamp=excursions.clamp

def sample(track,p,base):
    p=clamp(p);a,b=track[0],track[-1]
    for i in range(1,len(track)):
        if p<=track[i][0]:a,b=track[i-1:i+1];break
    u=clamp((p-a[0])/max(.001,b[0]-a[0]));u=u*u*(3-2*u)
    aa={**base,**a[1]};bb={**base,**b[1]}
    return {k:aa[k]+(bb[k]-aa[k])*u if isinstance(v,(int,float)) else bb[k] if u>.5 else aa[k] for k,v in base.items()}

def scale(age,species='duck'):
    age_factor={'hatchling':.35,'duckling':.5,'juvenile':.75,'mature':.8,'elder':.35,'legendary':.3}.get(age,1.)
    return age_factor*{'goose':.75,'owl':.7,'toad':1.15,'butterfly':0}.get(species,1.)

def controls(work):
    spec=ROUTINES[work['id']];t=work.get('ride_elapsed',0.);p=clamp(t/spec['duration']);out={}
    for role in ('a','b'):
        pose=sample(spec[role],p,POSE);factor=work.get('factors',{}).get(role,1.);jump=0.;press=pose['press'];impact=0.
        for start,end,height in spec['leaps'][role]:
            a=start*spec['duration'];length=(end-start)*spec['duration']*math.sqrt(max(.01,factor));b=a+length
            if a<=t<=b:
                u=(t-a)/max(.001,length);jump=max(jump,4*u*(1-u)*height*factor)
            if a-.5<=t<a:press=max(press,.55*math.sin(math.pi*(t-a+.5)/.5))
            if b<=t<b+1.2:
                age=t-b;impact=max(impact,1-age/1.2);press=max(press,.85*math.exp(-age*3))
        out[role]={**pose,'jump':jump,'press':clamp(press),'impact':impact}
    out.update(sample(spec['deck'],p,dict(lift=0.,tilt=0.)))
    return out

def choose(pond,item,plan):
    prefix='bounce' if item=='bounce_house' else 'carpet';age=pond.game.duck.growth_stage;needs=pond.game.duck.needs
    key=prefix+'_first'
    if age in ('elder','legendary') or needs.energy<40:key=prefix+'_quiet'
    elif pond.hour>=21 or pond.hour<6:key=prefix+'_moon'
    elif age in ('hatchling','duckling'):key=prefix+'_first'
    elif needs.fun<35:key=prefix+'_grumble'
    elif item=='bounce_house' and pond.season=='fall':key='bounce_leaf'
    elif item=='magic_carpet' and pond.hour>=18:key='carpet_evening'
    else:
        options=['bounce_echo','bounce_together','bounce_corners','bounce_statue','bounce_stomp','bounce_tiptoe','bounce_ripple','bounce_wings','bounce_bow'] if item=='bounce_house' else ['carpet_balance','carpet_banks','carpet_waves','carpet_climb','carpet_landings','carpet_fringe','carpet_clouds','carpet_peek','carpet_steady']
        key=options[pond.object_state(item,plan).get('uses',0)%len(options)]
    return dict(id=key,label=ROUTINES[key]['label'],stage='queue',clock=0.,elapsed=0.,ride_elapsed=0.,done=False,invitation_checked=False,
      factors=dict(a=scale(age),b=1.),events=[],landings=dict(a=0,b=0),surface_play=True)

def inside(w,role):
    if w['stage']=='board_'+role:return clamp(w['clock']/4)
    if w['stage']=='unload_'+role:return 1-clamp(w['clock']/4)
    return float(w['stage'] in (('board_b','play','land','unload_b') if role=='a' else ('play','land')))

def clear(pond,plan):
    if not plan or plan.get('target') not in ITEMS:return
    obj=pond.object_state(plan['target'],plan)
    if obj:
        s=excursions.state(plan['target'],obj)['surface'];s.update(lift=0.,tilt=0.,gate=0.,active=False)
        for role in ('a','b'):s[role].update(jump=0.,press=0.,u=0.,v=0.,impact=0.)

def advance(pond,plan,dt,r):
    from engine import carnival
    w=plan['carnival_work'];obj=pond.object_state(plan['target'],plan);e=excursions.state(plan['target'],obj);s=e['surface'];s['active']=True
    needs=pond.game.duck.needs;bad=carnival.blocked(pond) or needs.hunger<15 or needs.energy<10 or finite(obj.get('condition'),1.)<=.2
    if bad and not w.get('withdrawal'):
        w.update(withdrawal=True,withdrawal_at=w['elapsed']);plan['label']='Stepping off the spring floor' if plan['target']=='bounce_house' else 'Bringing the carpet back down'
    if w.get('withdrawal') and w['stage'] in ('queue','inflate','spread'):
        w.update(done=True,interrupted=True);clear(pond,plan);return False
    if w.get('withdrawal') and w['stage']=='play':
        w['landing_from']=copy.deepcopy(s);carnival.stage(w,'land',3 if plan['target']=='bounce_house' else 6)
    remaining=min(300,max(0,finite(dt)))
    for _ in range(20):
        if remaining<=0 or w['done']:break
        name=w['stage']
        if name=='queue':
            w['clock']+=remaining;w['elapsed']+=remaining;remaining=0
            if r and r['phase']=='approach' and w['clock']<26:return True
            if r and r['phase']=='approach':carnival.release(pond.minds,r['actor']);r=None
            w['paired']=bool(r and r['phase']=='ready' and r['mode']=='ride')
            if r:
                age,species=profile(pond.minds,r['actor']);w['factors']['b']=scale(age,species)
            w.update(inflation_from=e['inflation'],cover_from=e['cover'])
            carnival.stage(w,'inflate' if plan['target']=='bounce_house' else 'spread',6)
            break
        duration=w['stage_duration'];step=min(remaining,max(0,duration-w['clock']));old=w['clock'];w['clock']+=step;w['elapsed']+=step;remaining-=step
        u=clamp(w['clock']/max(.001,duration));smooth=u*u*(3-2*u)
        if name=='inflate':e['inflation']=w['inflation_from']+(1-w['inflation_from'])*smooth;s['gate']=smooth
        elif name=='spread':e['cover']=w['cover_from']*(1-smooth);s['gate']=smooth
        elif name=='play':
            w['ride_elapsed']=w['clock'];v=controls(w);s.update(lift=v['lift'],tilt=v['tilt'],gate=1.)
            for role in ('a','b'):
                present=role=='a' or bool(r and r['phase']=='ready' and r['mode']=='ride' and w['paired'])
                for k in ('jump','press','u','v','impact'):s[role][k]=v[role][k] if present else 0.
                if not present:continue
                for index,(start,end,height) in enumerate(ROUTINES[w['id']]['leaps'][role]):
                    landing=start*duration+(end-start)*duration*math.sqrt(max(.01,w['factors'][role]));key=role+':'+str(index)
                    if old<landing<=w['clock'] and key not in w['events']:
                        w['events'].append(key);w['landings'][role]+=1;obj['soft_landings']=min(9999,obj.get('soft_landings',0)+1)
            if r and r['phase']=='ready':r['overlap']+=step
        elif name=='land':
            start=w['landing_from'];s.update(lift=start['lift']*(1-smooth),tilt=start['tilt']*(1-smooth))
            for role in ('a','b'):
                present=role=='a' or bool(r and r['phase']=='ready' and r['mode']=='ride' and w['paired'])
                for k in ('jump','press','u','v','impact'):s[role][k]=start[role][k]*(1-smooth) if present else 0.
        if w['clock']<duration:break
        if name in ('inflate','spread'):carnival.stage(w,'board_a',4)
        elif name=='board_a':
            if w.get('withdrawal'):carnival.stage(w,'unload_a',4)
            elif w['paired'] and r:carnival.stage(w,'board_b',4)
            else:w['paired']=False;carnival.stage(w,'play',ROUTINES[w['id']]['duration'])
        elif name=='board_b':
            if w.get('withdrawal'):carnival.stage(w,'unload_b',4)
            else:carnival.stage(w,'play',ROUTINES[w['id']]['duration'])
        elif name=='play':
            w['landing_from']=copy.deepcopy(s);carnival.stage(w,'land',3 if plan['target']=='bounce_house' else 5)
        elif name=='land':carnival.stage(w,'unload_b' if w['paired'] else 'unload_a',4)
        elif name=='unload_b':carnival.stage(w,'unload_a',4)
        elif name=='unload_a':w.update(done=True,stage='done',interrupted=bool(w.get('withdrawal')));clear(pond,plan)
    pond._cache=None
    return not w['done']

def conversation(pond,plan,key,r):
    w=plan['carnival_work'];role='a' if key=='cheese' else 'b';watch=role=='b' and r and r['mode']=='watch';aboard=inside(w,role)>.99 and not watch
    s=excursions.state(plan['target'],pond.object_state(plan['target'],plan))['surface']
    status='watching beside the entry' if watch else 'in the air above the spring floor' if aboard and s[role]['jump']>.05 else 'on the surface' if aboard else 'stepping on' if w['stage']=='board_'+role else 'stepping off' if w['stage']=='unload_'+role else 'at the entry'
    return dict(object=plan['target'].replace('_',' '),activity=w['label'],stage=w['stage'],paused=bool(plan.get('paused')),
      body_status=status,
      current_jump_height=round(s[role]['jump'],2) if aboard else 0,carpet_lift=round(s['lift'],2),completed_landings=w['landings'][role] if aboard else 0,
      floor_pressure=round(s[role]['press'],2) if aboard else 0,
      company=pond.minds.model.residents[r['actor']]['name'] if r else None,company_status=r['phase']+' / '+r['mode'] if r else None,
      setting='The same patch of bank. This is a local hover, not a journey.' if plan['target']=='magic_carpet' else 'A spring floor inside the bounce house, with a separate lane for each resident.',
      returning_for_weather=bool(w.get('withdrawal')))
