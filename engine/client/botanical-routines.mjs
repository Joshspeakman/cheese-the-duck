import ROUTINES from './animation/botanical-routines.json' with {type:'json'};
export {ROUTINES as BOTANICAL_ROUTINES};
const clamp=n=>Math.max(0,Math.min(1,n));
const N={x:0,y:0,b:0,w:0,l:0,r:0,reach:0,pour:0,contact:0,u:0,v:0,eye:null,mark:''};
export function botanicalPose(routine,motion=true){
 const spec=ROUTINES[routine?.id];if(!spec||routine.interrupted)return null;
 const progress=motion?clamp(routine.elapsed/spec.duration):.5,track=spec.track;
 let a=track[0],b=track.at(-1);
 for(let i=1;i<track.length;i++)if(progress<=track[i][0]){a=track[i-1];b=track[i];break;}
 let u=clamp((progress-a[0])/Math.max(.001,b[0]-a[0]));u=u*u*(3-2*u);
 a={...N,...a[1]};b={...N,...b[1]};const pose={...a};
 for(const k of Object.keys(N))if(typeof N[k]==='number')pose[k]=a[k]+(b[k]-a[k])*u;
 if(u>.5){pose.eye=b.eye;pose.mark=b.mark;}
 return {...pose,botanical:true,progress,tool:spec.tool,anchor:spec.anchor};
}
export function botanicalOccupants(scene){
 const p=scene.living?.plan,records=[...(scene.living?.minds?.gardeners||[])];
 if(p?.care_routine&&!p.paused&&['prepare','act','settle'].includes(p.phase)){
  const progress=p.progress??p.elapsed/p.duration;
  records.push({actor:'cheese',id:p.target,instance:p.instance,destination:p.destination,slot:0,routine:p.care_routine,
   phase:p.phase==='act'?'inside':p.phase==='prepare'?'enter':'exit',
   elapsed:p.phase==='prepare'?clamp((progress-.15)/.13)*3:p.phase==='settle'?clamp((progress-.9)/.1)*3:0});
 }
 return records;
}
export function botanicalGeometry(home,worker,sx,sy){
 const c=worker.character,pose=botanicalPose(c.performance.routine,c.performance.motion!==false);
 const unit=sx*home.scale*home.detailScale,ch=unit*1.5;
 const left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*ch;
 const dir=worker.slot===0?1:-1,cw=c.scale*sx,hh=cw*1.5;
 const anchor=home.anchors[pose.anchor]||home.anchors.contact;
 const leaf=pose.anchor==='leaf'&&Number.isFinite(anchor.dx),length=leaf?Math.hypot(anchor.dx,anchor.dy)||1:1;
 const across=leaf?Math.min(2,anchor.width*.35):0;
 const dx=leaf?pose.u*anchor.dx*.18-pose.v*anchor.dy/length*across:pose.u*3;
 const dy=leaf?pose.u*anchor.dy*.18+pose.v*anchor.dx/length*across:pose.v*2;
 const target={x:left+(anchor.x+dx)*unit,y:top+(anchor.y+dy)*ch};
 const entry=home.anchors.entry,ground=top+entry.y*ch;
 const grip=c.grip||{x:c.anchorX+dir*4,y:c.groundRow-7};
 // Keep feet supported. A little two-step stool makes a high pot accessible
 // to a hatchling instead of stretching their wing or floating their body.
 const rest=c.workGripRest||grip;
 const reachAbove=pose.tool==='can'?-hh:hh*5;
 const lift=['lens','none'].includes(pose.tool)?0:Math.max(0,ground+(rest.y-c.groundRow)*hh-(top+anchor.y*ch)-reachAbove);
 const workX=left+anchor.x*unit-dir*cw*10-(rest.x-c.anchorX)*cw;
 const workY=pose.tool==='none'?Math.min(ground,top+anchor.y*ch+(c.groundRow-(c.rig?.head?.y||25))*hh):ground-lift;
 const character={...c,x:c.x+(workX/sx-c.x)*worker.inside,y:c.y+(workY/sy-c.y)*worker.inside,offsetY:0};
 const cl=Math.round(character.x*sx-c.anchorX*cw+(c.offsetX||0)*cw),ct=Math.round(character.y*sy-c.groundRow*hh);
 const hand={x:cl+(grip.x+.5)*cw,y:ct+(grip.y+.5)*hh};
 const points=[];
 const put=(x,y,glyph,color='#e9c788')=>points.push({x,y,glyph,color});
 const line=(a,b,glyph,color)=>{const n=Math.max(1,Math.ceil(Math.max(Math.abs(b.x-a.x)/cw,Math.abs(b.y-a.y)/hh)));for(let i=0;i<=n;i++){const u=i/n;put(a.x+(b.x-a.x)*u,a.y+(b.y-a.y)*u,glyph||((b.x-a.x)*(b.y-a.y)>0?'\\':'/'),color);}};
 let tip=null,stream=[];
 if(pose.tool!=='none'&&worker.inside>.02){
  const mapped=(x,y)=>({x:hand.x+x*cw*dir,y:hand.y+y*hh});
  const rows=(lines,x=0,y=0,color='#a7c8bc')=>lines.forEach((row,j)=>[...row].forEach((g,i)=>{if(g!==' '){const p=mapped(x+i,y+j);put(p.x,p.y,dir<0?({'/':'\\','\\':'/','(':')',')':'(','<':'>','>':'<'}[g]||g):g,color);}}));
  if(pose.tool==='can'){
   rows(['( )__','| |::|',' \\___/'],-1,0);
   const spout=mapped(8,-1-pose.reach);line(mapped(4,1),spout,null,'#b2d3ca');tip=spout;put(spout.x,spout.y,'o','#deebd1');
   // Every droplet travels from the actual spout to actual soil, and only
   // during the authored pour. The simulation clock freezes them on pause.
   if(pose.pour>.12&&worker.inside>.99){
    for(let i=0;i<6;i++){const f=(i/6+(c.performance.motion===false?0:c.performance.routine.elapsed*.9)%1)%1;
     const point={x:spout.x+(target.x-spout.x)*f,y:spout.y+(target.y-spout.y)*f};stream.push(point);put(point.x,point.y,'.','#b7e3df');}
    put(target.x,target.y,'~','#c4e5df');
   }
  }else{
   const rest=mapped(6+pose.u,-1+pose.v),touch=pose.tool==='lens'?0:pose.contact;
   tip={x:rest.x+(target.x-rest.x)*touch,y:rest.y+(target.y-rest.y)*touch};
   line(hand,tip,null,'#e0bc88');
   if(pose.tool==='lens'){
    [' .---.','(  /  )'," '---'"].forEach((row,y)=>[...row].forEach((glyph,x)=>{if(glyph!==' ')put(tip.x+(x-3)*cw,tip.y+(y-1)*hh,glyph,glyph==='/'?'#f1ebcd':'#b5e0d4');}));
   }
   else if(pose.tool==='probe')put(tip.x,tip.y,'v','#d4c1a0');
   else for(let i=-2;i<=2;i++)put(tip.x+i*cw,tip.y,pose.tool==='rake'?'v':'|',pose.tool==='rake'?'#d0c5a8':'#e6d59d');
   if(pose.contact>.8&&pose.tool==='brush')put(tip.x+dir*cw*3,tip.y-hh,'.','#bca17e');
  }
 }
 return {character,points,cw,hand,tip,target,stream,pose,
  stool:lift>.01?{x:workX,y:ground,top:workY,width:Math.max(10,c.rig?.body?.w||14)*cw,cw}:null};
}
export function drawBotanicalTools(ctx,staged,stool=false){
 const {cw}=staged;ctx.save();ctx.font='600 '+(cw*1.5)+'px Menlo, monospace';ctx.textAlign='center';ctx.textBaseline='middle';
 ctx.strokeStyle='#172b25';ctx.lineWidth=Math.max(.7,cw*.16);ctx.lineJoin='round';
 const glyph=(x,y,g,color)=>{ctx.fillStyle=color;ctx.strokeText(g,x,y);ctx.fillText(g,x,y);};
 if(stool&&staged.stool){const s=staged.stool;
  for(let x=-s.width/2;x<=s.width/2;x+=cw)glyph(s.x+x,s.top+cw*1.5,'=','#cba277');
  for(let y=s.top+cw*3;y<s.y;y+=cw*1.5)for(const dir of [-1,1])glyph(s.x+dir*(s.width/2-cw),y,'|','#b08d67');
  for(let x=-s.width/2;x<=s.width/2;x+=cw)glyph(s.x+x,(s.top+s.y)/2,'-','#cba277');
 }else if(!stool)for(const p of staged.points)glyph(p.x,p.y,p.glyph,p.color);
 ctx.restore();
}
