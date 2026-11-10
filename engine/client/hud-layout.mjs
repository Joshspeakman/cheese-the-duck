// Window-relative positions survive Retina scaling, resizing and text zoom.
export const HUD_PANELS={
 tools:{name:'Pond kit',visible:true},pond:{name:'Pond & weather',visible:true},
 emotion:{name:'Cheese’s emotions',visible:true},care:{name:'Care & connection',visible:false},
 menu:{name:'Game menu',visible:false},chat:{name:'Pond conversation',visible:true},
 progress:{name:'Growth & goals',visible:true},actions:{name:'Action belt',visible:true},
};
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
const finite=(n,fallback)=>typeof n==='number'&&Number.isFinite(n)?n:fallback;
export class HudLayout{
 constructor(saved=null){
  this.panels={};this.dialogs={};this.autoFade=true;
  if(saved?.version===1){
   this.autoFade=saved.autoFade!==false;
   for(const id of Object.keys(HUD_PANELS))if(saved.panels?.[id]){
    const p=saved.panels[id];this.panels[id]={visible:typeof p.visible==='boolean'?p.visible:HUD_PANELS[id].visible};
    if(Number.isFinite(p.u)&&Number.isFinite(p.v))Object.assign(this.panels[id],{u:clamp(p.u,0,1),v:clamp(p.v,0,1)});
    if(id==='chat'&&Number.isFinite(p.w)&&Number.isFinite(p.h))Object.assign(this.panels[id],{w:clamp(p.w,380,1000),h:clamp(p.h,180,650)});
   }
   for(const [id,p] of Object.entries(saved.dialogs||{}).slice(-24))if(Number.isFinite(p?.u)&&Number.isFinite(p?.v))this.dialogs[id]={u:clamp(p.u,0,1),v:clamp(p.v,0,1)};
  }
 }
 visible(id){return this.panels[id]?.visible??HUD_PANELS[id]?.visible??false;}
 show(id,visible=true){if(HUD_PANELS[id])this.panels[id]={...this.panels[id],visible};}
 defaults(W,H){
  const right=W-310;
  return {
   tools:{x:18,y:14,w:300,h:48},pond:{x:18,y:78,w:360,h:84},
   emotion:{x:right,y:78,w:292,h:210},care:{x:right,y:301,w:292,h:222},
   menu:{x:right,y:536,w:292,h:clamp(H-662,180,310)},
   chat:{x:18,y:H-365,w:Math.min(690,W-360),h:260},
   progress:{x:18,y:173,w:360,h:80},
   actions:{x:(W-Math.min(1090,W-32))/2,y:H-94,w:Math.min(1090,W-32),h:80},
  };
 }
 resolve(saved,base,W,H){
  const margin=8,w=Math.min(base.w,W-margin*2),h=Math.min(base.h,H-margin*2),dx=Math.max(0,W-w-margin*2),dy=Math.max(0,H-h-margin*2);
  return {x:clamp(saved?.u===undefined?base.x:margin+saved.u*dx,margin,margin+dx),y:clamp(saved?.v===undefined?base.y:margin+saved.v*dy,margin,margin+dy),w,h};
 }
 rect(id,W,H){const base=this.defaults(W,H)[id],p=this.panels[id];if(id==='chat'&&p?.w)Object.assign(base,{w:p.w,h:p.h});return this.resolve(p,base,W,H);}
 resize(id,w,h,W,H){
  if(id!=='chat')return;
  const r=this.rect(id,W,H);this.panels[id]={...this.panels[id],w:clamp(finite(w,r.w),380,Math.min(1000,W-16)),h:clamp(finite(h,r.h),180,Math.min(650,H-16))};
  this.move(id,r.x,r.y,W,H);
 }
 move(id,x,y,W,H){
  if(!HUD_PANELS[id])return;
  const r=this.rect(id,W,H),u=clamp((finite(x,r.x)-8)/Math.max(1,W-r.w-16),0,1),v=clamp((finite(y,r.y)-8)/Math.max(1,H-r.h-16),0,1);
  this.panels[id]={...this.panels[id],u,v};
 }
 dialogRect(id,base,W,H){return this.resolve(this.dialogs[id],base,W,H);}
 moveDialog(id,x,y,r,W,H){
  this.dialogs[id]={u:clamp((x-8)/Math.max(1,W-r.w-16),0,1),v:clamp((y-8)/Math.max(1,H-r.h-16),0,1)};
  if(Object.keys(this.dialogs).length>24)delete this.dialogs[Object.keys(this.dialogs)[0]];
 }
 preset(name='cozy'){
  this.panels={};this.dialogs={};
  if(name==='quiet')for(const id of Object.keys(HUD_PANELS))this.show(id,['tools','emotion','actions'].includes(id));
  if(name==='all')for(const id of Object.keys(HUD_PANELS))this.show(id,true);
 }
 save(){return {version:1,autoFade:this.autoFade,panels:structuredClone(this.panels),dialogs:structuredClone(this.dialogs)};}
}
export class IdleFade{
 constructor(now=0){this.lastInput=now;this.delay=60000;this.duration=1800;this.opacity=1;}
 wake(now){this.lastInput=now;this.opacity=1;}
 update(now,{eligible=true,enabled=true,reducedMotion=false}={}){
  if(!eligible||!enabled){this.wake(now);return 1;}
  const elapsed=Math.max(0,now-this.lastInput-this.delay);
  this.opacity=reducedMotion?(elapsed>0?0:1):1-clamp(elapsed/this.duration,0,1);
  return this.opacity;
 }
}
