"""Plaything companions arrive independently and share the native work clock.

Reservations are transient. Actual arrival, shared native time and completed work
are required for learning. The partner never duplicates an item use or reward.
"""
import copy
import json
from pathlib import Path
from engine import playkit
from engine.visitor_shelters import distance, departing, profile

SCORES=json.loads((Path(__file__).parent/'client/animation/playkit-company.json').read_text())

def active(minds,key='cheese'):
    return next(iter(minds.playmates.values()),None) if key=='cheese' else minds.playmates.get(key)

def ready(minds):
    return minds.pond.available() and minds.game.duck.current_action not in ('feed','play','clean','pet','sleep')

def valid(minds,r,plan=None):
    p=minds.pond;plan=plan or p.state.get('plan')
    pos=minds.game.renderer.duck_pos
    return bool(plan and plan.get('playkit_work') is r['work'] and playkit.valid(p,plan)
                and abs(pos.x-r['destination'][0])+abs(pos.y-r['destination'][1])<=3
                and r['actor'] in minds.present and minds.presence_tokens.get(r['actor'])==r['token']
                and (r['phase']=='approach' or distance(minds.present[r['actor']],r['spot'])<=3)
                and r['location']==p.location and not departing(minds,r['actor'])
                and r['actor'] not in minds.housing and not r['work'].get('withdrawal') and not r['work'].get('interrupted') and not playkit.wet(p) and not playkit.gusty(p))

def choose(minds,plan,key):
    work=plan['playkit_work'];core=work['id']
    if core.endswith('_pack'):return None
    age=minds.game.duck.growth_stage;stage,species=profile(minds,key);resident=minds.model.residents[key]
    if species=='butterfly':return 'hover_company'
    if stage=='duckling' or age in ('hatchling','duckling'):return 'young_company'
    if minds.pond.hour<6 or minds.pond.hour>=20:return 'night_company'
    if core.endswith('_gentle') or age in ('elder','legendary') or resident['energy']<.45 or resident['mood']<.25:return 'quiet_company'
    return {'disc_roll':'disc_finish','disc_wobble':'disc_wobble','disc_rim':'disc_polish',
      'rope_steps':'rope_stepwatch','rope_skip':'rope_count','rope_coil':'rope_hold','rope_uncoil':'rope_hold',
      'yoyo_drop':'yoyo_sleep','yoyo_walk':'yoyo_lane','yoyo_loops':'yoyo_cheer',
      'bubbler_start':'bubbler_drift','bubbler_stop':'quiet_company','bubbler_clean':'bubbler_clean',
      'wand_breath':'wand_bubbles','wand_giant':'wand_giant','wand_rinse':'wand_rinse',
      'pinwheel_turn':'pinwheel_count','pinwheel_watch':'pinwheel_count','pinwheel_smooth':'pinwheel_folds',
      'boat_push':'boat_finish','boat_tack':'boat_finish','boat_sail':'boat_rigging','boat_keel':'boat_keel',
      'board_balance':'board_spotter','board_steps':'board_spotter','board_wax':'board_waxpair'}.get(core)

def controls(work,score):
    return playkit.sample(work,SCORES[score]['track'],dict(u=1.08,v=0.,contact=0.))

def contact(minds,r,event,at):
    obj=minds.pond.object_state(r['id'],r.get('instance'));s=playkit.state(r['id'],obj)
    _,species=profile(minds,r['actor'])
    if species=='butterfly':return
    if event in ('clean','wax'):
        obj['dirt']=max(0.,obj.get('dirt',0)-.04)
        field='cleanings' if event=='clean' else 'waxes';s[field]=min(9999,s[field]+1)
    minds.pond._cache=None

def observations(minds,r):
    p=minds.pond;obj=p.object_state(r['id'],r.get('instance'));s=obj['playkit'];kind=playkit.ITEMS[r['id']]['type'];notes=[]
    events=[SCORES[r['score']]['events'][i][1] for i in r['events']]
    if 'clean' in events:notes.append('Brushed the far edge while Cheese tended the near side')
    if 'wax' in events:notes.append('Waxed the opposite rail of the board on the bank')
    if 'hold' in events:notes.append('Held the far '+('rope handle' if kind=='rope' else 'rigging cleat'))
    if kind in ('bubbler','wand') and s['bubbles']:notes.append('Watched real soap bubbles drifting past')
    elif kind=='bubbler':notes.append('Saw the bubble wheel '+('running' if s['power']>.5 else 'switched off'))
    elif kind=='pinwheel':notes.append('Watched the folded vanes '+('turn in the wind' if s['speed']>.1 else 'rest in still air'))
    elif kind=='boat':notes.append('Watched the little boat on the grass with its sail '+('open' if s['sail']>.9 else 'folded' if s['sail']<.1 else 'partway open'))
    elif kind=='rope':notes.append('Saw the braid '+('gathered into a coil' if s['coil']>.9 else 'laid out in low loops'))
    elif kind=='yoyo' and s['drop']>.8:notes.append('Followed the yo-yo down near the ground')
    elif kind=='disc' and s['travel']>.8:notes.append('Watched the disc reach the far end of its short rolling lane')
    elif kind=='board':notes.append('Practised beside the board on the bank; did not go surfing')
    return notes

def release(minds,key):
    if minds.playmates.pop(key,None):
        minds.playmate_retry[key]=minds.now+100
        minds.pond._cache=None

