"""Actual regular/rare/story arrivals, shared structure work and interrupted memories."""
import os,sys,tempfile,json,copy,random,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-structure-company-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,architecture,architecture_company as company
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.habitat import PlacedItem
from world.building import Structure,StructureStatus
from world.atmosphere import Weather,WeatherType,Season,VISITORS
from world.friends import visitor_animator
from world.guest_cast import PROFILES
from audio.sound import sound_engine
sys.stdout=host.WIRE;random.seed(45);checks=[];frames=[];clock=0.
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;b=p.minds;p.state['auto']=False;b.model.state['next_social']=1e9
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    friend=g.friends.generate_new_friend()

    def advance(n=1,capture=False,move=True):
        global clock
        for _ in range(n):
            clock+=.1;p.state['elapsed']+=.1;pos=g.renderer.duck_pos;pos._state_start_time-=.1;pos.update(.1);p._activity(.1)
            if g.friends.current_visit and move:
                visitor_animator._mind_motion=b.motion(g.friends.current_visit.friend_id);visitor_animator.update(clock,pos.x,pos.y)
            for item,obj,outside in __import__('engine.object_history',fromlist=['records']).records(p):architecture.update(p,item,obj,.1,outside,.35,p.weather_type)
            g.guest_motion.tick(g,clock);g.story_motion.tick(g,clock);b.tick()
            if capture and int(clock*10)%10==0:frames.append(snapshot(g,g.renderer))
    def reset(item='gate',kind='regular',stage='adult'):
        g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
        g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
        p.cancel();b.structure_helpers.clear();b.structure_retry.clear();b.ground_helpers.clear();b.ground_retry.clear();b.textile_helpers.clear();b.textile_retry.clear();b.readers.clear();b.creators.clear();b.tasks.clear();b.housing.clear();b.furnishings.clear();b.gardening.clear();b.musicians.clear();b.coactivities.clear()
        g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None;g.story_motion.actor=None;g.guest_motion.actor=None
        g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=stage;g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
        g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        if item=='stone_path':g.building.structures=[Structure(item,(8,6),status=StructureStatus.COMPLETE)]
        else:g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,10,6)]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=48;pos.y=21
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(temperature=18,wind=.2);p.state['cooldowns']={}
        placement=next((a for a in p.placements if a.item_id==item),None);iid=placement.instance if placement else None;obj=p.object_state(item,iid);obj['last_use']=-1000;obj['uses']=0;obj['dirt']=0;obj['wetness']=0;obj['architecture'].update(**architecture.CONTROLS,phase=0,speed=0,crank=0,taps=0,cleanings=0,season='spring');obj['architecture_routines']={}
        ok,msg=p.start('item',item,instance=iid);check(ok,item+' starts: '+msg);plan=p.state['plan'];dest=plan.get('destination',plan['architecture_work']['origin']);blueprint=architecture.ITEMS[item];start=[dest[0]+blueprint['w']*blueprint['scale']*.62*.58*132/192+8,dest[1]]
        if kind=='regular':
            g.friends.start_visit(friend.id);visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False
            visitor_animator._position_x=start[0];visitor_animator._position_y=start[1];visitor_animator._target_x=start[0];visitor_animator._target_y=start[1];visitor_animator._rest_until=clock+30;visitor_animator._last_move_time=clock;key=friend.id
        elif kind!='story':
            key='friendly_goose' if kind=='rare' else kind;g.atmosphere.current_visitor=(VISITORS[key],datetime.now().isoformat());g.guest_motion.tick(g,clock);g.guest_motion.actor.update(x=start[0],y=start[1])
        else:
            key='story:pip';p.state['story']={'id':'lost_duckling','step':0,'started':0};g.story_motion.tick(g,clock);g.story_motion.actor.update(x=start[0],y=start[1])
        b.sync();b.model.residents[key]['energy']=.9;b.model.residents[key]['mood']=.7;b.tasks[key]=dict(action='observe',until=b.now+100,context=b.context(key))
        return plan,key,obj
    def arrive(capture=False):
        for _ in range(1200):
            advance(capture=capture)
            r=company.active(b)
            if r and r['phase']=='inside':return r
            if not p.state['plan']:break
        raise AssertionError('friend did not arrive to help')
    def finish(capture=False):
        for _ in range(1400):
            advance(capture=capture)
            if not p.state['plan'] and not b.structure_helpers:return
        raise AssertionError('structure work did not finish')
    payload=[dict(id=s['preview'],elapsed=architecture.ROUTINES[s['preview']]['duration']*i/100,start=architecture.CONTROLS,duet=key,company=dict(id=key,role='b')) for key,s in company.SCORES.items() for i in range(101)]
    script="import {architecturePose} from './engine/client/architecture-routines.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(w=>{let p=architecturePose(w);return {u:p.actorU,v:p.actorV,contact:p.contact,open:p.open,bucket:p.bucket}})))"
    samples=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],input=json.dumps(payload).encode(),cwd=ROOT))
    check(all(all(abs(a[k]-v)<1e-9 for k,v in company.controls(w,w['duet']).items()) and a['open']==architecture.controls(w)['open'] and a['bucket']==architecture.controls(w)['bucket'] for w,a in zip(payload,samples)),str(len(payload))+' native and renderer samples agree without duplicate mechanism control')
    for index,(score,spec) in enumerate(company.SCORES.items()):
        kind='butterfly_fairy' if score=='hover_visit' else 'story' if score=='young_company' else ('regular','rare')[index%2]
        stage='elder' if score=='elder_rest' else 'adult'
        plan,key,obj=reset(spec['item'],kind,stage);work=plan['architecture_work'];work.update(id=spec['preview'],label=architecture.ROUTINES[spec['preview']]['label'])
        b.model.residents[key]['traits']['confidence']=.9
        if score=='night_watch':p.hour=23
        if score=='winter_vines':p.season='winter';obj['architecture']['season']='winter'
        if score=='gate_clear':work['start']['open']=obj['architecture']['open']=1.
        if spec['tool']=='brush':obj['dirt']=.8
        before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)};uses=obj['uses'];positions=set();r=None;waiting_checked=False;approach_checked=False
        for _ in range(1000):
            advance(capture=True);positions.add(tuple(round(v,3) for v in b.present[key]));r=company.active(b)
            if r and r['phase'] in ('approach','enter') and plan['phase']=='act' and not waiting_checked:check(work['elapsed']==0,score+' waits for the arriving partner');waiting_checked=True
            if r and r['phase']=='approach' and not approach_checked:
                approach_checked=True;facts=json.loads(b.prompt(key,'What are you looking at?')[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1]);check('garden_structure' not in facts,score+' withholds structure details before arrival')
            if r and r['phase']=='inside':break
        check(bool(r and r['phase']=='inside') and len(positions)>3,score+' has an independent real arrival: '+str(dict(phase=r and r['phase'],positions=len(positions),actor=b.present.get(key),spot=r and r['spot'],clock=work['elapsed'],plan=plan['phase'])))
        check(r['score']==score,score+' selected from the real structure and context: '+r['score'])
        check(all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),score+' arrival alone grants no shared learning')
        advance(40,capture=True);owner=p._plan_view()['architecture_work'];guest=company.snapshot(b)[0]['routine']
        check(owner['elapsed']==guest['elapsed'] and owner['company']['role']=='a' and guest['company']['role']=='b',score+' shares one clock with complementary roles')
        cached=p.snapshot();advance();fresh=p.snapshot();check(fresh['minds']['structure_helpers'][0]['routine']['elapsed']>cached['minds']['structure_helpers'][0]['routine']['elapsed'],score+' helper clock refreshes through cached ecology snapshots')
        finish(capture=True)
        check(obj['uses']==uses+1,score+' completes exactly one original use')
        check(all(b.model.residents[k]['counts']['share']==v+1 for k,v in before.items()),score+' both residents learn once after actual completion')
        check(obj.get('architecture_company',{}).get(score)==1,score+' records history on the selected copy')
        if score=='bridge_echo':check(obj['architecture']['taps']==3,'three actual landing contacts retain their count')
        if score=='mailbox_watch':check(any('empty mail compartment' in m['text'] for m in b.model.residents[key]['memories']),'visitor remembers the empty compartment, not an invented delivery')
        if score=='castle_history':check(any('MDCC / Q' in m['text'] for m in b.model.residents[key]['memories']),'visitor remembers the visible foundation carving')
        if score=='winter_vines':check(any('bare winter stems' in m['text'] for m in b.model.residents[key]['memories']),'visitor remembers the actual winter foliage')
        after={k:b.model.residents[k]['counts']['share'] for k in before};company.complete(b,plan)
        check(all(b.model.residents[k]['counts']['share']==v for k,v in after.items()),score+' completion cannot repeat')
    for stage in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        plan,key,obj=reset('picket_fence',stage=stage);r=arrive(capture=stage in ('hatchling','elder'));expected='young_company' if stage in ('hatchling','duckling') else 'elder_rest' if stage in ('elder','legendary') else 'picket_compare'
        check(r['score']==expected,stage+' has suitable shared work');finish()
    plan,key,obj=reset('gate');b.model.residents[key]['traits']['confidence']=.1;check(company.choose(b,plan,key)=='gate_clear','less confident visitors stay clear of a moving gate')
    b.model.residents[key]['mood']=.1;check(company.choose(b,plan,key)=='elder_rest','low mood chooses undemanding company')
    b.model.residents[key]['mood']=.7;b.model.residents[key]['energy']=.3;check(company.choose(b,plan,key)=='elder_rest','low energy chooses restful company')
    p.cancel();g.duck.growth_stage='egg';check(not p.start('item','gate')[0],'eggs cannot operate a gate');g.duck.growth_stage='adult'
    plan,key,obj=reset('gate');r=arrive();advance(90);before=copy.deepcopy(obj);clock_before=plan['architecture_work']['elapsed'];overlap=r['overlap'];plan['paused']=True;advance(30)
    check(obj==before and plan['architecture_work']['elapsed']==clock_before and r['overlap']==overlap,'pauses freeze both performers and gate controls')
    facts=json.loads(b.prompt(key,'What is happening?')[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1]);check(facts['shared_activity']['status']=='paused' and 'gate_open_fraction' in facts['garden_structure'],'paused speech knows the real gate position')
    visitor_animator._position_x+=10;b.sync();check(company.snapshot(b)==[],'displaced helper is never snapped back to the gate');b.tick();check(not b.structure_helpers,'displacement releases the reservation')
    plan,key,obj=reset('bridge');before=b.model.residents[key]['counts']['share'];advance(500,move=False);check(not b.structure_helpers and plan['architecture_work']['elapsed']>0,'unreachable visitor times out and Cheese continues alone');finish();check(b.model.residents[key]['counts']['share']==before,'missed invitation cannot grant shared learning')
    for reason in ('depart','new_visit','storm','rain','care','move','replace'):
        plan,key,obj=reset('gate');r=arrive();advance(40);before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
        if reason=='depart':g.friends.current_visit=None
        elif reason=='new_visit':g.friends.current_visit.started_at='replacement-visit'
        elif reason in ('storm','rain'):p.weather_type='stormy' if reason=='storm' else 'rainy'
        elif reason=='care':g.duck.current_action='feed'
        elif reason=='move':g.habitat.placed_items[0].x+=3;p.sync()
        else:g.habitat.placed_items=[PlacedItem('gate',10,6)];p.sync()
        advance(3);check(not b.structure_helpers and all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),reason+' cannot claim a shared completion')
    # Only the selected rail is cleaned, at actual helper contact.
    plan,key,obj=reset('picket_fence');g.habitat.placed_items[0].x=6;g.habitat.placed_items.append(PlacedItem('picket_fence',14,6));p.sync();p.cancel();p.state['cooldowns']={};obj['last_use']=-1000;p.start('item','picket_fence',instance=g.habitat.placed_items[0].instance_id);plan=p.state['plan'];plan['architecture_work']['id']='picket_brush';obj['dirt']=.8;other=p.object_state('picket_fence',g.habitat.placed_items[1].instance_id);other['dirt']=.8
    visitor_animator._position_x=plan['destination'][0]+19;visitor_animator._position_y=plan['destination'][1];b.sync();b.tasks[key]=dict(action='observe',until=b.now+100,context=b.context(key));r=arrive();before=b.model.residents[key]['counts']['share'];uses=obj['uses']
    while not r['events']:advance()
    check(abs(obj['dirt']-.76)<1e-9 and other['dirt']==.8,'helper brush alters only its physical copy at contact')
    p.cancel();advance(3);check(abs(obj['dirt']-.76)<1e-9 and obj['uses']==uses and b.model.residents[key]['counts']['share']==before,'cancel keeps real cleaning but grants no completion')
    plan,key,obj=reset('gate');r=arrive();advance(110);before=copy.deepcopy(obj['architecture']);plan['paused']=True;g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;b=p.minds;p.sync()
    loaded=p.object_state('gate',plan['instance']);check(not b.structure_helpers and p.state['plan']['paused'] and loaded['architecture']==before,'full save preserves gate state but discards stale helper reservations')
    p.state['plan']['paused']=False;advance(10);check(not b.structure_helpers,'resume does not invent a second invitation');finish()
    for item in architecture.ITEMS:
        plan,key,obj=reset(item)
        for cast,profile in PROFILES.items():
            b.model.ensure('cast:'+cast,profile.get('name',cast),profile)
            check(company.choose(b,plan,'cast:'+cast) in company.SCORES,cast+' has an appropriate role around '+item)
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True);(out/'architecture-company-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),frames=len(frames),scores=len(company.SCORES));(out/'architecture-company-native.json').write_text(json.dumps(dict(**result,assertions=checks),indent=2));print(json.dumps(result))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
