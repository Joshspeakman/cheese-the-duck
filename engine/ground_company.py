"""A ground companion walks to a fixed material and joins its native activity clock.

Reservations are transient. Actual arrival, shared native time and completed work
are required for learning. The partner never duplicates an item use or reward.
"""
import copy
import json
from pathlib import Path
from engine import groundworks, shelters
from engine.visitor_shelters import distance, departing, profile

SCORES=json.loads((Path(__file__).parent/'client/animation/ground-company.json').read_text())

def active(minds,key='cheese'):
    return next(iter(minds.ground_helpers.values()),None) if key=='cheese' else minds.ground_helpers.get(key)

def ready(minds):
    return minds.pond.available() and minds.game.duck.current_action not in ('feed','play','clean','pet','sleep')

def valid(minds,r,plan=None):
    p=minds.pond;plan=plan or p.state.get('plan')
    pos=minds.game.renderer.duck_pos
    return bool(plan and plan.get('ground_work') is r['work'] and groundworks.valid(p,plan)
                and abs(pos.x-r['destination'][0])+abs(pos.y-r['destination'][1])<=3
                and r['actor'] in minds.present and minds.presence_tokens.get(r['actor'])==r['token']
                and (r['phase']=='approach' or distance(minds.present[r['actor']],r['spot'])<=3)
                and r['location']==p.location and not departing(minds,r['actor'])
                and r['actor'] not in minds.housing and not r['work'].get('withdrawal') and not r['work'].get('interrupted') and not shelters.adverse(p.weather_type))

def choose(minds,plan,key):
    item=plan['target'];p=groundworks.ITEMS[item];work=plan['ground_work'];kind=p['type'];core=work['id']
    if core in ('wet_footing','frost_edge'):return None
    age=minds.game.duck.growth_stage;stage,species=profile(minds,key);resident=minds.model.residents[key]
    if species=='butterfly':return 'hover_observer'
    if p['style']=='stepping':return 'stone_spotter'
    if p['style']=='winding':return 'winding_guide'
    if kind=='lava':return 'lava_edge_pair'
    if kind=='cloud':return 'cloud_shapes'
    if kind=='rainbow':return 'rainbow_colors'
    if kind=='galaxy':return 'galaxy_patient' if resident['traits']['patience']>=.65 else 'galaxy_watch'
    if kind=='ice':return 'ice_bubbles'
    if core in ('seam_brush','marble_buff','glass_wipe'):return 'joint_sweep'
    if core=='sand_rake':return 'sand_rake_pair'
    if core=='sand_smooth':return 'sand_smooth_pair'
    if core=='sand_tracks':return 'sand_track_compare'
    if core=='snow_crunch':return 'snow_prints'
    if core=='snow_crystal':return 'snow_crystal_watch'
    if core in ('young_footing','elder_footing') or age in ('hatchling','duckling','elder','legendary') or stage=='duckling' or resident['energy']<.45 or resident['mood']<.25:return 'careful_company'
    if core=='night_surface' or minds.pond.hour<6 or minds.pond.hour>=19:return 'night_edge'
    if core=='board_knock':return 'board_echo'
    if kind in ('wood','plank'):return 'grain_compare'
    if kind=='glass':return 'glass_angles'
    if p['style']=='checker':return 'checker_echo'
    if p['style']=='mosaic':return 'mosaic_story' if resident['traits']['confidence']>=.55 else 'mosaic_detail'
    return {'cobbles':'cobble_compare','pebbles':'pebble_echo','slate':'slate_reader','marble':'marble_branch','sand':'sand_track_compare','snow':'snow_crystal_watch'}[p['style']]

def controls(work,score):
    return groundworks.sample(work,SCORES[score]['track'],dict(u=1.12,v=1.06,press=0.,contact=0.))

