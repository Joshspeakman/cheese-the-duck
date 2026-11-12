import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/costume-attachments.json' with {type:'json'};
export {BLUEPRINTS as COSTUME_ATTACHMENTS};
export function costumeColors(p){return {b:p.color,a:p.trim,s:p.shade,k:'#394c4b'};}
const mirror=c=>({'/':'\\','\\':'/','(':')',')':'(','<':'>','>':'<','[':']',']':'['}[c]||c);
// These are costume panels on a harness, not the duck's anatomical wings.
// Patterns are hand-built at each fitted size; no body or face cells are erased.
const PANELS={
 dragonfly:{large:['   __..--.',' ./:/:::/','/:/::.-\'','\\_.-\'',' /:./',' \\/'],small:[' .--.','/:./','\\-\'',' /:',' \\/']},
 moth:{large:['  .--._',' /:o::\\','(:/:::)',' \\:./',' /:*:\\','(::_:/'," '~-\'"],small:[' .--.','(:o:)',' \\:/',' /:*\\'," '~\' "]},
 feathers:{large:['    .-).','  .(///)',' (////)','(////)',' \\///)','  \\//)',"   '~'"],small:[' .-).','(///)','(//)',' \\/)',"  '\'"]},
 web:{large:['   /^\\',' ./|::\\_','/::|:/::^\\','\\::|/::/',' \\:/::/','  V~V~'],small:[' /^\\','/|:^\\','\\|:/',' V~V']},
 cupid:{large:[' .-..-.','(o(  )o)',' \\://)','  \\//)','  /))','  ~~'],small:[' .-.-.','(o:o)',' \\//','  \\/']}
};
export function fittedCostumeAttachment(rig,id,{phase=0}={}){
 const p=BLUEPRINTS[id];if(!p||!rig)return null;
 const back=new ObjectCanvas(76,48),front=new ObjectCanvas(76,48),b=rig.body,h=rig.head;
 const moving=/walking|dancing|hopping|flapping/.test(rig.action),rest=/sleeping|swimming/.test(rig.action),t=rig.motion===false?0:phase;
 const flex=rest?0:Math.sin(t*(moving?1.8:1))>.45?1:0,contacts={};
 if(PANELS[p.shape]){
  const small=rig.small,rows=PANELS[p.shape][small?'small':'large'],width=Math.max(...rows.map(r=>r.length));
  const root={x:Math.round(b.x),y:Math.round(b.y+Math.min(2,b.h*.35))};contacts.harness=root;
  const top=Math.max(1,root.y-(small?3:4)),bottom=Math.min(39,top+rows.length-1);
  const rootRow=rows[Math.min(rows.length-1,root.y-top)],inset=width-rootRow.trimEnd().length;
  // Flexible panel tips move; the final two root cells and backplate stay put.
  for(const side of [-1,1]){
   const base=side<0?root.x:Math.round(b.x+b.w-1),span=rest?Math.max(3,width-2):width;
   rows.forEach((row,j)=>{for(let i=0;i<row.length;i++)if(row[i]!==' '){
    const d=Math.min(span-1,width-1-i),x=base+side*(d+1-inset+(j<2?flex:0)),y=Math.min(bottom,top+j);
    const glyph=side<0?row[i]:mirror(row[i]),tone='o*'.includes(glyph)?'a':':/'.includes(glyph)?'s':'b';back.put(x,y,glyph,tone);
   }});
   back.line(base+side,root.y,base,root.y,'-','a');
   back.put(base+side,root.y,'o','a');
  }
  back.put(root.x-1,root.y+1,p.shape==='cupid'?'>':'[','s');
  if(p.shape==='dragonfly')back.put(root.x-width+1+inset,top+2,flex?':':'.','a');
 }else{
  const center=Math.round(h.x+(h.w-1)/2),width=Math.max(5,Math.min(11,Math.round(h.w))),left=center-Math.floor(width/2);
  const bandY=Math.max(1,Math.floor(h.y)-1),top=Math.max(0,bandY-(p.shape==='horns'?3:4));
  contacts.headband={x:Math.round(h.x),y:bandY};back.line(h.x,bandY,h.x+h.w-1,bandY,'~','s');
  if(p.shape==='horns'){
   for(const [i,x]of [left,left+width-3].entries()){
    const bend=(i?1:-1)*(flex?1:0);back.rows(i?[' /\\',' |:|',' \\_|']:['/\\','|:|','|_/'],x+bend,top,'b');
    back.put(x+1+bend,top+1,'/','a');back.line(x+1+bend,top+2,x+1,bandY,null,'s');
   }
  }else{
   // A foreshortened oval: inset upper arc, curved side turns and a lower
   // arc that runs into the wire support. No rectangular rim or bead curtain.
   const ringWidth=Math.max(8,width),ringLeft=center-Math.floor(ringWidth/2),ringTop=Math.max(0,top-1);
   back.line(h.x-1,bandY,h.x-1,ringTop+3,'|','s');
   back.line(h.x-1,ringTop+3,ringLeft+2,ringTop+3,'_','s');
   back.rows(['   .'+ '~'.repeat(ringWidth-7)+'.',
    " .'"+' '.repeat(ringWidth-4)+(flex?'\\':'.'),
    '('+' '.repeat(ringWidth-1)+')',
    " '-."+'_'.repeat(ringWidth-6)+".-'"],ringLeft,ringTop,'b');
   const glint=center-1+Math.floor(t*2)%3;back.put(glint,ringTop,'*','a');
   if(p.shape==='beaded_halo'){
    // Pearls follow the oval itself; the finer inner arc reads as a second wire.
    back.put(ringLeft+3,ringTop+3,'o','a');back.put(ringLeft+ringWidth-3,ringTop+3,'o','a');
    back.rows([" .-.","'   '"],center-2,ringTop+1,'s');
    back.put(center+2,ringTop+1,'o','a');
   }else back.put(ringLeft+ringWidth,ringTop+2,flex?'/':')','a');
  }
 }
 return {back:back.finish(),front:front.finish(),contacts,construction:'costume-attachment-v1'};
}
