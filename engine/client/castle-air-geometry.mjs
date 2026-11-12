// Object-art coordinates, before the shared native-world/camera projection.
// The existing gauge control anchor remains unchanged; reading addresses ink.
export const CASTLE_DIAL={face:{x:157,y:136,w:9,h:4},needle_origin:[161,139],needle_center:[161.5,139.5],radius_x:4,radius_y:3};
export const AIR_ATOMICS=['castle_start','castle_stop','castle_vent_open','castle_vent_close','castle_hose_straight','castle_hose_stow','castle_grill_clean','castle_gauge_check'];
const ACTIVE=Symbol('native air occurrence projection');
export function castleTransit(work){return work?.[ACTIVE]==='transit';}
export function castleActiveWork(work){
 if(work?.[ACTIVE])return work;
 const marked=work&&Object.hasOwn(work,'air_procedure'),procedure=['castle_pressure_check','castle_dust_service'].includes(work?.id);
 if(!marked&&!procedure)return work;
 const p=work?.air_procedure,a=work?.atomic;
 if(!procedure||p?.version!==1||p.id!==work.id||!p.attempt||!Array.isArray(p.occurrences)||!Number.isInteger(p.cursor)||p.cursor< -1||p.cursor>=p.occurrences.length)return null;
 if(p.current_occurrence===null&&!Object.hasOwn(work,'atomic')){
  const initial=p.phase==='approach'&&p.cursor===-1&&p.occurrences.every(o=>o.status==='pending');
  const exiting=['exit','done'].includes(p.phase)&&p.occurrences.every(o=>['finished','skipped'].includes(o.status));
  return initial||exiting?{...work,[ACTIVE]:'transit'}:null;
 }
 const occurrence=p.occurrences[p.cursor];
 if(!occurrence||occurrence.status!=='active'||occurrence.occurrence_id!==p.current_occurrence||occurrence.atomic_id!==a?.id||a?.occurrence_id!==p.current_occurrence||!AIR_ATOMICS.includes(a.id)||!Number.isFinite(a.clock)||!Number.isFinite(a.ride_elapsed)||!Array.isArray(a.events)||typeof a.stage!=='string')return null;
 // Child execution cannot replace the outer mechanical roots or identities.
 return {...work,id:a.id,clock:a.clock,ride_elapsed:a.ride_elapsed,events:a.events,stage:a.stage,start:a.start,fractions:a.fractions,[ACTIVE]:'atomic'};
}
export function castleVisibleEyes(c){
 const eyes=[];
 c.art.forEach((row,y)=>[...row].forEach((glyph,x)=>{if(![' ','-','_'].includes(glyph)&&c.tones?.[y]?.[x]==='e')eyes.push([x+.5-c.anchorX+(c.offsetX||0),y+.5-c.groundRow+(c.offsetY||0)/1.5]);}));
 return eyes;
}
// Conservative construction bounds across inflation, floor pressure, door and
// apron states. Separate pieces leave the low metal control panel readable.
// Bounds include raster endpoints; they are not a sampled animation envelope.
export const CASTLE_FABRIC_OCCLUDERS=[
 {part:'roof',x:14,y:8,w:153,h:63},
 {part:'back',x:26,y:49,w:129,h:62},
 {part:'left_tower',x:4,y:12,w:27,h:112},
 {part:'right_tower',x:149,y:12,w:27,h:112},
 {part:'floor',x:25,y:109,w:131,h:16},
 {part:'base',x:10,y:118,w:157,h:19},
 {part:'apron',x:73,y:132,w:13,h:10},
 {part:'flag_sweep',x:28,y:1,w:77,h:130},
];
