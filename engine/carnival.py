"""Saved carnival choreography; independent visitors and no duplicated rewards.

The ground simulation owns queue positions. This work record owns boarding paths,
seat indices and mechanism phase; the renderer projects them onto the actual ride.
Reservations are transient and never resurrect a departed visitor after loading.
"""
import copy,json,math
from pathlib import Path
from engine import excursions,shelters,surface_play,castle_work
from engine.visitor_shelters import distance,departing,profile
ROUTINES=json.loads((Path(__file__).parent/'client/animation/carnival-routines.json').read_text())
ITEMS={'ferris_wheel','carousel'}
ALL_ITEMS=ITEMS|surface_play.ITEMS
PROGRAMS={**ROUTINES,**surface_play.ROUTINES,**castle_work.ROUTINES}
TAU=math.pi*2
finite=excursions.finite
clamp=excursions.clamp

def is_shared(plan):
    if not isinstance(plan,dict) or not isinstance(plan.get('carnival_work'),dict):return False
    work=plan['carnival_work']
    # Route damaged shared saves to strict validation, never to legacy movement.
    return 'shared_physical' in work or 'shared' in work

def active(minds,key='cheese'):
    return next(iter(minds.carnival_guests.values()),None) if key=='cheese' else minds.carnival_guests.get(key)

def blocked(pond):
    return excursions.adverse(pond.weather_type) or finite(pond.state.get('ecology',{}).get('wind'))>=.8

def choose(pond,item,plan):
    if item in surface_play.ITEMS:return surface_play.choose(pond,item,plan)
    prefix='wheel' if item=='ferris_wheel' else 'carousel'
    age=pond.game.duck.growth_stage;needs=pond.game.duck.needs
    key=prefix+'_first'
    if needs.energy<40 or age in ('elder','legendary'):key=prefix+'_quiet'
    elif pond.hour>=18 or pond.hour<6:key='wheel_lights' if prefix=='wheel' else 'carousel_glow'
    elif age in ('hatchling','duckling'):key=prefix+'_first'
    elif prefix=='wheel':
        key='wheel_grumble' if needs.fun<35 else 'wheel_leaves' if pond.season=='fall' else 'wheel_clouds'
    else:key=['carousel_parade','carousel_trot','carousel_shy'][pond.object_state(item,plan).get('uses',0)%3]
    return dict(id=key,label=ROUTINES[key]['label'],stage='queue',clock=0.,elapsed=0.,ride_elapsed=0.,done=False,invitation_checked=False)

def prepare(pond,plan):
    w=plan['carnival_work'];origin=plan['destination'];offset=18 if plan['target']=='ferris_wheel' else 13
    # Fixed spots by this exact copy, never a target relative to Cheese.
    w['queue_a']=[origin[0]+offset,origin[1]];w['queue_b']=[origin[0]+offset+5,origin[1]]
    if plan['target'] in surface_play.ITEMS:w['queue_a']=[origin[0],origin[1]+2];w['queue_b']=[origin[0]+12,origin[1]+2]
    if w.get('physical_pilot'):
        castle_work.physical_prepare(pond,plan);return
    plan['approach_destination']=list(w['queue_a'])
    pond.game.renderer.duck_pos.move_to(*w['queue_a'])

def valid(pond,plan):
    if not isinstance(plan,dict):return False
    w=plan.get('carnival_work',{})
    if not isinstance(w,dict):return False
    key=w.get('id');item=plan.get('target')
    return bool(isinstance(item,str) and isinstance(key,str) and item in ALL_ITEMS and key in PROGRAMS and PROGRAMS[key]['item']==item and plan.get('instance') and item in pond.owned
        and shelters.still_placed(pond,dict(id=item,instance=plan['instance'],destination=plan.get('destination'))))

def owns(pond,item,obj):
    plan=pond.state.get('plan')
    if not (plan and plan.get('carnival_work') and plan.get('target')==item and pond.object_state(item,plan) is obj):return False
    return 'hold' if plan.get('paused') or plan['phase']!='act' or not pond.available() or pond.game.duck.current_action in ('feed','play','clean','pet','sleep') else 'service' if plan['carnival_work'].get('castle_care') else 'active'

