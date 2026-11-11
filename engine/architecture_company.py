"""Structure companions arrive independently and share the native work clock.

Reservations are transient. Actual arrival, shared native time and completed work
are required for learning. The partner never duplicates an item use or reward.
"""
import copy
import json
from pathlib import Path
from engine import architecture
from engine.visitor_shelters import distance, departing, profile

SCORES=json.loads((Path(__file__).parent/'client/animation/architecture-company.json').read_text())

def active(minds,key='cheese'):
    return next(iter(minds.structure_helpers.values()),None) if key=='cheese' else minds.structure_helpers.get(key)

def ready(minds):
    return minds.pond.available() and minds.game.duck.current_action not in ('feed','play','clean','pet','sleep')

def valid(minds,r,plan=None):
    p=minds.pond;plan=plan or p.state.get('plan')
    pos=minds.game.renderer.duck_pos
    return bool(plan and plan.get('architecture_work') is r['work'] and architecture.valid(p,plan)
                and abs(pos.x-r['destination'][0])+abs(pos.y-r['destination'][1])<=3
                and r['actor'] in minds.present and minds.presence_tokens.get(r['actor'])==r['token']
                and (r['phase']=='approach' or distance(minds.present[r['actor']],r['spot'])<=3)
                and r['location']==p.location and not departing(minds,r['actor'])
                and r['actor'] not in minds.housing and not r['work'].get('withdrawal') and not r['work'].get('interrupted') and not architecture.wet(p) and not architecture.gusty(p.weather_type))

def choose(minds,plan,key):
    item=plan['target'];kind=architecture.ITEMS[item]['type'];work=plan['architecture_work'];core=work['id']
    if core in ('rain_drips','storm_stepback'):return None
    age=minds.game.duck.growth_stage;stage,species=profile(minds,key);resident=minds.model.residents[key]
    if species=='butterfly':return 'hover_visit'
    if stage=='duckling' or age in ('hatchling','duckling') or core=='young_survey':return 'young_company'
    if age in ('elder','legendary') or core=='elder_survey' or resident['energy']<.45 or resident['mood']<.25:return 'elder_rest'
    if core=='night_survey' or minds.pond.hour<6 or minds.pond.hour>=19:return 'night_watch'
    if kind in ('arch','pergola','trellis') and minds.pond.season=='winter':return 'winter_vines'
    direct={'picket_knots':'picket_compare','picket_brush':'picket_brush','wall_layers':'masonry_course','wall_moss':'moss_watch',
        'arch_trace':'arch_frame','arch_shadow':'arch_light','bridge_cross':'bridge_spotter','bridge_listen':'bridge_echo',
        'watchtower_braces':'brace_compare','watchtower_roof':'tower_roof_watch','windmill_turn':'sail_count',
        'windmill_brake':'brake_watch','windmill_release':'brake_watch','gate_open':'gate_welcome' if resident['traits']['confidence']>=.5 else 'gate_clear',
        'gate_close':'gate_clear','gate_hinge':'hinge_brush','pergola_shade':'pergola_shade','pergola_beams':'pergola_vine',
        'mailbox_open':'mailbox_watch','mailbox_close':'mailbox_watch','mailbox_flag':'mailbox_flag','mailbox_lower_flag':'mailbox_flag',
        'well_lower':'bucket_watch','well_raise':'bucket_watch','well_echo':'well_echo','trellis_flowers':'trellis_petals','trellis_ties':'trellis_ties',
        'castle_arrowloop':'tower_roof_watch','castle_stones':'castle_history','iron_scroll':'iron_scrolls','iron_brush':'iron_brushpair'}
    return direct.get(core)

def controls(work,score):
    return architecture.sample(work,SCORES[score]['track'],dict(u=1.08,v=0.,contact=0.))

def contact(minds,r,event,at):
    obj=minds.pond.object_state(r['id'],r.get('instance'));s=architecture.state(r['id'],obj)
    _,species=profile(minds,r['actor'])
    if species=='butterfly':return
    if event=='clean':obj['dirt']=max(0.,obj.get('dirt',0)-.04);s['cleanings']=min(9999,s['cleanings']+1)
    elif event=='tap':s['taps']=min(9999,s['taps']+1)
    minds.pond._cache=None

