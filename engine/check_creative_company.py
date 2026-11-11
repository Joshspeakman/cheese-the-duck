"""Actual regular/rare/story arrivals, shared creative work and interrupted memories."""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-creative-company-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,creative_props,creative_company as company
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
    def reset(item='telescope',kind='regular',stage='adult'):
        p.cancel();b.creators.clear();b.creative_retry.clear();b.readers.clear();b.tasks.clear();b.housing.clear();b.furnishings.clear();b.gardening.clear();b.musicians.clear();b.coactivities.clear()
        g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None;g.story_motion.actor=None;g.guest_motion.actor=None
        g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage=stage;g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
        g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        if item!='paper_plane_design':
            g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,10,6)]
        else:g.materials.add_material(item,1)
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=48;pos.y=21
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(temperature=18,wind=.2);p.state['cooldowns']={}
        placement=next((a for a in p.placements if a.item_id==item),None);iid=placement.instance if placement else None;obj=p.object_state(item,iid);obj['last_use']=-1000;obj['creative'].update(creative_props.CONTROLS,strokes=0,observations=0,flights=0,folds=0);obj['creative_routines']={'kite_tail':1}
        ok,msg=p.start('item',item,instance=iid);check(ok,item+' starts: '+msg);plan=p.state['plan'];dest=plan.get('destination',plan['creative_work']['origin']);start=[dest[0]+19,dest[1]]
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
            if not p.state['plan'] and not b.creators:return
        raise AssertionError('creative work did not finish')
    for i,item in enumerate(creative_props.ITEMS):
        plan,key,obj=reset(item,('regular','rare','story')[i%3]);uses=obj['uses'];before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
        positions=set();waiting=False
        for _ in range(1000):
            advance(capture=True);positions.add(tuple(round(v,3) for v in b.present[key]))
            r=company.active(b)
            if r and r['phase'] in ('approach','enter') and plan['phase']=='act':
                waiting=True;assert plan['creative_work']['elapsed']==0
            if r and r['phase']=='inside':break
        check(bool(r and r['phase']=='inside') and len(positions)>3,item+' partner independently walks to the object')
        check(all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),item+' arrival never awards completed shared time')
        for _ in range(35):advance(capture=True)
        native=p._plan_view()['creative_work'];guest=company.snapshot(b)[0]['routine']
        check(native['elapsed']==guest['elapsed'] and native['company']['role']=='a' and guest['company']['role']=='b',item+' shares one clock with complementary roles')
        before_snapshot=copy.deepcopy(company.snapshot(b));advance();check(before_snapshot!=company.snapshot(b),'native creative work snapshots advance without mutating old frames')
        finish(capture=True)
        check(obj['uses']==uses+1,item+' partner does not duplicate original item use')
        check(all(b.model.residents[k]['counts']['share']==v+1 for k,v in before.items()),item+' both learn exactly once on a completed shared session')
        check(bool(obj.get('creative_company')),item+' physical object records its actual shared routine')
        if item=='easel':
            check(all(any('new brush marks' in m['text'] for m in b.model.residents[k]['memories']) for k in ('cheese',key)), 'both residents remember layers that actually appeared while together')
        after={k:b.model.residents[k]['counts']['share'] for k in before};company.complete(b,plan)
        check(all(b.model.residents[k]['counts']['share']==v for k,v in after.items()),item+' completion cannot be repeated')
    # All ages choose age-appropriate creative company; an egg never acts.
    for stage in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        plan,key,obj=reset(stage=stage);r=arrive(capture=stage in ('hatchling','elder'))
        expected='scope_first' if stage in ('hatchling','duckling') else 'scope_bank'
        check(r['score']==expected,stage+' has age-appropriate company');finish()
    p.cancel();g.duck.growth_stage='egg';check(not p.start('item','telescope')[0],'eggs cannot start shared creative work');g.duck.growth_stage='adult'
    plan,key,obj=reset();p.hour=23;r=arrive();check(r['score']=='scope_stars','night chooses quiet shared creative work');p.cancel();advance()
    plan,key,obj=reset();r=arrive();advance(60);clock_before=plan['creative_work']['elapsed'];overlap=r['overlap'];before=copy.deepcopy(obj);plan['paused']=True;advance(50)
    check(plan['creative_work']['elapsed']==clock_before and r['overlap']==overlap and obj==before,'pause freezes both creators and physical state')
    saved=LivingPond(p.save());check(not saved.minds.creators and saved.state['plan']['paused'],'load discards visitor reservations and pauses the saved work');saved.minds.close()
    prompt=b.prompt(key,'What are we doing together?');facts=json.loads(prompt[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1])
    check(facts['shared_activity']['status']=='paused' and facts['creative_work']['focus']==round(obj['creative']['focus'],2),'visitor conversation sees the actual paused telescope')
    p.cancel();advance();check(not b.creators,'cancel releases the helper to independent movement')
    plan,key,obj=reset();before=b.model.residents[key]['counts']['share'];advance(330,move=False)
    check(not b.creators and plan['creative_work']['elapsed']>0,'an unreachable helper times out and Cheese continues alone')
    finish();check(b.model.residents[key]['counts']['share']==before,'a missed invitation does not teach a shared experience')
    for reason in ('depart','new_visit','storm','care','move','replace','wind'):
        plan,key,obj=reset('easel');r=arrive();advance(40);before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
        if reason=='depart':g.friends.current_visit=None
        elif reason=='new_visit':g.friends.current_visit.started_at='replacement-visit'
        elif reason=='storm':p.weather_type='stormy'
        elif reason=='wind':p.state['ecology']['wind']=.95
        elif reason=='care':g.duck.current_action='feed'
        elif reason=='move':g.habitat.placed_items[0].x+=3;p.sync()
        else:g.habitat.placed_items=[PlacedItem('easel',10,6)];p.sync()
        advance(3)
        check(not b.creators and all(b.model.residents[k]['counts']['share']==v for k,v in before.items()),reason+' interrupts without shared completion')
    # Temperament and actual task context change the companion's job.
    plan,key,obj=reset('easel');b.model.residents[key]['traits']['confidence']=.8
    check(company.choose(b,plan,key)=='paint_proud','confident visitors choose an expansive pose')
    b.model.residents[key]['traits']['confidence']=.2
    check(company.choose(b,plan,key)=='paint_shy','shy visitors choose a tentative pose')
    g.duck.growth_stage='elder';check(company.choose(b,plan,key)=='paint_patient','older painters receive patient company')
    plan,key,obj=reset('paper_plane_design');p.state['ecology']['wind']=.6
    check(company.choose(b,plan,key)=='fold_pin_partner','wind chooses a real paper-corner helper')
    p.state['ecology']['wind']=.2;plan['creative_work']['id']='fold_wings'
    check(company.choose(b,plan,key)=='fold_wing_partner','wing folds choose complementary guidance')
    plan,key,obj=reset('kite');plan['creative_work']['id']='kite_tail'
    check(company.choose(b,plan,key)=='kite_tail_partner','knot work chooses a tail helper')
    plan['creative_work']['id']='kite_launch';g.duck.growth_stage='adult'
    check(company.choose(b,plan,key)=='kite_bridle','a launch chooses a bridle helper')
    for work_id in ('kite_reel','paint_cover','fold_unwrap','scope_polish'):
        plan['creative_work']['id']=work_id
        check(company.choose(b,plan,key) is None,'no misleading creative invitation during '+work_id)
    # Every cast profile can be a helper; flying guests are visual observers.
    plan,key,obj=reset();b.sync()
    for item in creative_props.ITEMS:
        plan,key,obj=reset(item)
        for cast,profile in PROFILES.items():
            b.model.ensure('cast:'+cast,profile.get('name',cast),profile)
            check(company.choose(b,plan,'cast:'+cast) in company.SCORES,cast+' can join '+item)
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'creative-company-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),frames=len(frames),scores=len(company.SCORES));(out/'creative-company-native.json').write_text(json.dumps(dict(**result,assertions=checks),indent=2));print(json.dumps(result))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
