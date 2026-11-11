import BLUEPRINTS from './animation/textiles.json' with {type:'json'};
export function textileSummary(id,state={}){
 const p=BLUEPRINTS[id],s=state.textile;if(!p||!s)return '';
 const damp=state.wetness>.5?'wet':state.wetness>.15?'damp':'dry',frost=s.frost>.25?' · frosted':'';
 if(p.type==='bundle')return (p.style==='reeds'?'Binding '+Math.round(s.tie*100)+'% secure':'Loft '+Math.round(s.loft*100)+'%')+' · '+damp+frost+' · original crafting material';
 return (['turf','moss','rubber'].includes(p.type)?p.material:s.roll>.8?'Rolled':s.roll>.05?'Partly folded':'Laid flat')+' · '+damp+frost+' · '+(s.tracks?.length||0)+' impressions';
}