def release(minds,key):
    r=minds.carnival_guests.pop(key,None)
    if r:
        if r.get('shared'):
            from engine import castle_actors
            castle_actors.release_owned(minds.pond,key,r)
        r['work'].pop('companion',None);minds.carnival_retry[key]=minds.now+100;minds.pond._cache=None
        plan=minds.pond.state.get('plan')
        if plan and plan.get('carnival_work') is r['work'] and plan.get('target') in surface_play.ITEMS:
            r['work']['paired']=False
            surface=excursions.state(plan['target'],minds.pond.object_state(plan['target'],plan))['surface']
            surface['b'].update(jump=0.,press=0.,u=0.,v=0.,impact=0.)

def cancel(minds):
    if is_shared(minds.pond.state.get('plan')):
        from engine import castle_shared
        castle_shared.interrupt(minds.pond,minds.pond.state['plan'],'The shared activity was set aside.')
    castle_work.clear(minds.pond,minds.pond.state.get('plan'))
    surface_play.clear(minds.pond,minds.pond.state.get('plan'))
    for key in list(minds.carnival_guests):release(minds,key)

def partner_valid(minds,r,plan=None):
    p=minds.pond;plan=plan or p.state.get('plan')
    return bool(plan and plan.get('carnival_work') is r['work'] and valid(p,plan) and r['location']==p.location
      and r['actor'] in minds.present and minds.presence_tokens.get(r['actor'])==r['token'] and not departing(minds,r['actor'])
      and (r['phase']=='approach' or distance(minds.present[r['actor']],r['spot'])<=3))

def tick(minds,dt):
    p=minds.pond;plan=p.state.get('plan')
    if is_shared(plan):
        from engine import castle_shared
        castle_shared.refresh(p)
        return
    for key,r in list(minds.carnival_guests.items()):
        if not partner_valid(minds,r):release(minds,key);continue
        if plan.get('paused') or not p.available() or minds.game.duck.current_action in ('feed','play','clean','pet','sleep'):continue
        if r['phase']=='approach':
            r['wait']+=max(0,finite(dt))
            if distance(minds.present[key],r['spot'])<=.8:r['phase']='ready'
            elif r['wait']>25:release(minds,key)
    if not plan or not plan.get('carnival_work') or plan.get('paused') or plan['phase'] not in ('prepare','act'):return
    w=plan['carnival_work']
    if blocked(p) and not (w.get('castle_care') and castle_work.allowed(p,w['id'])):return
    if w.get('physical_pilot'):w['invitation_checked']=True;return
    if w.get('invitation_checked') or w['stage']!='queue':return
    w['invitation_checked']=True
    if not valid(p,plan) or not all(6<=spot[0]<=122 and 3<=spot[1]<=36 for spot in (w['queue_a'],w['queue_b'])):return
    from engine import playdates
    options=[]
    reserved=('nest_helpers','playmates','structure_helpers','ground_helpers','textile_helpers','creators','readers','housing','furnishings','gardening','musicians')
    for key in minds.present:
        if key=='cheese' or departing(minds,key) or minds.now<minds.carnival_retry.get(key,0):continue
        if any(key in getattr(minds,name) for name in reserved) or minds.encounter_for(key) or playdates.active(minds,key):continue
        resident=minds.model.residents[key]
        if resident['energy']<.25 or minds.tasks.get(key,{}).get('action') not in ('observe','share','restore','practice'):continue
        d=distance(minds.present[key],w['queue_b'])
        if d>30:continue
        _,species=profile(minds,key)
        options.append((d-5*resident['traits']['sociability'],key,'watch' if species=='butterfly' or resident['energy']<.4 else 'ride'))
    if not options:return
    _,key,mode=min(options);minds.tasks.pop(key,None)
    if w.get('castle_care') and mode=='ride':mode='assist'
    w['companion']=dict(actor=key,mode=mode)
    minds.carnival_guests[key]=dict(actor=key,work=w,spot=list(w['queue_b']),location=p.location,token=minds.presence_tokens[key],
      phase='approach',wait=0.,mode=mode,overlap=0.,contexts={k:minds.context(k) for k in ('cheese',key)})
    p._cache=None

