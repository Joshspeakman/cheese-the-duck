import BLUEPRINTS from './animation/lighting.json' with {type:'json'};
const clamp=n=>Math.max(0,Math.min(1,n));
export function duskLevel(hour=12){const h=((hour%24)+24)%24;return h<5?1:h<7?(7-h)/2:h<17?0:h<19?(h-17)/2:1;}
export function lightOutput(id,state={},context={}){
 const p=BLUEPRINTS[id];if(!p)return 0;
 // Native per-copy state is authoritative. Catalogue previews use the same
 // deterministic dusk/weather rules, without mutating a game object.
 if(Number.isFinite(state.lighting?.level))return clamp(state.lighting.level);
 let level=p.style==='eternal'?1:state.lighting?.mode==='on'?1:state.lighting?.mode==='off'?0:duskLevel(context.hour??21);
 if(p.type==='fireflies')level=duskLevel(context.hour??21)*(context.season==='winter'?.12:1);
 const wet=/rain|storm|shower|drizzle|sleet/.test(context.weather||'');
 if(p.exposed&&wet)level*=Math.max(.08,1-(context.intensity??.7)*.92);
 return clamp(level);
}
// Map actual bulb coordinates through the exact item drawing transform. The
// compositor paints these modest pools beneath the sharp prop/character ink.
export function objectLightSources(object,sx,sy,night){
 if(!object.item||!object.lightSources)return [];
 const unit=sx*object.scale*(object.detailScale||1),left=object.x*sx-object.width*unit/2,top=object.y*sy-object.art.length*unit*1.5;
 return object.lightSources.map(s=>({x:(left+(s.x+.5)*unit)/sx,y:(top+(s.y+.5)*unit*1.5)/sy,radius:s.radius,power:s.power*(night?.32:.065),color:s.color}));
}
