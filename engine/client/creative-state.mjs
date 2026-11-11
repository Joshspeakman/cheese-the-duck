import BLUEPRINTS from './animation/creative-props.json' with {type:'json'};
export function creativeSummary(id,state={}){
 const p=BLUEPRINTS[id],s=state.creative;if(!p||!s)return '';
 if(p.type==='scope')return `${s.cap>.5?'Lens capped':'Lens open'} · ${s.observations||0} observations`;
 if(p.type==='easel')return `${s.strokes===12?'Finished painting':`${s.strokes||0} of 12 paint layers`} · ${s.motif||'pond'}${s.cover>.5?' · canvas covered':''}`;
 if(p.type==='kite')return `${s.flights||0} completed flights · check the tail before flying`;
 return `${s.fold>.95?'Practice plane folded':s.fold>.05?'Crease in progress':'Design laid flat'} · ${s.folds||0} folding sessions`;
}
