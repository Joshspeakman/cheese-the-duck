import { duckArt } from './ultra-art.mjs';

// Visitors retain their own authored faces, hats and props. These idle fallbacks
// are only needed by previews/older snapshots; the simulation supplies live art.
export const VISITOR_ART = {
  adventurous: ['   /^\\', '  (o.o)', '  /)_)\\>', '   " "'],
  scholarly:   ['  .--.', ' (O.O)', '  |__|>', "   ''"],
  artistic:    ['   ~@', '  (^.^)', '  /)~)\\>', "   ''"],
  playful:     ['   @/', '  (>.>)', '  /)_)\\>', "  d'' b"],
  mysterious:  ['  /_\\', ' (?_?)', '  |__|>', '   ~~'],
  generous:    ['  <3', '  (o.o)', '  /)_)\\>[+]', "   ''"],
  foodie:      ['  _|=|_', '  (o.o)', '  /)_)\\>', "   ''"],
  athletic:    ['  ===', ' (o.o)', ' /)_)\\>', '  / \\'],
};
const ACCENTS = {
  adventurous:'#eac386', scholarly:'#95d9ee', artistic:'#e5b9ec', playful:'#ffabbd',
  mysterious:'#bdb6ff', generous:'#f4bad4', foodie:'#ffbb80', athletic:'#b4dfa0',
};
const printable = line => [...line].map(c => c === '°' ? 'O' :
  c.charCodeAt(0) >= 32 && c.charCodeAt(0) <= 126 ? c : '*').join('');

export function characterSprite(duck,time,visitor=false) {
  const stage=duck.stage||'adult', state=duck.state||'idle';
  let art=(duck.art?.length ? duck.art : visitor ?
    VISITOR_ART[duck.personality]||VISITOR_ART.adventurous :
    duckArt(state,time,duck.facing!==false,stage)).map(printable);
  // Trim only shared padding, keeping the relative positions of every feature.
  const indents=art.filter(l=>l.trim()).map(l=>l.search(/\S/));
  const indent=indents.length?Math.min(...indents):0;
  art=art.map(l=>l.slice(indent).trimEnd());
  let faceRow=art.findIndex(l=>l.includes('('));
  if(!visitor&&stage!=='egg'&&faceRow>=0){
    const expression=state==='idle'?duck.mood||state:state;
    const eye=/happy|love|petting|playing|proud|danc|excited/.test(expression)?'^':
      /sleep|napping|bored/.test(expression)?'-':/sad|sick|cold/.test(expression)?';':
      /scared|surpris|quack|sing|yawn/.test(expression)?'O':/angry/.test(expression)?'>':
      /dizzy/.test(expression)?'@':null;
    if(eye)art[faceRow]=art[faceRow].replace(/[oO^;@]/,eye);
    else if(state==='idle'&&time%6.1>5.9)art[faceRow]=art[faceRow].replace('o','-');
  }
  const cosmetics=Object.values(duck.cosmetics||{}).join(' ');
  if(!visitor&&stage!=='egg'){
    if(/glass/.test(cosmetics)&&faceRow>=0)art[faceRow]=art[faceRow].replace(/[oO^;-]/,'@');
    if(/scarf|bow|tie/.test(cosmetics)&&art.length>2)art[2]=art[2].replace('__','><');
    if(/hat|crown|cap|beret/.test(cosmetics)){
      const hat=/crown/.test(cosmetics)?'\\V/V/':/party|wizard/.test(cosmetics)?' /^\\':
        /chef/.test(cosmetics)?' (___)':/beret/.test(cosmetics)?' ~@_':' _|_|_';
      art.unshift(hat);faceRow++;
    }
  }
  const width=Math.max(1,...art.map(l=>l.length));
  return {art,width,faceRow,name:visitor?duck.name||'Friend':'',
    scale:visitor?2.65:['hatchling','duckling'].includes(stage)?3.4:3.2,
    body:visitor?ACCENTS[duck.personality]||'#b8dee0':'#ffe29a',
    face:visitor?'#f4efdb':'#fff0b6',
    accent:visitor?ACCENTS[duck.personality]||'#b8dee0':'#ffba63',
    visitor,egg:stage==='egg',hat:!visitor&&/hat|crown|cap|beret/.test(cosmetics)};
}

export function drawCharacter(ctx,sprite,sx,sy,background) {
  const {art,scale,width,faceRow}=sprite;
  const cw=sx*scale,ch=cw*1.6;
  const left=Math.round(sprite.x*sx-width*cw/2),top=Math.round(sprite.y*sy-art.length*ch);
  ctx.save();
  ctx.font=`bold ${ch*.94}px Menlo, monospace`;
  ctx.textBaseline='middle';ctx.textAlign='center';ctx.lineJoin='round';
  // A quiet silhouette and a narrow outline keep tiny scenery/weather glyphs
  // out of the face. Blank space stays blank: no feather stippling or hatching.
  for(let row=0;row<art.length;row++){
    const line=art[row],start=line.search(/\S/),end=line.trimEnd().length;
    if(start<0)continue;
    ctx.fillStyle=background;
    ctx.fillRect(left+start*cw-cw*.08,top+row*ch+ch*.1,(end-start+.16)*cw,ch*.85);
  }
  for(let row=0;row<art.length;row++)for(let col=0;col<art[row].length;col++){
    const char=art[row][col];if(char===' ')continue;
    const px=left+(col+.5)*cw,py=top+(row+.5)*ch;
    ctx.strokeStyle=background;ctx.lineWidth=Math.max(2,cw*.17);
    ctx.strokeText(char,px,py,cw*1.12);
    ctx.fillStyle=row===faceRow?sprite.face:sprite.body;
    if((row===faceRow&&'<>'.includes(char))||row===art.length-1||(sprite.hat&&row===0))ctx.fillStyle=sprite.accent;
    ctx.fillText(char,px,py,cw*1.12);
  }
  if(sprite.name){
    const size=cw*.7,cy=top-size*.9;
    ctx.font=`bold ${size}px Menlo, monospace`;
    const nameWidth=ctx.measureText(sprite.name).width;
    ctx.fillStyle=background;ctx.fillRect(sprite.x*sx-nameWidth/2-4,cy-size*.6,nameWidth+8,size*1.2);
    ctx.fillStyle=sprite.body;ctx.fillText(sprite.name,sprite.x*sx,cy);
  }
  ctx.restore();
}
