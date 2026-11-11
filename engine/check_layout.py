"""Habitat arrangement through real ownership, placement, activity and saves."""
import os,sys,tempfile,json,copy,random
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-layout-')
os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host
from engine.pond_layout import PondLayout,FOOTPRINTS,bounds,overlaps
from engine.scene import snapshot
from world.habitat import Habitat,PlacedItem
from world.shop import get_item,ItemCategory
from world.atmosphere import Weather,WeatherType
from world.friends import visitor_animator
from world.building import Structure,StructureStatus
from datetime import datetime
sys.stdout=host.WIRE
checks=[]
def check(ok,label):
    assert ok,label
    checks.append(label)

h=Habitat();layout=PondLayout(h);h.placement_policy=layout
ids=[k for k in FOOTPRINTS if get_item(k) and get_item(k).category!=ItemCategory.COSMETIC]
for key in ids:
    h.owned_items=[key];h.placed_items=[];h.stored_items=[]
    check(h.show_item(key) and layout.check(key,h.placed_items[0].x,h.placed_items[0].y)[0],key+' fits an empty habitat')
h.owned_items=['couch','garden_bench','toy_ball','hammock','chair_wood','grass_patch']
h.placed_items=[];h.stored_items=[]
owned=list(h.owned_items);currency=h.currency
for key in h.owned_items:h.show_item(key)
check(bool(h.stored_items),'full habitat retains overflow in storage')
for a in h.get_visible_placed_items():
    check(layout.check(a.item_id,a.x,a.y)[0],a.item_id+' reserves clear space')
for key in h.stored_items:
    before=copy.deepcopy(h.to_dict())
    check(not h.show_item(key) and h.to_dict()==before,'full habitat cannot pretend to place '+key)
check(h.owned_items==owned and h.currency==currency,'placement preserves all ownership and currency')
before=copy.deepcopy(h.to_dict())
check(not layout.auto_place('castle_tower') and h.to_dict()==before,'unowned auto placement cannot grant or store an item')
check(not layout.put('toy_ball',float('nan'),5)[0] and h.to_dict()==before,'NaN cannot poison world coordinates')
check(not layout.put('toy_ball',True,5)[0] and h.to_dict()==before,'boolean is not a coordinate')
check(not layout.put('toy_ball',100,5)[0] and h.to_dict()==before,'outside placement has no side effects')
h.owned_items.append('hat_red')
check(not layout.auto_place('hat_red') and not layout.put('hat_red',10,5)[0],'clothing belongs in the wardrobe')
h.store_item('garden_bench')
check(h.show_item('chair_wood'),'storing a large piece makes room for another')
loaded=Habitat();loaded.from_dict(copy.deepcopy(h.to_dict()))
check(loaded.to_dict()==h.to_dict() and loaded.placement_policy is None,'physical coordinates and storage round-trip without serializing policy')

# Existing crowded saves migrate once, preserving possessions and finding honest space.
legacy=Habitat();legacy.owned_items=['couch','garden_bench','hammock','chair_wood','sofa_fancy','fireplace']
legacy.placed_items=[PlacedItem(k,10,6) for k in legacy.owned_items]
legacy.placed_items[0].x=-3
legacy.currency=413;policy=PondLayout(legacy)
report=policy.reconcile()
check(report['moved'] and report['stored'],'old overlapping placement is relocated or stored')
check(legacy.currency==413 and set(legacy.owned_items)==set(['couch','garden_bench','hammock','chair_wood','sofa_fancy','fireplace']),'migration never deletes ownership or spends coins')
before=copy.deepcopy(legacy.to_dict())
again=policy.reconcile()
check(not again['moved'] and not again['stored'] and legacy.to_dict()==before,'migration is stable on a second pass')
# External built structures reserve room even when they share a catalogue id.
external=PondLayout(legacy,lambda:[('couch',10,6)])
check(not external.check('couch',10,6)[0],'a separately built copy still blocks the selected object')

# Shared fixtures cover accepted positions, collisions and edge failures in JS.
cases=[];rng=random.Random(319)
for key in legacy.owned_items:
    for _ in range(80):
        x=round(rng.uniform(-2,22),2);y=round(rng.uniform(-2,14),2)
        cases.append(dict(id=key,x=x,y=y,ok=policy.check(key,x,y)[0]))
out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(exist_ok=True,parents=True)
(out/'layout-cases.json').write_text(json.dumps(dict(layout=policy.snapshot(),cases=cases)))

