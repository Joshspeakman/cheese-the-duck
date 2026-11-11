"""Exercise actual wardrobes, saved materials, care contact and cancellation."""
import os,sys,tempfile,json,copy,math
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT))
os.environ['CHEESE_SAVE_DIR']=tempfile.mkdtemp(prefix='cheese-accessories-');os.environ['SDL_AUDIODRIVER']='dummy'
from engine import host,headwear
from engine.scene import snapshot,equipped_wearables
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
  p.sync()
  if item in headwear.PROFILES:check(item in headwear.selected_items(g),item+' native material selection matches the equipped visible item')
 def inventory():return copy.deepcopy((g.inventory.to_dict(),g.materials.get_all_materials(),g.habitat.currency,g.habitat.owned_items,g.outfits.owned_items,g.seasonal_clothing.wardrobe.owned_items))
 def capture(item):care_frames.append(dict(id=item,scene=snapshot(g,g.renderer)))
 def ready(item):
  headwear.cancel(p);equip(item);p.state['apparel_care']={};p.state['apparel']={}
  headwear.state(p,item).update(wet=.8,snow=.7,fog=.75,wind=.9,soil=.65,slack=.6)
 for item,blueprint in headwear.ACCESSORIES.items():
  equip(item);before=inventory();headwear.update(p,120,'rainy',.8,10,.5);s=headwear.state(p,item)
  check(0<s['wet']<1 and s['wind']==.5,item+' worn surface collects actual rain')
  frozen=copy.deepcopy(p.state);headwear.snapshot(p)[item]['wet']=99;headwear.care_snapshot(p)
  check(p.state==frozen,item+' render snapshots cannot mutate saved materials')
  frames.append(dict(id=item,scene=snapshot(g,g.renderer)))
  previous=copy.deepcopy(s);clear();headwear.update(p,120,'snowy',1,-5,.9)
  check(s['wet']<previous['wet'] and s['snow']==0 and s['phase']==previous['phase'] and s['wind']==0,item+' stored accessory stays out of weather and motion')
  check(inventory()==before,item+' weather neither grants nor consumes possessions')
 # Renderer and native state must resolve conflicts across all three wardrobes.
 equip('summer_sunglasses');equip('glasses_nerd',False)
 check(headwear.selected_items(g)==['glasses_nerd'],'shop face wins over a covered seasonal accessory')
 p.state['apparel']={};headwear.update(p,90,'snowy',1,-5,.4)
 check(headwear.state(p,'glasses_nerd')['fog']>.5 and headwear.state(p,'summer_sunglasses')['fog']==0,'only the visible cold lens collects fog')
 equip('headphones');equip('halo',False)
 check('headphones' not in headwear.selected_items(g),'an unconstructed above-head cosmetic still suppresses hidden headphones')
 for age in ('egg','hatchling','duckling','juvenile','young_adult','adult','mature','elder','legendary'):
  g.duck.growth_stage=age;g.duck_store.sync_from_duck(g.duck);clear()
  g.habitat.equip_cosmetic('glasses_nerd');p.sync();p.state['apparel']={};headwear.update(p,60,'rainy',1,15,.4)
  check((headwear.state(p,'glasses_nerd')['wet']>0)==(age!='egg'),age+' exposes only a hatched fitted face')
  frames.append(dict(id='glasses_nerd',scene=snapshot(g,g.renderer)))
 g.duck.growth_stage='adult';g.duck_store.sync_from_duck(g.duck)
 equip('scarf_red');p.state['apparel']={};g.renderer.duck_pos.set_state_by_name('walking',120)
 headwear.update(p,60,'sunny',0,20,.6);s=headwear.state(p,'scarf_red')
 check(s['slack']>0 and s['soil']>0,'walking and dry wind loosen and soil the actual worn cloth')
 old=copy.deepcopy(s);headwear.update(p,300,'rainy',1,-5,1,offline=True)
 check(s['slack']==old['slack'] and s['soil']==old['soil'] and s['phase']==old['phase'],'offline time does not invent dressing gestures or walking wear')
 g.renderer.duck_pos.set_state_by_name('idle',1);g.duck.current_action=None
 for item in headwear.ACCESSORIES:
  for action,spec in headwear.ACCESSORY_CARE.items():
   if not headwear.suited(item,action):continue
   ready(item);before=inventory();s=headwear.state(p,item);old=s[spec['material']]
   check(headwear.request(p,item,action)[0],item+'/'+action+' starts through native wardrobe care')
   capture(item);headwear.care_step(p,spec['contact']-.01);capture(item)
   check(s[spec['material']]==old,item+'/'+action+' has no effect before contact')
   headwear.care_step(p,.01);capture(item);expected=old*spec['retained']
   check(abs(s[spec['material']]-expected)<1e-9,item+'/'+action+' contact changes saved material once')
   if action=='wipe_lenses':check(s['wet']==.4 and s['soil']==.39,'lens cloth also removes water and grime')
   headwear.care_step(p,.2);capture(item);check(s[spec['material']]==expected,'held contact cannot duplicate the effect')
   headwear.care_step(p,spec['duration']);capture(item)
   check(not p.state['apparel_care'].get('active') and not p.busy,'release frees the actor')
   check(not headwear.request(p,item,action)[0],'care respects its saved cooldown')
   check(inventory()==before,'wardrobe care does not create inventory or currency')
 for interrupt in ('unequip','walk','action','plan','offline','urgent_need','travel'):
  ready('scarf_red');headwear.request(p,'scarf_red','wring_scarf');headwear.care_step(p,.8)
  s=headwear.state(p,'scarf_red');old=s['wet'];pos=g.renderer.duck_pos;x=pos.x;location=p.location
  if interrupt=='unequip':clear()
  elif interrupt=='walk':pos.x+=3
  elif interrupt=='action':g.duck.current_action='feed'
  elif interrupt=='plan':p.state['plan']={'kind':'rest'}
  elif interrupt=='urgent_need':g.duck.needs.energy=0;g.duck_store.sync_from_duck(g.duck)
  elif interrupt=='travel':p.location='forest'
  headwear.care_step(p,8,offline=interrupt=='offline')
  check(not p.state['apparel_care'].get('active') and s['wet']==old,interrupt+' cancels before contact without a free effect')
  pos.x=x;p.location=location;g.duck.current_action=None;p.state['plan']=None;g.duck.needs.energy=90;g.duck_store.sync_from_duck(g.duck)
 ready('scarf_red');equip('glasses_nerd',False);equip('headphones',False);equip('hat_blue',False)
 for item in headwear.selected_items(g):headwear.state(p,item).update(wet=.8,snow=.7,fog=.75,soil=.6,slack=.6)
 check(len(headwear.selected_items(g))==4,'head, face, neck and headphones coexist in distinct render slots')
 ui_scene=snapshot(g,g.renderer);p._cache=None;ui_scene['living']=p.snapshot()
 check(len(ui_scene['duck']['hatCare']['items'])==4,'the real notebook receives all four equipped care inventories')
 p.command(dict(action='hat_care',target='glasses_nerd',text='wipe_lenses'))
 check(p.state['apparel_care']['active']['item']=='glasses_nerd','UI command addresses the selected accessory rather than the first hat')
 check(not headwear.request(p,'scarf_red','wring_scarf')[0],'one actor cannot perform two simultaneous clothing care actions')
 headwear.care_step(p,3.4);saved=copy.deepcopy(p.save());loaded=LivingPond(saved)
 check(not loaded.state['apparel_care'].get('active') and loaded.state['apparel']==p.state['apparel'] and loaded.state['apparel_care']['waits']==p.state['apparel_care']['waits'],'reload retains contacted materials and cooldowns without replaying unfinished hands');loaded.minds.close()
 headwear.cancel(p);g._save_game();g._flush_pending_save();saved=copy.deepcopy(p.state['apparel']);g._load_game();p=g.living_pond;p.state['auto']=False;p.sync()
 check(saved==p.state['apparel'],'full game save/load preserves accessory material records')
 ready('glasses_nerd');p.state['auto']=True;p.state['next_decision']=p.state['elapsed']+1000;p.advance(.1)
 check(p.state['apparel_care']['active']['id']=='wipe_lenses','ordinary simulation chooses lens care from saved fog')
 headwear.cancel(p);p.state['apparel_care']={};p.state['apparel']={};headwear.care_step(p,.1)
 check(not p.state['apparel_care'].get('active'),'dry clean secure accessories do not invent a reason for a care loop')
 p.state['auto']=False
 s=headwear.state(p,'glasses_nerd');s.update(wet=float('nan'),snow=-9,phase=float('inf'),fog='bad',soil=5,slack=-5);headwear.state(p,'glasses_nerd')
 check(all(math.isfinite(v) for v in s.values()) and s['soil']==1 and s['slack']==0,'optional material migration is finite and bounded')
 out=ROOT/'engine/artifacts/animation-milestone';out.mkdir(parents=True,exist_ok=True)
 for name,value in (('frames',frames),('care-frames',care_frames),('journal-scene',ui_scene)):(out/('accessories-'+name+'.json')).write_text(json.dumps(value))
 (out/'accessories-native.json').write_text(json.dumps(dict(result='PASS',checks=checks,frames=len(frames),careFrames=len(care_frames)),indent=2));print(json.dumps(dict(result='PASS',checks=len(checks),frames=len(frames),careFrames=len(care_frames))))
finally:
 g.living_pond.minds.close();g._save_executor.shutdown(wait=True)
 if getattr(g,'_talk_executor',None):g._talk_executor.shutdown(wait=False)
 sound_engine.shutdown()
