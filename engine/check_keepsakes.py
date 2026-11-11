"""Real ownership, physical copies, reading contacts, water and saved keepsakes."""
import os,sys,tempfile,json,copy,subprocess
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-keepsakes-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,keepsakes as k
from engine.scene import snapshot
from world.habitat import PlacedItem
from world.building import Structure,StructureStatus
from world.treasure import FoundTreasure,TreasureLocation
from world.atmosphere import Weather,WeatherType,Season
from audio.sound import sound_engine
sys.stdout=host.WIRE;checks=[];frames=[]
def check(ok,label):
    assert ok,label
    checks.append(label)
payload=[dict(id=id,elapsed=spec['duration']*i/100,start_open=start) for id,spec in k.ROUTINES.items() for i in range(101) for start in (0,.45,1)]
script="import {keepsakePose} from './engine/client/keepsake-routines.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(c=>keepsakePose(c).open)))"
render=json.loads(subprocess.check_output(['node','--input-type=module','-e',script],input=json.dumps(payload).encode(),cwd=ROOT))
check(all(abs(a-k.openness(w,k.ROUTINES[w['id']]))<1e-9 for a,w in zip(render,payload)),str(len(payload))+' native lid/page and preview samples agree')
bad={'keepsake':{'open':float('nan'),'page':float('inf'),'bookmark':-99,'litres':999}}
check(k.state('rain_barrel',bad)['litres']==60 and bad['keepsake']['open']==0,'damaged optional state gets finite bounded defaults')
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
    g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
    g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
    p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=1e9
    g.duck.growth_stage='adult';g.duck.needs.energy=95;g.duck.needs.hunger=95;g.duck_store.sync_from_duck(g.duck)
    def weather():
        g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
        g.atmosphere.current_season=Season.SPRING;g.atmosphere.current_weather=Weather(WeatherType.SUNNY,.5,1,datetime.now().isoformat())
        p.state['ecology'].update(temperature=18,wind=.2)
    weather()
    def own(item,twins=False):
        p.cancel();g.duck.current_action=None;g.behavior_ai.clear_action();g.habitat.owned_items=[];g.habitat.placed_items=[];g.habitat.stored_items=[];g.habitat.stored_placements=[];g.building.structures=[]
        for room in g.decorations.rooms.values():room.decorations=[]
        if item in ('treasure_chest','rain_barrel'):
            g.habitat.owned_items=[item];g.habitat.placed_items=[PlacedItem(item,10,6)]
            if twins:g.habitat.placed_items.append(PlacedItem(item,17,6))
        elif item=='storage_chest':g.building.structures=[Structure(item,(4,3),StructureStatus.COMPLETE)]
        elif item=='picture_frame':
            g.decorations.owned_decorations[item]=1
        elif item in ('duck_photo','storage_basket'):g.inventory.add_item(item)
        elif item=='ancient_tome':g.treasure.found_treasures[item]=[FoundTreasure(item,datetime.now().isoformat(),TreasureLocation.BEACH)]
        else:g.materials.add_material(item,1)
        p.sync();p.state['cooldowns']={};p._cache=None
        for obj in [*p.state['instances'].values(),*p.state['objects'].values()]:obj['last_use']=-1000
        pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=36;pos.y=21
        placed=next((x for x in p.placements if x.item_id==item),None);iid=placed.instance if placed else None
        return iid,p.object_state(item,iid)
    def possessions():return copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.treasure.to_dict()))
    def speech_facts():
        p.minds.sync()
        prompt=p.minds.prompt('cheese','What are you reading or looking at?')
        return json.loads(prompt[0]['content'].split('CHARACTER AND VERIFIED GAME STATE:\n',1)[1])
    def step(capture=False):
        p.state['elapsed']+=.2;pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p._activity(.2)
        if capture:frames.append(snapshot(g,g.renderer))
    def finish(capture=False):
        for n in range(900):
            if not p.state['plan']:return
            step(capture and n%15==0)
        raise AssertionError('keepsake action did not finish')
    for item in k.ITEMS:
        iid,obj=own(item);before=possessions();ok,msg=p.start('item',item,instance=iid);check(ok,item+' starts: '+msg)
        plan=p.state['plan'];initial=copy.deepcopy(obj)
        if iid:p._activity(1);check(obj==initial and plan['keepsake_work']['elapsed']==0,item+' cannot work on it before arrival')
        finish(item in ('ancient_tome','pirate_map','rain_barrel','storage_chest','friendship_card'))
        check(plan['keepsake_work']['done'] and obj['uses']==initial['uses']+1,item+' finishes native action once: '+json.dumps(dict(work=plan['keepsake_work'],uses=obj['uses'],initial=initial['uses'],destination=plan.get('destination'),pos=[g.renderer.duck_pos.x,g.renderer.duck_pos.y],instance=plan.get('instance'))))
        check(possessions()==before,item+' never redeems rewards, consumes inventory or fabricates contents')
        saved=copy.deepcopy(obj);k.complete(p,plan);check(obj==saved,item+' completion replay leaves state alone')
        check(bool(obj.get('keepsake_routines')),item+' records its actual completed sequence')
    # Context choices and all eight hatched ages retain their real identity.
    iid,obj=own('ancient_tome')
    for age in ('hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
        g.duck.growth_stage=age;spec=k.choose(p,'ancient_tome',{})
        expected='book_pictures' if age in ('hatchling','duckling') else 'book_bookmark' if age in ('mature','elder','legendary') else 'book_leaf'
        check(spec['id']==expected,age+' receives age-appropriate reading')
    g.duck.growth_stage='egg';check(not p.start('item','ancient_tome')[0],'an egg does not walk out and read');g.duck.growth_stage='adult'
    p.weather_type='rain';check(k.choose(p,'ancient_tome',{})['id']=='paper_shelter','rain closes exposed paper instead of soaking an open book')
    p.weather_type='sunny';iid,obj=own('pirate_map');p.state['ecology']['wind']=.9
    check(k.choose(p,'pirate_map',{})['id']=='paper_wind','a gust changes the map-reading action');p.state['ecology']['wind']=.2
    iid,obj=own('rain_barrel');k.update(p,'rain_barrel',obj,1200,True,True,1,20)
    check(abs(obj['keepsake']['litres']-30)<1e-9,'real rain fills the rain collector at a bounded rate')
    amount=obj['keepsake']['litres'];k.update(p,'rain_barrel',obj,500,True,False,.5,-4)
    check(obj['keepsake']['frozen'] and obj['keepsake']['litres']==amount,'frozen water is retained')
    k.update(p,'rain_barrel',obj,500,False,True,1,20);check(obj['keepsake']['litres']==amount,'stored barrel does not collect phantom rain')
    k.update(p,'rain_barrel',obj,1000,True,False,.5,25);check(obj['keepsake']['litres']<amount,'warm dry air slowly evaporates water')
    # Independent copies, cancellation at real page contact and full save/reload.
    iid,obj=own('treasure_chest',True);other=p.object_state('treasure_chest',g.habitat.placed_items[1].instance_id)
    check(p.start('item','treasure_chest',instance=iid)[0],'specific chest starts');finish()
    check(obj['uses']==1 and other['uses']==0,'looking inside one chest does not operate its twin')
    check(g.habitat.store_item('treasure_chest',iid),'physical chest stores');p.sync()
    check(not p.start('item','treasure_chest',instance=iid)[0],'stored copy cannot be operated through a stale selection')
    iid,obj=own('ancient_tome');start_page=obj['keepsake']['page'];uses=obj['uses'];p.start('item','ancient_tome');p.cancel()
    check(obj['keepsake']['page']==start_page and obj['uses']==uses,'cancelling before page contact changes nothing')
    p.start('item','ancient_tome');plan=p.state['plan']
    for _ in range(600):
        step()
        if plan['keepsake_work']['events']:break
    check(obj['keepsake']['page']==(start_page+1)%8 and not plan['keepsake_work']['done'],'the page changes at physical contact before completion')
    before_prompt=copy.deepcopy(p.state);facts=speech_facts()
    check(facts['keepsake']['page']==obj['keepsake']['page']+1 and facts['keepsake']['chapter']==k.ITEMS['ancient_tome']['chapters'][obj['keepsake']['page']][0], 'natural chat receives the actual currently open chapter after page contact')
    check(' '.join(k.ITEMS['ancient_tome']['chapters'][obj['keepsake']['page']][1:])==facts['keepsake']['visible_words'],'spoken book text comes from the same authored words as the artwork')
    # Synchronization may initialize a resident; constructing the prompt itself
    # must never turn pages, award a read or change the object.
    check(obj==before_prompt['objects']['ancient_tome'],'asking about a book leaves its physical state unchanged')
    facts['keepsake']['page']=999
    check(obj['keepsake']['page']!=999,'conversation context is detached from saved object state')
    before=copy.deepcopy(obj);plan['paused']=True;clock=plan['keepsake_work']['elapsed'];p._activity(30)
    check(obj==before and plan['keepsake_work']['elapsed']==clock,'pause holds the physical page and native animation clock')
    check(speech_facts()['keepsake']['paused'],'conversation reports a paused read truthfully')
    g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.sync();weather();obj=p.object_state('ancient_tome')
    check(p.state['plan']['paused'] and obj['keepsake']==before['keepsake'],'full-game save reload preserves the open book and pauses its pending action')
    p.cancel();check(obj['uses']==uses and obj['keepsake']['page']==(start_page+1)%8,'cancelling after contact keeps the page without a completed-use reward')
    iid,obj=own('ancient_tome');p.start('item','ancient_tome');plan=p.state['plan'];g.treasure.found_treasures.pop('ancient_tome');p.sync();p._activity(10)
    check(p.state['plan'] is None and obj['uses']==uses,'ownership loss cancels a queued read without rewards')
    check('keepsake' not in speech_facts(),'an absent book is not supplied as a current activity')
    iid,obj=own('rain_barrel');obj['keepsake']['litres']=23.4;p.start('item','rain_barrel',instance=iid)
    check('litres_collected' not in speech_facts()['keepsake'],'walking to the barrel does not expose a gauge before arrival')
    plan=p.state['plan'];g.renderer.duck_pos.x,g.renderer.duck_pos.y=plan['destination'];plan['phase']='act'
    check(speech_facts()['keepsake']['litres_collected']==23.4,'chat uses actual collected rainwater from the selected barrel')
    iid,obj=own('friendship_card');p.start('item','friendship_card');p.state['plan']['phase']='act'
    check(speech_facts()['keepsake']['visible_words']==k.ITEMS['friendship_card']['reading']['cover'],'a closed card does not reveal unread interior words')
    obj['keepsake']['open']=1
    check('YOU SHOWED UP.' in speech_facts()['keepsake']['visible_words'],'an open card supplies its real written message')
    for item in ('ancient_tome','rain_barrel','friendship_card'):
        iid,obj=own(item);p.start('item',item,instance=iid)
        for _ in range(600):
            step()
            if p.state['plan'] and p.state['plan']['keepsake_work']['elapsed']>12:
                s=snapshot(g,g.renderer);s['review']=item;frames.append(s);break
    out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
    (out/'keepsake-frames.json').write_text(json.dumps(frames));(out/'keepsake-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames)),indent=2))
    print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames))))
    if '--serve' in sys.argv:
        item='treasure_chest';iid,obj=own(item,True)
        def emit():
            p._cache=None
            copies=[a.instance for a in p.placements if a.item_id==item]
            print(json.dumps(dict(type='physical_frame',frame=dict(scene=snapshot(g,g.renderer),copies=copies,item=item))),flush=True)
        emit()
        for line in sys.stdin:
            command=json.loads(line)
            if command.get('type')=='quit':break
            if command.get('type')=='test_fixture':
                item=command['item'];iid,obj=own(item)
                if item=='ancient_tome':obj['keepsake'].update(page=0,bookmark=0,studies=0,open=0)
                if item=='rain_barrel':obj['keepsake']['litres']=12
            elif command.get('type')=='test_rain':k.update(p,item,obj,600,True,True,1,20)
            elif command.get('type')=='test_advance':
                if command.get('until') in ('contact','page'):
                    for _ in range(800):
                        step()
                        work=(p.state['plan'] or {}).get('keepsake_work',{})
                        if (work.get('events') if command['until']=='page' else work.get('elapsed',0)>=10):break
                else:finish()
            elif command.get('type')=='pond':p.command(command);p.sync()
            emit()
finally:
    g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
    if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
    sound_engine.shutdown()
