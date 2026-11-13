// Renderer side of the repertoire engine (engine/repertoire.py owns clocks and
// every effect). Works on ANY object construction: anchors are the builder's named
// anchors when present, else fractions of the drawn sprite box from the object file.
import {actorPitches} from './actor-projection.mjs';
import {sampleTrack} from './wonder-routines.mjs';
import DATA from './animation/repertoire.json' with {type:'json'};
export const REP_OBJECTS=DATA.objects,REP_ROUTINES=DATA.routines;
const clamp=n=>Math.max(0,Math.min(1,n));
const JOINTS=['x','y','b','w','l','r','reach','contact'];
const OBJ=['sway','lift','shake','glow','puff'];
export function repPose(work,motion=true){
 const spec=REP_ROUTINES[work?.id];if(!spec||work.interrupted)return null;
 const progress=motion?clamp(work.elapsed/spec.duration):.5;
 const pose=sampleTrack(spec.track,progress,JOINTS);
 const obj=spec.obj?sampleTrack([[0,{}],...spec.obj,[1,{}]],progress,OBJ):null;
 return {...pose,object:obj||{},rep:spec.tool!=='none'&&!work.transition,wonder:spec.tool!=='none'&&!work.transition,tool:spec.tool,progress,item:spec.object};
}
export function repAnchor(home,objectId,name){
 const named=home.anchors?.[name];if(named)return named;
 const f=REP_OBJECTS[objectId]?.anchors?.[name];if(!f)return null;
 return {x:f.x*(home.width-1),y:f.y*(home.art.length-1)};
}
// Object reaction at draw time: no re-raster, no state change.
export function applyObjectPose(model,pose){
 const objPose=pose?.object;if(!objPose)return model;
 const shake=(objPose.shake||0)*Math.sin((pose.progress||0)*90)*.03;
 return {...model,sway:(model.sway||0)+(objPose.sway||0)*.08+shake,lift:(model.lift||0)+(objPose.lift||0)*.6};
}
export function repGeometry(home,worker,sx,sy){
 const c=worker.character,routine=c.performance.routine,pose=repPose(routine,c.performance.motion!==false),oid=REP_ROUTINES[routine.id].object;
 const unit=sx*home.scale*(home.detailScale||1),hh=unit*1.5,left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*hh;
 const entry=home.anchors?.entry||{x:home.width/2,y:home.art.length-1},ground=top+entry.y*hh;
 const A=repAnchor(home,oid,pose.anchorA)||entry,B=repAnchor(home,oid,pose.anchorB)||A;
 const target={x:left+(A.x+(B.x-A.x)*pose.anchorBlend+.5)*unit,y:top+(A.y+(B.y-A.y)*pose.anchorBlend+.5)*hh};
 const {cw,ch}=actorPitches(c,sx,sy),rest=c.workGripRest||c.grip||{x:c.anchorX+5,y:c.groundRow-7};
 const workX=worker.slot===1?c.x*sx:pose.tool==='none'?left+home.width*unit*.5-(c.anchorX*.2)*cw:target.x-2*cw-(rest.x-c.anchorX)*cw;
 const character=worker.slot===1?{...c,offsetY:0}:{...c,x:c.x+(workX/sx-c.x)*worker.inside,y:c.y+(ground/sy-c.y)*worker.inside,offsetY:0};
 const grip=c.grip||rest,cl=Math.round(character.x*sx-c.anchorX*cw+(c.offsetX||0)*cw),ct=Math.round(character.y*sy-c.groundRow*ch);
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*ch},points=[],put=(x,y,g,col='#d9c49b')=>points.push({x,y,glyph:g,color:col});
 if(pose.tool!=='none'&&pose.contact>.01&&worker.inside>.01){
  const u=pose.contact*worker.inside,idle={x:hand.x+(c.facing===false?-5:5)*cw,y:hand.y-ch*2},tip={x:idle.x+(target.x-idle.x)*u,y:idle.y+(target.y-idle.y)*u};
  const n=Math.max(1,Math.ceil(Math.max(Math.abs(tip.x-hand.x)/cw,Math.abs(tip.y-hand.y)/ch)));
  for(let i=1;i<n;i++){const q=i/n;put(hand.x+(tip.x-hand.x)*q,hand.y+(tip.y-hand.y)*q,pose.tool==='wing'?(q<.5?'=':'~'):((tip.x-hand.x)*(tip.y-hand.y)>0?'\\':'/'),pose.tool==='wing'?'#f2e3b5':'#d9c49b');}
  put(tip.x,tip.y,pose.tool==='wing'?'>':'*','#f2e3b5');
 }
 const o=pose.object||{};
 if(o.glow>.1)for(const d of [-1,1])put(target.x+d*2*cw,target.y-ch,'*','#fff3b0');
 if(o.puff>.1)for(const d of [-1,0,1])put(target.x+d*cw,target.y-ch*(1+o.puff),'o','#d7e7e2');
 return {character,pose,ground,cw,hand,target,points};
}
export function drawRepTools(ctx,staged){
 ctx.save();ctx.font='600 '+staged.cw*1.5+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#172b24';ctx.lineWidth=Math.max(.6,staged.cw*.15);
 for(const p of staged.points){ctx.fillStyle=p.color;ctx.strokeText(p.glyph,p.x,p.y);ctx.fillText(p.glyph,p.x,p.y);}ctx.restore();
}
