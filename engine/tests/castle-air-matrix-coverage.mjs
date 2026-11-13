// Exact native matrix membership and completeness. Refusals are never counted
// as rendered successes, and one adapter/site cannot cover another case.
import {CASTLE_SCORES} from '../client/castle-care.mjs';
import {AIR_ATOMICS} from '../client/castle-air-geometry.mjs';
const check=(ok,label)=>{if(!ok)throw Error(label);};
const point=p=>Array.isArray(p)&&p.length===2&&p.every(Number.isFinite);
export function airFrameIdentity(scene){
 const w=scene.living?.plan?.carnival_work,s=w?.shared;
 if(!w)return null;
 return {mode:s?.mode==='egg-caregiver'?'egg':s?.mode==='flight-observer'?'flight':w.shared_physical?'shared':'solo',age:scene.duck.stage==='teen'?'juvenile':scene.duck.stage,cast:s?.operator.cast||'cheese',adapter:s?.operator.adapter||'cheese',score:w.id};
}
export class AirMatrixCoverage{
 constructor(manifest){
  check(manifest?.schema_version===1&&Array.isArray(manifest.cases)&&manifest.cases.length,'Invalid air matrix manifest');
  check(typeof manifest.frames_file==='string'&&/^[a-f0-9]{64}$/.test(manifest.frames_sha256),'Matrix must bind exact native frames');
  this.manifest=manifest;this.cases=new Map();this.seen=new Map();
  for(const c of manifest.cases){
   check(typeof c.id==='string'&&c.id&&!this.cases.has(c.id),'Duplicate or missing matrix case ID');
   check(['supported','refused'].includes(c.status)&&AIR_ATOMICS.includes(c.score),'Invalid matrix status or atomic score');
   for(const k of ['mode','age','cast','adapter'])check(typeof c[k]==='string'&&c[k],'Missing matrix identity '+k);
   if(c.status==='supported'){
    check(point(c.placement)&&point(c.center),'Supported case lacks exact placement/center');
    if(c.origin)check(point(c.origin.operator)&&(!c.origin.cheese||point(c.origin.cheese)),'Invalid selected fixture origin');
   }
   else{
    check(typeof c.reason==='string'&&c.reason.trim(),'Refusal lacks an explicit native reason');
    check(Array.isArray(c.attempts)&&c.attempts.length&&c.attempts.every(a=>point(a.placement)&&typeof a.reason==='string'&&a.reason.trim()),'Refusal lacks native placement attempts');
   }
   this.cases.set(c.id,c);
  }
 }
 match(scene){
  const id=scene._airMatrixCase,c=this.cases.get(id),identity=airFrameIdentity(scene);
  check(c,'Frame has no exact matrix case: '+id);check(c.status==='supported','Refused matrix case emitted a frame: '+id);check(identity,'Matrix frame lacks native work');
  for(const k of ['mode','age','cast','adapter','score'])check(identity[k]===c[k],`${id}: changed ${k}`);
  const center=scene.living.plan.carnival_work.physical?.center;
  check(point(center)&&center.every((v,i)=>Math.abs(v-c.center[i])<1e-9),id+': changed native placement center');
  return c;
 }
 record(scene,variant){
  const c=this.match(scene),key=c.id+'\n'+variant,s=this.seen.get(key)||{events:new Set(),phases:new Set(),frames:0};
  if(!s.phases.has('approach')&&scene.living.plan.carnival_work.physical.phase==='approach'){
   const w=scene.living.plan.carnival_work;s.origin={operator:[...w.physical.root],...(w.shared?.cheese?{cheese:[...w.shared.cheese.root]}:{})};
   if(c.origin)for(const actor of ['operator','cheese'])if(c.origin[actor])check(s.origin[actor]?.every((v,i)=>Math.abs(v-c.origin[actor][i])<1e-9),c.id+': changed selected '+actor+' origin');
  }
  s.phases.add(scene.living.plan.carnival_work.physical.phase);s.frames++;
  if(scene._physicalEvent!==undefined){const i=scene._physicalEvent;check(Number.isInteger(i)&&CASTLE_SCORES[c.score].effects[i],c.id+': invalid effect marker');s.events.add(i);}
  this.seen.set(key,s);
 }
 finish(variants){
  check(Array.isArray(variants)&&variants.length&&new Set(variants).size===variants.length,'Invalid replay variants');
  const supported=[],refused=[];
  for(const c of this.cases.values()){
   if(c.status==='refused'){refused.push(structuredClone(c));continue;}
   const checks={};for(const variant of variants){
    const s=this.seen.get(c.id+'\n'+variant);check(s,c.id+': missing rendered variant '+variant);
    for(const phase of ['approach','hold','exit'])check(s.phases.has(phase),c.id+': missing '+phase+' in '+variant);
    for(let i=0;i<CASTLE_SCORES[c.score].effects.length;i++)check(s.events.has(i),c.id+': missing authored effect '+i+' in '+variant);
    checks[variant]={frames:s.frames,phases:[...s.phases],effects:[...s.events].sort((a,b)=>a-b),origin:s.origin};
   }
   supported.push({...structuredClone(c),renderedVariants:checks});
  }
  const failedAttempts=[...this.cases.values()].flatMap(c=>(c.attempts||[]).filter(a=>a.accepted===false||c.status==='refused').map(a=>({caseId:c.id,...structuredClone(a)})));
  return {scope:this.manifest.scope,supportedCount:supported.length,refusedCount:refused.length,caseCount:this.cases.size,supported,refused,failedAttempts,failedAttemptCount:failedAttempts.length,supportedCasesWithPriorRefusals:supported.filter(c=>c.attempts?.some(a=>a.accepted===false)).length,ages:[...new Set([...this.cases.values()].map(c=>c.age))],casts:[...new Set([...this.cases.values()].map(c=>c.cast))],requiredPhases:['approach','hold','exit'],variants:variants.length,refusalValidation:'Native reasons retained; refused cases cannot emit rendered effect frames'};
 }
}
