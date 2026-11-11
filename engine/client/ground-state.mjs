import BLUEPRINTS from './animation/groundworks.json' with {type:'json'};
export function groundSummary(id,state={}){
 const p=BLUEPRINTS[id],s=state.ground;if(!p||!s)return '';
 const damp=state.wetness>.5?'wet':state.wetness>.15?'damp':'dry';
 return p.material+' · '+damp+(s.frost>.25?' · frosted':'')+' · '+(s.tracks?.length||0)+' footprints'+(p.type==='sand'?' · '+(s.furrows?.length||0)+' raked lines':p.type==='snow'?' · powder '+Math.round(s.powder*100)+'%':p.portable?' · original crafting material':'');
}
