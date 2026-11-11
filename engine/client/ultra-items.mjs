import {homeSprite} from './home-workshop.mjs';
import {playgroundSprite,PLAY_BLUEPRINTS} from './playground-workshop.mjs';
import {waterworksSprite,WATER_BLUEPRINTS} from './waterworks.mjs';
import {furnitureSprite,FURNITURE_BLUEPRINTS} from './furniture-workshop.mjs';
import {botanicalSprite,BOTANICAL_BLUEPRINTS} from './botanical-workshop.mjs';
import {detailItem,itemProfile} from './item-detail.mjs';
export {itemProfile};
import { ART } from './item-art.mjs';
import { ITEM_CATALOG } from './item-catalog.mjs';

// Specific shapes precede broad material families. Unknown future IDs keep their
// supplied original art; the coverage test requires every current ID to resolve.
const GROUPS={
 cap:'hat_red hat_blue cap_sports',party:'hat_party party_hat heart_hat',chef:'hat_chef',wizard:'hat_wizard wizard_hat',crown:'hat_crown crown_golden tiny_crown ancient_crown duck_crown snowflake_crown',viking:'hat_viking viking_helmet',pirate:'hat_pirate pirate_hat',cowboy:'hat_cowboy',tophat:'hat_tophat',beret:'hat_beret cherry_blossom_hat autumn_wreath_hat',beanie:'hat_beanie beanie_striped',sombrero:'hat_sombrero',glasses:'glasses_cool glasses_nerd sunglasses_aviator',monocle:'monocle',bow:'bowtie bow_tie_blue bow_tie_pink bandana',scarf:'scarf_red scarf_winter',cape:'cape cape_superhero invisible_cloak',wings:'wings_fairy',halo:'halo halo_angel guardian_blessing',horns:'devil_horns',headphones:'headphones',helmet:'space_helmet',bag:'backpack_tiny gathering_bag',
 ball:'toy_ball ball snowball frozen_dewdrop',blocks:'toy_blocks',trumpet:'toy_trumpet',skateboard:'toy_skateboard skateboard',piano:'toy_piano piano',trampoline:'toy_trampoline trampoline',slide:'toy_slide water_slide water_slide_mega rainbow_slide',swing:'toy_swing tire_swing',seesaw:'toy_seesaw',sandbox:'toy_sandbox sand_floor',radio:'toy_boombox nook_radio',disc:'frisbee',car:'toy_car',rope:'jump_rope rope string',yoyo:'yo_yo',kite:'kite paper_plane_design',telescope:'telescope',easel:'easel',drums:'drums',
 chair:'chair_wood',throne:'chair_throne golden_throne',table:'table_small coffee_table tiny_table bar_cart',bed:'bed_small bed_king cozy_bed',sofa:'couch sofa_fancy',shelf:'bookshelf bookshelf_wood trophy_case',desk:'desk desk_writing workbench',mirror:'mirror mirror_standing',cabinet:'dresser wardrobe cabinet',clock:'grandfather_clock clock',horse:'rocking_horse',fireplace:'fireplace',tv:'tv_stand',cushion:'bean_bag cushion',
 pool:'pool_kiddie pool_large pond hot_tub hot_tub_deluxe koi_pond infinity_pool pond_mat',fountain:'fountain_small fountain_grand fountain_decorative fountain_statue pond_fountain wish_fountain fountain',waterfall:'waterfall waterfall_mini',sprinkler:'sprinkler sprinkler_system',birdbath:'birdbath birdbath_garden bird_bath',bowl:'water_bowl',
 rose:'flower_rose rose rose_petal',tulip:'flower_tulip tulip tulip_bulb',sunflower:'flower_sunflower sunflower golden_flower golden_petal',tree:'tree_small tree_oak world_tree',cherry:'tree_cherry cherry_tree',willow:'willow_tree',hedge:'bush_hedge hedge_maze',rug:'grass_patch grass_floor moss_carpet carpet_red tatami_mat persian_rug rubber_mat welcome_mat rug woven_grass insulation thatch fabric_scrap',cactus:'cactus potted_cactus',bamboo:'bamboo',bonsai:'bonsai',flytrap:'venus_flytrap',garden:'herb_garden garden_plot flower_bed',mushroom:'mushroom_patch mushroom',duck:'topiary_duck duck_statue ice_sculpture duck_toy rubber_duck wind_up_duck squeaky_toy mud_sculpture',fern:'fern mint mint_leaves pond_weed seaweed pine_needle',flowerpot:'lavender flower_pot potted_plant wildflower garden_flower rainbow_flower flower dream_flower dandelion spring_petal flower_petal',
 house:'dog_house shed mud_hut wooden_cottage stone_house',fence:'picket_fence fence_section',wall:'stone_wall',arch:'archway cosmic_arch',gazebo:'gazebo',bridge:'bridge',tower:'tower castle_tower sand_castle watchtower',windmill:'windmill',gate:'gate',pergola:'pergola trellis',treehouse:'treehouse',birdhouse:'birdhouse',mailbox:'mailbox',well:'wishing_well',greenhouse:'greenhouse',barn:'barn',
 gnome:'garden_gnome',chimes:'wind_chimes shell_mobile fog_bell',sundial:'sundial',vane:'weather_vane',flag:'flag_pole parade_flag',hammock:'hammock',scarecrow:'scarecrow',totem:'totem_pole',path:'stepping_stones stone_tiles cobblestone pebble_path stone_path',bench:'garden_bench',zen:'zen_garden',lights:'fairy_lights glowsticks laser_lights',pinwheel:'pinwheel',barrel:'rain_barrel',wheelbarrow:'wheelbarrow',torch:'tiki_torch torches torch',trophy:'golden_duck_trophy memory_trophy splash_trophy fish_trophy master_trophy legendary_trophy',compass:'compass_rose pirate_compass',gong:'gong',bubbles:'bubble_machine bubble_wand frog_spawn',globe:'snow_globe snowglobe',lamp:'table_lamp floor_lamp lamp_floor fairy_lamp lamp crystal_lamp',chandelier:'chandelier candelabra',lantern:'paper_lantern lantern',lava_lamp:'lava_lamp',neon:'neon_sign',disco:'disco_ball',spotlight:'spotlight',streetlamp:'street_lamp',fire:'campfire eternal_flame warmth',lighthouse:'lighthouse',motes:'firefly_swarm fairy_dust dandelion_fluff mystery_sound',moon:'moon_lamp',projector:'star_projector hologram',aurora:'aurora',
 plank:'wooden_planks wooden_plank',tile:'marble_tiles checkered_floor mosaic_tiles ice_floor glass_floor',volcano:'volcano',lava_tile:'lava_floor',galaxy_tile:'galaxy_floor',cloud:'cloud_floor fog_essence',rainbow:'rainbow_path rainbow_generator',leaf:'autumn_leaves autumn_leaf red_maple_leaf golden_leaf leaf grass_blade moss lily_pad lettuce',snow:'snow_floor',portal:'portal wormhole teleporter dimensional_door',machine:'time_machine weather_machine cloning_machine transmogrifier money_printer',blackhole:'black_hole',infinity:'antigravity perpetual_motion',tornado:'tornado',egg:'dragon_egg mystery_egg mystic_egg',chest:'treasure_chest storage_chest weekly_chest',magic_carpet:'magic_carpet',orb:'crystal_ball force_field heart_of_pond',robot:'robot_butler',ray:'shrink_ray growth_ray',ufo:'ufo',genie:'genie_lamp',bouncehouse:'bounce_house',wheel:'ferris_wheel',carousel:'carousel',jetpack:'jetpack',submarine:'submarine',balloon:'hot_air_balloon',rocket:'rocket_ship',door:'tardis',dna:'DNA_mixer',dreamcatcher:'dream_catcher',gem:'philosophers_stone crystal crystal_shard mist_crystal crystal_icicle ice_crystal crystal_plant ruby_gem star_fragment sea_glass glitter_rock',
 bread:'fancy_bread ancient_bread honey_bread welcome_bread',crumbs:'bread breadcrumbs bread_crumb golden_crumb mysterious_crumb rainbow_crumb void_crumb rare_treat oats',seeds:'seeds seed sunflower_seeds vegetable_seed enchanted_seeds better_bait',worm:'worm juicy_worm giant_worm',fish:'fish_treat small_fish minnow carp bass trout koi salmon sturgeon golden_koi ghost_fish',puffer:'pufferfish',swordfish:'swordfish',catfish:'catfish',goldfish:'goldfish',dragonfish:'ancient_dragon_fish',feather:'feather eagle_feather golden_feather rainbow_feather static_feather snow_feather ancient_feather',rock:'shiny_pebble pebble smooth_stone rock iron_ore clay pond_clay sand shiny_object',clover:'lucky_clover clover',corn:'corn',peas:'peas',grapes:'grapes berry',boat:'tiny_boat',shell:'seashell shell sea_shell sand_dollar pretty_shell',stick:'cool_stick twig bark driftwood driftwood_large digging_stick',coin:'old_coin ancient_coin shiny_button',pearl:'river_pearl',bottlecap:'bottle_cap',frame:'duck_photo picture_frame sunset_photo',badge:'best_friend_badge racing_medal dance_medal spring_spirit_badge summer_spirit_badge harvest_spirit_badge winter_spirit_badge duck_day_champion_badge love_spirit_badge explorer_badge golden_badge',bottle:'medicine message_bottle glass_bottle',salad:'berry_salad',wreath:'flower_wreath flower_crown spring_wreath',basket:'storage_basket',amulet:'lucky_charm water_token earth_token sky_token ancient_amulet magpie_friendship_charm rainbow_charm',wand:'magic_wand',hammer:'stone_hammer',rod:'fishing_rod master_fishing_rod',nest:'basic_nest cozy_nest deluxe_nest nest_premium golden_nest',brick:'clay_brick stone_block',acorn:'acorn magic_acorn golden_acorn',pinecone:'pine_cone',reed:'reed',honey:'honeycomb',carrot:'carrot',tomato:'tomato fresh_apple',pumpkin:'pumpkin',strawberry:'strawberry',watermelon:'watermelon',wing:'butterfly_wing',jar:'rare_bug_jar',paper:'storm_sketch friendship_card',pie:'homemade_pie',gift:'mystery_gift',cookie:'heart_cookie',costume:'spring_duck_costume beach_duck_costume scarecrow_costume winter_coat_costume',surfboard:'surfboard',scale:'dragon_scale mermaid_scale',map:'pirate_map',key:'treasure_key',fossil:'fossil',book:'ancient_tome',plush:'plushie',
};
// Distinct surface treatments retain the familiar silhouettes of floor tiles.
ART.disc=['       .------------.','     .\' .----------. \'.','    (  (____________)  )',"     '----------------'"];
ART.tile=['       .--------------.','      / /__/__/__/__/ /|','     /_/__/__/__/__/ / |','    /_/__/__/__/__/_/ /','    |_______________|/'];
ART.cloud=['        .--.  .--.','     .-(    \/    )-.','    (                )',"     '--------------'"];
ART.snow=['       .------------.','      / * . * . * . /|','     / . * . * . * / /','    /_____________/ /','    |_____________|/'];
ART.magic_carpet=['      _/\__________/\_','     / /\/\/\/\/\/\/ /','    / /\/\ <> /\/\/ /','   /_______________/','     \/          \/'];
ART.genie=['             .--.','          __/____\__','     ____/          \o','    /___             )','        \___________/','             | |','          ___|_|___'];
const FAMILIES=new Map();
for(const [family,ids] of Object.entries(GROUPS))for(const id of ids.split(' '))FAMILIES.set(id,family);
for(const id of Object.keys(ITEM_CATALOG)){
  if(id.endsWith('_seeds'))FAMILIES.set(id,'seeds');
  if(ITEM_CATALOG[id].sources.includes('collectibles.COLLECTIBLES'))FAMILIES.set(id,'card');
}
export const itemFamily=id=>FAMILIES.get(id);
export const catalog=Object.values(ITEM_CATALOG);
const hash=value=>[...value].reduce((v,c)=>(v*31+c.charCodeAt(0))>>>0,7);
const RARITY={common:'#c5d5c6',uncommon:'#92d7a3',rare:'#83cde9',epic:'#c1a0f3',legendary:'#ffda80'};
export const rarityColor=value=>RARITY[value]||RARITY.common;
const SWATCHES=['#dfb37d','#83bedb','#ee9e9e','#b7cf8a','#d1ade0','#e9c574','#8fd3c4','#e7b0c9'];
const PLANTS=new Set('rose tulip sunflower tree cherry willow cactus bamboo bonsai flytrap fern flowerpot mushroom hedge garden leaf clover corn peas grapes reed'.split(' '));
const WATER=new Set('pool fountain waterfall sprinkler birdbath bowl'.split(' '));
const METAL=new Set('robot machine ray ufo rocket submarine jetpack telescope trumpet car radio tv helmet key clock compass'.split(' '));
const GLOW=new Set('torch fire lantern lamp lava_lamp chandelier lights neon disco spotlight streetlamp lighthouse motes moon projector aurora portal blackhole rainbow orb gem wand genie lava_tile galaxy_tile'.split(' '));
const ANIMATED=new Set([...PLANTS,...WATER,...GLOW,...'windmill chimes clock robot machine ray tornado infinity dna wheel carousel bubbles worm fish yoyo kite balloon vane'.split(' ')]);
const FLOOR=new Set('rug path tile snow zen magic_carpet lava_tile galaxy_tile'.split(' '));
export function itemPalette(id,family=itemFamily(id)){
  const item=ITEM_CATALOG[id],seed=hash(id);
  let body=SWATCHES[seed%SWATCHES.length],accent=SWATCHES[(seed+3)%SWATCHES.length];
  if(PLANTS.has(family)){body='#8cc68c';accent=/rose|berry|cherry|tomato/.test(id)?'#f2a4ad':/sun|gold/.test(id)?'#ffe08b':'#c0cdec';}
  else if(WATER.has(family)){body='#b7c8bf';accent='#8cdeed';}
  else if(METAL.has(family)){body='#c8d7dc';accent='#84dcd0';}
  else if(/chair|house|bed|desk|cabinet|bench|shelf|plank|barrel|nest|bridge|fence|barn/.test(family)){body='#c9a071';accent='#f0d6a0';}
  if(/gold|crown|throne|legend|philosoph/.test(id)){body='#e6bf65';accent='#fff0ab';}
  if(/crystal|ice|snow|ghost|glass/.test(id)){body='#a9d9e8';accent='#def9fb';}
  if(/red/.test(id)){body='#ea9b8d';accent='#ffd5ab';}
  if(/chef/.test(id)){body='#e9e2cf';accent='#fff6d9';}
  if(/wizard/.test(id)){body='#b2a1de';accent='#e9d18c';}
  if(/blue/.test(id)){body='#8fc6ed';accent='#b9e0ff';}
  if(/pink/.test(id)){body='#e9a4c3';accent='#ffe0ec';}
  if(/black|void/.test(id)){body='#a19dcc';accent='#e0baff';}
  const face='#'+body.slice(1).match(/../g).map(v=>Math.round(parseInt(v,16)*.6+255*.4).toString(16).padStart(2,'0')).join('');
  return {body,accent,face,shade:'#738f8c',rarity:rarityColor(item?.rarity)};
}
export function itemSprite(id,time=0,{motion=true,originalArt=null,state={},interaction=null,context={},pose={}}={}){
  const item=ITEM_CATALOG[id],family=itemFamily(id),seed=hash(id),t=motion?time:0,phase=Math.floor(t*3+seed%7);
  let lines=(ART[family]||originalArt||['[ item ]']).slice();
  if(family==='card'){
    const art=ART[id.startsWith('portrait')?'duck':id.includes('fish')?'fish':id.includes('frog')?'plush':id.includes('lily')?'rose':id.includes('dragonfly')?'wing':id.includes('sun')?'sunflower':id.includes('rainbow')?'rainbow':id.includes('rain')?'cloud':id.includes('snow')?'gem':id.includes('phoenix')?'wings':'egg'];
    const width=Math.max(20,...art.map(v=>v.length));
    lines=['+'+'='.repeat(width+2)+'+',...art.map(row=>'| '+row.padEnd(width)+' |'),'+'+'='.repeat(width+2)+'+'];
  }
  if(family==='windmill'&&phase%2){
    const rows=['      ||','      ||','======(o)======','      ||','      ||','      ||'];
    lines=rows.concat(lines.slice(6));
  }
  if(family==='clock')lines=lines.map((row,y)=>y===5?(phase%2?' |  o    |':' |    o  |'):row);
  if(family==='chimes')lines[lines.length-1]=phase%2?'    o':'      o';
  const animated=ANIMATED.has(family)||Boolean(item?.animated),emissive=GLOW.has(family)||/magic|rainbow|golden|crystal|enchanted/.test(id);
  // Use discrete authored glyph phases. No accumulated state: reduced motion and
  // reloading a menu are deterministic, and item movement cannot leave trails.
  lines=lines.map((line,y)=>[...line].map((c,x)=>{
    if(c==='~'&&WATER.has(family))return '~-~='[(phase+x+y)%4];
    if((c===':'||c==='.')&&family==='waterfall')return ':|:.'[(phase+y)%4];
    if(c==='*'&&emissive)return '*+*.'[(phase+x+y)%4];
    if(c==='@'&&/portal|orb|radio/.test(family))return '@oO@'[phase%4];
    if(c==='o'&&METAL.has(family)&&y>3)return phase%4===0?'*':'o';
    if(c===':'&&/fire|torch/.test(family))return ':|:.'[(phase+y)%4];
    if(c==='o'&&family==='clock'&&y===5)return phase%2?'o':'O';
    return c;
  }).join(''));
  const width=Math.max(...lines.map(v=>v.length)),colors=itemPalette(id,family);
  const tones=lines.map((line,y)=>[...line].map((c,x)=>{
    if(WATER.has(family)&&/[~:=.|]/.test(c)&&y<lines.length-2)return 'w';
    if(/[oO@*+<>]/.test(c))return 'a';
    if(PLANTS.has(family)&&/[;:]/.test(c))return 'f';
    if(/[=#]/.test(c))return 's';
    return y<2||x<width*.3?'f':'b';
  }).join(''));
  const base={...colors,id,family,art:lines,tones,width,anchorX:width/2,groundRow:lines.length,scale:1,
    emissive,animated,floor:FLOOR.has(family),name:'',
    // Slow physical movement where appropriate, kept much smaller than a cell.
    sway:(PLANTS.has(family)||['chimes','kite','swing'].includes(family))&&motion?Math.sin(t*1.3+seed)*.025:0,
    lift:/balloon|ufo|orb|motes|fish|worm/.test(family)&&motion?Math.sin(t*1.4+seed)*.25:0};
  const enriched={...base,...itemProfile(item||{},family)},options={motion,state,interaction,context,pose};
  return homeSprite(enriched,item||{id},t,options)||playgroundSprite(enriched,item||{id},t,options)||waterworksSprite(enriched,item||{id},t,options)||furnitureSprite(enriched,item||{id},t,options)||botanicalSprite(enriched,item||{id},t,options)||detailItem(base,item,family,t,{motion,state,interaction});
}
export function itemWorldScale(id){
  if(BOTANICAL_BLUEPRINTS[id])return BOTANICAL_BLUEPRINTS[id].scale;
  if(PLAY_BLUEPRINTS[id])return PLAY_BLUEPRINTS[id].scale;
  if(WATER_BLUEPRINTS[id])return WATER_BLUEPRINTS[id].scale;
  if(FURNITURE_BLUEPRINTS[id])return FURNITURE_BLUEPRINTS[id].scale;
  const item=ITEM_CATALOG[id],family=itemFamily(id);
  return ['house','barn','treehouse','greenhouse','tower','lighthouse','windmill','willow','tree'].includes(family)?1.15:
    item?.size==='large'?1.05:item?.size==='medium'?.85:.72;
}
// Match whole displayed names, longest first, never a random word in dialogue.
const names=catalog.flatMap(item=>item.aliases.map(name=>({id:item.id,name:name.toLowerCase()}))).sort((a,b)=>b.name.length-a.name.length);
export function selectedItem(ui,rows=[]){
  if(ui.itemPreview&&ITEM_CATALOG[ui.itemPreview])return ITEM_CATALOG[ui.itemPreview];
  const title=String(ui.modal?.title||'').toLowerCase();
  if(!/shop|invent|craft|build|material|decor|garden|seed|fish|collect|treasure|equip|wardrobe|use item/.test(title))return null;
  const selected=rows.find(row=>row.kind==='selected');if(!selected)return null;
  const text=selected.text.toLowerCase();
  const match=names.find(entry=>{const i=text.indexOf(entry.name);return i>=0&&!/[a-z]/.test(text[i-1]||'')&&!/[a-z]/.test(text[i+entry.name.length]||'');});
  return match?ITEM_CATALOG[match.id]:null;
}

// Cached, tightly bounded sprites avoid hundreds of per-glyph canvas calls for
// every placed object on every frame. Animation frames are quantized at 3 fps.
export class ItemPainter {
  constructor({maxBytes=64*1024*1024}={}){this.cache=new Map();this.bytes=0;this.maxBytes=maxBytes;}
  image(model,cw,surface='#102023ee',outline='#0c2024'){
    const unit=Math.max(2,Math.round(cw*2)/2),key=[model.id,unit,model.art.join('\n'),JSON.stringify([model.inks,model.panels,model.tones,model.fills]),surface,outline].join('|');
    if(this.cache.has(key)){const hit=this.cache.get(key);this.cache.delete(key);this.cache.set(key,hit);return hit;}
    const ch=unit*1.5,canvas=document.createElement('canvas');canvas.width=Math.ceil((model.width+2)*unit);canvas.height=Math.ceil((model.art.length+2)*ch);
    const ctx=canvas.getContext('2d');ctx.font=`600 ${ch}px Menlo, monospace`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.lineJoin='round';
    // Preserve the hand-built outline while keeping the busy terrain out of solid
    // furniture. No rectangular tile backgrounds and no blur on the ASCII ink.
    for(const fill of model.fills||[]){ctx.fillStyle=fill.opaque?(model.panels?.[fill.tone]||surface):model.body+'38';ctx.fillRect((fill.x+1)*unit,(fill.y+1)*ch,fill.w*unit,ch+.5);}
    model.art.forEach((line,y)=>{
      const a=line.search(/\S/),b=line.trimEnd().length;if(a<0)return;
      if(!model.fills&&!['motes','aurora','lights','chimes','reed','fern','sprinkler'].includes(model.family)){
        ctx.fillStyle=surface;ctx.fillRect((a+.8)*unit,(y+1)*ch,(b-a+.4)*unit,ch);
      }
    });
    model.art.forEach((line,y)=>[...line].forEach((c,x)=>{
      if(c===' ')return;
      const tone=model.tones[y][x],px=(x+1.5)*unit,py=(y+1.5)*ch;
      ctx.strokeStyle=outline;ctx.lineWidth=Math.max(1.3,unit*.23);ctx.strokeText(c,px,py,unit*1.15);
      ctx.fillStyle=model.inks?.[tone]||(tone==='a'?model.accent:tone==='f'?model.face:tone==='s'?model.shade:tone==='w'?'#8cdeed':model.body);
      ctx.fillText(c,px,py,unit*1.15);
    }));
    const bytes=canvas.width*canvas.height*4;
    while(this.cache.size&&(this.cache.size>=384||this.bytes+bytes>this.maxBytes)){
      const oldest=this.cache.keys().next().value;this.bytes-=this.cache.get(oldest).bytes;this.cache.delete(oldest);
    }
    const result={canvas,unit,ch,bytes};
    if(bytes<=this.maxBytes){this.cache.set(key,result);this.bytes+=bytes;}
    return result;
  }
  draw(ctx,model,x,y,cw,{shadow=true,surface,outline}={}){
    cw*=model.detailScale||1;
    const {canvas,unit,ch}=this.image(model,cw,surface,outline),width=(model.width+2)*cw,height=(model.art.length+2)*cw*1.5;
    ctx.save();ctx.translate(x,y-model.lift*cw*1.5);
    if(shadow){ctx.fillStyle='#05171965';ctx.beginPath();ctx.ellipse(0,0,width*.4,Math.max(2,cw*.55),0,0,Math.PI*2);ctx.fill();}
    ctx.transform(1,0,model.sway,1,0,0);
    ctx.drawImage(canvas,-width/2,-height+cw*1.5,width,height);ctx.restore();
  }
}
