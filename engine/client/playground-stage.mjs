import {sameInstance} from './physical-objects.mjs';
import {PLAY_BLUEPRINTS} from './playground-workshop.mjs';
const clamp=n=>Math.max(0,Math.min(1,n)),mix=(a,b,u)=>a+(b-a)*u;
export function playgroundStage(plan,objects,character,stage,motion=true){
 if(plan?.kind!=='item'||plan.paused||!['prepare','act','settle'].includes(plan.phase)||!character)return null;
 const p=PLAY_BLUEPRINTS[plan.target];if(!p||!['slide','swing','tire','trampoline','seesaw','horse','skateboard','sandbox'].includes(p.type))return null;
 const home=objects.find(o=>o.id===plan.target&&sameInstance(o,plan)&&(o.portable||!o.worldPosition||!plan.destination||o.worldPosition.every((n,i)=>Math.abs(n-plan.destination[i])<1.1)));
 if(!home)return null;
 const progress=clamp(plan.progress??plan.elapsed/plan.duration),u=clamp((progress-.28)/.62),a=home.anchors;
 const young=['hatchling','duckling'].includes(stage);
 let seat={...a.seat},gesture='balance',beat=u;
 if(p.type==='slide'){
  gesture='slide';
  if(young){seat={x:a.exit.x-4,y:a.exit.y};gesture='splash_steps';}
  else if(plan.phase==='prepare'){const climb=clamp((progress-.15)/.13);seat={x:mix(a.entry.x,a.top.x,climb),y:mix(a.entry.y,a.top.y,climb)};gesture='climb';beat=climb;}
  else{const at=Math.round(u*(a.path.length-1));seat={x:a.path[at][0],y:a.path[at][1]+3};}
 }
 if(p.type==='trampoline'){const cycle=motion?(plan.elapsed??u*12)*4:0;seat.y-=Math.max(0,-Math.sin(cycle))*(young?4:14);gesture='bounce';beat=(cycle/(Math.PI*2)+.7)%1;}
 if(p.type==='horse'){gesture='rock';beat=(u*3)%1;}
 if(p.type==='swing'||p.type==='tire'){gesture='swing_lean';beat=(u*3)%1;}
 if(p.type==='seesaw'){gesture='balance';beat=(u*3)%1;}
 if(p.type==='sandbox'){gesture='dig';beat=(u*4)%1;seat.x-=young?10:0;}
 if(p.type==='skateboard'){gesture='balance';beat=(u*4)%1;}
 const inside=plan.phase==='prepare'&&p.type!=='slide'?clamp((progress-.15)/.13):plan.phase==='settle'?clamp((1-progress)/.1):1;
 return {home,seat,inside,gesture,beat,young};
}
export function ridingGeometry(home,character,seat,inside,sx,sy){
 const unit=sx*home.scale*(home.detailScale||1),ch=unit*1.5;
 const x=home.x*sx+(seat.x-home.width/2)*unit,y=home.y*sy+(seat.y-home.art.length)*ch;
 return {...character,x:mix(character.x,x/sx,inside),y:mix(character.y,y/sy,inside)};
}
