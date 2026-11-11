import REGIONS from './animation/terrain-regions.json' with {type:'json'};
import GROUND from './animation/habitat-ground.json' with {type:'json'};
import {seedOf} from './ultra-grid.mjs';
export const regions=REGIONS.locations;
const seeds=Object.fromEntries(Object.keys(regions).map(name=>[name,seedOf(name)]));
export function region(location,biome='pond'){return regions[location]||{biome,terrain:'dry',bank:65,features:[]};}
export function bankGrid(location,gx){
 const r=region(location),seed=r.terrain==='home'?GROUND.seed:seeds[location]??seedOf(location),bank=r.terrain==='home'?GROUND.bank:r.bank;
 const a=r.terrain==='home'?GROUND.waveA:[.025,6],b=r.terrain==='home'?GROUND.waveB:[.077,2];
 return bank+Math.sin(gx*a[0]+seed)*a[1]+Math.sin(gx*b[0])*b[1];
}
export function waterAt(location,x,y,biome='pond'){
 const r=region(location,biome),gx=24+x*192/132,gy=46+y*47/42;
 if(r.terrain==='shore'||r.terrain==='home')return gy>bankGrid(location,gx);
 if(r.terrain==='stream')return Math.abs(gx-(119+Math.sin(gy*.075)*25))<Math.max(0,(gy-35)*.13);
 if(r.terrain==='drain')return gy>77;
 return false;
}
export function bankOnScreen(location,x,camera={x:0,y:0,w:132,h:42}){
 const wx=camera.x+(x-24)/192*camera.w,gx=24+wx*192/132;
 return 46+((bankGrid(location,gx)-46)*42/47-camera.y)/camera.h*47;
}
export function surfaceFitsRegion(item,box,location='Home Pond',biome='pond'){
 if(GROUND.eitherItems.includes(item))return true;
 const water=GROUND.waterItems.includes(item);
 const kind=region(location,biome).terrain;if(kind==='dry')return !water;
 const rows=kind==='stream'?[0,1,2,3,4,5,6,7,8]:[water?0:8];
 for(let ix=0;ix<=32;ix++)for(const iy of rows){
  const x=(box.x+box.w*ix/32)*132/20,y=(box.y+box.h*iy/8)*42/12;
  if(waterAt(location,x,y,biome)!==water)return false;
 }
 return true;
}
