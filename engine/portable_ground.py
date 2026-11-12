"""A temporary belonging is put down at a native, reserved world position.

Choosing a site never grants the item. The original routine starts only after
Cheese walks there; its clock, contacts and rewards remain in the existing system.
"""
from types import SimpleNamespace
from engine.pond_layout import PondLayout,FOOTPRINTS,finite

IDENTITY='portable:cheese'
OFFSET=7*132/192
WORKS=('keepsake_work','creative_work','playkit_work','textile_work','ground_work')
STANCE=dict(width=6,height=4,floor=False)

def policy(pond,location=None):
    location=location or pond.location
    if location=='Home Pond':return pond.layout
    from engine.terrain import region
    return PondLayout(SimpleNamespace(get_visible_placed_items=lambda:()),location=location,
                      biome=region(location,pond.biome)['biome'])

def point_ok(layout,item,point):
    if not isinstance(point,(list,tuple)) or len(point)!=2 or not all(finite(n) for n in point):return False
    x,y=point;ax=x-OFFSET
    if not 2<=ax<=124 or not 2<=y<=37:return False
    if not layout.check(item,x*20/132,y*12/42,IDENTITY)[0]:return False
    # Ducks can paddle, but cannot stand in a trunk or another belonging.
    return layout.check('rubber_duck',ax*20/132,y*12/42,IDENTITY,STANCE)[0]

def companion_spot(pond,plan,origin):
    """Reserve the far-side stance from the same center the renderer projects."""
    if plan.get('instance'):
        center=origin
    elif plan.get('portable') is not None:
        site=plan['portable']
        if not isinstance(site,dict) or site.get('location')!=pond.location:return None
        center=site.get('object')
    else:
        # Legacy plans lack a saved deployment point; OFFSET is in native cells.
        if not isinstance(origin,(list,tuple)) or len(origin)!=2 or not all(finite(n) for n in origin):return None
        center=[origin[0]+OFFSET,origin[1]]
    if not isinstance(center,(list,tuple)) or len(center)!=2 or not all(finite(n) for n in center):return None
    spot=[center[0]+9,center[1]]
    if not (6<=spot[0]<=122 and 3<=spot[1]<=36):return None
    # Match the existing duck stance policy: paddling is supported, but trees
    # and other belongings are not. The activity's own copy is its contact zone.
    if not policy(pond).check('rubber_duck',spot[0]*20/132,spot[1]*12/42,
                              plan.get('instance') or IDENTITY,STANCE)[0]:return None
    return spot

def choose(pond,item,origin=None,location=None):
    if item not in FOOTPRINTS:return None
    pos=pond.game.renderer.duck_pos
    origin=origin if isinstance(origin,(list,tuple)) and len(origin)==2 and all(finite(n) for n in origin) else [pos.x,pos.y]
    preferred=[origin[0]+OFFSET,origin[1]];layout=policy(pond,location)
    point=preferred if point_ok(layout,item,preferred) else None
    if point is None:
        points=[(x/2*132/20,y/4*42/12) for x in range(1,40) for y in range(4,43)]
        points.sort(key=lambda p:(p[0]-preferred[0])**2+(p[1]-preferred[1])**2*2)
        point=next((list(p) for p in points if point_ok(layout,item,p)),None)
    if point is None:return None
    return dict(location=location or pond.location,object=list(point),stance=[point[0]-OFFSET,point[1]],deployed=False)

def bind(plan,site):
    plan['portable']=site
    plan['destination']=list(site['stance'])
    for key in WORKS:
        if plan.get(key):plan[key]['origin']=list(site['stance'])

def valid(pond,plan):
    site=plan.get('portable')
    if not isinstance(site,dict) or site.get('location')!=plan.get('location') or plan['target'] not in pond.owned:return False
    point=site.get('object');stance=site.get('stance')
    if not point_ok(policy(pond,site['location']),plan['target'],point):return False
    return isinstance(stance,(list,tuple)) and len(stance)==2 and all(finite(n) for n in stance) and abs(stance[0]-(point[0]-OFFSET))+abs(stance[1]-point[1])<1e-6

def reservation(pond):
    plan=pond.state.get('plan');site=plan.get('portable') if plan else None
    if site and site.get('location')=='Home Pond':
        point=site.get('object')
        if isinstance(point,(list,tuple)) and len(point)==2 and all(finite(n) for n in point):
            return (plan['target'],point[0]*20/132,point[1]*12/42,IDENTITY)
    return None

def restore(pond):
    plan=pond.state.get('plan')
    if not plan or plan.get('kind')!='item' or plan.get('instance') or plan['target'] in pond.placed:return
    if plan.get('portable') and valid(pond,plan):return
    origin=next((plan[key]['origin'] for key in WORKS if plan.get(key,{}).get('origin')),None)
    site=choose(pond,plan['target'],origin,plan.get('location'))
    if site:
        site['deployed']=plan.get('phase')!='approach'
        bind(plan,site)
    else:pond.cancel()

def walk_back(pond,plan):
    plan.update(phase='approach',arrived=False,approach_time=0.)
    pond.game.renderer.duck_pos.move_to(*plan['portable']['stance'])
