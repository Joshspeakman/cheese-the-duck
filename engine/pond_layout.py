"""Physical habitat layout: measured artwork, entry space and honest storage.

The existing 20 x 12 habitat coordinates remain the source of truth for walking,
save files and both renderers. This module never offsets a drawing alone.
"""
import hashlib
import json
import math
from pathlib import Path
from engine import terrain

DATA=Path(__file__).parent/'client/animation/object-footprints.json'
FOOTPRINTS=json.loads(DATA.read_text())['items']
GROUND_PATH=DATA.with_name('habitat-ground.json')
GROUND=json.loads(GROUND_PATH.read_text())
REVISION=hashlib.sha256(DATA.read_bytes()+GROUND_PATH.read_bytes()+terrain.DATA.read_bytes()).hexdigest()[:16]
WIDTH,HEIGHT=20,12

def finite(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)

def bounds(item,x,y,footprint=None):
    f=footprint or FOOTPRINTS.get(item,{'width':26,'height':18,'floor':False})
    # The largest live camera spans 132 x 42 world units, projected into
    # 192 x 47 ground cells. The drawing grows upward from its actual feet.
    w=f['width']*20/192+.5;h=f['height']*12/47
    box=dict(x=x-w/2,y=y-h,w=w,h=h+.65,floor=f['floor'])
    box['ground']=ground_bounds(item,box,y)
    return box

def overlaps(a,b):
    if a['floor']!=b['floor']:return False  # Rugs belong under furniture.
    return a['x']<b['x']+b['w'] and a['x']+a['w']>b['x'] and a['y']<b['y']+b['h'] and a['y']+a['h']>b['y']

def shoreline(x):
    gx=24+x*192/20
    return (terrain.bank_grid('Home Pond',gx)-46)*12/47

def ground_bounds(item,box,y):
    # Upright drawings rise from their feet. Flat mats/paths occupy their whole
    # drawn ground plane, including the back edge (important for floating pads).
    depth=(box['h']-.65 if box['floor'] else .35 if item in GROUND['waterItems']
           else max(.35,min(1.8,(box['h']-.65)*.18)))
    return dict(x=box['x'],y=y-depth,w=box['w'],h=depth+.35,floor=False)

def scenery():
    result=[]
    for feature in GROUND['scenery']:
        f=dict(feature)
        y=f.get('y',shoreline(f.get('shoreX',f['x']))+f.get('shoreOffset',0))
        f.update(y=y,box=dict(x=f['x']-f['width']/2,y=y-f['depth']/2,
                             w=f['width'],h=f['depth'],floor=False))
        result.append(f)
    return result

SCENERY=scenery()

def surface_fits(item,box,y,location='Home Pond',biome='pond'):
    return terrain.surface_fits(item,ground_bounds(item,box,y),location,biome)

