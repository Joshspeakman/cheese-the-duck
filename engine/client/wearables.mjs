import { WEARABLE_CATALOG } from './wearable-catalog.mjs';
import {HEADWEAR_BLUEPRINTS,fittedHat} from './headwear-workshop.mjs';

// Each family has its own fitted construction and motion. Slots describe where
// art attaches, independently of the three original wardrobe systems.
const GROUPS={
 cap:['head','hat_red hat_blue cap_sports'],party:['head','hat_party party_hat newyear_party_hat'],chef:['head','hat_chef'],
 wizard:['head','hat_wizard wizard_hat witch_hat halloween_witch_hat'],crown:['head','hat_crown crown_golden birthday_crown'],
 viking:['head','hat_viking viking_helmet'],pirate:['head','hat_pirate pirate_hat'],cowboy:['head','hat_cowboy'],
 tophat:['head','hat_tophat thanksgiving_pilgrim_hat'],beret:['head','hat_beret'],beanie:['head','hat_beanie beanie_striped'],
 sunhat:['head','hat_sombrero sun_hat summer_sun_hat spring_gardener_hat'],flowers:['head','flower_crown spring_flower_crown autumn_leaf_crown winter_snowflake_crown'],
 santa:['head','santa_hat winter_santa_hat'],ears:['head','bunny_ears easter_bunny_ears'],antlers:['head','winter_reindeer_antlers'],
 headband:['head','valentine_heart_headband'],icecream:['head','summer_ice_cream_cone'],earmuffs:['head','winter_earmuffs'],helmet:['head','space_helmet'],
 shades:['face','glasses_cool sunglasses_cool sunglasses_aviator summer_sunglasses'],glasses:['face','glasses_nerd'],
 hearts:['face','heart_glasses'],mask:['face','masquerade_mask'],newyear:['face','newyear_fancy_glasses'],monocle:['face','monocle'],
 bow:['neck','bowtie bow_tie_blue bow_tie_pink bowtie_red spring_butterfly_bow'],scarf:['neck','scarf_red scarf_winter scarf_striped autumn_scarf winter_cozy_scarf'],
 bandana:['neck','bandana'],pearls:['neck','pearl_necklace'],lei:['neck','flower_lei'],bell:['neck','bell_collar'],charm:['neck','autumn_acorn_charm'],
 cape:['back','cape cape_superhero superhero_cape'],bag:['back','backpack_tiny'],fairy:['wings','wings_fairy fairy_wings valentine_cupid_wings'],
 angel:['wings','angel_wings'],bat:['wings','bat_wings'],halo:['above','halo halo_angel'],horns:['above','devil_horns'],headphones:['above','headphones'],
 sweater:['body','sweater_cozy autumn_cozy_sweater'],shirt:['body','hawaiian_shirt summer_hawaiian_shirt'],tuxedo:['body','tuxedo'],
 robe:['body','wizard_robe'],santa_suit:['body','santa_suit'],raincoat:['body','raincoat spring_raincoat'],coat:['body','winter_puffy_coat'],
 pumpkin:['body','halloween_pumpkin_costume'],ghost:['body','halloween_ghost_sheet'],elf:['body','winter_elf_costume'],sash:['sash','birthday_sash'],
 boots:['feet','rain_boots spring_rain_boots autumn_boots winter_snow_boots'],slippers:['feet','bunny_slippers'],skates:['feet','ice_skates'],sandals:['feet','summer_flip_flops'],
 umbrella:['held','umbrella'],wand:['held','magic_wand'],rod:['held','fishing_rod'],bouquet:['held','bouquet'],basket:['held','easter_egg_basket'],mittens:['hands','winter_mittens'],
 sparkle:['special','sparkle_aura'],rainbow:['special','rainbow_trail'],bubbles:['special','heart_bubbles'],ring:['waist','summer_swim_ring'],
};
const LOOKS=new Map();
for(const [family,[slot,ids]] of Object.entries(GROUPS))for(const id of ids.split(' '))LOOKS.set(id,{family,slot});
const COLORS={red:'#ef8275',blue:'#80c8f1',pink:'#efa4cf',purple:'#ba9ae5',yellow:'#f3cf70',gold:'#f1ce73',white:'#e9eee6',black:'#9aa5be',silver:'#bddae5',brown:'#cda579',cyan:'#7fd7ce',rainbow:'#d69fe9'};
const BASE={cap:'red',party:'pink',chef:'white',wizard:'purple',crown:'gold',viking:'silver',pirate:'black',cowboy:'brown',tophat:'black',beret:'red',beanie:'blue',sunhat:'yellow',flowers:'pink',santa:'red',ears:'pink',antlers:'brown',headband:'pink',icecream:'pink',earmuffs:'blue',helmet:'cyan',shades:'black',glasses:'blue',hearts:'pink',mask:'purple',newyear:'gold',monocle:'gold',bow:'red',scarf:'red',bandana:'red',pearls:'white',lei:'pink',bell:'gold',charm:'brown',cape:'red',bag:'brown',fairy:'pink',angel:'white',bat:'purple',halo:'gold',horns:'red',headphones:'purple',sweater:'blue',shirt:'cyan',tuxedo:'black',robe:'purple',santa_suit:'red',raincoat:'yellow',coat:'blue',pumpkin:'yellow',ghost:'white',elf:'cyan',sash:'pink',boots:'yellow',slippers:'pink',skates:'silver',sandals:'cyan',umbrella:'red',wand:'gold',rod:'brown',bouquet:'pink',basket:'brown',mittens:'red',sparkle:'gold',rainbow:'rainbow',bubbles:'pink',ring:'yellow'};
const MOTION={
 cap:'A fitted brim follows head turns; a stitched badge catches the light.',party:'The pompom sways and the foil pattern flickers.',chef:'The soft crown puffs and settles above its fitted band.',wizard:'A bent tip sways over a fitted brim as embroidered stars twinkle.',
 crown:'Jewels catch the light while the band stays seated on his head.',viking:'The horns rock with his head; the metal rivet glints.',pirate:'The tricorn brim follows his head and the skull winks.',cowboy:'The curved brim tips with his head and its buckle glints.',tophat:'The tall crown stays fitted while the hatband buckle shines.',beret:'The soft crown shifts and its little stem flops.',beanie:'The pompom bobs above a snug knitted band.',sunhat:'The broad brim follows his head while its ribbon flicks.',flowers:'Individual flowers, leaves or snowflakes gently flutter.',santa:'A soft tip and white pompom flop independently.',ears:'The ears fold and spring back.',antlers:'Bells swing from the antlers as his head moves.',headband:'A heart bobs on its spring.',icecream:'The scoop wobbles above its cone.',earmuffs:'The padded cups move with his head and their stitch glints.',helmet:'A visor highlight sweeps over the fitted helmet.',
 shades:'The lens catches a moving reflection without covering his bill.',glasses:'The rim stays on his eye while a tiny reflection travels.',hearts:'Heart-shaped rims follow his expression and shimmer.',mask:'The eye opening stays clear while its feather flutters.',newyear:'Festive frames flash their little stars.',monocle:'The fitted lens glints while its chain swings.',
 bow:'The knot stays at his neck while the wings of the bow flex.',scarf:'The fitted neck wrap stays put while its loose tail streams behind.',bandana:'The neck knot stays attached as its triangular tail flutters.',pearls:'Pearls sway under the neck and catch small highlights.',lei:'Flowers bob independently around the neck.',bell:'The collar stays fitted while its little bell swings.',charm:'An acorn pendant swings from its cord.',cape:'The shoulder fastening stays attached while the hem billows behind.',bag:'The shoulder strap stays fitted while the flap and latch bounce.',fairy:'Two translucent wings beat and shimmer from his shoulders.',angel:'Feathered wings fold, spread and glow from the shoulders.',bat:'Webbed wings open and tuck behind his body.',halo:'A small halo floats and its highlights orbit.',horns:'Horns follow his head while their tips glint.',headphones:'The headband fits his head; the cups pulse to their own beat.',
 sweater:'The hem hugs his belly and its knit pattern rises with each breath.',shirt:'The collar fits his chest and the flower print shifts with his breathing.',tuxedo:'Fitted lapels and buttons follow his body.',robe:'A fitted robe hem sways while stitched stars twinkle.',santa_suit:'A white-trimmed coat and belt move with his body.',raincoat:'The hem sways and tiny droplets slide down its front.',coat:'Quilted panels compress with his breathing.',pumpkin:'The round costume follows his belly while the carved face flickers.',ghost:'The sheet drapes around his body with a rippling hem.',elf:'A fitted tunic ends in little swaying points.',sash:'The diagonal sash stays across his chest while its badge twinkles.',
 boots:'Each boot follows its own planted or lifted foot.',slippers:'Soft slippers follow each foot; their ears flop on a step.',skates:'Each blade follows its foot and catches a travelling glint.',sandals:'The straps stay on each foot through the waddle.',umbrella:'The wing holds the handle while the canopy rocks and sheds drops.',wand:'The wing holds the wand while its tip sends out little sparks.',rod:'A held rod flexes and its line and float sway.',bouquet:'The stems stay in his wing while the flowers nod.',basket:'The handle stays in his wing as the eggs jiggle.',mittens:'The mittens move with the wings.',sparkle:'Tiny sparks orbit outside his silhouette.',rainbow:'Short colored ribbons trail behind his steps.',bubbles:'Little hearts float up from his shoulder.',ring:'A fitted swim ring bobs around his belly.',
};
export const wearableCatalog=Object.values(WEARABLE_CATALOG);
export function wearableSpec(id){
 const look=LOOKS.get(id);if(!look)return null;
 const data=WEARABLE_CATALOG[id]||{id,name:id,rarity:'common'};
 let color=data.color||BASE[look.family];
 if(/blue|winter_cozy/.test(id))color='blue';else if(/pink|valentine/.test(id))color='pink';
 else if(/snow/.test(id))color='white';else if(/autumn/.test(id))color='brown';
 return {...data,...look,color:COLORS[color]||COLORS[BASE[look.family]],motion:MOTION[look.family]};
}
export function wornItems(cosmetics={}){
 const slots=new Map();for(const id of Object.values(cosmetics)){const item=wearableSpec(id);if(item)slots.set(item.slot,item);}
 return [...slots.values()];
}