t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer)
t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;p.state['auto']=False
    g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
    g.day_night.get_current_hour=lambda:15
    g.day_night.get_current_minute=lambda:0
    g.habitat.owned_items=['couch','garden_bench','toy_ball','hammock','chair_wood']
    g.habitat.placed_items=[];g.habitat.stored_items=[]
    for key in g.habitat.owned_items:g.habitat.show_item(key)
    p.sync()
    check('hammock' not in p.placed,'stored habitat possessions are not activity targets')
    # A stale hidden record from an old save is also unavailable.
    g.habitat.placed_items.append(PlacedItem('hammock',10,6));p.sync()
    check('hammock' not in p.placed,'legacy hidden placements cannot be used')
    g.habitat.placed_items=[a for a in g.habitat.placed_items if a.item_id!='hammock']
    g.duck.growth_stage='adult';p.state['cooldowns']={}
    ok,message=p.start('item','couch')
    check(ok,'real activity can approach the arranged couch: '+message)
    before=p.state['objects']['couch']['uses']
    p.command(dict(action='layout_store',target='couch'))
    check(not p.state['plan'] and 'couch' not in p.placed,'storage cancels the actual approach and releases its target')
    check(p.state['objects']['couch']['uses']==before,'interrupted furniture arrangement earns no use')
    seq=p.state['layout']['reply']['sequence']
    p.command(dict(action='layout_place',target='chair_wood',x=float('inf'),y=5))
    check(not p.state['layout']['reply']['ok'] and p.state['layout']['reply']['sequence']==seq+1,'failed placement returns an explicit acknowledgement')
    p.command(dict(action='layout_place',target='hat_wizard',x=10,y=5))
    check(not p.state['layout']['reply']['ok'],'unowned command returns failure without granting an item')
    p.command(dict(action='layout_auto',target='couch'))
    check(p.state['layout']['reply']['ok'] and 'couch' in p.placed,'real command places a stored belonging')
    couch=next(a for a in g.habitat.placed_items if a.item_id=='couch')
    couch.anim_offset_x=2;couch.anim_offset_y=-1;p.sync()
    visual=next(a for a in snapshot(g,g.renderer)['items'] if a['id']=='couch')
    check(visual['x']==couch.x*132/20 and visual['y']==couch.y*42/12,'legacy bounce cannot move Ultra furniture off its ground reservation')
    check(p.placed['couch'].get_display_position()==(couch.x,couch.y),'activity destinations ignore decorative legacy bounce')
    couch.anim_offset_x=0;couch.anim_offset_y=0
    friend=g.friends.generate_new_friend();g.friends.start_visit(friend.id)
    visitor_animator._friend_name=friend.name;visitor_animator._is_leaving=False
    visitor_animator._position_x=couch.x*132/20-2;visitor_animator._position_y=couch.y*42/12
    visitor_animator._last_move_time=0
    b=p.minds;b.sync();b.tasks.clear();b.model.residents[friend.id]['energy']=.3;b.tick()
    check(friend.id in b.furnishings,'a real visiting friend independently reserves arranged furniture')
    rewards=b.model.residents[friend.id]['counts']['rest']
    p.command(dict(action='layout_store',target='couch'));b.tick()
    check(friend.id not in b.furnishings and b.model.residents[friend.id]['counts']['rest']==rewards,'storing the visitor destination releases their reservation without learning a false rest')
    g.friends.current_visit=None;p.command(dict(action='layout_auto',target='couch'));b.sync()
    couch=next(a for a in g.habitat.placed_items if a.item_id=='couch')
    building=Structure('shed',(couch.x/2,couch.y*8/12),status=StructureStatus.COMPLETE)
    g.building.structures.append(building)
    before_owned=list(g.habitat.owned_items);before_coins=g.habitat.currency
    p.sync()
    check(all(p.layout.check(a.item_id,a.x,a.y)[0] for a in g.habitat.get_visible_placed_items()),'new completed buildings trigger spacing checks against actual structure positions')
    check(g.habitat.owned_items==before_owned and g.habitat.currency==before_coins,'making room for a completed building preserves belongings and coins')
    g.building.structures.remove(building);p.sync();p.command(dict(action='layout_auto',target='couch'))
    g.renderer.render_frame(g)
    check(True,'Classic renderer accepts actual fractional habitat positions')
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    before=copy.deepcopy(g.habitat.to_dict())
    frame=dict(scene=snapshot(g,g.renderer))
    check(g.habitat.to_dict()==before,'render snapshots never change placement')
    check(frame['scene']['living']['layout']['reply']['ok'],'live frames deliver placement acknowledgements')
    (out/'layout-frame.json').write_text(json.dumps(frame))
    (out/'layout-simulation.json').write_text(json.dumps(dict(result='PASS',checks=len(checks),placeable=len(ids),assertions=checks),indent=2))
    if '--serve' in sys.argv:
        print(json.dumps(dict(type='layout_frame',frame=frame)),flush=True)
        for line in sys.stdin:
            request=json.loads(line)
            if request.get('type')=='quit':break
            p.command(request);p._cache=None
            print(json.dumps(dict(type='layout_frame',frame=dict(scene=snapshot(g,g.renderer)))),flush=True)
    else:print(json.dumps(dict(result='PASS',checks=len(checks),placeable=len(ids))))
finally:
    g._running=False
    if g.living_pond:g.living_pond.minds.close()
    if hasattr(g,'_save_executor'):g._save_executor.shutdown(wait=True)
    if hasattr(g,'_talk_executor'):g._talk_executor.shutdown(wait=False)
    from audio.sound import sound_engine
    sound_engine.shutdown()
