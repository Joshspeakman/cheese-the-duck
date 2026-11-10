import { duckRig } from './duck-rig.mjs';
import { visitorRig } from './visitor-rig.mjs';

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
  const model=visitor?visitorRig(duck,time):duckRig(duck,time);
  return {...model,width:Math.max(1,...model.art.map(row=>row.length)),
    name:visitor?duck.name||'Friend':'',visitor};
}

export function drawCharacter(ctx,sprite,sx,sy,background) {
  const {art,scale,width}=sprite;
  const cw=sx*scale,ch=cw*1.5;
  const left=Math.round(sprite.x*sx-(sprite.anchorX??width/2)*cw+(sprite.offsetX||0)*cw);
  const top=Math.round(sprite.y*sy-(sprite.groundRow??art.length)*ch+(sprite.offsetY||0)*cw);
  ctx.save();
  ctx.font=`600 ${ch}px Menlo, monospace`;
  ctx.textBaseline='middle';ctx.textAlign='center';ctx.lineJoin='round';
  // A quiet silhouette and a narrow outline keep tiny scenery/weather glyphs
  // out of the face. Blank space stays blank: no feather stippling or hatching.
  for(let row=0;!sprite.fills&&row<art.length;row++){
    const line=art[row],start=line.search(/\S/),end=line.trimEnd().length;
    if(start<0)continue;
    if(sprite.backdrop){
      for(let col=start;col<end;col++){ctx.fillStyle=sprite.backdrop(left+(col+.5)*cw,top+(row+.5)*ch);ctx.fillRect(left+col*cw,top+row*ch,cw+.5,ch+.5);}
    }else{
      ctx.fillStyle=background;ctx.fillRect(left+start*cw-cw*.08,top+row*ch+ch*.1,(end-start+.16)*cw,ch*.85);
    }
  }
  // Colored feather interiors make the compact silhouette read at world scale.
  // Sunlight changes the material gently; the ASCII detail keeps its contrast.
  const shade=(hex,f)=>'#'+hex.slice(1,7).match(/../g).map(v=>Math.round(parseInt(v,16)*f).toString(16).padStart(2,'0')).join('');
  for(const fill of sprite.fills||[]){
    ctx.fillStyle=shade(sprite.inks[fill.tone]||sprite.body,(.50+.14*(1-fill.y/art.length))*(.62+.38*(sprite.sun??.7)));
    ctx.fillRect(left+fill.x*cw,top+fill.y*ch,fill.w*cw,ch+.25);
  }
  for(let row=0;row<art.length;row++)for(let col=0;col<art[row].length;col++){
    const char=art[row][col];if(char===' ')continue;
    const px=left+(col+.5)*cw,py=top+(row+.5)*ch;
    ctx.strokeStyle=sprite.outline||background;ctx.lineWidth=sprite.material==='feathers'?Math.max(.5,cw*.13):Math.max(1,cw*.17);
    ctx.strokeText(char,px,py,cw*1.12);
    const tone=sprite.tones?.[row]?.[col];
    ctx.fillStyle=sprite.inks?.[tone]||(tone==='c'?sprite.cosmetic||sprite.accent:tone==='a'?sprite.accent:tone==='f'?sprite.face:tone==='s'?sprite.shade:tone==='w'?'#8dc6cc':sprite.body);
    ctx.fillText(char,px,py,cw*1.12);
    if(tone==='e'&&char==='O'){ctx.font=`600 ${ch*.5}px Menlo,monospace`;ctx.fillStyle='#f3f1da';ctx.fillText('.',px-cw*.1,py-ch*.16);ctx.font=`600 ${ch}px Menlo,monospace`;}
  }
  if(sprite.name){
    const size=Math.max(cw*.95,sx*1.6),cy=top+Math.max(0,art.findIndex(r=>r.trim()))*ch-size*.9;
    ctx.font=`bold ${size}px Menlo, monospace`;
    const nameWidth=ctx.measureText(sprite.name).width;
    ctx.fillStyle=background;ctx.fillRect(sprite.x*sx-nameWidth/2-4,cy-size*.6,nameWidth+8,size*1.2);
    ctx.fillStyle=sprite.body;ctx.fillText(sprite.name,sprite.x*sx,cy);
  }
  ctx.restore();
}
