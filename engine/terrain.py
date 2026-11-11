"""World-space terrain shared with the Ultra renderer, independent of camera."""
import json
import math
from functools import lru_cache
from pathlib import Path

DATA=Path(__file__).parent/'client/animation/terrain-regions.json'
REGIONS=json.loads(DATA.read_text())['locations']
GROUND=json.loads(DATA.with_name('habitat-ground.json').read_text())

@lru_cache(maxsize=128)
def seed_of(name):
    seed=0
    for char in name:seed=(seed*31+ord(char))&0xffffffff
    return seed if seed<0x80000000 else seed-0x100000000

def region(location,biome='pond'):
    return REGIONS.get(location,dict(biome=biome,terrain='dry',bank=65,features=[]))

def bank_grid(location,gx):
    r=region(location)
    seed=GROUND['seed'] if r['terrain']=='home' else seed_of(location)
    bank=GROUND['bank'] if r['terrain']=='home' else r['bank']
    wave_a=GROUND['waveA'] if r['terrain']=='home' else (.025,6)
    wave_b=GROUND['waveB'] if r['terrain']=='home' else (.077,2)
    return bank+math.sin(gx*wave_a[0]+seed)*wave_a[1]+math.sin(gx*wave_b[0])*wave_b[1]

def water_at(location,x,y,biome='pond'):
    r=region(location,biome);gx=24+x*192/132;gy=46+y*47/42
    if r['terrain'] in ('shore','home'):return gy>bank_grid(location,gx)
    if r['terrain']=='stream':return abs(gx-(119+math.sin(gy*.075)*25))<max(0,(gy-35)*.13)
    if r['terrain']=='drain':return gy>77
    return False

def features(location,biome='pond'):
    result=[]
    if location=='Home Pond':
        for source in GROUND['scenery']:
            f=dict(source)
            y=f.get('y',(bank_grid(location,24+f.get('shoreX',f['x'])*192/20)-46)*12/47+f.get('shoreOffset',0))
            result.append(dict(id=f['id'],name=f['name'],box=dict(x=f['x']-f['width']/2,y=y-f['depth']/2,w=f['width'],h=f['depth'],floor=False)))
    else:
        for f in region(location,biome)['features']:
            if f.get('soft'):continue
            x=(f['x']-24)*20/192;y=(f['y']-46)*12/47
            w=f['width']*20/192;h=f['depth']*12/47
            result.append(dict(id=f['id'],name=f.get('art',f['kind']).replace('_',' ').lower(),box=dict(x=x-w/2,y=y-h/2,w=w,h=h,floor=False)))
    return result

def surface_fits(item,box,location='Home Pond',biome='pond'):
    if item in GROUND['eitherItems']:return True
    want=item in GROUND['waterItems']
    kind=region(location,biome)['terrain']
    if kind=='dry':return not want
    rows=(0,) if want else (8,)
    if kind=='stream':rows=range(9)
    # Include the whole support plane; stream banks can cross under its middle.
    for ix in range(33):
        x=(box['x']+box['w']*ix/32)*132/20
        for iy in rows:
            y=(box['y']+box['h']*iy/8)*42/12
            if water_at(location,x,y,biome)!=want:return False
    return True