def stage(w,name,duration=0.,start=None,target=None):
    w.update(stage=name,clock=0.,stage_duration=duration)
    if start is not None:w.update(turn_from=start,turn_to=target)

def dock(pond,plan):
    w=plan['carnival_work'];s=excursions.state(plan['target'],pond.object_state(plan['target'],plan));phase=s['phase']
    base=math.pi/2 if plan['target']=='ferris_wheel' else math.pi/4
    n=round((phase-base)/(math.pi/2));target=base+n*math.pi/2
    w.update(seat_a=(-n)%4,seat_b=(1-n)%4 if plan['target']=='carousel' else (-n-1)%4,dock=target,phase=phase)
    stage(w,'align',max(2,abs(target-phase)/.14),phase,target)

def advance(pond,plan,dt):
    w=plan.get('carnival_work')
    if is_shared(plan):
        from engine import castle_shared
        return castle_shared.advance(pond,plan,dt)
    if not w or w.get('done'):return False
    if w.get('physical_pilot'):
        if not valid(pond,plan):return castle_work.physical_interrupt(pond,plan,'The house is no longer placed here.')
        return castle_work.physical_advance(pond,plan,dt)
    if plan['phase']!='act':return False
    pos=pond.game.renderer.duck_pos
    if not valid(pond,plan) or distance((pos.x,pos.y),w['queue_a'])>3:
        w.update(done=True,interrupted=True);cancel(pond.minds);return False
    s=excursions.state(plan['target'],pond.object_state(plan['target'],plan));r=active(pond.minds)
    if r and not partner_valid(pond.minds,r,plan):release(pond.minds,r['actor']);r=None
    if w.get('castle_care'):return castle_work.advance(pond,plan,dt,r)
    if plan['target'] in surface_play.ITEMS:return surface_play.advance(pond,plan,dt,r)
    needs=pond.game.duck.needs
    if (blocked(pond) or needs.hunger<15 or needs.energy<10 or finite(pond.object_state(plan['target'],plan).get('condition'),1.)<=.2) and not w.get('withdrawal'):
        w.update(withdrawal=True,withdrawal_at=w['elapsed']);plan['label']='Returning to the boarding platform'
    if w.get('withdrawal') and w['stage']=='ride':
        target=w['turn_to'];stage(w,'weather_return',max(4,abs(target-w['phase'])/.15),w['phase'],target)
    # Weather closes the queue immediately; aboard residents return to the dock.
    if w.get('withdrawal') and w['stage'] in ('queue','align'):
        w.update(done=True,interrupted=True);cancel(pond.minds);return False
    remaining=min(300,max(0,finite(dt)))
    for _ in range(24):
        if remaining<=0 or w['done']:break
        name=w['stage']
        if name=='queue':
            w['clock']+=remaining;w['elapsed']+=remaining;remaining=0
            if r and r['phase']=='approach' and w['clock']<26:return True
            if r and r['phase']=='approach':release(pond.minds,r['actor']);r=None
            w['paired']=bool(r and r['phase']=='ready' and r['mode']=='ride');dock(pond,plan);break
        duration=w['stage_duration'];step=min(remaining,max(0,duration-w['clock']))
        w['clock']+=step;w['elapsed']+=step;remaining-=step
        if name in ('align','index_b','ride','weather_return','return_a'):
            u=clamp(w['clock']/max(.001,duration));ease=u*u*(3-2*u)
            w['phase']=w['turn_from']+(w['turn_to']-w['turn_from'])*ease;s['phase']=w['phase']%TAU
            s['speed']=abs(w['turn_to']-w['turn_from'])*6*u*(1-u)/max(.001,duration)
            s['running']=s['speed']>0
        else:s.update(speed=0.,running=False)
        if name=='ride':
            w['ride_elapsed']=w['clock']
            if r and r['phase']=='ready':r['overlap']+=step
        if w['clock']<duration:break
        if name=='align':stage(w,'board_a',6)
        elif name=='board_a':
            if w.get('withdrawal'):stage(w,'unload_a',6)
            elif w['paired'] and r:
                if plan['target']=='ferris_wheel':stage(w,'index_b',12,w['dock'],w['dock']+math.pi/2)
                else:stage(w,'board_b',6)
            else:
                w['paired']=False;stage(w,'ride',ROUTINES[w['id']]['duration'],w['phase'],w['phase']+TAU)
        elif name=='index_b':
            if r and not w.get('withdrawal'):stage(w,'board_b',6)
            else:stage(w,'return_a',12,w['phase'],w['phase']-math.pi/2)
        elif name=='board_b':
            # Both guests are at the docking station already if rain interrupts
            # boarding, so reverse the path before rotating back to Cheese.
            if w.get('withdrawal'):stage(w,'unload_b',6)
            else:stage(w,'ride',ROUTINES[w['id']]['duration'],w['phase'],w['phase']+TAU)
        elif name in ('ride','weather_return'):
            if w['paired']:stage(w,'unload_b',6)
            else:stage(w,'unload_a',6)
        elif name=='unload_b':
            if plan['target']=='ferris_wheel':stage(w,'return_a',12,w['phase'],w['phase']-math.pi/2)
            else:stage(w,'unload_a',6)
        elif name=='return_a':stage(w,'unload_a',6)
        elif name=='unload_a':
            w.update(done=True,stage='done',interrupted=bool(w.get('withdrawal')));s.update(speed=0.,running=False)
    pond._cache=None
    return not w['done']