def contact(minds,r,event,at):
    """A present helper makes the corresponding mark at the actual native pose."""
    obj=minds.pond.object_state(r['id'],r.get('instance'));s=groundworks.state(r['id'],obj)
    work={**r['work'],'elapsed':at*groundworks.ROUTINES[r['work']['id']]['duration']};pose=controls(work,r['score'])
    stage,species=profile(minds,r['actor'])
    if species=='butterfly':return
    if event=='foot':groundworks.footprint(r['id'],obj,pose['u'],pose['v'],r['actor'],species,stage=='duckling')
    elif event=='furrow':s['furrows']=(s['furrows']+[dict(u0=.64,u1=.86,v=groundworks.clamp(pose['v']-.12),life=1.,by=r['actor'])])[-6:]
    elif event=='clean':obj['dirt']=max(0.,obj.get('dirt',0)-.05)
    elif event=='tap':s['taps']=min(9999,s['taps']+1)
    elif event=='smooth':
        s['tracks']=[t for t in s['tracks'] if t['u']<.6]
        s['furrows']=[t for t in s['furrows'] if t['u1']<.6]
    minds.pond._cache=None

def release(minds,key):
    if minds.ground_helpers.pop(key,None):
        minds.ground_retry[key]=minds.now+100
        minds.pond._cache=None

def tick(minds,dt):
    p=minds.pond;plan=p.state.get('plan')
    for key,r in list(minds.ground_helpers.items()):
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
            duration=groundworks.ROUTINES[r['work']['id']]['duration']
            for index,(at,event) in enumerate(SCORES[r['score']]['events']):
                # An invitation/approach cannot retroactively perform a gesture.
                if index in r['events'] or not elapsed-shared_dt<at*duration<=elapsed:continue
                r['events'].append(index);contact(minds,r,event,at)
            visible=groundworks.conversation(p,plan) or {};observations=[]
            obj=p.object_state(r['id'],r.get('instance'));surface=obj['ground'];kind=groundworks.ITEMS[r['id']]['type']
            fresh=[t for t in surface['tracks'] if t not in r['initial_tracks']]
            authors={t.get('by','cheese') for t in fresh}
            if 'cheese' in authors and key in authors:observations.append('Compared their two fresh footprint trails in the '+visible.get('material','ground'))
            elif 'cheese' in authors:observations.append('Watched Cheese leave fresh impressions in the '+visible.get('material','ground'))
            if key in authors:
                shape=next(t.get('shape','webbed') for t in fresh if t.get('by')==key)
                observations.append('Left '+shape+' prints beside Cheese')
            events=[SCORES[r['score']]['events'][i][1] for i in r['events']]
            if 'furrow' in events and any(t.get('by')=='cheese' for t in surface['furrows']):observations.append('Drew two separate sets of sand furrows')
            if 'tap' in events:observations.append('Answered the taps from the opposite end of the wood')
            if 'clean' in events:observations.append('Brushed grit off their own side of the surface')
            if kind=='lava':observations.append('Watched the molten ribbons together from outside the stone lip')
            if groundworks.ITEMS[r['id']]['style']=='mosaic':observations.append('Looked at the fish medallion and its tiny chips')
            for text in observations:
                noticed=r.setdefault('noticed',{});noticed[text]=noticed.get(text,0)+shared_dt
            if r['work'].get('done'):r['phase']='finished'
        # Stay through Cheese's settling phase so actual completion, not an
        # optimistic preview, decides whether the pair remembers this ground session.
    if not plan or not plan.get('ground_work') or plan.get('paused') or not ready(minds) or shelters.adverse(p.weather_type):return
    work=plan['ground_work'];spec=groundworks.ROUTINES.get(work.get('id'))
    if not spec or work.get('invitation_checked') or work.get('done') or work['elapsed']>0 or plan['phase'] not in ('prepare','act'):return
    work['invitation_checked']=True
    if minds.ground_helpers:return
    origin=list(plan.get('destination',work['origin']))
    # A portable prop is laid down seven native cells beside Cheese. Its companion
    # reserves the far edge, never a destination relative to Cheese's next move.
    center=[origin[0]+(0 if plan.get('instance') else 7),origin[1]]
    spot=[center[0]+9,center[1]]
    if not (6<=spot[0]<=122 and 3<=spot[1]<=36):return
    from engine import playdates
    options=[]
    for key in minds.present:
        if key=='cheese' or departing(minds,key) or minds.now<minds.ground_retry.get(key,0):continue
        if key in minds.carnival_guests or key in minds.nest_helpers or key in minds.playmates or key in minds.structure_helpers or key in minds.textile_helpers or key in minds.creators or key in minds.readers or key in minds.housing or key in minds.gardening or key in minds.furnishings or key in minds.musicians or minds.encounter_for(key) or playdates.active(minds,key):continue
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
    # Preserve the leader's lane through a departure or save; a vanished helper
    # must never move Cheese back to the old center of a partly drawn mark.
    work['duet']=score
    minds.ground_helpers[key]=dict(actor=key,id=plan['target'],instance=plan.get('instance'),destination=origin,spot=spot,
        location=p.location,token=minds.presence_tokens[key],phase='approach',elapsed=0.,started=minds.now,
        score=score,work=work,initial_tracks=copy.deepcopy(p.object_state(plan['target'],plan)['ground']['tracks']),events=[],overlap=0.,last_clock=work['elapsed'],contexts={k:minds.context(k) for k in ('cheese',key)})
    p._cache=None

