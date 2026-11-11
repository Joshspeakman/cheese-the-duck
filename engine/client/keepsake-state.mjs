import BLUEPRINTS from './animation/keepsakes.json' with {type:'json'};
const GLOBE_CHOICES=[['globe_pump','Stir the snow'],['globe_follow','Follow a snowflake'],['globe_scene','Explore the miniature'],['globe_polish','Polish the rim']];
export const KEEPSAKE_CHOICES={snow_globe:GLOBE_CHOICES,snowglobe:GLOBE_CHOICES,crystal_ball:[['oracle_focus','Read the next weather front'],['oracle_compare','Compare with the sky'],['oracle_rim','Trace the sun and moon']]};
export function keepsakeSummary(id,state={}){
 const p=BLUEPRINTS[id],s=state.keepsake;if(!p||!s)return '';
 if(p.type==='globe'){const g=s.glass||{};return `${g.energy>.5?'Snow swirling':g.energy>.03?'Snow settling':'Snow resting'} · ${g.pumps||0} pump strokes · ${s.studies||0} miniature visits`;}
 if(p.type==='oracle'){const g=s.glass||{};return g.vision?`Last reading: ${g.vision.weather.replaceAll('_',' ')} at ${g.vision.biome.replaceAll('_',' ')} · ${g.readings||0} readings. Forecasts can change.`:'No reading yet. Touch the cradle to look at the next weather front.';}
 if(p.type==='barrel')return `${Number(s.litres||0).toFixed(1)} / ${p.capacity} L collected · ${s.frozen?'frozen':'liquid water'}`;
 if(p.type==='book')return `Page ${(s.page||0)+1} of ${p.pages} · ribbon at page ${(s.bookmark||0)+1} · ${s.studies||0} reading sessions`;
 if(p.type==='chest'||p.type==='basket')return `${p.type==='basket'?'Woven lining':s.open>.1?'Lid open':'Lid closed'} · ${s.sorted||0} careful sorts`;
 if(p.type==='frame')return `${s.studies||0} remembered moments`;
 return `${s.open>.5?'Open':p.type==='map'?'Rolled up':'Folded'} · ${s.studies||0} reading sessions`;
}