def completion_ready(pond,plan):
    """Gate all item rewards using the explicit, already-consumed plan."""
    if not isinstance(plan,dict):return False
    w=plan.get('carnival_work')
    if not isinstance(w,dict) or not valid(pond,plan) or w.get('done') is not True or w.get('interrupted') or w.get('recorded'):return False
    if is_shared(plan):
        from engine import castle_shared
        return castle_shared.completion_ready(pond,plan)
    if w['id'] in castle_work.PHYSICAL_SCORES or w.get('physical_pilot'):
        if not castle_work.physical_geometry_ok(pond,plan) or w.get('stage')!='done':return False
        pos=pond.game.renderer.duck_pos;root=[pos.x,pos.y];physical=w['physical']
        if max(abs(root[i]-physical['exit'][i]) for i in (0,1))>.51:return False
        if not castle_work.supported(pond,plan,root,physical['center']):return False
    return True

def complete(pond,plan):
    w=plan.get('carnival_work')
    if not completion_ready(pond,plan):return
    if is_shared(plan):
        from engine import castle_shared
        return castle_shared.complete(pond,plan)
    w['recorded']=True;obj=pond.object_state(plan['target'],plan);history=obj.setdefault('carnival_routines',{})
    history[w['id']]=min(9999,history.get(w['id'],0)+1)
    pond.remember('belongings',w['label']+'.',.5,plan['target'])
    r=active(pond.minds)
    if r and partner_valid(pond.minds,r,plan) and r['overlap']>=PROGRAMS[w['id']]['duration']*.8:
        m=pond.minds;key=r['actor'];note=w['label']+(' together; boarded separately and returned to the platform.' if r['mode']=='ride' else '; watched from the platform and waved back.')
        if plan['target'] in surface_play.ITEMS:note=w['label']+('; watched from beside the entry.' if r['mode']=='watch' else '; shared the surface and stepped off together.')
        if w.get('castle_care'):note=w['label']+('; watched the real controls from outside.' if r['mode']=='watch' else '; worked together at the empty house, then stepped away.')
        for actor,other in (('cheese',key),(key,'cheese')):
            m.model.learn(actor,'share',r['contexts'][actor],.25,m.now,note,other);m.model.bond(actor,other,.18,m.now,note)
        counts=obj.setdefault('carnival_company',{});counts[key]=min(9999,counts.get(key,0)+1)
        pond.remember('neighbors',m.model.residents[key]['name']+' and Cheese: '+note,.6,key)
    cancel(pond.minds)

def view(pond,plan):
    if is_shared(plan):
        from engine import castle_shared
        return castle_shared.view(pond,plan)
    w=copy.deepcopy(plan['carnival_work']);r=active(pond.minds)
    if w.get('physical_pilot') and isinstance(w.get('physical'),dict):
        pos=pond.game.renderer.duck_pos;root=[pos.x,pos.y]
        if root!=w['physical'].get('root'):w['physical']['contact_ready']=False
        w['physical']['root']=root
    if not r or not partner_valid(pond.minds,r,plan):w.pop('companion',None)
    elif w.get('companion'):w['companion']['ready']=r['phase']=='ready'
    return w

