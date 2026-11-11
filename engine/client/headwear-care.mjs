import CARE from './animation/headwear-care.json' with {type:'json'};
import ACCESSORY_CARE from './animation/accessory-care.json' with {type:'json'};
import GARMENT_CARE from './animation/garment-care.json' with {type:'json'};
export {GARMENT_CARE};
export {ACCESSORY_CARE};
export {CARE as HAT_CARE};
export const hatCareChoices=p=>Object.entries(CARE).filter(([,s])=>(!s.materials||s.materials.includes(p.material))&&(!s.shapes||s.shapes.includes(p.shape))&&!s.excludeShapes?.includes(p.shape));
const clamp=v=>Math.max(0,Math.min(1,Number.isFinite(v)?v:0));
const smooth=v=>{const t=clamp(v);return t*t*(3-2*t);};
// Separate physical gestures, read solely from the native elapsed/contact state.
// The wing follows the age's fitted hat anchor, not a fixed adult coordinate.
export function hatCarePose(active,motion=true){
 const spec=CARE[active?.id]||ACCESSORY_CARE[active?.id]||GARMENT_CARE[active?.id];if(!spec||!motion)return null;
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
 case 'wipe_lenses':case 'clean_frames':x=-stroke*.4;sweep=Math.sin(t*Math.PI*6)*stroke;break;
 case 'dry_frames':y=stroke*.5;sweep=Math.sin(t*Math.PI*4)*stroke*.5;break;
 case 'settle_frames':x=-reach*.5;hold=t>=contact&&t<.8;break;
 case 'retie_bow':y=reach;sweep=Math.sin(t*Math.PI*6)*stroke*.7;break;
 case 'wring_scarf':y=reach*.7;sweep=Math.sin(t*Math.PI*8)*stroke;break;
 case 'brush_collar_snow':y=reach;sweep=stroke;break;
 case 'dab_bow':y=reach*.6;sweep=Math.sin(t*Math.PI*4)*stroke*.5;break;
 case 'clean_pendant':y=reach;sweep=Math.sin(t*Math.PI*6)*stroke;break;
 case 'settle_pendant':y=reach*.5;hold=t>=contact&&t<.8;break;
 case 'dab_earpads':x=stroke*.7;sweep=Math.sin(t*Math.PI*4)*stroke;break;
 case 'settle_headband':y=-reach*.4;hold=t>=contact&&t<.8;break;
 case 'brush_garment_snow':y=reach*.5;sweep=stroke*1.2;break;
 case 'brush_cloth':x=-stroke*.5;y=reach;sweep=Math.sin(t*Math.PI*6)*stroke;break;
 case 'smooth_cloth':y=reach*.7;sweep=stroke*.6;break;
 case 'wring_hem':x=-stroke;y=reach;sweep=Math.sin(t*Math.PI*8)*stroke;break;
 case 'shed_coat':x=Math.sin(t*Math.PI*6)*stroke;y=reach*.5;sweep=Math.sin(t*Math.PI*6)*stroke;break;
 case 'settle_collar':y=reach*.5;hold=t>=contact&&t<.8;break;
 case 'straighten_lapels':y=reach;sweep=Math.sin(t*Math.PI*4)*stroke*.7;break;
 case 'shake_cape':x=-reach;y=stroke;sweep=Math.sin(t*Math.PI*8)*stroke;break;
 case 'settle_clasp':x=-reach*.7;y=reach*.6;hold=t>=contact&&t<.8;break;
 case 'brush_bag':x=-reach;y=reach;sweep=Math.sin(t*Math.PI*6)*stroke;break;
 case 'dry_pocket':x=-reach;y=reach*.5;sweep=Math.sin(t*Math.PI*8)*stroke*.7;break;
 case 'tighten_straps':x=-reach*.5;y=reach*.6;sweep=stroke;break;
 case 'straighten_sash':y=reach*.7;sweep=Math.sin(t*Math.PI*4)*stroke*.6;break;
 }
 return {id:active.id,item:active.item,t,contact,anchor:spec.anchor,x,y,wing,sweep,hold,
  debris:active.applied&&t>=contact&&t<contact+.26?clamp((t-contact)/.26):null};
}
