"""Real copy ownership, storage, migration and activity regressions on disposable saves."""
import copy
import json
import os
import random
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-physical-objects-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,botany,instrument_sessions as music,furniture_rests as furniture,shelters
from engine.living_world import LivingPond
from engine.pond_layout import PondLayout
from engine.scene import snapshot
from world.habitat import Habitat,PlacedItem
from world.building import BuildingSystem,Structure,StructureStatus
from world.decorations import DecorationsSystem,PlacedDecoration,RoomType
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine

sys.stdout=host.WIRE
random.seed(410)
checks=[]
def check(ok,label):
    assert ok,label
    checks.append(label)

# Old records migrate deterministically without conflating identical positions.
legacy={'owned_items':['potted_plant'],'placed_items':[dict(item_id='potted_plant',x=4,y=5)]*2}
h=Habitat();h.from_dict(copy.deepcopy(legacy));other=Habitat();other.from_dict(copy.deepcopy(legacy))
check(h.to_dict()==other.to_dict(),'legacy habitat identity migration is deterministic')
check(len({p.instance_id for p in h.placed_items})==2,'identical legacy copies receive distinct identities')
ids={p.instance_id for p in h.placed_items};PondLayout(h).reconcile()
check({p.instance_id for p in h.placed_items+h.stored_placements}==ids,'layout reconciliation retains every legacy copy')
check(all(PondLayout(h).check(p.item_id,p.x,p.y,p.instance_id)[0] for p in h.placed_items),'legacy twins reserve independent space')

decor=DecorationsSystem();decor.owned_decorations['potted_plant']=2
check(decor.place_decoration('potted_plant','garden',(1,1))[0] and decor.place_decoration('potted_plant','garden',(7,1))[0],'two purchased decorations can be placed')
first,second=decor.rooms['garden'].decorations
check(first.instance_id!=second.instance_id,'decoration purchases have individual identities')
check(decor.remove_decoration('garden',(1,1))[0] and decor.place_decoration('potted_plant','garden',(1,5))[0],'decoration storage and replacement succeeds')
check(decor.rooms['garden'].decorations[-1].instance_id==first.instance_id,'returned decoration keeps its own identity')
check(decor.remove_decoration('garden',(7,1))[0] and decor.stored_placements[0].instance_id==second.instance_id,'another stored decoration retains its own identity')
check(json.loads(json.dumps(DecorationsSystem.from_dict(json.loads(json.dumps(decor.to_dict()))).to_dict()))==json.loads(json.dumps(decor.to_dict())),'decorations preserve placed and stored copies across JSON saves')
building=BuildingSystem();building.structures=[Structure('basic_nest',(1,1),StructureStatus.COMPLETE),Structure('basic_nest',(6,1),StructureStatus.COMPLETE)]
building_saved=building.to_dict()
check(BuildingSystem.from_dict(json.loads(json.dumps(building_saved))).to_dict()==building_saved,'built structures keep independent identities on load')
for d in building_saved['structures']:d.pop('instance_id')
check(BuildingSystem.from_dict(building_saved).to_dict()==BuildingSystem.from_dict(building_saved).to_dict(),'legacy structure migration is deterministic')

