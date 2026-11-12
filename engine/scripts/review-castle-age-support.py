"""Read-only placement/support checks for proposed age contacts; no game or saves."""
import json,math,sys
from pathlib import Path
from types import SimpleNamespace
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from engine.pond_layout import PondLayout
from engine.terrain import water_at
geometry=json.loads((Path(__file__).resolve().parents[1]/'client/animation/castle-geometry.json').read_text())
layout=PondLayout(SimpleNamespace(get_visible_placed_items=lambda:()))
q=.66*geometry['detail_scale']
results=[]
for row in json.load(sys.stdin):
    x,y=row['root'];cx,cy=row['center'];m=row['metric'];bx=m['scale']*132/192;by=m['scale']*42/47
    ok,reason=layout.check('rock',x*20/132,y*12/42,None,dict(width=6,height=4,floor=False))
    ground=cy+(geometry['ground_row']-geometry['height'])*q*42/47
    left=cx-geometry['width']/2*q*132/192;right=cx+geometry['width']/2*q*132/192
    if ok and y<ground and left-3*bx<x<right+3*bx:ok,reason=False,'Inside own castle exterior clearance.'
    for fx,fy in m['feet']:
        if ok and water_at('Home Pond',x+fx*bx,y+fy*by,'pond'):ok,reason=False,'Actual posed foot is on water.'
        if ok and abs(fy)>1e-9:ok,reason=False,'Actual posed feet are not on the root ground row.'
    results.append(dict(supported=ok,reason=reason))
json.dump(results,sys.stdout)
