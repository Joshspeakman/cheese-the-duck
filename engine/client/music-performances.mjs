import SCORES from './animation/music-scores.json' with {type:'json'};
import {drawBotanicalTools} from './botanical-routines.mjs';
import INSTRUMENTS from './animation/instruments.json' with {type:'json'};
export {SCORES as MUSIC_SCORES};
const clamp=n=>Math.max(0,Math.min(1,n)),ease=n=>{n=clamp(n);return n*n*(3-2*n);};
export function musicNotes(item,score){
 const spec=SCORES[score?.id],p=INSTRUMENTS[item];if(!spec||!p)return [];
 const beat=60/spec.tempo,offset=p.type==='piano'?(p.style==='toy'?0:7):0;
 return spec.notes.filter(n=>!score.role||!spec.shared||n[2]===score.role).map((n,index)=>({index,at:2+n[0]*beat,hold:(n[3]??.7)*beat,key:p.type==='piano'?n[1]%8+offset:p.type==='horn'?n[1]%3:p.type==='chimes'?n[1]%(p.style==='bell'?1:p.style==='shells'?5:7):p.type==='radio'?2:n[1]%6,hand:spec.shared?(score.role==='b'?'r':'l'):n[2],velocity:n[4]??.6}));
}
function passage(notes,time){
 const groups=[];
 for(const note of notes){let g=groups.at(-1);if(!g||g.at!==note.at){g={at:note.at,hold:note.hold,notes:[]};groups.push(g);}g.notes.push(note);g.hold=Math.max(g.hold,note.hold);}
 const a=groups.filter(g=>g.at<=time).at(-1)||groups[0],b=groups.find(g=>g.at>time)||a;
 if(!a)return null;
 const leave=a.at+Math.min(a.hold,(b.at-a.at)*.8),u=a===b?0:ease((time-leave)/Math.max(.01,b.at-leave));
 return {a,b,u,walking:u>0&&u<1};
}
export function musicPose(item,score,motion=true){
 const spec=SCORES[score?.id],p=INSTRUMENTS[item];if(!spec||!p||score.interrupted)return null;
 // One frozen, physically meaningful pose when reduced motion is enabled.
 const time=motion?score.elapsed:2.1,notes=musicNotes(item,score),hits=[];
 const alive=time>=2&&time<spec.duration-3;
 for(const n of notes){const dt=time-n.at;if(dt>=0&&dt<n.hold)hits.push({...n,press:p.type==='drums'&&spec.gesture!=='brush'?Math.exp(-dt*18):ease((dt+.045)/.08)*ease((n.hold-dt)/.12)});}
 const hands=[];
 for(const hand of ['l','r']){
  const track=notes.filter(n=>n.hand===hand);if(!track.length)continue;
  const next=track.find(n=>n.at>time),last=track.filter(n=>n.at<=time).at(-1),a=last||next,b=next||last;
  if(!a)continue;
  const u=a===b?0:ease((time-(a.at+a.hold))/Math.max(.1,b.at-a.at-a.hold));
  const pressed=hits.find(n=>n.hand===hand);
  const waiting=!pressed&&(!last||time>last.at+last.hold+.25)&&(!next||next.at-time>.35);
  if(waiting||hits.length&&!pressed)continue;
  hands.push({hand,key:a.key,next:b.key,mix:u,press:pressed?.press||0,lift:pressed?(p.type==='drums'&&spec.gesture!=='brush'?ease((time-pressed.at-.05)/.2)*2:0):Math.sin(Math.PI*u)*1.5+.5});
 }
 const pressure=Math.max(0,...hits.map(h=>h.press)),hesitant=spec.gesture==='tentative'&&!hits.length;
 const walking=passage(notes,time)?.walking,step=walking?Math.sin(time*20):0;
 const pulse=alive?Math.sin(Math.max(0,time-2)*Math.PI*spec.tempo/60):0;
 return {instrument:true,type:p.type,gesture:spec.gesture,time,playing:alive,hits,hands,progress:clamp(time/spec.duration),
  x:spec.gesture==='jab'?pressure*.6:hesitant?-.4:p.type==='radio'?pulse*.25:0,
  y:spec.gesture==='patient'?.3:spec.gesture==='jab'?pressure*.45:p.type==='horn'?-hits.length*.2:pulse*.13,
  b:p.type==='drums'?pressure*.3:p.type==='radio'?Math.abs(pulse)*.3:spec.gesture==='waltz'?pulse*.2:0,
  w:p.type==='chimes'?.6:.3,l:p.type==='radio'?Math.max(0,pulse):Math.max(0,step),r:p.type==='radio'?Math.max(0,-pulse):Math.max(0,-step),
  reach:0,eye:spec.gesture==='jab'?'>':spec.gesture==='lullaby'?'-':p.type==='horn'&&hits.length?'>':alive&&spec.gesture==='listen'?'^':null,mark:hesitant&&time<2?'?':'',
  ringing:notes.filter(n=>time>=n.at&&time-n.at<3).map(n=>({key:n.key,amount:Math.sin((time-n.at)*18)*Math.exp(-(time-n.at)*1.8)})),
  dial:ease(time/1.8),strike:hits.reduce((n,h)=>Math.max(n,h.press),0)};
}
export function musicOccupants(scene){
 const plan=scene.living?.plan,records=[...(scene.living?.minds?.musicians||[])];
 if(plan?.instrument&&plan.music_score&&!plan.paused&&['prepare','act','settle'].includes(plan.phase)){
  const progress=plan.progress??plan.elapsed/plan.duration;
  records.push({actor:'cheese',id:plan.target,instance:plan.instance,destination:plan.destination,slot:plan.instrument.slot,score:plan.music_score,
   phase:plan.phase==='act'?'inside':plan.phase==='prepare'?'enter':'exit',elapsed:plan.phase==='prepare'?clamp((progress-.15)/.13)*3:plan.phase==='settle'?clamp((progress-.9)/.1)*3:0});
 }
 return records;
}
export function musicGeometry(home,worker,sx,sy){
 const c=worker.character,pose=musicPose(home.id,c.performance.routine,c.performance.motion!==false);
 const unit=sx*home.scale*home.detailScale,ch=unit*1.5,cw=c.scale*sx,hh=cw*1.5,dir=worker.slot===0?1:-1;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*ch;
 const point=a=>({x:left+(a.x+.5)*unit,y:top+(a.y+.5)*ch});
 const key=n=>point(home.anchors.keys[Math.max(0,Math.min(home.anchors.keys.length-1,n))]);
 const entry=point(home.anchors.entry),grip=c.grip||{x:c.anchorX+dir*4,y:c.groundRow-7},rest=c.workGripRest||grip;
 const targets=pose.hands.map(h=>{const a=key(h.key),b=key(h.next);return {...h,x:a.x+(b.x-a.x)*h.mix,y:a.y+(b.y-a.y)*h.mix-h.lift*hh};});
 // During rests the player waits beside the most recently played surface.
 const path=passage(musicNotes(home.id,c.performance.routine),pose.time);
 const center=g=>g.notes.map(n=>key(n.key)).reduce((v,k)=>({x:v.x+k.x/g.notes.length,y:v.y+k.y/g.notes.length}),{x:0,y:0});
 const a=path?center(path.a):point(home.anchors.contact),b=path?center(path.b):a;
 const mean={x:a.x+(b.x-a.x)*(path?.u||0),y:a.y+(b.y-a.y)*(path?.u||0)};
 const reach=pose.type==='drums'?6:pose.type==='chimes'?4:2;
 let workX=mean.x-dir*reach*cw-(rest.x-c.anchorX)*cw;
 let workY=Math.min(entry.y,mean.y+(c.groundRow-rest.y+1)*hh);
 if(pose.type==='piano'){
  const surface=point({x:home.anchors.contact.x,y:home.anchors.keyboard+7});
  workY=Math.min(entry.y,surface.y+(c.groundRow-rest.y+1)*hh);
 }
 if(pose.type==='radio'){
  const knob=point(worker.slot===0?home.anchors.keys[0]:home.anchors.dial);
  workX=knob.x-dir*3*cw-(rest.x-c.anchorX)*cw;workY=entry.y;
  targets.length=0;
  if(pose.time<2)targets.push({hand:'r',x:knob.x,y:knob.y,press:ease(pose.time/.5)*ease((2-pose.time)/.5),key:worker.slot===0?0:1});
 }else if(pose.type==='horn'&&c.bill){
  const mouth=point(home.anchors.mouth);
  workX=mouth.x-(c.bill.x+.5-c.anchorX)*cw;
  workY=mouth.y-(c.bill.y+.5-c.groundRow)*hh;
 }else if(c.rig?.species==='butterfly'){
  workX=mean.x-dir*3*cw;workY=mean.y+(c.groundRow-c.rig.body.y)*hh;
 }
 const character={...c,x:c.x+(workX/sx-c.x)*worker.inside,y:c.y+(workY/sy-c.y)*worker.inside,offsetY:0};
 const cl=Math.round(character.x*sx-c.anchorX*cw+(c.offsetX||0)*cw),ct=Math.round(character.y*sy-c.groundRow*hh);
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*hh};
 const points=[],contacts=[];const put=(x,y,glyph,color='#e4c391')=>points.push({x,y,glyph,color});
 const line=(a,b,glyph,color)=>{const n=Math.max(1,Math.ceil(Math.max(Math.abs(b.x-a.x)/cw,Math.abs(b.y-a.y)/hh)));for(let i=0;i<=n;i++){const u=i/n;put(a.x+(b.x-a.x)*u,a.y+(b.y-a.y)*u,glyph||((b.x-a.x)*(b.y-a.y)>0?'\\':'/'),color);}};
 if(worker.inside>.02&&c.rig?.species!=='butterfly')for(const [i,target] of targets.entries()){
  let tip={x:target.x+(pose.gesture==='brush'?Math.sin(pose.time*8)*unit*1.4:0),y:target.y},origin={x:hand.x-dir*i*cw*3,y:hand.y-i*hh};
  if(pose.type==='radio')tip={x:origin.x+(tip.x-origin.x)*target.press,y:origin.y+(tip.y-origin.y)*target.press};
  if(!target.press&&pose.type!=='radio'){const d=Math.hypot((tip.x-origin.x)/cw,(tip.y-origin.y)/hh),u=Math.min(1,7/Math.max(.01,d));tip={x:origin.x+(tip.x-origin.x)*u,y:origin.y+(tip.y-origin.y)*u};}
  const stick=['drums','chimes'].includes(pose.type);
  line(origin,tip,stick?null:'~',stick?'#e3c49b':c.inks.w||c.face);
  put(tip.x,tip.y,stick?'o':dir>0?')':'(',stick?'#f1dfba':c.face);
  if(pose.gesture==='brush')for(let tooth=-2;tooth<=2;tooth++)line({x:tip.x-dir*2*cw,y:tip.y-hh},{x:tip.x+tooth*cw*.5,y:tip.y+hh*.4},'|','#c4d3cb');
  contacts.push({...target,origin,tip,distance:Math.hypot((tip.x-origin.x)/cw,(tip.y-origin.y)/hh)});
 }
 const lift=Math.max(0,entry.y-workY);
 // A real wide step/bench supports the player; young bodies retain their
 // approved proportions rather than growing limbs to reach a tall keyboard.
 const stool=lift>hh*.3&&c.rig?.species!=='butterfly'?{x:pose.type==='piano'?entry.x:workX,y:entry.y,top:workY,width:pose.type==='piano'?home.width*unit*.78:Math.max(12,(c.rig?.body?.w||14)+5)*cw,cw}:null;
 return {character,points,contacts,cw,hand,pose,stool,targets};
}
export function drawMusicTools(ctx,staged,support=false){
 if(!support){drawBotanicalTools(ctx,staged);return;}
 const s=staged.stool;if(!s)return;
 const {cw}=staged,hh=cw*1.5;
 ctx.save();ctx.font='600 '+hh+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';ctx.strokeStyle='#14251e';ctx.lineWidth=Math.max(.7,cw*.16);
 const glyph=(x,y,g,color='#c5a078')=>{ctx.fillStyle=color;ctx.strokeText(g,x,y);ctx.fillText(g,x,y);};
 // Solid tread, paired legs, diagonal bracing and a short stair flight. These
 // supports are constructed glyphs rather than two unexplained long lines.
 for(let x=-s.width/2;x<=s.width/2;x+=cw){glyph(s.x+x,s.top+hh,'=');glyph(s.x+x,s.top+hh*2,'-','#927a5e');}
 for(let y=s.top+hh*3;y<s.y;y+=hh){
  for(const dir of [-1,1]){glyph(s.x+dir*(s.width/2-cw),y,'|');glyph(s.x+dir*(s.width/2-2*cw),y,':','#8d8168');}
  const u=(y-s.top)/(s.y-s.top);glyph(s.x+(u-.5)*(s.width-4*cw),y,'/','#9b896d');
 }
 const steps=Math.max(1,Math.ceil((s.y-s.top)/(hh*4))),side=staged.character.anchorX<38?-1:1;
 for(let i=0;i<steps;i++){
  const y=s.top+(s.y-s.top)*(i+1)/steps,x=s.x+side*(s.width/2+i*cw*2);
  for(let n=0;n<4;n++)glyph(x+side*n*cw,y,'=');
  if(i<steps-1)for(let yy=y+hh;yy<y+(s.y-s.top)/steps;yy+=hh)glyph(x+side*3*cw,yy,'|','#a08866');
 }
 for(const dir of [-1,1])for(let x=-2;x<=2;x++)glyph(s.x+dir*(s.width/2-cw)+x*cw,s.y,'_','#a48e6c');
 ctx.restore();
}
