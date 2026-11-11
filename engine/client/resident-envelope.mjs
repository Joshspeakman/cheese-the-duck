import {duckRig} from './duck-rig.mjs';
import {visitorRig} from './visitor-rig.mjs';
import COMPANY from './animation/home-company.json' with {type:'json'};
import SEATING from './animation/seating-routines.json' with {type:'json'};

const cache=new Map();
export function inkBounds(character){
 let left=Infinity,right=-Infinity,top=Infinity,bottom=-Infinity;
 character.art.forEach((r,y)=>{const a=r.search(/\S/),b=r.trimEnd().length;if(a<0)return;left=Math.min(left,a);right=Math.max(right,b-1);top=Math.min(top,y);bottom=Math.max(bottom,y);});
 return {left,right,top,bottom};
}
export function residentEnvelope(character,repertoire='shelter'){
 // Fit a whole repertoire once. Recomputing scale from each posed frame makes
 // a tall visitor shrink and swell whenever it looks up at the roof.
 const stage=character.rig?.stage||'adult',id=character.profileId||'',facing=character.facing!==false;
 const gear=character.wearables||[],key=JSON.stringify([stage,id,facing,gear,repertoire]);
 if(cache.has(key))return cache.get(key);
 const source={stage,castId:id,facing,cosmetics:Object.fromEntries(gear.map((id,i)=>[i,id]))};
 const rig=id?visitorRig:duckRig;
 let bounds=inkBounds(character);
 function include(model){const b=inkBounds(model);bounds={left:Math.min(bounds.left,b.left),right:Math.max(bounds.right,b.right),top:Math.min(bounds.top,b.top),bottom:Math.max(bounds.bottom,b.bottom)};}
 for(let t=0;t<8;t++)include(rig({...source,state:'sleeping'},t));
 for(const [kind,spec] of Object.entries(repertoire==='seating'?SEATING:COMPANY))for(const role of ['a','b']){
  const track=repertoire==='seating'?(role==='b'&&spec.reply?spec.reply:spec.track):spec[role];
  const beats=track.map(([at])=>at);
  for(const progress of [...beats,...beats.slice(1).map((b,i)=>(b+beats[i])/2)]){
   const performance=repertoire==='seating'?{kind:'seating',routine:{id:kind,role,elapsed:progress*spec.duration}}:{kind,role,progress};
   include(rig({...source,performance},progress*8));
  }
 }
 // Reserve a glyph for rounded poses and independently fluttering feathers.
 bounds={left:bounds.left-1,right:bounds.right+1,top:bounds.top-1,bottom:bounds.bottom+1};
 if(cache.size>=256)cache.delete(cache.keys().next().value);
 cache.set(key,bounds);return bounds;
}
