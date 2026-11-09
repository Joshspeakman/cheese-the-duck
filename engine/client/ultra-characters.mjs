import { cheeseDrawing,visitorDrawing } from './character-art.mjs';

// Original idle sprites used as the expression/accessory reference in previews.
// Live snapshots supply the original animated pose to the expanded drawings.
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
const COLORS = {
  adventurous:['#e6c69a','#fff1d4','#a9cf8a'],
  scholarly:['#c7d0dc','#f1f2df','#9dcde9'],
  artistic:['#e7e2dc','#fff5e4','#d9a6e8'],
  playful:['#f3db8d','#fff1c1','#ee9eaa'],
  mysterious:['#aaa8ce','#dedcf0','#b9a0e8'],
  generous:['#ebcd8e','#fff1c2','#ebaecb'],
  foodie:['#efbd86','#ffe5c1','#f6eddb'],
  athletic:['#c5a480','#f1d8b8','#f4b777'],
};
export function characterSprite(duck,time,visitor=false) {
  const model=visitor?visitorDrawing(duck,time):cheeseDrawing(duck,time);
  const [body,face,accent]=visitor?COLORS[duck.personality]||COLORS.adventurous:
    ['#efce80','#ffe9ad','#f5ab58'];
  return {...model,width:Math.max(1,...model.art.map(row=>row.length)),
    name:visitor?duck.name||'Friend':'',body,face,accent,shade:visitor?'#9da8a6':'#c49e59',visitor};
}

export function drawCharacter(ctx,sprite,sx,sy,background) {
  const {art,scale,width}=sprite;
  const cw=sx*scale,ch=cw*1.5;
  const left=Math.round(sprite.x*sx-(sprite.anchorX??width/2)*cw),top=Math.round(sprite.y*sy-art.length*ch);
  ctx.save();
  ctx.font=`bold ${ch}px Menlo, monospace`;
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
    const tone=sprite.tones?.[row]?.[col];
    ctx.fillStyle=tone==='a'?sprite.accent:tone==='f'?sprite.face:tone==='s'?sprite.shade:tone==='w'?'#8dc6cc':sprite.body;
    ctx.fillText(char,px,py,cw*1.12);
  }
  if(sprite.name){
    const size=Math.max(cw*.95,sx*1.6),cy=top-size*.9;
    ctx.font=`bold ${size}px Menlo, monospace`;
    const nameWidth=ctx.measureText(sprite.name).width;
    ctx.fillStyle=background;ctx.fillRect(sprite.x*sx-nameWidth/2-4,cy-size*.6,nameWidth+8,size*1.2);
    ctx.fillStyle=sprite.body;ctx.fillText(sprite.name,sprite.x*sx,cy);
  }
  ctx.restore();
}