class PondLayout:
    def __init__(self,habitat,obstacles=lambda:(),location='Home Pond',biome='pond'):
        self.habitat=habitat;self.obstacles=obstacles
        self.location=location;self.biome=biome;self.features=terrain.features(location,biome)

    def occupied(self,exclude='',instance=None):
        # Idle bobbing never changes the permanent space reservation.
        return [(p.item_id,p.x,p.y,None) for p in self.habitat.get_visible_placed_items()
                if (p.instance_id!=instance if instance is not None else p.item_id!=exclude)]+[
                    (*p[:3],p[4] if len(p)>4 else None) for p in self.obstacles() if len(p)<4 or p[3]!=instance]

    def eligible(self,item):
        from world.shop import get_item,ItemCategory
        definition=get_item(item)
        return item in self.habitat.owned_items and item in FOOTPRINTS and definition and definition.category!=ItemCategory.COSMETIC

    def check(self,item,x,y,instance=None,footprint=None):
        if not finite(x) or not finite(y):return False,'Choose a point inside the habitat.'
        if item not in FOOTPRINTS:return False,'This object does not have a placement drawing yet.'
        f=bounds(item,x,y,footprint)
        if f['x']<.2 or f['x']+f['w']>WIDTH-.2 or x>124*20/132 or y<1 or y>37*12/42:
            return False,'Leave room around the edge for the whole object.'
        # The visible upper sky can contain a tall roof; the ground anchor
        # must stay reachable. No object can be hidden above the window.
        if 46+y*47/12-(footprint or FOOTPRINTS[item])['height']<2:
            return False,'That tall object needs a spot farther down the bank.'
        if not surface_fits(item,f,y,self.location,self.biome):
            return False,'That belongs on the water.' if item in GROUND['waterItems'] else 'Keep its feet on the dry bank.'
        feet=ground_bounds(item,f,y)
        for feature in self.features:
            if overlaps(feet,feature['box']):
                return False,'Leave room for the '+feature['name'].lower()+'.'
        for other,ox,oy,shape in self.occupied(item,instance):
            other_box=bounds(other,ox,oy,shape)
            if f['floor']==other_box['floor'] and overlaps(feet,other_box['ground']):
                return False,'That spot overlaps '+other.replace('_',' ')+'.'
        return True,'There is room here.'

    def find(self,item,preferred=None,instance=None,footprint=None):
        if item not in FOOTPRINTS:return None
        if preferred and len(preferred)==2 and all(finite(v) for v in preferred):
            if self.check(item,*preferred,instance=instance,footprint=footprint)[0]:return list(preferred)
        else:preferred=(10,5)
        # Quarter-cell vertical steps and half-cell horizontal steps make small
        # nooks useful without reducing the actual drawing or contact space.
        points=[(x/2,y/4) for x in range(1,40) for y in range(4,45)]
        points.sort(key=lambda p:((p[0]-preferred[0])**2+(p[1]-preferred[1])**2*2,p[1],p[0]))
        return next((list(p) for p in points if self.check(item,*p,instance=instance,footprint=footprint)[0]),None)

    def put(self,item,x,y,instance=None):
        h=self.habitat
        if item not in h.owned_items:return False,'That item is not owned.'
        from world.shop import get_item,ItemCategory
        definition=get_item(item)
        if not definition or definition.category==ItemCategory.COSMETIC:return False,'Use the wardrobe for clothing.'
        current=next((p for p in h.placed_items+h.stored_placements if p.item_id==item and (not instance or p.instance_id==instance)),None)
        if instance and current is None:return False,'That copy is no longer in the habitat.'
        identity=current.instance_id if current else ''
        ok,message=self.check(item,x,y,identity)
        if not ok:return False,message
        from world.habitat import PlacedItem
        if current:
            current.x=x;current.y=y
            current.anim_offset_x=0;current.anim_offset_y=0
            current.is_animating=False
            if current in h.stored_placements:h.stored_placements.remove(current)
        else:
            current=h.take_stored_placement(item) or PlacedItem(item,x,y)
            current.x,current.y=x,y
        if current not in h.placed_items:h.placed_items.append(current)
        h.stored_items=[key for key in h.stored_items if key!=item]
        return True,'Placed '+definition.name+'.'

    def auto_place(self,item,preferred=None,instance=None):
        if not self.eligible(item):return False
        current=next((p for p in self.habitat.get_visible_placed_items() if p.item_id==item and (not instance or p.instance_id==instance)),None)
        identity=instance or (current.instance_id if current else '')
        if instance and not any(p.item_id==item and p.instance_id==instance for p in self.habitat.placed_items+self.habitat.stored_placements):return False
        if current and self.check(item,current.x,current.y,identity)[0]:return True
        spot=self.find(item,preferred,identity)
        if spot:return self.put(item,*spot,instance=instance)[0]
        # A failed attempt to rearrange a placed item must not remove it.
        if not current:self.habitat.store_item(item,instance)
        return False

    def reconcile(self):
        h=self.habitat;old=list(h.get_visible_placed_items())
        h.stored_placements.extend(p for p in h.placed_items if p not in old)
        h.placed_items=[]
        moved=[];stored=[]
        for p in old:
            if not self.eligible(p.item_id):
                h.stored_placements.append(p)
                continue
            spot=self.find(p.item_id,(p.x,p.y),p.instance_id)
            if spot:
                if spot!=[p.x,p.y]:moved.append(p.item_id)
                p.x,p.y=spot
                p.anim_offset_x=0;p.anim_offset_y=0
                p.is_animating=False
                h.placed_items.append(p)
            else:
                stored.append(p.item_id)
                h.stored_placements.append(p)
        for item in stored:
            if item not in h.stored_items and not any(p.item_id==item for p in h.placed_items):h.stored_items.append(item)
        return dict(revision=REVISION,moved=moved,stored=stored)

    def snapshot(self):
        h=self.habitat
        from world.shop import get_item,ItemCategory
        return dict(width=WIDTH,height=HEIGHT,revision=REVISION,
            items=[dict(id=key,placed=any(p.item_id==key for p in h.get_visible_placed_items()),
                        footprint=FOOTPRINTS[key]) for key in h.owned_items
                   if key in FOOTPRINTS and get_item(key) and get_item(key).category!=ItemCategory.COSMETIC],
            copies=[dict(id=p.item_id,instance=p.instance_id,placed=p in h.get_visible_placed_items()) for p in h.placed_items+h.stored_placements if self.eligible(p.item_id)],
            placed=[dict(id=p.item_id,instance=p.instance_id,x=p.x,y=p.y,box=bounds(p.item_id,p.x,p.y)) for p in h.get_visible_placed_items()],
            scenery=self.features,
            obstacles=[dict(id=p[0],x=p[1],y=p[2],instance=p[3] if len(p)>3 else None,
                            box=bounds(*p[:3],p[4] if len(p)>4 else None)) for p in self.obstacles()])
