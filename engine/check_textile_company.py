"""Actual regular/rare/story arrivals, shared textile work and interrupted memories."""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-textile-company-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,textiles,textile_company as company
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.habitat import PlacedItem
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
            g.guest_motion.tick(g,clock);g.story_motion.tick(g,clock);b.tick()
            if capture and int(clock*10)%10==0:frames.append(snapshot(g,g.renderer))
    def reset(item='persian_rug',kind='regular',stage='adult'):
        g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
        g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
        p.cancel();b.textile_helpers.clear();b.textile_retry.clear();b.readers.clear();b.tasks.clear();b.housing.clear();b.furnishings.clear();b.gardening.clear();b.musicians.clear();b.coactivities.clear()
        g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None;g.story_motion.actor=None;g.guest_motion.actor=None
        g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=stage;g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
        g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        if item=='rug':g.decorations.owned_decorations[item]=1;g.decorations.place_decoration(item,'garden',(5,3))
        elif item=='moss_carpet':g.inventory.add_item(item)
        elif textiles.ITEMS[item]['portable']:g.materials.add_material(item,1)
        else:g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,10,6)]
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=48;pos.y=21
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(temperature=18,wind=.2);p.state['cooldowns']={}
        placement=next((a for a in p.placements if a.item_id==item),None);iid=placement.instance if placement else None;obj=p.object_state(item,iid);obj['last_use']=-1000;obj['uses']=0;obj['dirt']=0;obj['wetness']=0;obj['textile'].update(textiles.CONTROLS,fringe=.2,nap=.3,frost=0,tracks=[]);obj['textile_routines']={}
        ok,msg=p.start('item',item,instance=iid);check(ok,item+' starts: '+msg);plan=p.state['plan'];dest=plan.get('destination',plan['textile_work']['origin']);start=[dest[0]+19,dest[1]]
        if kind=='regular':
            g.friends.start_visit(friend.id);visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False
            visitor_animator._position_x=start[0];visitor_animator._position_y=start[1];visitor_animator._last_move_time=clock;key=friend.id
        elif kind=='rare':
            key='friendly_goose';g.atmosphere.current_visitor=(VISITORS[key],datetime.now().isoformat());g.guest_motion.tick(g,clock);g.guest_motion.actor.update(x=start[0],y=start[1])
        else:
            key='story:pip';p.state['story']={'id':'lost_duckling','step':0,'started':0};g.story_motion.tick(g,clock);g.story_motion.actor.update(x=start[0],y=start[1])
        b.sync();b.model.residents[key]['energy']=.9;b.tasks[key]=dict(action='observe',until=b.now+100,context=b.context(key))
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
            if not p.state['plan'] and not b.textile_helpers:return
        raise AssertionError('textile work did not finish')
    for i,item in enumerate(textiles.ITEMS):
        plan,key,obj=reset(item,('regular','rare','story')[i%3]);uses=obj['uses'];before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
        positions=set();waiting=False;checked_words=False
        for _ in range(1000):
            advance(capture=True);positions.add(tuple(round(v,3) for v in b.present[key]))
            r=company.active(b)
            if r and r['phase'] in ('approach','enter') and plan['phase']=='act':
                waiting=True;assert plan['textile_work']['elapsed']==0
            if item=='welcome_mat' and r and r['phase']=='approach' and not checked_words:
                facts=json.loads(b.prompt(key,'What does that mat say?')[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1]);checked_words=True
                check('textile_work' not in facts and 'QUACK-OME' not in str(facts.get('shared_activity')),'an approaching guest has not read the mat greeting yet')
            if r and r['phase']=='inside':break
        check(bool(r and r['phase']=='inside') and len(positions)>3,item+' partner independently walks to the object')
        check(all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),item+' arrival never awards completed shared time')
        for _ in range(35):advance(capture=True)
        native=p._plan_view()['textile_work'];guest=company.snapshot(b)[0]['routine']
        check(native['elapsed']==guest['elapsed'] and native['company']['role']=='a' and guest['company']['role']=='b',item+' shares one clock with complementary roles')
        before_snapshot=copy.deepcopy(company.snapshot(b));advance();check(before_snapshot!=company.snapshot(b),'native textile work snapshots advance without mutating old frames')
        finish(capture=True)
        check(obj['uses']==uses+1,item+' partner does not duplicate original item use')
        check(all(b.model.residents[k]['counts']['share']==v+1 for k,v in before.items()),item+' both learn exactly once on a completed shared session')
        check(bool(obj.get('textile_company')),item+' physical object records its actual shared routine')
        if item=='welcome_mat':
            check(all(any('QUACK-OME' in m['text'] for m in b.model.residents[k]['memories']) for k in ('cheese',key)), 'both residents remember the greeting they actually saw')
        after={k:b.model.residents[k]['counts']['share'] for k in before};company.complete(b,plan)
        check(all(b.model.residents[k]['counts']['share']==v for k,v in after.items()),item+' completion cannot be repeated')
    # All ages choose age-appropriate textile company; an egg never acts.
    for stage in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        plan,key,obj=reset(stage=stage);r=arrive(capture=stage in ('hatchling','elder'))
        expected='patient_steps' if stage in ('hatchling','duckling','elder','legendary') else company.choose(b,plan,key)
        check(r['score']==expected,stage+' has age-appropriate company');finish()
    p.cancel();g.duck.growth_stage='egg';check(not p.start('item','persian_rug')[0],'eggs cannot start shared textile work');g.duck.growth_stage='adult'
    plan,key,obj=reset();p.hour=23;r=arrive();check(r['score']=='night_listen','night chooses quiet shared textile work');p.cancel();advance()
    plan,key,obj=reset();r=arrive();advance(60);clock_before=plan['textile_work']['elapsed'];overlap=r['overlap'];before=copy.deepcopy(obj);plan['paused']=True;advance(50)
    check(plan['textile_work']['elapsed']==clock_before and r['overlap']==overlap and obj==before,'pause freezes both textile_helpers and physical state')
    saved=LivingPond(p.save());check(not saved.minds.textile_helpers and saved.state['plan']['paused'],'load discards visitor reservations and pauses the saved work');saved.minds.close()
    prompt=b.prompt(key,'What are we doing together?');facts=json.loads(prompt[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1])
    check(facts['shared_activity']['status']=='paused' and facts['textile_work']['rolled']==round(obj['textile']['roll'],2),'visitor conversation sees the actual paused rug')
    p.cancel();advance();check(not b.textile_helpers,'cancel releases the helper to independent movement')
    plan,key,obj=reset();before=b.model.residents[key]['counts']['share'];advance(330,move=False)
    check(not b.textile_helpers and plan['textile_work']['elapsed']>0,'an unreachable helper times out and Cheese continues alone')
    finish();check(b.model.residents[key]['counts']['share']==before,'a missed invitation does not teach a shared experience')
    for reason in ('depart','new_visit','storm','care','move','replace'):
        plan,key,obj=reset('persian_rug');r=arrive();advance(40);before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
        if reason=='depart':g.friends.current_visit=None
        elif reason=='new_visit':g.friends.current_visit.started_at='replacement-visit'
        elif reason=='storm':p.weather_type='stormy'
        elif reason=='care':g.duck.current_action='feed'
        elif reason=='move':g.habitat.placed_items[0].x+=3;p.sync()
        else:g.habitat.placed_items=[PlacedItem('persian_rug',10,6)];p.sync()
        advance(3)
        check(not b.textile_helpers and all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),reason+' interrupts without shared completion')
    # Pausing cannot pin a displaced visitor back onto the material in snapshots.
    plan,key,obj=reset();r=arrive();advance(40);plan['paused']=True
    visitor_animator._position_x+=8;b.sync()
    check(company.snapshot(b)==[],'a displaced paused visitor is absent from the shared drawing')
    facts=json.loads(b.prompt(key,'Are you helping Cheese?')[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1])
    check('shared_activity' not in facts and 'textile_work' not in facts,'a displaced visitor no longer claims the shared work')
    b.tick();check(not b.textile_helpers,'paused displacement releases the reservation')
    # Real contact belongs to the chosen copy, and cancellation retains only it.
    plan,key,obj=reset('persian_rug');obj['dirt']=.8;plan['textile_work']=textiles.choose(p,'persian_rug',plan);g.habitat.placed_items.append(PlacedItem('persian_rug',17,6));p.sync();other=p.object_state('persian_rug',g.habitat.placed_items[-1].instance_id);other['dirt']=.8
    r=arrive();uses=obj['uses'];before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
    while not r['events']:advance()
    check(abs(obj['dirt']-.75)<1e-9 and other['dirt']==.8,'partner brush changes only the actual selected copy after contact')
    saved_dirt=obj['dirt'];p.cancel();advance(3)
    check(obj['dirt']==saved_dirt and obj['uses']==uses and all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),'cancel retains helper contact without completion rewards or shared learning')
    # Saved work cannot resurrect an old helper or replay their already made marks.
    plan,key,obj=reset('persian_rug');obj['dirt']=.8;plan['textile_work']=textiles.choose(p,'persian_rug',plan);r=arrive()
    while not r['events']:advance()
    plan['paused']=True;g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;b=p.minds;p.sync()
    check(not b.textile_helpers and p.state['plan']['paused'],'full game save reload releases the old transient helper')
    p.state['plan']['paused']=False;advance(10);check(not b.textile_helpers,'resumed work does not issue a second invitation')
    # Temperament and task context select different complementary jobs.
    plan,key,obj=reset();b.model.residents[key]['traits']['confidence']=.8
    check(company.choose(b,plan,key)=='pattern_story','confident guests interpret patterns expansively')
    b.model.residents[key]['traits']['confidence']=.2
    check(company.choose(b,plan,key)=='quiet_pattern','shy guests examine the small knots')
    g.duck.growth_stage='elder';check(company.choose(b,plan,key)=='patient_steps','elders receive patient company')
    for item,core,expected in [('carpet_red','mat_unroll','unroll_edge'),('persian_rug','fringe_comb','fringe_pair'),('grass_patch','grass_dew','dew_observer'),('fabric_scrap','scrap_fold','scrap_corner'),('thatch','reed_sort','reed_bundle')]:
        plan,key,obj=reset(item);plan['textile_work']['id']=core
        check(company.choose(b,plan,key)==expected,core+' has its own helper role')
    for core in ('mat_roll','rolled_inspect','frost_sweep','edge_shake'):
        plan['textile_work']['id']=core;check(company.choose(b,plan,key) is None,'no misleading invitation during '+core)
    # Every cast profile can be a helper; flying guests are visual observers.
    plan,key,obj=reset();b.sync()
    for item in textiles.ITEMS:
        plan,key,obj=reset(item)
        for cast,profile in PROFILES.items():
            b.model.ensure('cast:'+cast,profile.get('name',cast),profile)
            check(company.choose(b,plan,'cast:'+cast) in company.SCORES,cast+' can join '+item)
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'textile-company-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),frames=len(frames),scores=len(company.SCORES));(out/'textile-company-native.json').write_text(json.dumps(dict(**result,assertions=checks),indent=2));print(json.dumps(result))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