t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    sound_engine.enabled=False
    p=g.living_pond;p.state['auto']=False
    g.building.structures=[]
    for room in g.decorations.rooms.values():room.decorations=[]
    p.sync()
    g.duck.growth_stage='adult';g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
    g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
    g.atmosphere.current_season=Season.SPRING
    g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    def twins(item):
        p.cancel();p.minds.music_scenes.clear();p.minds.musicians.clear()
        g.habitat.owned_items=[item];g.habitat.stored_items=[];g.habitat.stored_placements=[]
        a,b=PlacedItem(item,4,6),PlacedItem(item,16,6)
        g.habitat.placed_items=[a,b];p.sync();p.minds.sync();p.state['cooldowns']={}
        p.state['ecology'].update(water=.8,temperature=20)
        return a,b,p.object_state(item,a.instance_id),p.object_state(item,b.instance_id)
    def finish():
        for _ in range(900):
            if not p.state['plan']:return
            p.state['elapsed']+=.2
            pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
        raise AssertionError('activity did not complete')

    a,b,sa,sb=twins('fern')
    sa['botany']['moisture']=.1;sb['botany']['moisture']=.6
    before=copy.deepcopy(sb)
    check(p.start('item','fern',instance=a.instance_id)[0],'explicit first plant can be tended instead of catalogue representative')
    check(p.state['plan']['instance']==a.instance_id and p.state['plan']['plant_care']=='water','care choice uses selected plant moisture')
    finish()
    check(sa['botany']['moisture']>.7 and sa['uses']==1 and sa['care_routines'],'watering records actual care on selected copy')
    check(sb==before,'watering one plant leaves its twin completely unchanged')
    check(p.start('item','fern',instance=b.instance_id)[0],'one plant cooldown does not block its twin')
    check(p.state['plan']['plant_care']=='inspect','well watered twin chooses inspection independently');p.cancel()
    sa['last_use']=sb['last_use']=-1000;sa['botany']['moisture']=.1;sb['botany']['moisture']=.8
    g.duck.needs.cleanliness=5;g.duck.needs.fun=95;g.duck.needs.social=95;g.duck_store.sync_from_duck(g.duck)
    p.state['cooldowns']={};p.decide()
    check(any(c['instance']==a.instance_id and 'roots' in c['reason'] for c in p.state['decision']),'autonomy considers thirsty copies separately')
    check(p.state['plan'] and p.state['plan']['instance']==a.instance_id,'Cheese independently chooses the thirsty plant instead of its well-watered twin');p.cancel()
    sa['dirt']=.7;sb['dirt']=.8
    check(p.start('clean_item','fern',instance=a.instance_id)[0],'specific dirty plant can be cleaned');finish()
    check(sa['dirt']==0 and sb['dirt']==.8,'cleaning does not clean another copy')
    before=copy.deepcopy(sa['botany']);sibling_moisture=sb['botany']['moisture']
    check(g.habitat.store_item('fern',a.instance_id),'one physical plant goes into storage')
    p.sync();p._environment(60,True)
    check(sa['botany']==before and sb['botany']['moisture']<sibling_moisture,'storage freezes only stored plant biology')
    check('fern' not in g.habitat.stored_items and len(g.habitat.get_visible_placed_items())==1,'storing a copy leaves its sibling outside')
    spot=p.layout.find('fern',(4,5),a.instance_id)
    check(spot is not None,'stored plant has an available physical spot')
    p.command(dict(action='layout_place',target='fern',instance=a.instance_id,x=spot[0],y=spot[1]))
    check(p.state['layout']['reply']['ok'] and g.habitat.placed_items[-1].instance_id==a.instance_id,'arrangement restores the selected physical copy')
    check(p.object_state('fern',a.instance_id) is sa,'restored copy keeps its original care record')
    before=g.habitat.to_dict()
    p.command(dict(action='layout_place',target='fern',instance='missing-copy',x=10,y=5))
    check(not p.state['layout']['reply']['ok'] and g.habitat.to_dict()==before,'stale placement identity cannot substitute another copy')

    a,b,sa,sb=twins('toy_piano')
    check(p.start('item','toy_piano',instance=a.instance_id)[0],'specific piano starts')
    plan=p.state['plan'];finish()
    check(sa.get('music_scores',{}).get(plan['music_score']['id'])==1 and sa['uses']==1,'completed musical phrase belongs to selected piano')
    check(not sb.get('music_scores') and sb['uses']==0,'unplayed piano keeps a clean history')
    # A visitor finishing at a different copy writes to that reservation too.
    music.record(p,'toy_piano',dict(id='first_keys'),dict(instance=b.instance_id))
    check(sb['music_scores']=={'first_keys':1} and sa['music_scores'].get('first_keys',0)==0,'independent visitor recording resolves its own instrument')
    check(p.start('item','toy_piano',instance=b.instance_id)[0],'second piano has its own cooldown')
    stale=p.state['plan'];replacement=PlacedItem('toy_piano',b.x,b.y)
    g.habitat.placed_items=[a,replacement];p.sync();p._activity(.2)
    check(p.state['plan'] is None and sb['uses']==0,'same-position replacement cancels old action without credit')
    check(not shelters.still_placed(p,stale['instrument']),'old reservation cannot attach to a replacement instrument')
    check(not p.start('item','toy_piano',instance=b.instance_id)[0],'removed copy cannot be selected through an old click')
    check(p.start('item','toy_piano',instance=replacement.instance_id)[0],'replacement can be selected as its own instrument')
    replacement.x=10;p.sync();p._activity(.2)
    check(p.state['plan'] is None,'moving selected copy interrupts approach at its old destination')

    a,b,sa,sb=twins('garden_bench')
    check(p.start('item','garden_bench',instance=a.instance_id)[0],'specific bench starts')
    plan=p.state['plan'];finish()
    check(sa.get('seat_routines',{}).get(plan['seat_routine']['id'])==1 and not sb.get('seat_routines'),'rest history belongs only to occupied bench')
    p.command(dict(action='layout_store',target='garden_bench',instance=a.instance_id))
    check(p.state['layout']['reply']['ok'] and b in g.habitat.placed_items,'store command leaves a second bench in place')

    # The original inventory/command path uses the first habitat copy. Its
    # completion must not write to the catalogue's last-copy representative.
    from world.interaction_controller import InteractionSource
    a,b,sa,sb=twins('toy_ball');controller=g.interaction_controller
    controller.cancel_interaction();controller._cooldown_end=0
    check(controller.request_interaction('toy_ball',InteractionSource.PLAYER_COMMAND)[0],'original item interaction starts')
    check(controller._pending.instance==a.instance_id,'original controller binds selected habitat copy')
    controller._complete_interaction()
    check(sa['uses']==1 and sb['uses']==0,'original interaction callback records only its selected copy')
    controller._cooldown_end=0
    check(controller.request_interaction('toy_ball',InteractionSource.PLAYER_COMMAND)[0],'second original interaction starts')
    before=copy.deepcopy(g.duck.needs.to_dict())
    g.habitat.placed_items=[PlacedItem('toy_ball',a.x,a.y),b];p.sync();controller._complete_interaction()
    check(controller._pending is None and g.duck.needs.to_dict()==before,'original completion rejects same-position replacement without rewards')

    # Migrate once: the old aggregate goes to one copy, never duplicated rewards.
    a,b,_,_=twins('fern')
    legacy_record=dict(condition=.4,dirt=.6,wetness=.2,bond=.8,uses=17,last_use=12,growth=.7,active=True,botany=dict(moisture=.23,health=.8,bloom=.4,care_count=9,last_care='water'),care_routines={'pot_slow_pour':9})
    p.state['instances']={};p.state['objects']={'fern':copy.deepcopy(legacy_record)};p.sync()
    sa=p.object_state('fern',a.instance_id);sb=p.object_state('fern',b.instance_id)
    check(sa['uses']==0 and sb['uses']==17 and sb['botany']['care_count']==9,'legacy aggregate history migrates to one representative copy')
    check(not sa['active'] and not sb['active'],'migration clears stale active flags')
    sb['botany']['moisture']=.8
    check(sa['botany']['moisture']!=sb['botany']['moisture'],'migrated nested biology is independent')
    before=copy.deepcopy(p.state['instances']);p.sync()
    check(p.state['instances']==before,'second sync cannot duplicate or reset migrated history')
    p.state['plan']=dict(kind='item',target='fern',destination=shelters.position(p.placements[0]),paused=True)
    p.sync()
    check(p.state['plan'].get('instance')==a.instance_id,'unambiguous legacy activity binds to its saved location')
    p.state['plan']=dict(kind='item',target='fern',destination=[-1,-1],paused=True)
    p.sync()
    check(p.state['plan'] is None,'vanished legacy destination cannot resume against another copy')
    sa['active']=True
    saved_pond=LivingPond(p.save())
    check(not saved_pond.object_state('fern',a.instance_id)['active'],'loaded paused game clears stale physical activity flags')
    saved_pond.minds.close();sa['active']=False
    b.instance_id=a.instance_id;p.sync()
    check(b.instance_id!=a.instance_id,'duplicate imported identities are repaired on the saved object')
    identities=[x.instance_id for x in g.habitat.placed_items];p.sync()
    check([x.instance_id for x in g.habitat.placed_items]==identities,'repaired identities remain stable on future snapshots')
    p.object_state('fern',a.instance_id)['uses']=3;p.object_state('fern',b.instance_id)['uses']=8
    g.habitat.store_item('fern',a.instance_id);p.sync()
    g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond
    check(p.object_state('fern',a.instance_id)['uses']==3 and p.object_state('fern',b.instance_id)['uses']==8,'real game save and load keeps individual histories')
    check(any(x.instance_id==a.instance_id for x in g.habitat.stored_placements),'real save preserves physical copy in storage')
    p.sync();p._cache=None;frame=snapshot(g,g.renderer)
    item=next(i for i in frame['items'] if i['id']=='fern')
    check(item['instance']==b.instance_id and frame['living']['instances'][b.instance_id]['uses']==8,'scene protocol exports selected copy state and identity')
    frame['living']['instances'][b.instance_id]['botany']['moisture']=0
    check(p.object_state('fern',b.instance_id)['botany']['moisture']!=0,'render snapshot cannot mutate saved nested state')
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(exist_ok=True)
    (out/'physical-objects-native.json').write_text(json.dumps(dict(result='PASS',checks=checks),indent=2))
    if '--serve' in sys.argv:
        # Loading an empty construction list adds the original starter nest.
        # The UI fixture needs a clear bank for two large fern drawings.
        g.building.structures=[];p.sync()
        p.command(dict(action='layout_auto',target='fern',instance=a.instance_id))
        check(p.state['layout']['reply']['ok'],'both copies restored for live UI review: '+str(p.state['layout']['reply'])+' obstacles '+str(p.layout.obstacles())+' stored '+str([(x.item_id,x.instance_id) for x in g.habitat.stored_placements]))
        p.object_state('fern',a.instance_id).update(dirt=.8,growth=.4)
        p.object_state('fern',a.instance_id)['botany'].update(health=.4,moisture=.1)
        p.object_state('fern',b.instance_id)['botany'].update(health=1,moisture=.8)
        p._cache=None
        frame=dict(scene=snapshot(g,g.renderer),copies=[a.instance_id,b.instance_id])
        (out/'physical-objects-frame.json').write_text(json.dumps(frame))
        print(json.dumps(dict(type='physical_frame',frame=frame)),flush=True)
        for line in sys.stdin:
            request=json.loads(line)
            if request.get('type')=='quit':break
            p.command(request);p._cache=None
            print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),copies=frame['copies']))),flush=True)
    else:print(json.dumps(dict(result='PASS',checks=len(checks))))
finally:
    g._running=False
    if g.living_pond:g.living_pond.minds.close()
    g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
