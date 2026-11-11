"""Physical habitat layout: measured artwork, entry space and honest storage.

The existing 20 x 12 habitat coordinates remain the source of truth for walking,
save files and both renderers. This module never offsets a drawing alone.
"""
import hashlib
import json
import math
from pathlib import Path

DATA=Path(__file__).parent/'client/animation/object-footprints.json'
FOOTPRINTS=json.loads(DATA.read_text())['items']
GROUND_PATH=DATA.with_name('habitat-ground.json')
GROUND=json.loads(GROUND_PATH.read_text())
REVISION=hashlib.sha256(DATA.read_bytes()+GROUND_PATH.read_bytes()).hexdigest()[:16]
WIDTH,HEIGHT=20,12

def finite(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)

def bounds(item,x,y):
    f=FOOTPRINTS.get(item,{'width':26,'height':18,'floor':False})
    # The largest live camera spans 132 x 42 world units, projected into
    # 192 x 47 ground cells. The drawing grows upward from its actual feet.
    w=f['width']*20/192+.5;h=f['height']*12/47
    return dict(x=x-w/2,y=y-h,w=w,h=h+.65,floor=f['floor'])

def overlaps(a,b):
    if a['floor']!=b['floor']:return False  # Rugs belong under furniture.
    return a['x']<b['x']+b['w'] and a['x']+a['w']>b['x'] and a['y']<b['y']+b['h'] and a['y']+a['h']>b['y']

def shoreline(x):
    gx=24+x*192/20
    return (GROUND['bank']+math.sin(gx*GROUND['waveA'][0]+GROUND['seed'])*GROUND['waveA'][1]+math.sin(gx*GROUND['waveB'][0])*GROUND['waveB'][1]-46)*12/47

def surface_fits(item,box,y):
    if item in GROUND['eitherItems']:return True
    water=item in GROUND['waterItems']
    for step in range(33):
        shore=shoreline(box['x']+box['w']*step/32)
        if not water and y+.35>shore:return False
        if water and y-.35<shore:return False
    return True

class PondLayout:
    def __init__(self,habitat,obstacles=lambda:()):
        self.habitat=habitat;self.obstacles=obstacles

    def occupied(self,exclude=''):
        # Idle bobbing never changes the permanent space reservation.
        return [(p.item_id,p.x,p.y) for p in self.habitat.get_visible_placed_items() if p.item_id!=exclude]+list(self.obstacles())

    def eligible(self,item):
        from world.shop import get_item,ItemCategory
        definition=get_item(item)
        return item in self.habitat.owned_items and item in FOOTPRINTS and definition and definition.category!=ItemCategory.COSMETIC

    def check(self,item,x,y):
        if not finite(x) or not finite(y):return False,'Choose a point inside the habitat.'
        if item not in FOOTPRINTS:return False,'This object does not have a placement drawing yet.'
        f=bounds(item,x,y)
        if f['x']<.2 or f['x']+f['w']>WIDTH-.2 or x>124*20/132 or y<1 or y>37*12/42:
            return False,'Leave room around the edge for the whole object.'
        # The visible upper sky can contain a tall roof; the ground anchor
        # must stay reachable. No object can be hidden above the window.
        if 46+y*47/12-FOOTPRINTS[item]['height']<2:
            return False,'That tall object needs a spot farther down the bank.'
        if not surface_fits(item,f,y):
            return False,'That belongs on the water.' if item in GROUND['waterItems'] else 'Keep its feet on the dry bank.'
        for other,ox,oy in self.occupied(item):
            if overlaps(f,bounds(other,ox,oy)):
                return False,'That spot overlaps '+other.replace('_',' ')+'.'
        return True,'There is room here.'

    def find(self,item,preferred=None):
        if item not in FOOTPRINTS:return None
        if preferred and len(preferred)==2 and all(finite(v) for v in preferred):
            if self.check(item,*preferred)[0]:return list(preferred)
        else:preferred=(10,5)
        # Quarter-cell vertical steps and half-cell horizontal steps make small
        # nooks useful without reducing the actual drawing or contact space.
        points=[(x/2,y/4) for x in range(1,40) for y in range(4,45)]
        points.sort(key=lambda p:((p[0]-preferred[0])**2+(p[1]-preferred[1])**2*2,p[1],p[0]))
        return next((list(p) for p in points if self.check(item,*p)[0]),None)

    def put(self,item,x,y):
        h=self.habitat
        if item not in h.owned_items:return False,'That item is not owned.'
        from world.shop import get_item,ItemCategory
        definition=get_item(item)
        if not definition or definition.category==ItemCategory.COSMETIC:return False,'Use the wardrobe for clothing.'
        ok,message=self.check(item,x,y)
        if not ok:return False,message
        from world.habitat import PlacedItem
        current=next((p for p in h.placed_items if p.item_id==item),None)
        if current:
            current.x=x;current.y=y
            current.anim_offset_x=0;current.anim_offset_y=0
            current.is_animating=False
        else:current=PlacedItem(item,x,y)
        h.placed_items=[p for p in h.placed_items if p.item_id!=item]+[current]
        h.stored_items=[key for key in h.stored_items if key!=item]
        return True,'Placed '+definition.name+'.'

    def auto_place(self,item,preferred=None):
        if not self.eligible(item):return False
        current=next((p for p in self.habitat.get_visible_placed_items() if p.item_id==item),None)
        if current and self.check(item,current.x,current.y)[0]:return True
        spot=self.find(item,preferred)
        if spot:return self.put(item,*spot)[0]
        # A failed attempt to rearrange a placed item must not remove it.
        if not current:self.habitat.store_item(item)
        return False

    def reconcile(self):
        h=self.habitat;old=list(h.get_visible_placed_items());h.placed_items=[]
        moved=[];stored=[];seen=set()
        for p in old:
            if p.item_id in seen:continue
            seen.add(p.item_id)
            if not self.eligible(p.item_id):continue
            spot=self.find(p.item_id,(p.x,p.y))
            if spot:
                if spot!=[p.x,p.y]:moved.append(p.item_id)
                p.x,p.y=spot
                p.anim_offset_x=0;p.anim_offset_y=0
                p.is_animating=False
                h.placed_items.append(p)
            else:
                stored.append(p.item_id)
                if p.item_id not in h.stored_items:h.stored_items.append(p.item_id)
        return dict(revision=REVISION,moved=moved,stored=stored)

    def snapshot(self):
        h=self.habitat
        from world.shop import get_item,ItemCategory
        return dict(width=WIDTH,height=HEIGHT,revision=REVISION,
            items=[dict(id=key,placed=any(p.item_id==key for p in h.get_visible_placed_items()),
                        footprint=FOOTPRINTS[key]) for key in h.owned_items
                   if key in FOOTPRINTS and get_item(key) and get_item(key).category!=ItemCategory.COSMETIC],
            placed=[dict(id=p.item_id,x=p.x,y=p.y,box=bounds(p.item_id,p.x,p.y)) for p in h.get_visible_placed_items()],
            obstacles=[dict(id=key,x=x,y=y,box=bounds(key,x,y)) for key,x,y in self.obstacles()])
