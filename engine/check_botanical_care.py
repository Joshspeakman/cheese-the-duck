"""Native clocks, arrivals and completed learning for independent gardeners."""
import os,sys,tempfile,json,copy,random
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-garden-care-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,botany,botanical_care as care,shelters
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.habitat import PlacedItem
from world.friends import visitor_animator
from world.atmosphere import Weather,WeatherType,VISITORS,Season
sys.stdout=host.WIRE;random.seed(40);checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;b=p.minds;p.state['auto']=False;b.model.state['next_social']=10**9
    g.habitat.owned_items.extend(botany.ROOTED);g.duck.growth_stage='adult';g.duck.needs.energy=90;g.duck.needs.hunger=90;g.duck_store.sync_from_duck(g.duck)
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat());p.sync()
    p.season='spring';p.hour=12;p.state['ecology'].update(temperature=20,water=.8)
    cases=[('cap_brush','mushroom_patch','brush','adult',12,'spring'),('root_ring','bamboo','water','adult',12,'spring'),('pot_slow_pour','potted_plant','water','adult',12,'spring'),
      ('cactus_drops','cactus','water','adult',12,'spring'),('furrow_water','garden_plot','water','adult',12,'spring'),
      ('little_water','fern','water','hatchling',12,'spring'),('leaf_dust','flower_rose','brush','adult',12,'spring'),
      ('pot_rim','potted_plant','brush','adult',12,'spring'),('root_rake','tree_oak','brush','adult',12,'spring'),
      ('spine_brush','cactus','brush','adult',12,'spring'),('soil_probe','fern','inspect','adult',12,'spring'),
      ('bark_lens','tree_oak','inspect','adult',12,'spring'),('petal_lens','flower_rose','inspect','adult',12,'spring'),
      ('trap_watch','venus_flytrap','inspect','adult',12,'spring'),('winter_roots','fern','inspect','adult',12,'winter'),
      ('night_buds','flower_rose','inspect','adult',23,'spring'),('young_discovery','fern','inspect','hatchling',12,'spring'),
      ('elder_soil','fern','inspect','elder',12,'spring')]
    for expected,item,mode,stage,hour,season in cases:
        g.duck.growth_stage=stage;p.hour=hour;p.season=season
        check(care.choose(p,item,mode=mode)['id']==expected,'context chooses '+expected)
    from world.guest_cast import PROFILES as GUEST_CAST
    butterfly_id=next(k for k,v in GUEST_CAST.items() if v['species']=='butterfly')
    b.model.ensure(butterfly_id,'Butterfly',GUEST_CAST[butterfly_id])
    check(care.choose(p,'flower_rose',butterfly_id,'water')['id']=='petal_hover','butterflies inspect petals without carrying a can')
    clock=0.
    def advance(n,brains=False):
        global clock
        for _ in range(n):
            clock+=.2;p.state['elapsed']+=.2
            pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
            if brains:
                if g.friends.current_visit:
                    visitor_animator._mind_motion=b.motion(g.friends.current_visit.friend_id);visitor_animator.update(clock,pos.x,pos.y)
                g.guest_motion.tick(g,clock);g.story_motion.tick(g,clock);b.tick()
            if int(clock*5)%5==0 and (p.state['plan'] or b.gardening):frames.append(snapshot(g,g.renderer))
    def reset(item='tree_oak',stage='adult'):
        p.cancel();b.gardening.clear();b.garden_scenes.clear();b.garden_retry.clear();b.tasks.clear();b.furnishings.clear();b.housing.clear();b.coactivities.clear()
        g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None;g.story_motion.actor=None
        g.duck.growth_stage=stage;g.duck.needs.energy=90;g.duck_store.sync_from_duck(g.duck)
        g.habitat.placed_items=[PlacedItem(item,10,6)];p.sync();b.sync();p.weather_type='sunny';p.season='spring';p.hour=12
        p.state['cooldowns']={};p.state['objects'][item].update(last_use=-1000,dirt=0)
        botany.state(p.state['objects'][item]).update(moisture=.1)
        p.state['ecology'].update(water=.8,temperature=20)
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=48;pos.y=21
        ok,msg=p.start('item',item);check(ok,'start '+item+' '+stage+': '+msg)
        return p.state['plan']
    for stage in shelters.AGES[1:]:
        plan=reset('fern',stage);before=p.state['objects']['fern']['uses'];learned=b.model.residents['cheese']['counts']['garden']
        for _ in range(600):
            advance(1)
            if not p.state['plan']:break
        check(plan.get('care_routine',{}).get('done') and p.state['objects']['fern']['uses']==before+1,stage+' completes a physically arrived care score exactly once')
        check(b.model.residents['cheese']['counts']['garden']==learned+1,stage+' learns gardening from completed care')
    reset('mushroom_patch');p.cancel();obj=p.state['objects']['mushroom_patch'];obj['dirt']=.7;obj['botany']['moisture']=.65
    ok,msg=p.start('item','mushroom_patch');check(ok,'start actual mushroom cap cleaning')
    plan=p.state['plan']
    for _ in range(600):
        advance(1)
        if not p.state['plan']:break
    check(plan['care_routine']['id']=='cap_brush' and plan['care_routine']['done'] and abs(obj['dirt']-.4)<.001,'mushroom cap cleaning completes with actual dirt removal')
    plan=reset('fern');advance(100);routine=plan['care_routine'];before=copy.deepcopy(p.state['objects']['fern']);elapsed=routine['elapsed'];plan['paused']=True;advance(30)
    check(routine['elapsed']==elapsed and p.state['objects']['fern']==before,'paused care cannot progress or grant effects')
    saved=LivingPond(p.save());check(saved.state['plan']['paused'] and not saved.minds.gardening,'save preserves paused care but not visitor reservations')
    plan['paused']=False;g.habitat.placed_items=[];p.sync();advance(2)
    before['active']=False
    check(p.state['plan'] is None and p.state['objects']['fern']==before,'stored plant interrupts care without reward')
    plan=reset('tree_oak');friend=g.friends.generate_new_friend();g.friends.start_visit(friend.id)
    visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False;visitor_animator._position_x=74;visitor_animator._position_y=21;visitor_animator._last_move_time=clock
    g.atmosphere.current_visitor=(VISITORS['friendly_goose'],datetime.now().isoformat());g.guest_motion.tick(g,clock);g.guest_motion.actor.update(x=85,y=24)
    p.state['story']={'id':'lost_duckling','step':0,'started':0};g.story_motion.tick(g,clock);g.story_motion.actor.update(x=45,y=22)
    g.habitat.placed_items.extend([PlacedItem('fern',16,6),PlacedItem('potted_cactus',4,6)]);p.sync();b.sync()
    keys=[k for k in b.present if k!='cheese'];starts={k:b.model.residents[k]['counts']['garden'] for k in keys}
    shares={k:b.model.residents[k]['counts']['share'] for k in b.present}
    for key in keys:
        b.model.residents[key]['energy']=.9;b.tasks[key]=dict(action='garden',until=b.now+50,context=b.context(key))
    b.tick();check(len(b.gardening)==3,'regular friend, rare visitor and Pip choose independently reserved plants')
    destinations={k:list(r['spot']) for k,r in b.gardening.items()};paths={k:set() for k in keys};arrived=set();paired=False
    for _ in range(650):
        advance(1,True)
        for k in keys:
            paths[k].add(tuple(round(n,3) for n in b.present[k]))
            if k in b.gardening:
                r=b.gardening[k];check(r['spot']==destinations[k],k+' target remains attached to the plant') if len(paths[k])==2 else None
                if r['phase']=='inside':arrived.add(k)
        if b.garden_scenes:
            paired=True
            for s in b.garden_scenes.values():
                if not all(s['completed'].values()):
                    assert all(b.model.residents[k]['counts']['share']==shares[k] for k in s['sessions']),s
        if all(b.model.residents[k]['counts']['garden']>starts[k] for k in keys) and not p.state['plan']:break
    check(all(len(path)>5 for path in paths.values()) and arrived==set(keys),'all visitor controllers walk through intermediate positions and actually arrive')
    check(all(b.model.residents[k]['counts']['garden']==starts[k]+1 for k in keys),'all three learn gardening exactly once after finishing')
    check(paired and b.model.residents['cheese']['counts']['share']==shares['cheese']+1,'shared work is remembered only after both finish overlapping care')
    check(not b.gardening and not b.garden_scenes,'completed visitors leave their tools and resume independent life')
    check(not LivingPond(p.save()).minds.garden_scenes,'shared gardening is not resurrected by load')
    # Nearby walkers are not partners. Losing either unfinished worker cancels
    # the pending shared memory, even if the other later finishes their task.
    b.garden_retry.clear();b.tasks[friend.id]=dict(action='garden',until=b.now+50,context=b.context(friend.id));b.tick()
    lone=b.gardening[friend.id];share_before=b.model.residents[friend.id]['counts']['share']
    check(not b.garden_scenes,'a walking visitor creates no invented shared-care memory')
    old_item=lone['id'];old_count=p.state['objects'][old_item]['botany']['care_count']
    care.release(b,friend.id)
    check(p.state['objects'][old_item]['botany']['care_count']==old_count,'aborted approach does not care for the plant')
    # Force another approach then invalidate its visit; no unearned learning.
    b.garden_retry.clear();b.tasks[friend.id]=dict(action='garden',until=b.now+50,context=b.context(friend.id));b.tick()
    check(friend.id in b.gardening,'a later garden task reserves a new approach')
    before=b.model.residents[friend.id]['counts']['garden'];g.friends.current_visit.started_at='new-visit';advance(1,True)
    check(friend.id not in b.gardening and b.model.residents[friend.id]['counts']['garden']==before,'replaced visit discards its unfinished work')
    b.garden_retry.clear();b.tasks[friend.id]=dict(action='garden',until=b.now+50,context=b.context(friend.id));b.tick();p.weather_type='stormy';advance(1,True)
    check(not b.gardening,'storm interrupts outdoor gardening')
    check(b.model.residents[friend.id]['counts']['garden']==before,'weather interruption grants no care learning')
    plan=reset('tree_oak');g.friends.start_visit(friend.id)
    visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False;visitor_animator._position_x=70;visitor_animator._position_y=21;visitor_animator._last_move_time=clock
    b.sync();b.tasks[friend.id]=dict(action='garden',until=b.now+50,context=b.context(friend.id));b.tick()
    for _ in range(350):
        advance(1,True)
        if b.garden_scenes:break
    check(bool(b.garden_scenes),'both residents arrive before shared work begins')
    scene=next(iter(b.garden_scenes.values()));overlap=scene['overlap']
    plan['care_routine']['done']=True;b.gardening[friend.id]['routine']['done']=True
    care.company_tick(b,2)
    check(scene['overlap']==overlap,'settling and leaving cannot pad the shared working time')
    plan['care_routine']['done']=False;b.gardening[friend.id]['routine']['done']=False
    before={k:b.model.residents[k]['counts']['share'] for k in ('cheese',friend.id)}
    p.cancel();advance(5,True)
    check(not b.garden_scenes,'canceling Cheese interrupts the shared memory')
    for _ in range(300):
        advance(1,True)
        if friend.id not in b.gardening:break
    check(all(b.model.residents[k]['counts']['share']==n for k,n in before.items()),'the remaining gardener cannot award a canceled shared experience')
    plan=reset('fern');advance(100);before=p.state['objects']['fern']['uses'];plan['care_routine']['id']='missing-score'
    advance(1);check(not p.state['plan'] and p.state['objects']['fern']['uses']==before,'unknown saved routine cancels without reward')
    for water,temp in ((.1,20),(.8,-3)):
        plan=reset('fern');advance(100);before=p.state['objects']['fern']['botany']['care_count'];learned=b.model.residents['cheese']['counts']['garden']
        p.state['ecology'].update(water=water,temperature=temp);advance(2)
        check(not p.state['plan'] and p.state['objects']['fern']['botany']['care_count']==before and b.model.residents['cheese']['counts']['garden']==learned,'unavailable or frozen water interrupts care without learning')
    g.duck.growth_stage='egg';p.state['cooldowns']={}
    check(not p.start('item','fern')[0],'eggs cannot carry tools')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(exist_ok=True)
    (out/'botanical-care-frames.json').write_text(json.dumps(frames))
    result=dict(result='PASS',checks=len(checks),scores=len(care.ROUTINES),frames=len(frames))
    (out/'botanical-care-native.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    from audio.sound import sound_engine
    sound_engine.shutdown()
