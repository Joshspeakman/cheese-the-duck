"""Actual worn cloth, environment response, native care contacts and saved state."""
import os,sys,tempfile,json,copy,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-garments-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,headwear
from engine.scene import snapshot
from engine.living_world import LivingPond
from world.shop import SHOP_ITEMS
from duck.outfits import OUTFIT_ITEMS,OutfitSlot
from audio.sound import sound_engine
sys.stdout=host.WIRE;checks=[];frames=[];care_frames=[]
def check(ok,label):assert ok,label;checks.append(label)
t=host.DesktopInput();g=host.DesktopGame(terminal=t,renderer_factory=host.CanvasRenderer);t.game=g;g.renderer.game=g;g.renderer.present=lambda lines:None
try:
 g._running=True;g._start_new_game();g._flush_pending_save();g._state='playing';g.renderer._show_talk=False;sound_engine.enabled=False
 g.renderer._viewport_width=132;g.renderer._viewport_height=42;g.renderer._update_camera(132,42)
 g.day_night.get_current_hour=lambda:12;g.day_night.get_current_minute=lambda:0
 p=g.living_pond;p.state['auto']=False;p.minds.model.state['next_social']=1e9
 for k in ('energy','hunger','fun','cleanliness','social'):setattr(g.duck.needs,k,90)
 g.duck.growth_stage='adult';g.duck_store.sync_from_duck(g.duck)
 def clear():
  g.habitat.equipped_cosmetics.clear();g.seasonal_clothing.wardrobe.equipped.clear()
  for slot in OutfitSlot:setattr(g.outfits.current_outfit,slot.value,None)
 def equip(item,replace=True):
  if replace:clear()
  if item in SHOP_ITEMS:
   if item not in g.habitat.owned_items:g.habitat.owned_items.append(item)
   g.habitat.equip_cosmetic(item);check(item in g.habitat.equipped_cosmetics.values(),item+' original shop equip succeeds')
  elif item in OUTFIT_ITEMS:
   if item not in g.outfits.owned_items:g.outfits.owned_items.append(item)
   check(g.outfits.equip_item(item)[0],item+' original outfit equip succeeds')
  else:
   g.seasonal_clothing.add_item(item);check(g.seasonal_clothing.equip_item(item),item+' original seasonal equip succeeds')
  p.sync();check(item in headwear.selected_items(g),item+' native material selection matches visible wardrobe')
 def inventory():return copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.habitat.owned_items,g.outfits.owned_items,g.seasonal_clothing.wardrobe.owned_items))
 def capture(item):care_frames.append(dict(id=item,scene=snapshot(g,g.renderer)))
 def ready(item):
  headwear.cancel(p);equip(item);p.state['apparel_care']={};p.state['apparel']={}
  headwear.state(p,item).update(wet=.8,snow=.7,wind=.9,soil=.65,slack=.6,crease=.7)
 for item in headwear.GARMENTS:
  equip(item);before=inventory();headwear.update(p,120,'rainy',.8,10,.5);s=headwear.state(p,item)
  check(0<s['wet']<1 and s['wind']==.5,item+' worn fabric collects rain')
  frozen=copy.deepcopy(p.state);headwear.snapshot(p)[item]['wet']=99;headwear.care_snapshot(p)
  check(p.state==frozen,item+' render snapshots do not mutate saved cloth')
  frames.append(dict(id=item,scene=snapshot(g,g.renderer)))
  old=copy.deepcopy(s);clear();headwear.update(p,120,'snowy',1,-5,.9)
  check(s['wet']<old['wet'] and s['snow']==0 and s['phase']==old['phase'] and s['wind']==0,item+' stored cloth stays out of weather')
  check(inventory()==before,item+' exposure does not create possessions')
 equip('spring_raincoat');equip('tuxedo',False)
 check(headwear.selected_items(g)==['tuxedo'],'outfit selection suppresses the older seasonal body layer')
 p.state['apparel']={};headwear.update(p,120,'snowy',1,-5,.4)
 check(headwear.state(p,'tuxedo')['snow']>.5 and headwear.state(p,'spring_raincoat')['snow']==0,'hidden garments do not collect a visible coat\'s snow')
 for age in ('egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
  g.duck.growth_stage=age;g.duck_store.sync_from_duck(g.duck);clear();g.outfits.equip_item('tuxedo');p.sync()
  p.state['apparel']={};headwear.update(p,60,'rainy',1,15,.4)
  check((headwear.state(p,'tuxedo')['wet']>0)==(age!='egg'),age+' exposes cloth only on a hatched body')
  frames.append(dict(id='tuxedo',scene=snapshot(g,g.renderer)))
 g.duck.growth_stage='adult';g.duck_store.sync_from_duck(g.duck);equip('sweater_cozy');p.state['apparel']={}
 g.renderer.duck_pos.set_state_by_name('sleeping',120);headwear.update(p,60,'sunny',0,20,0);s=headwear.state(p,'sweater_cozy')
 check(s['crease']>0,'sleeping rumples the actual equipped sweater')
 old=copy.deepcopy(s);headwear.update(p,600,'stormy',1,-5,1,offline=True)
 check(s['crease']==old['crease'] and s['soil']==old['soil'] and s['slack']==old['slack'] and s['phase']==old['phase'],'offline time does not invent sleeping wear or garment animation')
 g.renderer.duck_pos.set_state_by_name('walking',120);headwear.update(p,60,'sunny',0,20,.8)
 check(s['slack']>0 and s['soil']>0 and s['crease']>old['crease'],'real walking and dusty gusts loosen and crease cloth')
 g.renderer.duck_pos.set_state_by_name('idle',1);g.duck.current_action=None
 for item in headwear.GARMENTS:
  for action,spec in headwear.GARMENT_CARE.items():
   if not headwear.suited(item,action):continue
   ready(item);before=inventory();s=headwear.state(p,item);old=s[spec['material']]
   check(headwear.request(p,item,action)[0],item+'/'+action+' starts through the native handler')
   capture(item);headwear.care_step(p,spec['contact']-.01);capture(item)
   check(s[spec['material']]==old,item+'/'+action+' has no effect before contact')
   headwear.care_step(p,.01);capture(item);expected=old*spec['retained']
   check(abs(s[spec['material']]-expected)<1e-9,item+'/'+action+' changes saved cloth at contact')
   headwear.care_step(p,.2);capture(item);check(s[spec['material']]==expected,'held contact applies only once')
   headwear.care_step(p,spec['duration']);capture(item)
   check(not p.state['apparel_care'].get('active') and not p.busy,'release frees Cheese')
   check(not headwear.request(p,item,action)[0],'clothing care respects its cooldown')
   check(inventory()==before,'clothing care does not consume or grant possessions')
 for interrupt in ('unequip','walk','action','plan','offline','urgent_need','travel'):
  ready('sweater_cozy');headwear.request(p,'sweater_cozy','wring_hem');headwear.care_step(p,.8)
  s=headwear.state(p,'sweater_cozy');old=s['wet'];pos=g.renderer.duck_pos;x=pos.x;location=p.location
  if interrupt=='unequip':clear()
  elif interrupt=='walk':pos.x+=3
  elif interrupt=='action':g.duck.current_action='feed'
  elif interrupt=='plan':p.state['plan']={'kind':'rest'}
  elif interrupt=='urgent_need':g.duck.needs.energy=0;g.duck_store.sync_from_duck(g.duck)
  elif interrupt=='travel':p.location='forest'
  headwear.care_step(p,9,offline=interrupt=='offline')
  check(not p.state['apparel_care'].get('active') and s['wet']==old,interrupt+' cancels without a free contact effect')
  pos.x=x;p.location=location;g.duck.current_action=None;p.state['plan']=None;g.duck.needs.energy=90;g.duck_store.sync_from_duck(g.duck)
 ready('raincoat');equip('cape_superhero',False);equip('scarf_red',False);equip('glasses_nerd',False)
 for item in headwear.selected_items(g):headwear.state(p,item).update(wet=.8,snow=.7,soil=.6,slack=.6,crease=.7)
 check(len(headwear.selected_items(g))==4,'body, cape, scarf and glasses keep separate native records')
 ui_scene=snapshot(g,g.renderer);p._cache=None;ui_scene['living']=p.snapshot()
 p.command(dict(action='hat_care',target='raincoat',text='shed_coat'))
 check(p.state['apparel_care']['active']['item']=='raincoat','notebook command addresses the actual worn coat')
 check(not headwear.request(p,'cape_superhero','shake_cape')[0],'only one dressing gesture can occupy Cheese')
 headwear.care_step(p,3.1);saved=copy.deepcopy(p.save());loaded=LivingPond(saved)
 check(not loaded.state['apparel_care'].get('active') and loaded.state['apparel']==p.state['apparel'] and loaded.state['apparel_care']['waits']==p.state['apparel_care']['waits'],'load retains contacted cloth and cooldowns without replaying unfinished hands');loaded.minds.close()
 headwear.cancel(p);g._save_game();g._flush_pending_save();saved=copy.deepcopy(p.state['apparel']);g._load_game();p=g.living_pond;p.state['auto']=False;p.sync()
 check(saved==p.state['apparel'],'full native save/load preserves every garment material')
 ready('sweater_cozy');p.state['auto']=True;p.state['next_decision']=p.state['elapsed']+1000;p.advance(.1)
 check(p.state['apparel_care']['active']['id']=='brush_garment_snow','ordinary simulation chooses care for accumulated shoulder snow')
 headwear.cancel(p);p.state['apparel_care']={};p.state['apparel']={};headwear.care_step(p,.1)
 check(not p.state['apparel_care'].get('active'),'dry clean smooth garments do not create a care loop')
 p.state['auto']=False
 s=headwear.state(p,'sweater_cozy');s.update(wet=float('nan'),snow=-9,phase=float('inf'),soil='bad',slack=-5,crease=5);headwear.state(p,'sweater_cozy')
 check(all(math.isfinite(v) for v in s.values()) and s['crease']==1 and s['slack']==0,'optional garment state migrates to finite bounded values')
 # Time partitioning must not change the weather or movement wear outcome.
 equip('sweater_cozy');g.renderer.duck_pos.set_state_by_name('walking',120);p.state['apparel']={};headwear.update(p,100,'rainy',.6,10,.3);whole=copy.deepcopy(p.state['apparel']);p.state['apparel']={}
 for _ in range(100):headwear.update(p,1,'rainy',.6,10,.3)
 check(all(abs(p.state['apparel'][i][k]-v)<1e-9 for i,r in whole.items() for k,v in r.items()),'material and crease integration is independent of time-step partitioning')
 out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
 for name,value in (('frames',frames),('care-frames',care_frames),('journal-scene',ui_scene)):(out/('garments-'+name+'.json')).write_text(json.dumps(value))
 (out/'garments-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames),careFrames=len(care_frames)),indent=2));print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),careFrames=len(care_frames))))
finally:
 g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
 if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
 sound_engine.shutdown()