def tick(minds,dt):
    p=minds.pond;plan=p.state.get('plan')
    for key,r in list(minds.playmates.items()):
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
            duration=playkit.ROUTINES[r['work']['id']]['duration']
            for index,(at,event) in enumerate(SCORES[r['score']]['events']):
                # An invitation/approach cannot retroactively perform a gesture.
                if index in r['events'] or not elapsed-shared_dt<at*duration<=elapsed:continue
                r['events'].append(index);contact(minds,r,event,at)
            for text in observations(minds,r):
                noticed=r.setdefault('noticed',{});noticed[text]=noticed.get(text,0)+shared_dt
            if r['work'].get('done'):r['phase']='finished'
        # Stay through Cheese's settling phase so actual completion, not an
        # optimistic preview, decides whether the pair remembers this play session.
    if not plan or not plan.get('playkit_work') or plan.get('paused') or not ready(minds) or playkit.wet(p) or playkit.gusty(p):return
    work=plan['playkit_work'];spec=playkit.ROUTINES.get(work.get('id'))
    if not spec or work.get('invitation_checked') or work.get('done') or work['elapsed']>0 or plan['phase'] not in ('prepare','act'):return
    work['invitation_checked']=True
    if minds.playmates:return
    origin=list(plan.get('destination',work['origin']))
    # Reserve a fixed destination by this copy, independent of Cheese's later movement.
    blueprint=playkit.ITEMS[plan['target']]
    # Reserve the far side of this toy in native world coordinates.
    # This remains fixed when Cheese moves or the toy rolls during play.
    far_edge=blueprint['w']*blueprint['scale']*.62*.58*132/192
    spot=[origin[0]+far_edge,origin[1]]
    if not (6<=spot[0]<=122 and 3<=spot[1]<=36):return
    from engine import playdates
    options=[]
    for key in minds.present:
        if key=='cheese' or departing(minds,key) or minds.now<minds.playmate_retry.get(key,0):continue
        if key in minds.structure_helpers or key in minds.ground_helpers or key in minds.textile_helpers or key in minds.creators or key in minds.readers or key in minds.housing or key in minds.gardening or key in minds.furnishings or key in minds.musicians or minds.encounter_for(key) or playdates.active(minds,key):continue
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
    minds.playmates[key]=dict(actor=key,id=plan['target'],instance=plan.get('instance'),destination=origin,spot=spot,
        location=p.location,token=minds.presence_tokens[key],phase='approach',elapsed=0.,started=minds.now,
        score=score,work=work,events=[],overlap=0.,last_clock=work['elapsed'],contexts={k:minds.context(k) for k in ('cheese',key)})
    p._cache=None

def waiting(minds):
    r=active(minds)
    return bool(r and valid(minds,r) and (r['phase']=='enter' or r['phase']=='approach' and minds.now-r['started']<=25))

def complete(minds,plan):
    r=active(minds)
    if not r or not valid(minds,r,plan) or r.get('recorded') or r['phase'] not in ('inside','finished'):return
    work=r['work'];duration=playkit.ROUTINES[work['id']]['duration']
    if not work.get('done') or work.get('interrupted') or r['overlap']<max(5,duration*.45) or distance(minds.present[r['actor']],r['spot'])>3:return
    r['recorded']=True;key=r['actor'];note=SCORES[r['score']]['label']+'.'
    noticed=[text for text,seconds in r.get('noticed',{}).items() if seconds>=2]
    if noticed:note+=' Together: '+ ' / '.join(noticed[-2:])+'.'
    for actor,other in (('cheese',key),(key,'cheese')):
        minds.model.learn(actor,'share',r['contexts'][actor],.25,minds.now,note,other)
        minds.model.bond(actor,other,.18,minds.now,note)
    obj=minds.pond.object_state(plan['target'],plan);history=obj.setdefault('playkit_company',{})
    history[r['score']]=min(9999,history.get(r['score'],0)+1)
    minds.pond.remember('neighbors',minds.model.residents[key]['name']+' and Cheese: '+note,.55,key)

def work_view(minds,work,role='a'):
    out=copy.deepcopy(work);r=active(minds)
    if r and r['work'] is work and valid(minds,r) and (role=='b' or r['phase'] in ('inside','finished')):
        out['company']=dict(id=r['score'],role=role)
    plan=minds.pond.state.get('plan')
    if plan and plan.get('playkit_work') is work:
        progress=plan['elapsed']/plan['duration']
        if role=='a' and plan['phase']=='prepare':out['transition']=dict(phase='enter',elapsed=max(0,min(2,(progress-.15)/.13*2)))
        elif plan['phase']=='settle':out['transition']=dict(phase='exit',elapsed=max(0,min(2,(progress-.9)/.1*2)))
        elif role=='b' and r and r['phase']=='enter':out['transition']=dict(phase='enter',elapsed=r['elapsed'])
    return out

def snapshot(minds):
    result=[]
    for r in minds.playmates.values():
        if not valid(minds,r):continue
        work=work_view(minds,r['work'],'b')
        record={k:copy.deepcopy(r[k]) for k in ('actor','id','instance','destination','spot','phase','elapsed')}
        if work.get('transition',{}).get('phase')=='exit':record.update(phase='exit',elapsed=work['transition']['elapsed'])
        result.append(dict(**record,routine=work))
    return result

def motion(minds,key):
    r=minds.playmates.get(key)
    return dict(target=list(r['spot']),facing=False,phase=r['phase'],gesture='idle') if r else None

def conversation(minds,key):
    r=active(minds,key)
    if not r or not valid(minds,r):return None
    partner=r['actor'] if key=='cheese' else 'cheese';plan=minds.pond.state['plan']
    return dict(with_name=minds.model.residents[partner]['name'],activity=SCORES[r['score']]['label'],
                status='paused' if plan.get('paused') else 'walking over' if r['phase']=='approach' else 'settling in' if r['phase']=='enter' else 'finished the session' if r['phase']=='finished' else 'looking after the plaything together now')