def waiting(minds):
    r=active(minds)
    return bool(r and valid(minds,r) and (r['phase']=='enter' or r['phase']=='approach' and minds.now-r['started']<=25))

def complete(minds,plan):
    r=active(minds)
    if not r or not valid(minds,r,plan) or r.get('recorded') or r['phase'] not in ('inside','finished'):return
    work=r['work'];duration=groundworks.ROUTINES[work['id']]['duration']
    if not work.get('done') or work.get('interrupted') or r['overlap']<max(5,duration*.45) or distance(minds.present[r['actor']],r['spot'])>3:return
    r['recorded']=True;key=r['actor'];note=SCORES[r['score']]['label']+'.'
    noticed=[text for text,seconds in r.get('noticed',{}).items() if seconds>=2]
    if noticed:note+=' Together: '+ ' / '.join(noticed[-2:])+'.'
    for actor,other in (('cheese',key),(key,'cheese')):
        minds.model.learn(actor,'share',r['contexts'][actor],.25,minds.now,note,other)
        minds.model.bond(actor,other,.18,minds.now,note)
    obj=minds.pond.object_state(plan['target'],plan);history=obj.setdefault('ground_company',{})
    history[r['score']]=min(9999,history.get(r['score'],0)+1)
    minds.pond.remember('neighbors',minds.model.residents[key]['name']+' and Cheese: '+note,.55,key)

def work_view(minds,work,role='a'):
    out=copy.deepcopy(work);r=active(minds)
    if r and r['work'] is work and valid(minds,r) and (role=='b' or r['phase'] in ('inside','finished')):
        out['company']=dict(id=r['score'],role=role)
    plan=minds.pond.state.get('plan')
    if plan and plan.get('ground_work') is work:
        progress=plan['elapsed']/plan['duration']
        if role=='a' and plan['phase']=='prepare':out['transition']=dict(phase='enter',elapsed=max(0,min(2,(progress-.15)/.13*2)))
        elif plan['phase']=='settle':out['transition']=dict(phase='exit',elapsed=max(0,min(2,(progress-.9)/.1*2)))
        elif role=='b' and r and r['phase']=='enter':out['transition']=dict(phase='enter',elapsed=r['elapsed'])
    return out

def snapshot(minds):
    result=[]
    for r in minds.ground_helpers.values():
        if not valid(minds,r):continue
        work=work_view(minds,r['work'],'b')
        record={k:copy.deepcopy(r[k]) for k in ('actor','id','instance','destination','spot','phase','elapsed')}
        if work.get('transition',{}).get('phase')=='exit':record.update(phase='exit',elapsed=work['transition']['elapsed'])
        result.append(dict(**record,routine=work))
    return result

def motion(minds,key):
    r=minds.ground_helpers.get(key)
    return dict(target=list(r['spot']),facing=False,phase=r['phase'],gesture='idle') if r else None

def conversation(minds,key):
    r=active(minds,key)
    if not r or not valid(minds,r):return None
    partner=r['actor'] if key=='cheese' else 'cheese';plan=minds.pond.state['plan']
    return dict(with_name=minds.model.residents[partner]['name'],activity=SCORES[r['score']]['label'],
                status='paused' if plan.get('paused') else 'walking over' if r['phase']=='approach' else 'settling in' if r['phase']=='enter' else 'finished the session' if r['phase']=='finished' else 'exploring the surface together now')
