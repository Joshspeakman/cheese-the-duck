"""Production invites and arrivals at saved portable/placed object centers.

Disposable game only. This does not certify full repertoires or encounter reward
ownership; it checks the four company controllers' physical invitation contract.
"""
import os,sys,tempfile,json,random,copy
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-company-anchors-')
os.environ['SDL_AUDIODRIVER']='dummy';os.environ['SDL_VIDEODRIVER']='dummy'
from engine import host,portable_ground,keepsake_company,creative_company,textile_company,ground_company
from engine import creative_props,textiles
from world.habitat import PlacedItem
from world.atmosphere import Weather,WeatherType,Season
from world.friends import visitor_animator
from audio.sound import sound_engine
sys.stdout=host.WIRE;random.seed(45);checks=[];clock=0.
def check(ok,label):
    assert ok,label
    checks.append(label)
CASES=[(keepsake_company,'keepsake','duck_photo','rain_barrel'),
       (creative_company,'creative','paper_plane_design','telescope'),
       (textile_company,'textile','fabric_scrap','persian_rug'),
       (ground_company,'ground','wooden_plank','marble_tiles')]
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;b=p.minds;p.state['auto']=False;b.model.state['next_social']=1e9
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    friend=g.friends.generate_new_friend();key=friend.id
    def counts():return {k:b.model.residents[k]['counts']['share'] for k in ('cheese',key)}
    def advance(move=True):
        global clock
        clock+=.1;p.state['elapsed']+=.1;pos=g.renderer.duck_pos;pos._state_start_time-=.1;pos.update(.1);p._activity(.1)
        if move:
            visitor_animator._mind_motion=b.motion(key);visitor_animator.update(clock,pos.x,pos.y)
        b.tick()
    def reset(company,family,item,placed):
        p.cancel()
        for name in ('readers','creators','textile_helpers','ground_helpers','reading_retry','creative_retry','textile_retry','ground_retry','tasks','housing','furnishings','gardening','musicians','coactivities'):
            getattr(b,name).clear()
        g.friends.current_visit=None;g.atmosphere.current_visitor=None;p.state['story']=None;g.story_motion.actor=None;g.guest_motion.actor=None
        g.duck.current_action=None;g.behavior_ai.clear_action();g.duck.growth_stage='adult';g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
        g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        if placed:g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,10,6)]
        elif item=='duck_photo':g.inventory.add_item(item)
        else:g.materials.add_material(item,1)
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=48;pos.y=21
        p.sync();p.weather_type='sunny';p.season='spring';p.hour=12;p.state['ecology'].update(temperature=18,wind=.2);p.state['cooldowns']={}
        placement=next((a for a in p.placements if a.item_id==item),None);iid=placement.instance if placement else None
        obj=p.object_state(item,iid);obj.update(last_use=-1000,dirt=0,wetness=0,uses=0)
        if family=='creative':obj['creative'].update(creative_props.CONTROLS,strokes=0,observations=0,flights=0,folds=0)
        if family=='textile':obj['textile'].update(textiles.CONTROLS,fringe=.2,nap=.3,frost=0,tracks=[])
        if family=='ground':obj['ground'].update(powder=.8,frost=0,tracks=[],furrows=[])
        obj[family+'_routines']={}
        ok,msg=p.start('item',item,instance=iid);check(ok,item+' starts through native item path: '+msg)
        plan=p.state['plan'];work=plan[family+'_work']
        # Let Cheese physically reach the production-selected site before invite.
        for _ in range(1000):
            pos._state_start_time-=.1;pos.update(.1);p._activity(.1)
            if plan['phase']!='approach':break
        check(plan['phase']=='prepare',item+' Cheese arrived before invite')
        center=plan['destination'] if placed else plan['portable']['object']
        g.friends.start_visit(key);visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False
        visitor_animator._position_x=center[0]+14;visitor_animator._position_y=center[1];visitor_animator._last_move_time=clock
        b.sync();b.model.residents[key]['energy']=.9;b.tasks[key]=dict(action='observe',until=b.now+100,context=b.context(key))
        return plan,work,obj,center
    for company,family,portable,placed_item in CASES:
        for placed,item in [(False,portable),(True,placed_item)]:
            plan,work,obj,center=reset(company,family,item,placed);before=counts();uses=obj['uses']
            company.tick(b,.1);r=company.active(b)
            check(bool(r),item+' production invite succeeds')
            check(r['spot']==[center[0]+9,center[1]],item+' companion uses authoritative object center')
            check(r['instance']==plan.get('instance') and r['work'] is work,item+' preserves copy and work identity')
            check(counts()==before and obj['uses']==uses,item+' invite gives no shared credit or use')
            view=p._plan_view()
            if not placed:
                check(view['portable']['object']==center,item+' renderer snapshot shares native center')
                check(abs((r['spot'][0]-9-plan['destination'][0])*192/132-7)<1e-9,item+' native displacement equals renderer seven cells')
            else:check(plan['destination']==[10*132/20,6*42/12],item+' placed center stays in native habitat coordinates')
            check(portable_ground.policy(p).check('rubber_duck',r['spot'][0]*20/132,r['spot'][1]*12/42,plan.get('instance') or portable_ground.IDENTITY,portable_ground.STANCE)[0],item+' stance obeys support and collision policy')
            positions=set()
            for _ in range(1000):
                advance();positions.add(tuple(round(n,3) for n in b.present[key]));r=company.active(b)
                if r and r['phase']=='inside':break
            check(bool(r and r['phase']=='inside') and len(positions)>3,item+' companion independently arrives')
            check(counts()==before,item+' arrival alone gives no shared credit')
            for _ in range(35):advance()
            guest=company.snapshot(b)[0]['routine'];native=p._plan_view()[family+'_work']
            check(guest['elapsed']==native['elapsed'] and guest['company']['role']=='b' and native['company']['role']=='a',item+' shares one native clock')
            # Cancel before completed shared work: reservations must release and
            # neither the original use nor a shared completion may be invented.
            p.cancel();company.tick(b,.1);company.complete(b,plan)
            check(company.active(b) is None and counts()==before and obj['uses']==uses,item+' interrupted session has no phantom shared completion')
            if not placed:
                plan,work,obj,center=reset(company,family,item,False);before=counts();company.tick(b,.1)
                for _ in range(1800):
                    advance()
                    if p.state['plan'] is None and company.active(b) is None:break
                check(p.state['plan'] is None and company.active(b) is None,item+' successful session completes and releases')
                check(obj['uses']==1 and all(counts()[actor]==amount+1 for actor,amount in before.items()),item+' successful shared completion credits once')
                company.complete(b,plan)
                check(obj['uses']==1 and all(counts()[actor]==amount+1 for actor,amount in before.items()),item+' duplicate completion gives no extra use or shared credit')
            # Actual invite denial with an independently placed blocking object.
            plan,work,obj,center=reset(company,family,item,placed);before=counts();origin=plan['destination'];spot=portable_ground.companion_spot(p,plan,origin)
            check(spot is not None,item+' unblocked companion stance exists')
            blocker=PlacedItem('rock',spot[0]*20/132,spot[1]*12/42);g.habitat.owned_items.append('rock');g.habitat.placed_items.append(blocker)
            company.tick(b,.1);company.complete(b,plan)
            check(company.active(b) is None and counts()==before and obj['uses']==0,item+' occupied stance gracefully refuses without shared credit')
            check(work.get('invitation_checked') and key in b.tasks,item+' failed invitation preserves visitor task')
    # Saved deployments win over any stale legacy origin. Invalid saved data
    # fails closed; legacy data alone uses the same converted renderer offset.
    plan,work,obj,center=reset(keepsake_company,'keepsake','duck_photo',False)
    expected=[center[0]+9,center[1]]
    check(portable_ground.companion_spot(p,plan,[1,1])==expected,'saved deployment is authoritative over origin')
    legacy={k:v for k,v in plan.items() if k!='portable'}
    check(portable_ground.companion_spot(p,legacy,plan['destination'])==expected,'legacy deployment uses native OFFSET')
    for point in (None,[float('nan'),20],[40],[40,20,1],[True,20],[200,20]):
        broken=copy.deepcopy(plan);broken['portable']['object']=point
        check(portable_ground.companion_spot(p,broken,plan['destination']) is None,'malformed or offscreen deployment fails closed: '+str(point))
    # Stance policy intentionally permits duck water support, while scenic
    # solids are rejected. Locate real examples instead of mocking terrain.
    from engine.terrain import water_at
    examples={'water':False,'scenery':False}
    for x in range(10,115):
        for y in range(4,36):
            q=dict(location=p.location,portable=dict(location=p.location,object=[x-9,y]))
            result=portable_ground.companion_spot(p,q,[0,0])
            if result and water_at(p.location,x,y,p.biome):examples['water']=True
            layout=portable_ground.policy(p);ok,reason=layout.check('rubber_duck',x*20/132,y*12/42,portable_ground.IDENTITY,portable_ground.STANCE)
            if not ok and 'Leave room for the' in reason and result is None:examples['scenery']=True
        if all(examples.values()):break
    check(all(examples.values()),'real terrain admits paddling support and rejects scenery solids')
    print(json.dumps(dict(result='PASS',checks=len(checks),production_paths=8,save_dir=os.environ['CHEESE_SAVE_DIR'])))
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