def restore(pond):
    plan=pond.state.get('plan')
    if not plan or not isinstance(plan.get('carnival_work'),dict):return
    w=plan['carnival_work']
    if is_shared(plan):
        from engine import castle_shared
        castle_shared.interrupt(pond,plan,'A saved shared activity needs a new invitation.')
        return
    if w.get('physical_pilot') and not castle_work.physical_active(plan):
        castle_work.physical_interrupt(pond,plan,'Invalid saved control reservation.');return
    if not valid(pond,plan) or pond.location!=plan['location']:return
    if w.get('physical_pilot'):
        castle_work.physical_restore(pond,plan);return
    if plan['target'] in surface_play.ITEMS:
        w['paired']=False
        surface=excursions.state(plan['target'],pond.object_state(plan['target'],plan))['surface']
        surface['b'].update(jump=0.,press=0.,u=0.,v=0.,impact=0.)
    if plan['phase']=='act' and w.get('stage') not in ('queue','align','done'):
        # The saved seat is the physical location; its ground projection must be
        # restored as well when a fresh process constructs a new position actor.
        pos=pond.game.renderer.duck_pos;pos.cancel_movement();pos.x,pos.y=w['queue_a'];pos.set_state_by_name('thinking',0)

def motion(minds,key):
    if is_shared(minds.pond.state.get('plan')):
        from engine import castle_shared
        return castle_shared.motion(minds,key)
    r=minds.carnival_guests.get(key)
    return dict(target=list(r['spot']),phase=r['phase'],facing=False,gesture='idle') if r else None

def conversation(pond,plan,key='cheese'):
    if not plan or not plan.get('carnival_work') or not valid(pond,plan):return None
    w=plan['carnival_work'];r=active(pond.minds)
    if r and not partner_valid(pond.minds,r,plan):r=None
    if key!='cheese' and (not r or key!=r['actor']):return None
    if w.get('castle_care'):return castle_work.conversation(pond,plan,key,r)
    if plan['target'] in surface_play.ITEMS:return surface_play.conversation(pond,plan,key,r)
    role='a' if key=='cheese' else 'b';watch=bool(role=='b' and r and r['mode']=='watch')
    aboard=w['stage'] in (('index_b','board_b','ride','weather_return','unload_b','return_a') if role=='a' else ('ride','weather_return')) and not watch
    status='watching from the platform' if watch else 'aboard' if aboard else 'boarding' if w['stage']=='board_'+role else 'getting off' if w['stage']=='unload_'+role else 'at the platform'
    return dict(object=plan['target'].replace('_',' '),activity=w['label'],stage=w['stage'],paused=bool(plan.get('paused')),
      seating_status=status,actual_seat=w.get('seat_'+role) if aboard else None,mechanism_phase=round(w.get('phase',0),3),
      company=pond.minds.model.residents[r['actor']]['name'] if r else None,company_status=r['phase']+' / '+r['mode'] if r else None,
      returning_for_weather=bool(w.get('withdrawal')))

def request(pond,item,choice,instance=None,together=False):
    if item not in ALL_ITEMS or not isinstance(choice,str) or choice not in PROGRAMS or PROGRAMS[choice]['item']!=item:return False,'Choose an activity for this ride.'
    proposal=None
    if together:
        if choice not in castle_work.PHYSICAL_SCORES:return False,'Choose one of the shared control activities.'
        from engine import castle_shared
        proposal,reason=castle_shared.propose(pond,choice,instance)
        if proposal is None:return False,reason
    ok,message=pond.start('item',item,instance=instance,carnival_choice=choice,shared_proposal=proposal)
    if not ok:return ok,message
    p=pond.state['plan']
    if not is_shared(p):p['carnival_work'].update(id=choice,label=PROGRAMS[choice]['label']);p['label']=PROGRAMS[choice]['label']
    return True,p['label']+'.'
