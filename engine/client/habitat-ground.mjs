import GROUND from './animation/habitat-ground.json' with {type:'json'};
import {bankGrid,bankOnScreen,surfaceFitsRegion} from './terrain.mjs';
export function homeShore(x){
 const gx=24+x*192/20;
 return (bankGrid('Home Pond',gx)-46)*12/47;
}
export function homeBankOnScreen(x,camera={x:0,y:0,w:132,h:42}){
 return bankOnScreen('Home Pond',x,camera);
}
export function itemSurface(id){return GROUND.waterItems.includes(id)?'water':GROUND.eitherItems.includes(id)?'either':'land';}
export function groundBounds(id,box,y){
 const depth=box.floor?box.h-.65:itemSurface(id)==='water'?.35:Math.max(.35,Math.min(1.8,(box.h-.65)*.18));
 return {x:box.x,y:y-depth,w:box.w,h:depth+.35};
}
export const homeScenery=GROUND.scenery.map(f=>{
 const y=f.y??homeShore(f.shoreX??f.x)+(f.shoreOffset||0);
 return {...f,y,box:{x:f.x-f.width/2,y:y-f.depth/2,w:f.width,h:f.depth}};
});
export const intersects=(a,b)=>a.x<b.x+b.w&&a.x+a.w>b.x&&a.y<b.y+b.h&&a.y+a.h>b.y;
export function surfaceFits(id,box,y){
 return surfaceFitsRegion(id,groundBounds(id,box,y));
}
