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
    # Match native exterior clearance: retain its body margin and include the
    # actual age's outermost foot, even when it extends beyond three glyphs.
    left_margin=max(3,max(f[0] for f in m['feet']))*bx
    right_margin=max(3,-min(f[0] for f in m['feet']))*bx
    if ok and y<ground and left-left_margin<x<right+right_margin:ok,reason=False,'Inside own castle exterior clearance.'
    for fx,fy in m['feet']:
        if ok and water_at('Home Pond',x+fx*bx,y+fy*by,'pond'):ok,reason=False,'Actual posed foot is on water.'
        if ok and abs(fy)>1e-9:ok,reason=False,'Actual posed feet are not on the root ground row.'
    results.append(dict(supported=ok,reason=reason))
json.dump(results,sys.stdout)
