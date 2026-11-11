"""Actual regular/rare/story arrivals, shared plaything work and interrupted memories."""
import os,sys,tempfile,json,copy,random,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-plaything-company-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,playkit,playkit_company as company
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
            for item,obj,outside in __import__('engine.object_history',fromlist=['records']).records(p):playkit.update(p,item,obj,.1,outside,.35,p.weather_type)
            g.guest_motion.tick(g,clock);g.story_motion.tick(g,clock);b.tick()
            if capture and int(clock*10)%10==0:frames.append(snapshot(g,g.renderer))
    def reset(item='frisbee',kind='regular',stage='adult'):
        g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
        g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
        p.cancel();b.structure_helpers.clear();b.playmates.clear();b.playmate_retry.clear();b.ground_helpers.clear();b.ground_retry.clear();b.textile_helpers.clear();b.textile_retry.clear();b.readers.clear();b.creators.clear();b.tasks.clear();b.housing.clear();b.furnishings.clear();b.gardening.clear();b.musicians.clear();b.coactivities.clear()
        g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None
        g.story_motion.actor=g.story_motion.token=None;g.guest_motion.actor=g.guest_motion.token=None
        g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=stage;g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
        g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        g.inventory.items=[]
        if item in ('bubble_wand','tiny_boat'):g.inventory.add_item(item)
        elif item=='surfboard':g.materials.add_material(item,1)
        else:g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,10,6)]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=48;pos.y=21
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(temperature=18,wind=.2);p.state['cooldowns']={}
        placement=next((a for a in p.placements if a.item_id==item),None);iid=placement.instance if placement else None;obj=p.object_state(item,iid);obj['last_use']=-1000;obj['uses']=0;obj['dirt']=0;obj['wetness']=0;obj['playkit']={};playkit.state(item,obj);obj['playkit_routines']={};obj['playkit_company']={}
        ok,msg=p.start('item',item,instance=iid);check(ok,item+' starts: '+msg);plan=p.state['plan'];dest=plan.get('destination',plan['playkit_work']['origin']);blueprint=playkit.ITEMS[item];start=[dest[0]+blueprint['w']*blueprint['scale']*.62*.58*132/192+8,dest[1]]
        if kind=='regular' or kind.startswith('friend:'):
            selected=friend
            if kind.startswith('friend:'):
                selected=copy.deepcopy(friend);selected.id=kind;selected.name=PROFILES[kind]['name'];g.friends.friends[kind]=selected
            g.friends.start_visit(selected.id);visitor_animator._friend_name=selected.name;visitor_animator._is_leaving=False
            visitor_animator._position_x=start[0];visitor_animator._position_y=start[1];visitor_animator._target_x=start[0];visitor_animator._target_y=start[1];visitor_animator._rest_until=clock+30;visitor_animator._last_move_time=clock;key=selected.id
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
            if not p.state['plan'] and not b.playmates:return
        raise AssertionError('plaything work did not finish')
    payload=[dict(id=s['preview'],elapsed=playkit.ROUTINES[s['preview']]['duration']*i/100,start=playkit.CONTROLS,company=dict(id=key,role='b')) for key,s in company.SCORES.items() for i in range(101)]
    script="import {playkitPose} from './engine/client/playkit-routines.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(w=>{let p=playkitPose(w);return {u:p.actorU,v:p.actorV,contact:p.contact}})))"
    rendered=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],input=json.dumps(payload).encode(),cwd=ROOT))
    check(all(all(abs(v[k]-n)<1e-9 for k,n in company.controls(w,w['company']['id']).items()) for v,w in zip(rendered,payload)),str(len(payload))+' native/renderer helper samples agree')
    for n,(score,spec) in enumerate(company.SCORES.items()):
        kind='butterfly_fairy' if score=='hover_company' else ['regular','rare','story','grumpy_toad','wise_owl'][n%5]
        if score!='young_company' and kind=='story':kind='regular'
        plan,key,obj=reset(spec['item'],kind=kind,stage='hatchling' if score=='young_company' else 'adult')
        work=plan['playkit_work'];work.update(id=spec['preview'],label=playkit.ROUTINES[spec['preview']]['label']);plan['label']=work['label']
        if score=='night_company':p.hour=23;g.day_night.get_current_hour=lambda:23
        before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)};uses=obj['uses'];positions=set();r=None;waiting_checked=False;approach_checked=False
        for _ in range(1000):
            advance(capture=True);positions.add(tuple(round(v,3) for v in b.present[key]));r=company.active(b)
            if r and r['phase'] in ('approach','enter') and plan['phase']=='act' and not waiting_checked:check(work['elapsed']==0,score+' waits for partner arrival');waiting_checked=True
            if r and r['phase']=='approach' and not approach_checked:
                approach_checked=True;facts=json.loads(b.prompt(key,'What are you looking at?')[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1]);check('plaything' not in facts,score+' withholds contact details before arrival')
            if r and r['phase']=='inside':break
        check(bool(r and r['phase']=='inside') and len(positions)>3,score+' has an independent real arrival: '+str(dict(phase=r and r['phase'],positions=len(positions),actor=b.present.get(key),spot=r and r['spot'],clock=work['elapsed'],plan=plan['phase'])))
        check(r['score']==score,score+' chosen from real activity and context: '+r['score'])
        check(all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),score+' arrival alone grants no learning')
        advance(40,capture=True);owner=p._plan_view()['playkit_work'];guest=company.snapshot(b)[0]['routine']
        check(owner['elapsed']==guest['elapsed'] and owner['company']['role']=='a' and guest['company']['role']=='b',score+' participants share one native clock')
        cached=p.snapshot();advance();fresh=p.snapshot();check(fresh['minds']['playmates'][0]['routine']['elapsed']>cached['minds']['playmates'][0]['routine']['elapsed'],score+' helper clock refreshes through snapshot cache')
        finish(capture=True)
        check(obj['uses']==uses+1,score+' grants one original use')
        check(all(b.model.residents[k]['counts']['share']==v+1 for k,v in before.items()),score+' both brains learn once from completion')
        check(obj.get('playkit_company',{}).get(score)==1,score+' retains per-copy shared history')
        if score=='wand_bubbles':check(any('real soap bubbles' in m['text'] for m in b.model.residents[key]['memories']),'visitor remembers bubbles actually seen')
        if score=='boat_rigging':check(any('sail open' in m['text'] for m in b.model.residents[key]['memories']),'visitor remembers the actual open sail on the grass')
        after={k:b.model.residents[k]['counts']['share'] for k in before};company.complete(b,plan);check(all(b.model.residents[k]['counts']['share']==v for k,v in after.items()),score+' cannot repeat completion')
    # Exercise actual native entry and movement for each cast identity, in
    # addition to the exhaustive type/rig/choice coverage below.
    for n,cast in enumerate(PROFILES):
        item=list(playkit.ITEMS)[n%len(playkit.ITEMS)];plan,key,obj=reset(item,kind=cast)
        before=b.model.residents[key]['counts']['share'];r=arrive();check(b.model.residents[key]['cast']==cast,cast+' arrives with its own real identity')
        advance(60,capture=True);finish();check(b.model.residents[key]['counts']['share']==before+1,cast+' completes a native shared play session')
    for item in playkit.ITEMS:
        plan,key,obj=reset(item,kind='story');before=b.model.residents[key]['counts']['share'];r=arrive()
        check(r['score']=='young_company','Pip uses a gentle role beside '+item);advance(60,capture=True);finish();check(b.model.residents[key]['counts']['share']==before+1,'Pip learns after real play with '+item)
    for stage in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        plan,key,obj=reset(stage=stage);r=arrive(capture=stage in ('hatchling','elder'));expected='young_company' if stage in ('hatchling','duckling') else 'quiet_company' if stage in ('elder','legendary') else 'disc_finish'
        check(r['score']==expected,stage+' receives suitable shared play');finish()
    plan,key,obj=reset();b.model.residents[key]['mood']=.1;check(company.choose(b,plan,key)=='quiet_company','low mood chooses quiet company')
    b.model.residents[key]['mood']=.7;b.model.residents[key]['energy']=.3;check(company.choose(b,plan,key)=='quiet_company','low energy chooses quiet company')
    plan,key,obj=reset();r=arrive();advance(70);before=copy.deepcopy(obj);clock_before=plan['playkit_work']['elapsed'];overlap=r['overlap'];plan['paused']=True;advance(30)
    check(obj==before and plan['playkit_work']['elapsed']==clock_before and r['overlap']==overlap,'pause freezes shared control work and learning')
    facts=json.loads(b.prompt(key,'What is happening?')[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1]);check(facts['shared_activity']['status']=='paused' and facts['plaything']['paused'],'speech follows the paused activity')
    visitor_animator._position_x+=10;b.sync();check(company.snapshot(b)==[],'displaced helper is never snapped to the toy');b.tick();check(not b.playmates,'displacement releases the toy reservation')
    plan,key,obj=reset();before=b.model.residents[key]['counts']['share'];advance(500,move=False);check(not b.playmates and plan['playkit_work']['elapsed']>0,'missed arrival times out so Cheese can play alone');finish();check(b.model.residents[key]['counts']['share']==before,'missed arrival earns no memory')
    for reason in ('depart','new_visit','storm','rain','care','move','replace','portable_lost'):
        item='bubble_wand' if reason=='portable_lost' else 'frisbee';plan,key,obj=reset(item);r=arrive();advance(40);before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
        if reason=='depart':g.friends.current_visit=None
        elif reason=='new_visit':g.friends.current_visit.started_at='replacement-visit'
        elif reason in ('storm','rain'):p.weather_type='stormy' if reason=='storm' else 'rainy'
        elif reason=='care':g.duck.current_action='feed'
        elif reason=='move':g.habitat.placed_items[0].x+=3;p.sync()
        elif reason=='portable_lost':g.inventory.remove_item('bubble_wand');p.sync()
        else:g.habitat.placed_items=[PlacedItem('frisbee',10,6)];p.sync()
        advance(3);check(not b.playmates and all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),reason+' cannot claim shared completion')
    plan,key,obj=reset('bubble_machine');g.habitat.placed_items[0].x=6;g.habitat.placed_items.append(PlacedItem('bubble_machine',14,6));p.sync();p.cancel();p.state['cooldowns']={};obj['last_use']=-1000;p.start('item','bubble_machine',instance=g.habitat.placed_items[0].instance_id);plan=p.state['plan'];plan['playkit_work']['id']='bubbler_clean';obj['dirt']=.8;other=p.object_state('bubble_machine',g.habitat.placed_items[1].instance_id);other['dirt']=.8
    visitor_animator._position_x=plan['destination'][0]+19;visitor_animator._position_y=plan['destination'][1];b.sync();b.tasks[key]=dict(action='observe',until=b.now+100,context=b.context(key));r=arrive();before=b.model.residents[key]['counts']['share'];uses=obj['uses']
    while not r['events']:advance()
    check(other['dirt']==.8 and obj['dirt']<.8 and obj['playkit']['cleanings']>=1,'real helper contact cleans only the selected physical copy')
    dirt=obj['dirt'];p.cancel();advance(3);check(obj['dirt']==dirt and obj['uses']==uses and b.model.residents[key]['counts']['share']==before,'cancel retains actual cleaning without a completed-play reward')
    plan,key,obj=reset();r=arrive();advance(80);before=copy.deepcopy(obj['playkit']);plan['paused']=True;g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;b=p.minds;p.sync()
    loaded=p.object_state('frisbee',plan['instance']);check(not b.playmates and p.state['plan']['paused'] and loaded['playkit']==before,'save preserves disc state but discards transient visitor reservations')
    p.state['plan']['paused']=False;advance(10);check(not b.playmates,'resume does not fabricate a second visit');finish()
    for item in playkit.ITEMS:
        plan,key,obj=reset(item)
        for cast,profile in PROFILES.items():
            b.model.ensure('cast:'+cast,profile.get('name',cast),profile)
            check(company.choose(b,plan,'cast:'+cast) in company.SCORES,cast+' has a suitable role beside '+item)
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True);(out/'playkit-company-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),frames=len(frames),scores=len(company.SCORES));(out/'playkit-company-native.json').write_text(json.dumps(dict(**result,assertions=checks),indent=2));print(json.dumps(result))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
