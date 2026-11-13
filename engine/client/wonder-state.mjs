// Plain-language readings of a wonder's saved native state, and the player's
// choices (every authored routine; Python decides whether it makes sense now).
import BLUEPRINTS from './animation/wonders.json' with {type:'json'};
import ROUTINES from './animation/wonder-routines.json' with {type:'json'};
export const WONDER_CHOICES=Object.fromEntries(Object.keys(BLUEPRINTS).map(id=>[id,Object.entries(ROUTINES).filter(([,r])=>r.item===id).map(([key,r])=>[key,r.label])]));
const pct=v=>Math.round((Number(v)||0)*100)+'%';
const SUMMARY={
 topiary:s=>`Growth ${pct(s.growth)} · roots ${s.moisture<.35?'dry':'moist'}${s.snow>.2?' · snow on its head':''}${s.blossom>.3?' · in blossom':''} · ${s.trims|0} trims`,
 zen:s=>`${['Waves','Rings','Spiral','Smoothed'][Math.round(s.pattern)%4]} raked ${pct(s.raked)} crisp${s.leaves>.2?' · leaves on the sand':''}`,
 ice:s=>`Melted ${pct(s.melt)} · detail ${pct(s.detail)}${s.tarp>.5?' · under canvas':''}${s.puddle>.2?' · puddle at the base':''}`,
 sandcastle:s=>`${Math.round(s.towers)} towers · moat ${pct(s.moat)} · erosion ${pct(s.erosion)}${s.flag>.5?' · flag flying':''}`,
 gong:s=>`${s.ring>.1?'Still humming':'Quiet'} · bronze shine ${pct(s.shine)} · ${s.strikes|0} strikes`,
 aurora:s=>`${s.power>.5?'On':'Off'} · ${Math.round(s.ribbons)} ribbons · hue ${pct(s.hue)}`,
 rainbow:s=>`Water tank ${pct(s.water)} · ${s.arc>.2?'a rainbow is hanging in the mist':'no rainbow showing'}`,
 weather:s=>`Setting: ${['sun','rain','snow','wind'][Math.round(s.setting)%4]} · charge ${pct(s.charge)} · ${s.runs|0} tiny clouds made`,
 portal:s=>`${s.energy>.3?'Swirling':'Dormant'} · stability ${pct(s.stability)} · ${s.sent|0} pebbles sent through`,
 wormhole:s=>`Aperture ${pct(s.aperture)} · alignment ${pct(s.align)} · ${s.boats|0} paper boats`,
 blackhole:s=>`Containment ${pct(s.containment)}${s.containment<.3?' (needs tightening!)':''} · mass ${pct(s.mass)} · ${s.fed|0} leaves fed`,
 volcano:s=>`Pressure ${pct(s.pressure)}${s.eruption>.1?' · ERUPTING':''} · ${s.eruptions|0} eruptions${s.ash>.2?' · ash to sweep':''}`,
 tornado:s=>`${s.covered>.5?'Asleep under its cloth':'Spinning'} · size ${pct(s.size)} · mood ${s.mood>.5?'happy':'grumbly'}`,
 antigravity:s=>`Field ${pct(s.field)} · ${Math.round(s.floaters)} things floating · rings ${pct(s.rings)} aligned`,
 forcefield:s=>`Dome ${s.shield>.5?'up':'down'} · charge ${pct(s.charge)} · ${s.hits|0} dry sit-outs`,
 arch:s=>`Alignment ${pct(s.align)} · starlight ${pct(s.starlight)} · ${Math.round(s.traced)} stars traced${s.moss>.3?' · mossy':''}`,
 timemachine:s=>`Set to ${Math.round(s.year)} · charge ${pct(s.charge)} · ${s.trips|0} trips (he always comes back)`,
 booth:s=>`Door ${s.door>.5?'open':'shut'} · ${s.knocks|0} knocks, no answer yet${s.dust>.3?' · dusty':''}`,
 dimdoor:s=>`Opens onto: ${['the stars','under the sea','candy country','a lava field','an enormous eye'][Math.round(s.dimension)%5]} · hinges ${s.hinge<.4?'squeaky':'smooth'}`,
 teleporter:s=>`Charge ${pct(s.charge)} · lens ${s.lens<.5?'smudged':'clean'} · ${s.sent|0} pebbles beamed`,
 robot:s=>`Battery ${pct(s.battery)} · joints ${s.oil<.3?'squeaky':'oiled'}${s.rust>.2?' · rust spots':''} · ${s.greetings|0} greetings`,
 cloner:s=>`${s.sample>.5?'Feather loaded':'Empty pods'}${s.hologram>.2?' · a glowing double is standing in pod B':''} · ${s.cycles|0} cycles`,
 transmog:s=>`Hopper ${s.hopper>.5?'loaded':'empty'} · last result: ${['nothing','a flower','a rubber duck','one sock','a teacup'][Math.round(s.output)%5]}${s.jam>.3?' · JAMMED':''}`,
 printer:s=>`Paper ${pct(s.paper)} · ${Math.round(s.stack*40)} play Duck Bucks stacked (not real money)${s.jam>.3?' · jammed':''}`,
 perpetual:s=>`${Math.floor(s.turns)} turns and counting${s.oil<.25?' · squeaking':''}`,
 dna:s=>`${s.mixes|0} mixes${s.printout>.5?' · a printout is waiting':''} · vials ${s.clean<.4?'grubby':'clean'}`,
 ray:s=>`Charge ${pct(s.charge)} · target at ${Math.round(s.target*100)}% size · ${s.zaps|0} zaps`,
 lamp:s=>`Polish ${pct(s.polish)} · ${3-Math.round(s.wishes)} wishes left${s.smoke>.3?' · smoke curling out':''}`,
 cloak:s=>`${s.folded>.5?'Folded':'Hanging'} · shimmer ${pct(s.shimmer)}`,
 dreamcatcher:s=>`${pct(s.dreams)} full of dreams · ${Math.round(s.feathers)} feathers${s.tangle>.3?' · tangled':''}`,
 dragonegg:s=>`Warmth ${pct(s.warmth)} · incubation ${pct(s.incubation)}${s.incubation>=.99?' · something is looking out!':''} · embers ${pct(s.embers)}`,
};
export function wonderSummary(id,state={}){
 const p=BLUEPRINTS[id];if(!p||!state.wonder)return '';
 const s=Object.fromEntries(Object.entries(p.fields).map(([k,[d,lo,hi]])=>{const v=Number(state.wonder[k]);return [k,Number.isFinite(v)?Math.max(lo,Math.min(hi,v)):d];}));
 return SUMMARY[p.type]?.(s)||'';
}
