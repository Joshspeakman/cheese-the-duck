import { scruffySprite, STAGES } from './scruffy-sprites.mjs';

// Translate the simulation's authored state names into the approved pose cycles.
export function bedheadAction(state='idle') {
  if(/sleep|napping/.test(state))return 'sleeping';
  if(/diving|swim|float|splash/.test(state))return 'swimming';
  if(/eating|peck|hungry/.test(state))return 'eating';
  if(/jump|hopp/.test(state))return 'hopping';
  if(/danc|playing|excited/.test(state))return 'dancing';
  if(/flap|wav|stretch/.test(state))return 'flapping';
  if(/clean|preen|shak/.test(state))return 'preening';
  if(/quack|sing|yawn/.test(state))return 'quacking';
  if(/walk|waddle|sneak/.test(state))return 'walking';
  return 'idle';
}
function expression(duck) {
  const state=duck.state||'idle',feeling=state==='idle'?duck.mood||state:state;
  if(/sleep|napping|bored/.test(feeling))return '-';
  if(/ecstatic|happy|love|petting|playing|proud|danc|excited/.test(feeling))return '^';
  if(/sad|miserable|sick|cold/.test(feeling))return ';';
  if(/scared|hiding|surpris|dramatic/.test(feeling))return 'O';
  if(/angry|grumpy|petty/.test(feeling))return '>';
  if(/dizzy/.test(feeling))return '@';
  if(/think|curious|reminiscing|wise/.test(feeling))return '.';
  return undefined;
}
export function bedheadDrawing(duck,time) {
  const state=duck.state||'idle',action=bedheadAction(state);
  const requested=duck.stage==='teen'?'juvenile':duck.stage;
  const stage=STAGES.some(s=>s.id===requested)?requested:'adult';
  const speed=state==='waddle_fast'?1.6:state==='sneaking'?.65:1;
  const emote=/love|petting/.test(state)?'<3':/think|curious/.test(state)?'?':/scared|angry/.test(state)?'!':undefined;
  const model=scruffySprite('B',stage,action,time*speed,duck.facing!==false,{
    eye:expression(duck),emote,cosmetics:duck.cosmetics,diving:state==='diving',
  });
  return {...model,scale:1.8,groundRow:21.5,design:'bedhead-bandit',action};
}
