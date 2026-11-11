"""Real wardrobe, terrain, two-foot contacts, interruptions and saves."""
import os,sys,tempfile,json,copy,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-footwear-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,headwear,footwear
from engine.scene import snapshot
from engine.living_world import LivingPond
from engine.terrain import water_at
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
 def land():
  pos=g.renderer.duck_pos;pos.cancel_movement();pos.x=66;pos.y=8;pos.set_state_by_name('idle',1);p.location='Home Pond'
  check(not water_at(p.location,pos.x,pos.y,p.biome),'fixture has actual dry land')
 def clear():
  g.habitat.equipped_cosmetics.clear();g.seasonal_clothing.wardrobe.equipped.clear()
  for slot in OutfitSlot:setattr(g.outfits.current_outfit,slot.value,None)
 def equip(item):
  clear()
  if item in OUTFIT_ITEMS:
   if item not in g.outfits.owned_items:g.outfits.owned_items.append(item)
   check(g.outfits.equip_item(item)[0],item+' original outfit equip succeeds')
  else:g.seasonal_clothing.add_item(item);check(g.seasonal_clothing.equip_item(item),item+' original seasonal equip succeeds')
  p.sync();check(item in headwear.selected_items(g),item+' native slot follows visible footwear')
 def inventory():return copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.outfits.owned_items,g.seasonal_clothing.wardrobe.owned_items))
 def ready(item):
  headwear.cancel(p);land();equip(item);p.state['apparel_care']={};p.state['apparel']={}
  s=headwear.state(p,item)
  for key in footwear.FIELDS:
   s[key+'_left']=.8;s[key+'_right']=.6
  footwear.summarize(s);return s
 def capture(item):care_frames.append(dict(id=item,scene=snapshot(g,g.renderer)))
 land()
 for item in footwear.BLUEPRINTS:
  equip(item);before=inventory();p.state['apparel']={};g.renderer.duck_pos.set_state_by_name('walking',120)
  headwear.update(p,100,'rainy',.8,12,.4);s=headwear.state(p,item)
  check(s['wet_left']>0 and s['soil_left']>0 and s['slack_left']>0,item+' walking in rain wets and muddies actual shoes')
  frozen=copy.deepcopy(p.state);headwear.snapshot(p)[item]['soil_left']=99;headwear.care_snapshot(p)
  check(p.state==frozen,item+' snapshots do not mutate shoes')
  frames.append(dict(id=item,scene=snapshot(g,g.renderer)))
  old=copy.deepcopy(s);clear();headwear.update(p,120,'snowy',1,-5,.9)
  check(s['wet_left']<old['wet_left'] and s['snow_left']==0 and s['soil_left']==old['soil_left'] and s['slack_left']==old['slack_left'],item+' stored shoes dry without dirt, snow or invented wear')
  check(inventory()==before,item+' weather changes no possessions')
  equip(item);g.renderer.duck_pos.x=66;g.renderer.duck_pos.y=40;g.renderer.duck_pos.set_state_by_name('swimming',120)
  check(water_at(p.location,66,40,p.biome),'swimming fixture is real water');headwear.update(p,100,'sunny',0,20,0)
  check(s['wet_left']>.8 and not footwear.solid_footing(p),item+' submerged shoes become wet')
  check(all(not o['enabled'] and 'solid footing' in o['reason'] for o in headwear.options(p,item)),item+' care cannot balance on open water')
  check(not headwear.request(p,item,'brush_shoe_snow')[0],item+' rejects a care request in water')
  old=copy.deepcopy(s);headwear.update(p,300,'rainy',1,10,.8,offline=True)
  check(s['wet_left']<old['wet_left'] and s['soil_left']==old['soil_left'] and s['slack_left']==old['slack_left'] and s['phase']==old['phase'],item+' offline catch-up invents no footsteps')
  land()
 for age in ('egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
  g.duck.growth_stage=age;g.duck_store.sync_from_duck(g.duck);clear();g.outfits.equip_item('rain_boots');p.sync();p.state['apparel']={};headwear.update(p,60,'snowy',1,-5,.4)
  check((headwear.state(p,'rain_boots')['snow_left']>0)==(age!='egg'),age+' footwear exposure matches a hatched body');frames.append(dict(id='rain_boots',scene=snapshot(g,g.renderer)))
 g.duck.growth_stage='adult';g.duck_store.sync_from_duck(g.duck)
 for item in footwear.BLUEPRINTS:
  for action,spec in footwear.CARE.items():
   if not headwear.suited(item,action):continue
   s=ready(item);before=inventory();key=spec['material'];left=s[key+'_left'];right=s[key+'_right']
   check(headwear.request(p,item,action)[0],item+'/'+action+' begins on land');capture(item)
   headwear.care_step(p,spec['contacts'][0]-.01);capture(item);check(s[key+'_left']==left and s[key+'_right']==right,'neither shoe changes before contact')
   headwear.care_step(p,.02);capture(item)
   check(abs(s[key+'_left']-left*spec['retained'])<1e-9 and s[key+'_right']==right,'first contact only changes the left shoe')
   check(p.state['apparel_care']['active']['appliedFeet']==[0],'native contact ledger records the left shoe')
   first=copy.deepcopy(s);headwear.care_step(p,.1);check(s==first,'holding the left shoe applies no repeated effect')
   headwear.care_step(p,spec['contacts'][1]-spec['contacts'][0]-.12);capture(item);check(s[key+'_right']==right,'right shoe waits for its own contact')
   headwear.care_step(p,.02);capture(item);check(abs(s[key+'_right']-right*spec['retained'])<1e-9,'second contact changes the right shoe')
   headwear.care_step(p,.2);capture(item);check(abs(s[key+'_right']-right*spec['retained'])<1e-9,'holding the right shoe applies no repeated effect')
   headwear.care_step(p,spec['duration']);capture(item);check(not p.state['apparel_care'].get('active'),'pair care releases Cheese')
   check(not headwear.request(p,item,action)[0],'pair care respects its cooldown');check(inventory()==before,'pair care changes no possessions')
 for interrupt in ('unequip','walk','water','action','plan','offline','urgent_need','travel'):
  s=ready('rain_boots');headwear.request(p,'rain_boots','scrape_soles');headwear.care_step(p,2.6);first=copy.deepcopy(s);pos=g.renderer.duck_pos
  if interrupt=='unequip':clear()
  elif interrupt=='walk':pos.x+=3
  elif interrupt=='water':pos.y=40
  elif interrupt=='action':g.duck.current_action='feed'
  elif interrupt=='plan':p.state['plan']={'kind':'rest'}
  elif interrupt=='urgent_need':g.duck.needs.energy=0;g.duck_store.sync_from_duck(g.duck)
  elif interrupt=='travel':p.location='forest'
  headwear.care_step(p,9,offline=interrupt=='offline')
  check(not p.state['apparel_care'].get('active') and s==first,interrupt+' preserves only the first completed foot contact')
  g.duck.current_action=None;p.state['plan']=None;g.duck.needs.energy=90;g.duck_store.sync_from_duck(g.duck)
 s=ready('ice_skates');headwear.request(p,'ice_skates','tie_skates');headwear.care_step(p,2.9);saved=copy.deepcopy(p.save());loaded=LivingPond(saved)
 check(not loaded.state['apparel_care'].get('active') and loaded.state['apparel']==p.state['apparel'] and loaded.state['apparel_care']['waits']==p.state['apparel_care']['waits'],'load preserves one tightened skate without replaying the other');loaded.minds.close()
 headwear.cancel(p);g._save_game();g._flush_pending_save();saved=copy.deepcopy(p.state['apparel']);g._load_game();p=g.living_pond;p.state['auto']=False;p.sync()
 check(saved==p.state['apparel'],'full native save/load retains both shoes independently')
 s=ready('rain_boots');p.state['auto']=True;p.state['next_decision']=p.state['elapsed']+1000;p.advance(.1)
 check(p.state['apparel_care']['active']['id']=='brush_shoe_snow','autonomy chooses actual snow on the shoes');headwear.cancel(p);p.state['auto']=False
 p.state['apparel']={};p.state['apparel_care']={};headwear.care_step(p,1)
 check(not p.state['apparel_care'].get('active'),'clean dry footwear does not create a care loop')
 s=headwear.state(p,'rain_boots');s.update(wet_left=float('nan'),soil_right=7,slack_left='bad');headwear.state(p,'rain_boots')
 check(s['wet_left']==0 and s['soil_right']==1 and s['slack_left']==0,'optional per-foot state is bounded on migration')
 equip('rain_boots');g.renderer.duck_pos.set_state_by_name('walking',120);p.state['apparel']={};headwear.update(p,100,'rainy',.6,10,.3);whole=copy.deepcopy(p.state['apparel']);p.state['apparel']={}
 for _ in range(100):headwear.update(p,1,'rainy',.6,10,.3)
 check(all(abs(p.state['apparel'][i][k]-v)<1e-9 for i,r in whole.items() for k,v in r.items()),'footwear materials are independent of time-step partitioning')
 s=ready('ice_skates');ui_scene=snapshot(g,g.renderer);p._cache=None;ui_scene['living']=p.snapshot()
 out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
 for name,value in (('frames',frames),('care-frames',care_frames),('journal-scene',ui_scene)):(out/('footwear-'+name+'.json')).write_text(json.dumps(value))
 (out/'footwear-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames),careFrames=len(care_frames)),indent=2));print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),careFrames=len(care_frames))))
finally:
 g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
 if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
 sound_engine.shutdown()