def observations(minds,r):
    p=minds.pond;obj=p.object_state(r['id'],r['instance']);s=obj['architecture'];kind=architecture.ITEMS[r['id']]['type'];notes=[]
    events=[SCORES[r['score']]['events'][i][1] for i in r['events']]
    if 'clean' in events:notes.append('Brushed grit from opposite ends of the structure')
    if 'tap' in events:notes.append('Tapped the far landing stone '+str(events.count('tap'))+' times')
    if kind=='gate':notes.append('Saw the iron gate '+('open' if s['open']>.9 else 'closed' if s['open']<.1 else 'partway open'))
    elif kind=='mailbox':
        if s['panel']>.7:notes.append('Looked into the empty mail compartment; no delivery arrived')
        notes.append('Saw the red flag '+('raised' if s['flag']>.9 else 'lowered' if s['flag']<.1 else 'partway up'))
    elif kind=='well':notes.append('Watched the bucket '+('below the rim' if s['bucket']>.6 else 'at the rim' if s['bucket']<.1 else 'partway down')+'; collected nothing')
    elif kind=='windmill':notes.append('Watched the sails '+('turning' if s['speed']>.05 else 'at rest')+' with the brake '+('applied' if s['brake']>.9 else 'released' if s['brake']<.1 else 'partly applied'))
    elif kind in ('pergola','trellis','arch'):notes.append('Compared '+('bare winter stems' if s['season']=='winter' else 'autumn climbing leaves' if s['season']=='fall' else 'climbing leaves and small roses'))
    elif kind=='castle' and r['score']=='castle_history':notes.append('Read the foundation carving: '+architecture.ITEMS[r['id']]['inscription'])
    return notes

def release(minds,key):
    if minds.structure_helpers.pop(key,None):
        minds.structure_retry[key]=minds.now+100
        minds.pond._cache=None

def tick(minds,dt):
    p=minds.pond;plan=p.state.get('plan')
    for key,r in list(minds.structure_helpers.items()):
        if not valid(minds,r) or not ready(minds):release(minds,key);continue
        if plan.get('paused'):
            r['started']+=dt
            continue
        if r['phase']=='approach':
            if minds.now-r['started']>25:release(minds,key);continue
            if distance(minds.present[key],r['spot'])<=.8:r.update(phase='enter',elapsed=0.)
        elif distance(minds.present[key],r['spot'])>3:release(minds,key);continue
        elif r['phase']=='enter':
            r['elapsed']+=dt
            if r['elapsed']>=2:r.update(phase='inside',elapsed=0.,last_clock=r['work']['elapsed'])
        elif r['phase']=='inside':
            elapsed=r['work']['elapsed'];shared_dt=max(0,elapsed-r['last_clock']);r['overlap']+=shared_dt;r['last_clock']=elapsed
            duration=architecture.ROUTINES[r['work']['id']]['duration']
            for index,(at,event) in enumerate(SCORES[r['score']]['events']):
                # An invitation/approach cannot retroactively perform a gesture.
                if index in r['events'] or not elapsed-shared_dt<at*duration<=elapsed:continue
                r['events'].append(index);contact(minds,r,event,at)
            for text in observations(minds,r):
                noticed=r.setdefault('noticed',{});noticed[text]=noticed.get(text,0)+shared_dt
            if r['work'].get('done'):r['phase']='finished'
        # Stay through Cheese's settling phase so actual completion, not an
        # optimistic preview, decides whether the pair remembers this structure session.
    if not plan or not plan.get('architecture_work') or plan.get('paused') or not ready(minds) or architecture.wet(p) or architecture.gusty(p.weather_type):return
    work=plan['architecture_work'];spec=architecture.ROUTINES.get(work.get('id'))
    if not spec or work.get('invitation_checked') or work.get('done') or work['elapsed']>0 or plan['phase'] not in ('prepare','act'):return
    work['invitation_checked']=True
    if minds.structure_helpers:return
    origin=list(plan.get('destination',work['origin']))
    # Reserve a fixed destination by this copy, independent of Cheese's later movement.
    blueprint=architecture.ITEMS[plan['target']]
    # The architecture is much wider than the old props. Walk to its far
    # landing in native world coordinates instead of entering at its center.
    far_edge=blueprint['w']*blueprint['scale']*.62*.58*132/192
    spot=[origin[0]+far_edge,origin[1]]
    if not (6<=spot[0]<=122 and 3<=spot[1]<=36):return
    from engine import playdates
    options=[]
    for key in minds.present:
        if key=='cheese' or departing(minds,key) or minds.now<minds.structure_retry.get(key,0):continue
        if key in minds.playmates or key in minds.ground_helpers or key in minds.textile_helpers or key in minds.creators or key in minds.readers or key in minds.housing or key in minds.gardening or key in minds.furnishings or key in minds.musicians or minds.encounter_for(key) or playdates.active(minds,key):continue
        resident=minds.model.residents[key]
        if resident['energy']<.25 or minds.tasks.get(key,{}).get('action') not in ('observe','share','restore','practice'):continue
        d=distance(minds.present[key],spot)
        if d>24:continue
        score=choose(minds,plan,key)
        if score:
            relationship=resident.get('relationships',{}).get('cheese',{})
            options.append((d-5*resident['traits']['sociability']-2*relationship.get('warmth',0),key,score))
    if not options:return
    _,key,score=min(options);minds.tasks.pop(key,None)
    # Preserve the choreography selection through departures and saves.
    work['duet']=score
    minds.structure_helpers[key]=dict(actor=key,id=plan['target'],instance=plan.get('instance'),destination=origin,spot=spot,
        location=p.location,token=minds.presence_tokens[key],phase='approach',elapsed=0.,started=minds.now,
        score=score,work=work,events=[],overlap=0.,last_clock=work['elapsed'],contexts={k:minds.context(k) for k in ('cheese',key)})
    p._cache=None