// Rig coordinates are already posed. Art is built in character cells, so hats
// fit the age's head width and footwear follows the two actual foot contacts.
export function fitWearables(rig,cosmetics={},time=0,apparel={}){
 const layers=[],fills=[],items=wornItems(cosmetics),inks={};
 const h=rig.head,b=rig.body,n=rig.neck,e=rig.eye;
 const sleeping=rig.action==='sleeping',wet=rig.action==='swimming';
 const moving=/walking|dancing|hopping|flapping/.test(rig.action),small=rig.small;
 for(const [index,item] of items.entries()){
  const phase=Math.floor(time*(moving?7:3)+(index%3))%8,p=phase%4;
  const main=String.fromCharCode(256+index*3),trim=String.fromCharCode(257+index*3),shade=String.fromCharCode(258+index*3);
  inks[main]=item.color;inks[trim]='#fff0c7';inks[shade]='#819dbe';
  const add=(art,x,y,{tone=main,rear=false,clear=false,protectHead=false}={})=>layers.push({id:item.id,art:typeof art==='string'?[art]:art,x:Math.round(x),y:Math.round(y),tone,rear,clear,protectHead});
  const w=Math.max(3,h.w),center=h.x+(w-1)/2,fill=(c,size=w-2)=>c.repeat(Math.max(1,size));
  const headpiece=art=>{
   if(small){
    const compact={party:[p<2?' *':' o','/|\\','==='],wizard:[' /\\','/'+(p<2?'*':':')+'\\','===='],chef:[p<2?'.o.':'.-.','(_)','==='],
      viking:['\\_/','[=]'],pirate:['/X\\','==='],cowboy:['_^_','===='],beret:[p<2?' @':'~@','(==)'],
      sunhat:[' _ ','/==\\','====='],santa:[p<2?'/~o':'/~.','[=]'],ears:[p<2?'||':'|/','~~'],antlers:['Y Y','~o~'],
      headband:[p<2?'<3':' *',' |','~~~'],icecream:[p<2?'(o)':'(O)','\\:/',' V']};
    art=compact[item.family]||art;
   }
   const width=Math.max(...art.map(row=>row.length));
   if(rig.crest)add([' '.repeat(rig.crest.w)],rig.crest.x,rig.crest.y,{clear:true});
   add(art,Math.round(center-(width-1)/2),h.y-art.length+1,{clear:true});
  };
  const glint=phase===2||phase===6?'*':'.';
  if(HEADWEAR_BLUEPRINTS[item.id]){
   const material=apparel[item.id]||{},hat=fittedHat(rig,item.id,{material,phase:rig.motion===false||rig.hatCare?.hold?0:Number.isFinite(material.phase)?material.phase:time*3});
   const colors={b:HEADWEAR_BLUEPRINTS[item.id].color,f:'#eee0be',a:'#d4b47e',s:'#7e8986',k:'#343d3e',p:'#e5c5ba',q:'#93c1c9',g:'#8ab18a'};
   const tones=Object.fromEntries(Object.entries(colors).map(([tone,color],i)=>{const code=String.fromCharCode(512+index*12+i);inks[code]=color;return [tone,code];}));
   if(rig.crest&&!['flowers','ears','headband','antlers','earmuffs'].includes(item.family))add(' '.repeat(rig.crest.w),rig.crest.x,rig.crest.y,{clear:true});
   for(const f of hat.fills){add(' '.repeat(f.w),hat.x+f.x,hat.y+f.y,{clear:true});fills.push({id:item.id,x:hat.x+f.x,y:hat.y+f.y,w:f.w,tone:tones[f.tone]||tones.b});}
   hat.art.forEach((row,j)=>{for(let i=0;i<row.length;i++)if(row[i]!==' ')add(row[i],hat.x+i,hat.y+j,{tone:tones[hat.tones[j][i]]||tones.b});});
   continue;
  }
  switch(item.family){
   case 'cap':headpiece(['.'+fill('-')+'.','|'+fill('_')+(moving&&p===1?'_/':'_>')]);add(glint,Math.round(center),h.y-1,{tone:trim});break;
   case 'party':headpiece([p<2?'  o':' o~',' /'+(p%2?'*':':')+'\\','/'+fill('_')+'\\']);break;
   case 'chef':headpiece([p<2?'.-.-.':'.---.',p<2?'(   )':'(~~~)','|'+fill('_')+'|']);break;
   case 'wizard':headpiece([p<2?'   /\\':'  /~\\','  /'+glint+' \\',' / :  \\','='+fill('=',w)+'=']);break;
   case 'crown':headpiece(['\\'+fill('V',w-2)+'/','['+fill('=')+']']);add(glint,Math.round(center),h.y,{tone:trim});break;
   case 'viking':headpiece(['\\ '+fill('_')+' /',' ['+fill('=')+'] ']);add(glint,Math.round(center),h.y,{tone:trim});break;
   case 'pirate':headpiece(['  _'+(p===2?'x':'X')+'_',' /'+fill('_')+'\\','='+fill('=',w)+'=']);break;
   case 'cowboy':headpiece(['  _/\\_','\\_'+fill('_')+'_/']);add(p%2?'o':'*',Math.round(center),h.y,{tone:trim});break;
   case 'tophat':headpiece(['.'+fill('-')+'.','|'+fill(' ')+'|','|'+fill('=')+'|','='+fill('=',w)+'=']);add(glint,Math.round(center),h.y-1,{tone:trim});break;
   case 'beret':headpiece([p<2?'   @':'  ~@','.'+fill('~')+'.',"'"+fill('=')+"'"]);break;
   case 'beanie':headpiece([p<2?'  o':'   o','/'+fill('^')+'\\','['+fill('=')+']']);break;
   case 'sunhat':headpiece(['  .'+fill('-')+'.','__|'+fill('=')+'|__',"'"+fill('=',w+4)+"'"]);add(p<2?'~':'\\',h.x-1,h.y+1);break;
   case 'flowers':headpiece([(item.id.includes('leaf')?'vV':item.id.includes('snow')?'*+':p<2?'*o':'o*').repeat(Math.ceil(w/2)).slice(0,w),'~'+fill('~')+'~']);break;
   case 'santa':headpiece([p<2?'   /~o':'  /~~o','  /   \\','['+fill('=')+']']);break;
   case 'ears':headpiece([p<2?' /\\ /\\':' /\\ _/',' |/ |/','~'+fill('~')+'~']);break;
   case 'antlers':headpiece(['\\/| |\\/',' \\| |/ ',p<2?' o~~~o':'  o~o']);break;
   case 'headband':headpiece([p<2?'  <3':'   <3',p<2?'   |':'   /','~'+fill('~')+'~']);break;
   case 'icecream':headpiece([p<2?' .-o-.':' .-O-.','(~~~~~)',' \\:/ ','  \\/']);break;
   case 'earmuffs':headpiece(['.'+fill('-')+'.']);add('('+glint+')',h.x-3,h.y+1);add(']',h.x+w,h.y);break;
   case 'helmet':{
    if(rig.crest)add([' '.repeat(rig.crest.w)],rig.crest.x,rig.crest.y,{clear:true});
    add([' .'+fill('-',w)+'.'],h.x-2,h.y-1);for(let y=0;y<h.h;y++){add('|',h.x-2,h.y+y);if(y!==1)add('|',h.x+w+1,h.y+y);}
    add([' \\'+fill('_',w)+'/'],h.x-2,h.y+h.h);add(p<2?'/':"'",h.x-1,h.y,{tone:trim});break;
   }
   case 'shades':add(p===2?'[*]--':'[#]--',e.x-1,e.y);break;
   case 'glasses':add('['+e.char+']-',e.x-1,e.y);add(p===2?"'":'.',e.x+2,e.y-1,{tone:trim});break;
   case 'hearts':add(p<2?'<3>-':'<*>-',e.x-1,e.y);break;
   case 'mask':add('<'+e.char+'>~',e.x-1,e.y);add(p<2?'/':'~',e.x-1,e.y-1);break;
   case 'newyear':add(p<2?'[*]*':'[+]+',e.x-1,e.y);break;
   case 'monocle':add('('+e.char+')',e.x-1,e.y);add(p<2?':':';',e.x+1,e.y+1);add(p<2?'o':'.',e.x+1+(p===2?1:0),e.y+2,{tone:trim});break;
   case 'bow':add(p<2?'>o<':'}o{',n.x,n.y);break;
   case 'scarf':{
    add('['+'='.repeat(n.w)+']',n.x-1,n.y);
    const tail=sleeping?['|~','|_']:wet?['~~~',p<2?' ~~':'~~ ']:p<2?['~~\\','  ~']:['~\\',' ~\\'];
    add('~'.repeat(Math.max(1,n.x-b.x+1)),b.x-1,n.y,{rear:true});
    add(tail,b.x-3,n.y+1,{rear:true});add('|',n.x+1,n.y,{tone:trim});break;
   }
   case 'bandana':add('='+fill('=',n.w)+'=',n.x-1,n.y);add(p<2?'\\v/':'\\V/',n.x,n.y+1);break;
   case 'pearls':add(p<2?'o.o.o':'o*o.o',n.x-1,n.y);break;
   case 'lei':add(p<2?'*o*o*':'o*o*o',n.x-1,n.y);break;
   case 'bell':case 'charm':add('~'+fill('~',n.w)+'~',n.x-1,n.y);add(item.family==='bell'?(p<2?'(o)':'(+)'):'(@)',n.x+(p<2?0:1),n.y+1);break;
   case 'cape':{
    const size=small?3:5,spread=sleeping?2:wet?4:p<2?size:size+1;
    add(['/'+fill('~',spread-1)+'|','/'+fill(' ',spread-1)+'|',p<2?"'"+fill('~',spread):' '+fill('~',spread)],b.x-spread+1,b.y,{rear:true});
    add('o',b.x+1,b.y,{tone:trim,protectHead:true});break;
   }
   case 'bag':add(small?['._.','|'+(p<2?'o':'+')+'|']:['.---.','|'+(p<2?'[o]':'[+]')+'|','|___|'],b.x-(small?2:3),b.y,{rear:true});add('/',b.x+1,b.y,{protectHead:true});break;
   case 'fairy':case 'angel':case 'bat':{
    const fold=sleeping||wet,open=!fold&&p<2;
    const art=item.family==='bat'?(open?['/\\/\\','|/\\/']:['/|','|/']):item.family==='angel'?(open?['/)))','(///',' \\/']:['/))',' \\)']):(open?['/o\\','\\*/',' \\/']:['/|','|/']);
    add(art,b.x-(open?4:2),b.y-1,{rear:true});
    add(art.map(row=>[...row].reverse().map(c=>({'/':'\\','\\':'/','(' : ')',')':'('}[c]||c)).join('')),b.x+b.w-1,b.y-1,{rear:true});break;
   }
   case 'halo':add(p<2?'(=*=)':'(*==)',Math.round(center)-2,h.y-4-(phase===3?1:0),{tone:main});break;
   case 'horns':add('/^',h.x,h.y-1);add('^\\',h.x+w-2,h.y-1);add(glint,h.x+w-1,h.y-2,{tone:trim});break;
   case 'headphones':add('.'+fill('-')+'.',h.x,h.y-1);add(p%2?'[#]':'[=]',h.x-3,h.y+1);add(']',h.x+w,h.y);break;
   case 'sweater':case 'shirt':{
    // Cut each row to the actual posed feather silhouette: narrow shoulders,
    // curved breast, tucked belly and a feathered tail outside the garment.
    const knit=item.family==='sweater',torso=rig.torso||[],wing=rig.wing,face=rig.faceBounds||h;
    const color=(hex,f)=>'#'+hex.slice(1).match(/../g).map(c=>Math.min(255,Math.round(parseInt(c,16)*f)).toString(16).padStart(2,'0')).join('');
    inks[shade]=color(item.color,.62);inks[trim]=knit?color(item.color,1.15):'#f3dcb2';
    const inside=(x,y,r)=>r&&x>=r.x&&x<r.x+r.w&&y>=r.y&&y<r.y+r.h;
    for(const [j,span] of torso.entries()){
     const last=j===torso.length-1,first=j===0;
     const left=span.x+(span.w>10?2:0),right=span.x+span.w-1;
     let run=null;
     for(let x=left;x<=right;x++){
      const wingInset=wing&&span.y!==wing.y+1&&wing.h>1?1:0;
      const opening=wing?{...wing,x:wing.x+wingInset,w:wing.w-wingInset*2}:null;
      const foot=rig.feet.some(f=>span.y===f.y&&x>=f.x&&x<f.x+2);
      if(foot||inside(x,span.y,face)||inside(x,span.y,opening)){run=null;continue;}
      const q=x-left,edge=x===left||x===right;
      let ch=' ',tone=main;
      if(first){ch=knit?(q===0?'(':x===right?')':'='):(q===0?'\\':x===right?'/':q===Math.floor((right-left)/2)?'v':' ');tone=trim;}
      else if(last){ch=x===left?"'":x===right?"'":knit?'=':'_';tone=trim;}
      else if(edge){ch=x===left?(j<torso.length/2?'/':'\\'):(j<torso.length/2?'\\':'/');tone=shade;}
      else if(knit){ch=(q+j)%4===0?'v':q%4===0?':':' ';tone=(q+j)%4===0?trim:main;}
      else if((q+2*j)%7===1){ch='*';tone=trim;}
      else if((q+2*j)%7===2){ch='/';tone=shade;}
      // A stitched front/placket sits beside the wing, not across its feathers.
      if(!first&&!last&&x===right-2){ch=knit?':':j%2?'o':':';tone=knit?shade:trim;}
      if(!first&&!last&&!edge&&x===left+2&&j===Math.min(2,torso.length-2)){ch=moving?(p<2?'/':'~'):sleeping?'~':p===2?':':'/';tone=shade;}
      add(ch,x,span.y,{tone,clear:true,protectHead:true});
      // Cloth gets its own shaded fill; feather wings and faces stay exposed.
      if(!run||run.x+run.w!==x){run={id:item.id,x,y:span.y,w:1,tone:main};fills.push(run);}else run.w++;
     }
    }
    break;
   }
   case 'tuxedo':case 'robe':case 'santa_suit':case 'raincoat':case 'coat':case 'pumpkin':case 'ghost':case 'elf':{
    const width=Math.max(5,b.w-1),inner=width-2;
    let motif={sweater:p<2?'v':'^',shirt:p<2?'*':'+',tuxedo:' ',robe:p<2?'.':'*',santa_suit:'=',raincoat:p<2?':':"'",coat:p<2?'=':'-',pumpkin:p<2?'v':'V',ghost:' ',elf:p<2?'v':'^'}[item.family];
    const rows=['/'+fill('_',inner)+'\\',...Array.from({length:Math.max(1,b.h-2)},(_,j)=>'('+Array.from({length:inner},(_,x)=>x%5===0?'|':(x+j)%3===0?motif:'.').join('')+')'),"'"+fill(item.family==='ghost'?(p<2?'~':'v'):'_',inner)+"'"];
    if(item.family==='tuxedo')rows[1]='('+fill(' ',Math.max(0,Math.floor(inner/2)-1))+'V'+fill(' ',Math.max(0,inner-Math.floor(inner/2)))+')';
    add(rows.slice(0,b.h),b.x+1,b.y,{clear:true,protectHead:true});
    add(item.family==='pumpkin'?'o_o':item.family==='santa_suit'?'[+]':item.family==='tuxedo'?':':'o',b.x+Math.floor(width/2),b.y+1,{tone:trim,protectHead:true});break;
   }
   case 'sash':for(let j=0;j<b.h;j++)add(j===1?(p<2?'*':'o'):'/',b.x+b.w-3-j,b.y+j,{protectHead:true});break;
   case 'boots':case 'slippers':case 'skates':case 'sandals':{
    if(wet||sleeping)break;
    for(const [i,foot] of rig.feet.entries()){
     const rows=item.family==='boots'?['|=|','|_>']:item.family==='slippers'?[p<2?'^^':'^~','(o>']:item.family==='skates'?['|_]','-->']:[' /_','(__'];
     add(rows,foot.x,foot.y-1,{clear:true});if(item.family==='skates'&&phase===i+2)add('*',foot.x+2,foot.y,{tone:trim});
    }break;
   }
   case 'umbrella':{
    const x=b.x+b.w+3,y=h.y-3;
    add([p<2?' .---.':' .-~-.','/|_|_|\\'],x-3,y);for(let j=y+2;j<=b.y+1;j++)add('|',x,j);
    add('o--J',x-3,b.y+1,{tone:trim});add(phase%2?'.':"'",x+4,y+3+(p%2),{tone:shade});break;
   }
   case 'wand':{const x=b.x+b.w+1;add([' *','/'],x,b.y-2);add('--',x-1,b.y);add(p<2?'+':'.',x+3,b.y-3-p%2,{tone:trim});break;}
   case 'rod':{const x=b.x+b.w;add(p<2?['   /~.','  /  :',' /   :','/    o']:['   /~.','  /   :',' /    :','/    o'],x,b.y-3);add('--',x-1,b.y,{tone:trim});break;}
   case 'bouquet':case 'basket':{const x=b.x+b.w;add(item.family==='bouquet'?[p<2?'*o*':'o*o','\\|/',' V ']:[' /\\',p<2?'(oO)':'(Oo)','[==]'],x,b.y-2);add('--',x-1,b.y,{tone:trim});break;}
   case 'mittens':add(p<2?'(m)':'(w)',b.x-1,b.y+1);add('(m)',b.x+b.w-1,b.y+1);break;
   case 'sparkle':case 'bubbles':{
    const x=b.x-3+(p%2),y=b.y-1-p;
    add(item.family==='bubbles'?(p<2?'<3':'o'):p<2?'*':'+',x,y,{tone:trim,rear:true});
    add(item.family==='bubbles'?'o':'.',b.x+b.w+2,b.y-2+(p%2),{rear:true});break;
   }
   case 'rainbow':add(p<2?['~--',' ~~','  ~']:[' ~~','~--',' ~~'],b.x-5,b.y+1,{rear:true});add('~',b.x-3,b.y+2,{tone:trim,rear:true});break;
   case 'ring':add('('+fill('=',b.w)+')',b.x-1,b.y+b.h-1);add(p<2?'o':'*',b.x+b.w,b.y+b.h-1,{tone:trim});break;
  }
 }
 return {layers,fills,inks,items};
}

export function paintWearables(cells,tones,rig,plan){
 const H=cells.length,W=cells[0].length;
 const inside=(x,y,r)=>x>=r.x&&x<r.x+r.w&&y>=r.y&&y<r.y+r.h;
 let clipped=false;
 for(const layer of [...plan.layers.filter(l=>l.rear),...plan.layers.filter(l=>!l.rear)]){
  for(const [row,line] of layer.art.entries())for(const [col,char] of [...line].entries()){
   const x=layer.x+col,y=layer.y+row;
   if(char===' '&&!layer.clear)continue;
   if(x<0||x>=W||y<0||y>=H){if(char!==' ')clipped=true;continue;}
   if((layer.protectHead||plan.items.find(i=>i.id===layer.id)?.slot==='neck')&&inside(x,y,rig.faceBounds||rig.head))continue;
   if(layer.rear&&(inside(x,y,rig.body)||inside(x,y,rig.faceBounds||rig.head)||cells[y][x]!==' '))continue;
   cells[y][x]=char;tones[y][x]=layer.tone;
  }
 }
 return clipped;
}
