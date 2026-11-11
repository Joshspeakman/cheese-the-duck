import BLUEPRINTS from './animation/architecture.json' with {type:'json'};
export function architectureSummary(id,state={}){
 const p=BLUEPRINTS[id],s=state.architecture;if(!p||!s)return '';
 const amount=(value,a,b)=>value>.9?a:value<.1?b:'partway';
 if(p.type==='flag')return 'Pennant '+amount(s.flag,'raised','lowered')+' · '+s.adjustments+' careful halyard pulls';
 if(p.type==='sundial')return s.sun>.1?'Sunlight casts a shadow across the dial':'No readable sunlight shadow';
 if(p.type==='vane')return 'Wind from '+['E','SE','S','SW','W','NW','N','NE'][Math.round((s.bearing||0)/(Math.PI/4))%8]+' · '+(s.wind>.1?'arrow following the breeze':'light air');
 if(p.type==='gate')return 'Gate '+amount(s.open,'open','closed')+' · '+s.adjustments+' careful adjustments';
 if(p.type==='mailbox')return 'Door '+amount(s.panel,'open','closed')+' · flag '+amount(s.flag,'raised','lowered')+' · empty compartment';
 if(p.type==='well')return 'Bucket '+amount(s.bucket,'lowered','at the rim')+' · nothing collected';
 if(p.type==='windmill')return (s.brake>.5?'Brake applied':'Brake released')+' · '+(s.speed>.05?'sails turning':'sails resting');
 return p.material+' · '+(s.season||'spring')+' · '+s.studies+' completed studies';
}
export const ARCHITECTURE_CHOICES={
 flag_pole:[['flag_hoist','Raise pennant','flag',1],['flag_lower','Lower pennant','flag',0]],
 gate:[['gate_open','Open gate','open',1],['gate_close','Close gate','open',0]],
 mailbox:[['mailbox_open','Open box','panel',1],['mailbox_close','Close box','panel',0],['mailbox_flag','Raise flag','flag',1],['mailbox_lower_flag','Lower flag','flag',0]],
 wishing_well:[['well_lower','Lower bucket','bucket',1],['well_raise','Raise bucket','bucket',0]],
 windmill:[['windmill_brake','Apply brake','brake',1],['windmill_release','Release brake','brake',0]]
};
