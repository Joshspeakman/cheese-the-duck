// Read-only normalization of actual-host captures. Only review markers are
// attached to cloned scenes; native clocks, roots and execution stay untouched.
import {CASTLE_SCORES} from '../client/castle-care.mjs';
const check=(ok,label)=>{if(!ok)throw Error(label);};
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
export function airSessionEvidence(input){
 if(Array.isArray(input))return {frames:input,sessions:null};
 check(input?.schema_version===1&&typeof input.source==='string'&&Array.isArray(input.frames),'Invalid actual-host session evidence');
 const sessions=new Map();
 const frames=input.frames.map(f=>{
  const w=f.work,p=w?.air_procedure,attempt=p?.attempt;
  check(attempt&&w.id===f.score&&w.shared.attempt===attempt,'Wrong captured procedure attempt');
  const group=sessions.get(attempt)||{attempt,score:w.id,mode:f.mode,phases:new Set(),events:new Set(),initial:0,final:0,occurrences:null};
  check(group.score===w.id&&group.mode===f.mode,'Session identity changed');group.phases.add(f.session_phase);
  const s=structuredClone(f.scene),live=s.living?.plan?.carnival_work;
  if(f.label==='final'){check(!live&&p.phase==='done','Final session still owns a plan');group.final++;group.occurrences=p.occurrences;}
  else if(!live)check(f.session_phase==='done'&&p.phase==='done','Nonfinal session lost actual plan');
  else check(same(live,w),'Captured work differs from actual host scene');
  if(f.label==='initial')group.initial++;
  check(same(f.operator.root,w.physical.root),'Captured operator root differs from physical root');
  if(f.label==='native_event'){
   check(f.events?.length===1,'An exact event frame must contain one event');const e=f.events[0],a=w.atomic,spec=CASTLE_SCORES[a?.id];
   check(a&&a.occurrence_id===e.occurrence_id&&p.current_occurrence===e.occurrence_id&&a.id===e.atomic_id,'Wrong captured event occurrence');
   check(spec?.effects[e.index]&&a.events.includes(e.index)&&Math.abs(a.clock-e.clock)<1e-8,'Wrong captured event execution');
   check(same(e.actual_operator,f.operator),'Event operator differs from captured actual actor');
   check(same(spec.effects[e.index].slice(1),[e.field,e.value]),'Wrong event material field');
   group.events.add(e.occurrence_id+'/'+e.index);s._physicalEvent=e.index;
  }else check(!f.events?.length,'Event appeared outside exact event frame');
  s._airSessionCapture={label:f.label,attempt,phase:f.session_phase,operator:f.operator,observer:f.observer,shared:w.shared};sessions.set(attempt,group);return s;
 });
 for(const g of sessions.values()){
  check(g.initial===1&&g.final===1,'Incomplete session endpoints');
  for(const o of g.occurrences){
   if(o.status==='skipped'){check(o.reason&&!g.events.has(o.occurrence_id+'/0'),'Skipped occurrence acquired an effect');continue;}
   check(o.status==='finished','Unfinished final occurrence');
   for(let i=0;i<CASTLE_SCORES[o.atomic_id].effects.length;i++)check(o.execution.events.includes(i)&&g.events.has(o.occurrence_id+'/'+i),'Missing actual event capture '+o.occurrence_id+'/'+i);
  }
 }
 return {frames,sessions:[...sessions.values()].map(g=>({...g,phases:[...g.phases],events:[...g.events]})),source:input.source};
}
