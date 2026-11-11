"""Real wardrobe selection, saved hat materials and read-only scene projection."""
import os,sys,tempfile,json,copy,math
from pathlib import Path
from datetime import datetime
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-headwear-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,headwear
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.habitat import PlacedItem
from world.atmosphere import Weather,WeatherType
from world.shop import SHOP_ITEMS
from duck.outfits import OUTFIT_ITEMS
from duck.seasonal_clothing import ALL_SEASONAL_ITEMS
from audio.sound import sound_engine
sys.stdout=host.WIRE;checks=[];frames=[]
def check(ok,label):assert ok,label;checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
 g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
 g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
 g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
 p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=1e9
 def clear():
  g.habitat.equipped_cosmetics.clear();g.outfits.current_outfit.hat=None;g.seasonal_clothing.wardrobe.equipped.clear()
 def equip(item):
  clear()
  if item in SHOP_ITEMS:
   if item not in g.habitat.owned_items:g.habitat.owned_items.append(item)
   g.habitat.equip_cosmetic(item)
  elif item in OUTFIT_ITEMS:
   if item not in g.outfits.owned_items:g.outfits.owned_items.append(item)
   check(g.outfits.equip_item(item)[0],item+' original outfit handler equips')
  else:
   g.seasonal_clothing.add_item(item);check(g.seasonal_clothing.equip_item(item),item+' original seasonal handler equips')
  p.sync();check(headwear.selected(g)==item,item+' original wardrobe selection is authoritative')
 def weather(kind):g.atmosphere.current_weather=Weather(kind,.8,1,datetime.now().isoformat());p.sync();p.weather_type=kind.value
 def inventory():return copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.habitat.owned_items,g.outfits.owned_items,g.seasonal_clothing.wardrobe.owned_items))
 g.duck.growth_stage='adult';g.duck_store.sync_from_duck(g.duck)
 for n,(item,blueprint) in enumerate(headwear.BLUEPRINTS.items()):
  equip(item);before=inventory();weather(WeatherType.RAINY);headwear.update(p,120,'rainy',.8,10,.5);s=headwear.state(p,item)
  check(0<s['wet']<1 and s['wind']==.5,item+' actual worn material becomes wet')
  frozen=copy.deepcopy(p.state['apparel']);view=headwear.snapshot(p);view[item]['wet']=99
  check(p.state['apparel']==frozen,item+' render snapshot cannot mutate wardrobe state')
  scene=snapshot(g,g.renderer);frames.append(dict(id=item,scene=scene));check(scene['duck']['apparel'][item]==s,item+' actual scene carries current material')
  previous=copy.deepcopy(s);clear();headwear.update(p,120,'rainy',1,10,.9)
  check(s['wet']<previous['wet'] and s['phase']==previous['phase'] and s['wind']==0,item+' putting away stops wind motion and dries the real material')
  check(inventory()==before,item+' weather neither grants nor consumes possessions')
 # One worn slot across all original wardrobe systems, matching visual priority.
 equip('santa_hat');g.seasonal_clothing.add_item('winter_santa_hat');g.seasonal_clothing.equip_item('winter_santa_hat');g.habitat.equip_cosmetic('hat_blue')
 check(headwear.selected(g)=='hat_blue','shop hat wins the same visual conflict as the renderer')
 p.state['apparel']={};headwear.update(p,120,'snowy',1,-5,.8)
 check(headwear.state(p,'hat_blue')['snow']>.5 and headwear.state(p,'santa_hat')['snow']==0 and headwear.state(p,'winter_santa_hat')['snow']==0,'covered-up selections do not collect another hat\'s snow')
 for age in ('egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
  g.duck.growth_stage=age;g.duck_store.sync_from_duck(g.duck);p.state['apparel']={};headwear.update(p,60,'rainy',1,15,.4)
  check((headwear.state(p,'hat_blue')['wet']>0)==(age!='egg'),age+' exposes only an actual cosmetic head')
  frames.append(dict(id='hat_blue',scene=snapshot(g,g.renderer)))
 g.duck.growth_stage='adult';g.duck_store.sync_from_duck(g.duck);equip('space_helmet');p.state['apparel']={};headwear.update(p,80,'snowy',.8,-5,.2)
 check(headwear.state(p,'space_helmet')['fog']>.5,'cold worn helmet builds saved visor fog')
 before=copy.deepcopy(p.state['apparel']);headwear.update(p,600,'rainy',1,18,.9,offline=True)
 check(headwear.state(p,'space_helmet')['fog']<before['space_helmet']['fog'] and headwear.state(p,'space_helmet')['phase']==before['space_helmet']['phase'],'offline storage dries without replaying a wearer animation')
 # A reachable real roof stops exposure only after Cheese gets inside.
 equip('hat_red');weather(WeatherType.RAINY);g.habitat.owned_items.append('wooden_cottage');g.habitat.placed_items=[PlacedItem('wooden_cottage',8,6)];p.sync()
 for k in ('energy','hunger','fun','cleanliness','social'):setattr(g.duck.needs,k,90)
 g.duck_store.sync_from_duck(g.duck);check(p.start('rest','wooden_cottage')[0],'actual cottage accepts a shelter plan')
 check(not headwear.sheltered(p),'a plan to seek shelter does not already protect the hat')
 for _ in range(500):
  if p.state['plan'] and p.state['plan']['phase']=='act':break
  pos=g.renderer.duck_pos;pos._state_start_time-=.2;pos.update(.2);p.state['elapsed']+=.2;p._activity(.2)
 check(headwear.sheltered(p),'arriving inside the actual roof protects the hat')
 s=headwear.state(p,'hat_red');s['wet']=.7;headwear.update(p,120,'rainy',1,10,.9)
 check(s['wet']<.7 and s['wind']==0,'sheltered fabric dries in ongoing rain')
 p.cancel();before=s['wet'];headwear.update(p,120,'rainy',1,10,.9);check(s['wet']>before,'leaving the roof restores real exposure')
 saved=copy.deepcopy(p.state['apparel']);g._save_game();g._flush_pending_save();g._load_game();p=g.living_pond;p.state['auto']=False;p.sync()
 check(p.state['apparel']==saved,'native save/load preserves all hat materials and phases')
 blank=LivingPond();check(blank.state['apparel']=={},'older saves can start without apparel records');blank.minds.close()
 # Native environment integration, not only a direct updater call.
 equip('hat_red');p.state['apparel']={};weather(WeatherType.RAINY);p._weather_front=lambda offline:('rainy',.8);p.state['weather'].setdefault(p.biome,{})
 p._environment(120,False);check(headwear.state(p,'hat_red')['wet']>0,'ordinary native environment updates the equipped hat')
 p.state['apparel']={};headwear.update(p,120,'double_rainbow',1,20,.1);check(headwear.state(p,'hat_red')['wet']==0,'rainbows do not soak the hat')
 # Numeric migration and partitioned clocks are finite and time-step stable.
 s=headwear.state(p,'hat_red');s.update(wet=float('nan'),snow=-9,phase=float('inf'),fog='bad');headwear.state(p,'hat_red')
 check(all(math.isfinite(v) for v in s.values()),'invalid optional material values become finite')
 p.state['apparel']={};headwear.update(p,100,'rainy',.6,10,.3);whole=copy.deepcopy(p.state['apparel']);p.state['apparel']={}
 for _ in range(100):headwear.update(p,1,'rainy',.6,10,.3)
 check(all(abs(p.state['apparel'][i][k]-v)<1e-9 for i,r in whole.items() for k,v in r.items()),'material integration agrees across time steps')
 # Actual wardrobe care: contact changes the same saved cloth that weather wets.
 care_frames=[];p.cancel();g.duck.current_action=None;g.renderer.duck_pos.set_state_by_name('idle',1)
 def ready(item):
  headwear.cancel(p);equip(item);p.state['apparel_care']={};p.state['apparel']={}
  headwear.state(p,item).update(wet=.8,snow=.7,fog=.75 if headwear.BLUEPRINTS[item]['shape']=='helmet' else 0,wind=.9)
 def capture(item):care_frames.append(dict(id=item,scene=snapshot(g,g.renderer)))
 for item in headwear.BLUEPRINTS:
  for action,spec in headwear.CARE.items():
   if not headwear.suited(item,action):continue
   ready(item);before=inventory();s=headwear.state(p,item);old=s[spec['material']]
   check(headwear.request(p,item,action)[0],item+'/'+action+' accepts real material care')
   snapshot_before=copy.deepcopy(p.state);headwear.care_snapshot(p)
   check(p.state==snapshot_before,'care snapshot is read-only')
   capture(item);headwear.care_step(p,spec['contact']-.01);capture(item)
   check(s[spec['material']]==old,item+'/'+action+' no effect before contact')
   headwear.care_step(p,.01);capture(item)
   check(p.state['apparel_care']['active']['applied'],item+'/'+action+' native contact recorded')
   expected=old*spec.get('retained',1)
   check(abs(s[spec['material']]-expected)<1e-9,item+'/'+action+' changes only the contacted material')
   headwear.care_step(p,.2);capture(item);check(s[spec['material']]==expected,'same contact cannot apply twice')
   headwear.care_step(p,spec['duration']);capture(item)
   check(not p.state['apparel_care'].get('active') and not p.busy,'release frees the real actor')
   check(not headwear.request(p,item,action)[0],'repeated care respects its native cooldown')
   check(inventory()==before,'small clothing care never grants items or changes currency')
 for age in ('egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
  g.duck.growth_stage=age;g.duck_store.sync_from_duck(g.duck)
  # Equip uses the original wardrobe even while the egg has no visible head.
  if age=='egg':
   clear();g.habitat.equip_cosmetic('hat_red');p.state['apparel_care']={}
   check(not headwear.request(p,'hat_red','brush_snow')[0],'unhatched Cheese cannot perform dressing gestures');continue
  ready('hat_red');check(headwear.request(p,'hat_red','brush_snow')[0],age+' can reach his own hat')
  headwear.care_step(p,3);capture('hat_red')
 g.duck.growth_stage='adult';g.duck_store.sync_from_duck(g.duck)
 for interrupt in ('unequip','walk','action','plan','offline','urgent_need'):
  ready('hat_red');headwear.request(p,'hat_red','brush_snow');headwear.care_step(p,.8)
  s=headwear.state(p,'hat_red');old=s['snow'];pos=g.renderer.duck_pos;x=pos.x
  if interrupt=='unequip':clear()
  elif interrupt=='walk':pos.x+=3
  elif interrupt=='action':g.duck.current_action='feed'
  elif interrupt=='plan':p.state['plan']={'kind':'rest'}
  elif interrupt=='urgent_need':g.duck.needs.energy=0;g.duck_store.sync_from_duck(g.duck)
  headwear.care_step(p,6,offline=interrupt=='offline')
  check(not p.state['apparel_care'].get('active') and s['snow']==old,interrupt+' cancels before contact without a free material effect')
  pos.x=x;g.duck.current_action=None;p.state['plan']=None;g.duck.needs.energy=90;g.duck_store.sync_from_duck(g.duck)
 ready('space_helmet');headwear.request(p,'space_helmet','wipe_visor');headwear.care_step(p,3.2)
 saved=copy.deepcopy(p.save());loaded=LivingPond(saved)
 check(not loaded.state['apparel_care'].get('active') and loaded.state['apparel']['space_helmet']['fog']==p.state['apparel']['space_helmet']['fog'],'save/load keeps completed contact and cooldown, without replaying a hand pose');loaded.minds.close()
 ready('hat_blue');ui_scene=snapshot(g,g.renderer);p._cache=None;ui_scene['living']=p.snapshot()
 p.command(dict(action='hat_care',target='hat_blue',text='brush_snow'))
 check(p.state['apparel_care']['active']['id']=='brush_snow','notebook command reaches actual wardrobe care');headwear.cancel(p)
 ready('hat_red');g.duck.current_action='idle';check(headwear.request(p,'hat_red','brush_snow')[0],'legacy idle state after a journey permits clothing care');headwear.cancel(p);g.duck.current_action=None
 ready('hat_red');p.state['auto']=True;p.state['next_decision']=p.state['elapsed']+1000
 p.advance(.1);check(p.state['apparel_care']['active']['id']=='brush_snow','ordinary live simulation chooses care from the accumulated snow')
 headwear.cancel(p);p.state['apparel_care']={};p.state['apparel']={};weather(WeatherType.SUNNY);p._weather_front=lambda offline:('sunny',0);p.state['ecology']['wind']=0
 headwear.care_step(p,.1);check(not p.state['apparel_care'].get('active'),'dry calm weather does not invent a reason for clothing care')
 p.state['auto']=False
 out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
 (out/'headwear-care-frames.json').write_text(json.dumps(care_frames))
 (out/'headwear-journal-scene.json').write_text(json.dumps(ui_scene))
 (out/'headwear-frames.json').write_text(json.dumps(frames));(out/'headwear-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames),careFrames=len(care_frames)),indent=2));print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),careFrames=len(care_frames))))
finally:
 g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
 if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
 sound_engine.shutdown()
