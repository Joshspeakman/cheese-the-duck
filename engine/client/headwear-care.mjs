import CARE from './animation/headwear-care.json' with {type:'json'};
export {CARE as HAT_CARE};
export const hatCareChoices=p=>Object.entries(CARE).filter(([,s])=>(!s.materials||s.materials.includes(p.material))&&(!s.shapes||s.shapes.includes(p.shape))&&!s.excludeShapes?.includes(p.shape));
const clamp=v=>Math.max(0,Math.min(1,Number.isFinite(v)?v:0));
const smooth=v=>{const t=clamp(v);return t*t*(3-2*t);};
// Separate physical gestures, read solely from the native elapsed/contact state.
// The wing follows the age's fitted hat anchor, not a fixed adult coordinate.
export function hatCarePose(active,motion=true){
 const spec=CARE[active?.id];if(!spec||!motion)return null;
 const t=clamp(active.elapsed/spec.duration),contact=spec.contact/spec.duration;
 const reach=smooth(t/.24)*(1-smooth((t-.78)/.22));
 const stroke=smooth((t-.25)/.25)*(1-smooth((t-.58)/.2));
 let x=0,y=0,wing=reach,sweep=0,hold=false;
 switch(active.id){
 case 'shed_rain':x=Math.sin(t*Math.PI*8)*Math.sin(t*Math.PI)*1.7;y=Math.sin(t*Math.PI)*.6;wing=0;break;
 case 'dab_brim':y=smooth(t/.3)*.8;sweep=Math.sin(t*Math.PI*6)*stroke*.8;break;
 case 'brush_snow':x=-stroke;y=stroke;sweep=stroke;break;
 case 'wipe_visor':x=-stroke*.5;sweep=Math.sin(t*Math.PI*4)*stroke;break;
 case 'steady_brim':x=-reach*.6;y=reach*.4;hold=t>=contact&&t<.82;break;
 }
 return {id:active.id,item:active.item,t,contact,anchor:spec.anchor,x,y,wing,sweep,hold,
  debris:active.applied&&t>=contact&&t<contact+.26?clamp((t-contact)/.26):null};
}