def waiting(minds):
    r=active(minds)
    return bool(r and valid(minds,r) and (r['phase']=='enter' or r['phase']=='approach' and minds.now-r['started']<=25))

def complete(minds,plan):
    r=active(minds)
    if not r or not valid(minds,r,plan) or r.get('recorded') or r['phase'] not in ('inside','finished'):return
    work=r['work'];duration=architecture.ROUTINES[work['id']]['duration']
    if not work.get('done') or work.get('interrupted') or r['overlap']<max(5,duration*.45) or distance(minds.present[r['actor']],r['spot'])>3:return
    r['recorded']=True;key=r['actor'];note=SCORES[r['score']]['label']+'.'
    noticed=[text for text,seconds in r.get('noticed',{}).items() if seconds>=2]
    if noticed:note+=' Together: '+ ' / '.join(noticed[-2:])+'.'
    for actor,other in (('cheese',key),(key,'cheese')):
        minds.model.learn(actor,'share',r['contexts'][actor],.25,minds.now,note,other)
        minds.model.bond(actor,other,.18,minds.now,note)
    obj=minds.pond.object_state(plan['target'],plan);history=obj.setdefault('architecture_company',{})
    history[r['score']]=min(9999,history.get(r['score'],0)+1)
    minds.pond.remember('neighbors',minds.model.residents[key]['name']+' and Cheese: '+note,.55,key)

def work_view(minds,work,role='a'):
    out=copy.deepcopy(work);r=active(minds)
    if r and r['work'] is work and valid(minds,r) and (role=='b' or r['phase'] in ('inside','finished')):
        out['company']=dict(id=r['score'],role=role)
    plan=minds.pond.state.get('plan')
    if plan and plan.get('architecture_work') is work:
        progress=plan['elapsed']/plan['duration']
        if role=='a' and plan['phase']=='prepare':out['transition']=dict(phase='enter',elapsed=max(0,min(2,(progress-.15)/.13*2)))
        elif plan['phase']=='settle':out['transition']=dict(phase='exit',elapsed=max(0,min(2,(progress-.9)/.1*2)))
        elif role=='b' and r and r['phase']=='enter':out['transition']=dict(phase='enter',elapsed=r['elapsed'])
    return out

def snapshot(minds):
    result=[]
    for r in minds.structure_helpers.values():
        if not valid(minds,r):continue
        work=work_view(minds,r['work'],'b')
        record={k:copy.deepcopy(r[k]) for k in ('actor','id','instance','destination','spot','phase','elapsed')}
        if work.get('transition',{}).get('phase')=='exit':record.update(phase='exit',elapsed=work['transition']['elapsed'])
        result.append(dict(**record,routine=work))
    return result

def motion(minds,key):
    r=minds.structure_helpers.get(key)
    return dict(target=list(r['spot']),facing=False,phase=r['phase'],gesture='idle') if r else None

def conversation(minds,key):
    r=active(minds,key)
    if not r or not valid(minds,r):return None
    partner=r['actor'] if key=='cheese' else 'cheese';plan=minds.pond.state['plan']
    return dict(with_name=minds.model.residents[partner]['name'],activity=SCORES[r['score']]['label'],
                status='paused' if plan.get('paused') else 'walking over' if r['phase']=='approach' else 'settling in' if r['phase']=='enter' else 'finished the session' if r['phase']=='finished' else 'looking after the structure together now')
