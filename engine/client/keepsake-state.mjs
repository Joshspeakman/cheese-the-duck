import BLUEPRINTS from './animation/keepsakes.json' with {type:'json'};
export function keepsakeSummary(id,state={}){
 const p=BLUEPRINTS[id],s=state.keepsake;if(!p||!s)return '';
 if(p.type==='barrel')return `${Number(s.litres||0).toFixed(1)} / ${p.capacity} L collected · ${s.frozen?'frozen':'liquid water'}`;
 if(p.type==='book')return `Page ${(s.page||0)+1} of ${p.pages} · ribbon at page ${(s.bookmark||0)+1} · ${s.studies||0} reading sessions`;
 if(p.type==='chest'||p.type==='basket')return `${p.type==='basket'?'Woven lining':s.open>.1?'Lid open':'Lid closed'} · ${s.sorted||0} careful sorts`;
 if(p.type==='frame')return `${s.studies||0} remembered moments`;
 return `${s.open>.5?'Open':p.type==='map'?'Rolled up':'Folded'} · ${s.studies||0} reading sessions`;
}
