import {detailItem} from './item-detail.mjs';
import {EVENT_CATALOG,EVENT_ASSETS} from './event-catalog.mjs';
import {WILDLIFE} from './wildlife.mjs';
import {itemSprite,itemFamily} from './ultra-items.mjs';
const SPECIFIC={ButterflyAnimator:'butterfly',ButterflySwarmAnimator:'butterfly',BirdAnimator:'bird_flying',DuckVisitorAnimator:'baby_duck',FrogAnimator:'frog',DragonflyAnimator:'dragonfly',SquirrelAnimator:'squirrel',TurtleAnimator:'turtle',FireflyAnimator:'firefly',CrumbAnimator:'breadcrumbs',ShinyObjectAnimator:'coin',LilyPadAnimator:'lily_pad',DreamCloudAnimator:'thought_cloud',RainbowAnimator:'rainbow',MoonAnimator:'moon',UFOAnimator:'ufo',GhostDuckAnimator:'baby_duck',PortalAnimator:'portal',IcePalaceAnimator:'crystal'};
const ALIASES={hammer:'stone_hammer',basket:'storage_basket',bottle:'message_bottle',cookie:'heart_cookie',bell:'bell_collar',sundial:'clock',marble:'shiny_pebble',bread_loaf:'fancy_bread',seed_pile:'seeds',apple:'fresh_apple',bread_crumbs:'breadcrumbs',pizza_crust:'homemade_pie',donut:'heart_cookie',pretzel:'fancy_bread',sandwich:'fancy_bread',popcorn:'corn',muffin:'homemade_pie',crouton:'breadcrumbs',grape:'grapes',waffle:'heart_cookie',chip:'breadcrumbs',noodle:'worm',baguette:'fancy_bread',golden_bread:'honey_bread',feather_obj:'feather',old_map:'pirate_map',painted_rock:'shiny_pebble',snail_shell:'seashell',compass:'compass',fishing_line:'fishing_rod',key:'treasure_key',crystal:'crystal_shard',lantern:'lantern',bell:'bell_collar',nest:'basic_nest'};
const SKY={
 rainbow:['         .-------------------.','     .--\' .-----------------. \`--.','   .\' .--\' .------------- . \`--. \`.','  / ./ .--\'               \`--. \\. \\',' / / ./                       \\. \\ \\'],
 moon:['       .----.','     .\' .:::.\`\',','    / .:o::::. \\','   ( .:::: o:.  )','    \\ .:::.o. /',"     '.__..__.'"],
 aurora:['  /~~\\     /~~\\        /~~~\\',' /::  \\___/ :: \\______/ ::  \\','/.:    ~~~  .:    ~~~~   .:   \\','  :   :   .  :  .   :   .   :','  .       :     .       :    .'],
 constellation:['    *---.       *','   /     *-----/','  *       \\','   \\       *----*','    *----*'],
 shooting_star:[' .    .','   --==*','        \\','         .'],
 sun_rays:['    \\  |  /','  --- (O) ---','    /  |  \\','  /    |    \\'],
 cloud:['          .----.','      .--\' .::. \`--.','   .-\' .::::::..::  \`-.','  ( .::....::..::..::. )',"   '------------------'"],
 planet:['        .----.','    __./ .:::.\\.__','  _(==| ::o::: |==)_',"    '--\\.___. /--'"],
};
function ascii(rows){return rows.map(r=>r.replace(/[^\x20-\x7e]/g,c=>({'°':'o','•':'.','★':'*','♥':'<','→':'>','~':'~'}[c]||'*')));}
export function eventModel(event,time=0,motion=true){
 const meta=EVENT_CATALOG[event.id]||{},recipe=meta.recipe||[],asset=SPECIFIC[event.family||meta.animator]||event.asset||recipe[0];
 const t=motion?time:0,phase=Math.floor(t*5)%8;
 let art=WILDLIFE[asset]||SKY[asset],item=null;const authored=Boolean(art);
 if(!art){const id=ALIASES[asset]||asset;if(itemFamily(id)){item=itemSprite(id,t,{motion});art=item.art;}else art=EVENT_ASSETS[asset]?.frames?.idle||Object.values(EVENT_ASSETS[asset]?.frames||{})[0]||event.art||meta.original||[' . * .'];}
 if(!art.length)art=['  .   *',' *  .  ','   .  *'];
 if(!authored&&!item&&EVENT_ASSETS[asset]){
   const source=ascii(art),base={art:source,body:'#c9c5ae',accent:'#e6c573',face:'#e5dec1',shade:'#8e9e81',sway:0,lift:0};
   item=detailItem(base,{id:asset,category:EVENT_ASSETS[asset].category},asset,t,{motion});art=item.art;
 }
 art=ascii(art).map((line,y)=>[...line].map((c,x)=>{
  if((c==='O'||c==='o')&&y<art.length*.45&&phase===7)return '-';
  if(asset==='firefly'&&c==='*')return phase%2?'*':'.';
  if(asset==='aurora'&&c===':')return ['|',':','.'][Math.floor(t+x/3+y)%3];return c;
 }).join(''));
 const airborne=/bird_flying|hawk|bat|butterfly|bee|moth|dragonfly|mosquito|helicopter|balloon/.test(asset);
 if(airborne&&phase%4<2)art=art.map((r,y)=>' '.repeat(y<art.length/2?1:0)+r);
 const width=Math.max(...art.map(r=>r.length)),warm=/fox|squirrel|robin|crab|food/.test(asset),cool=/ghost|moon|portal|fish/.test(asset);
 const body=warm?'#d4a476':cool?'#b6d8e5':/frog|toad|turtle|insect/.test(asset)?'#acd18d':'#c9c5ae';
 const tones=art.map((r,y)=>[...r].map((c,x)=>'oO'.includes(c)?'e':/[=<>]/.test(c)?'a':/[.:v/]/.test(c)?'s':(x+y)%3?'b':'h').join(''));
 return {...item,art,tones,width,anchorX:width/2,groundRow:art.length,scale:(airborne?.75:.92)*(item?.detailScale||1),body,face:body,accent:'#e6c573',shade:'#809d87',inks:{b:body,h:'#e5dec1',s:cool?'#84aabc':'#8e9e81',a:'#e6c573',e:'#fff1ba'},offsetY:motion?(airborne?Math.sin(t*5)*.65:Math.sin(t*3)*.10):0,asset,name:'',event:true,design:'pond-wildlife',clipped:false};
}
export {EVENT_CATALOG,EVENT_ASSETS};
