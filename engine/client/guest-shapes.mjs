// Character components are drawn in glyphs, never scaled copies of Cheese.
// Each named duck has a chosen head/body combination and signature belongings.
const HEADS={
 small:['      ,~.','     / .\\','    ( O _)=>',"     '._/"],
 round:['      .---.','    .\' . .\`.','   / .     . \\','  (  O    ___)==>',"   \\  .  .  /","    '------'"],
 longbill:['       .--.','     .\' .  \\','    ( O  ___)=====>',"     \\ .__.-'","      |  |"],
 swept:['       /\\_','     _/  /\`.','   .\' . / . \\','  ( O    ___)==>',"   '.__.-'"],
 brow:['      .----.','    .\' .::  \\','   /  ---   .|','  (   O  ___)==>',"   \\ .___.. /","    '------'"],
 bob:['      .----.','    .\'______\`.','   /|  . .  |\\','  ( | O  ___)==>',"   \\|.___..|/"],
 tuft:['     /| /|','    / |/ /_','   ( . . . \`.','  /  O   ___)==>',"  \\ .  .  /","   '------'"],
 wedge:['       /\\','      / .\`-.','     / . .  \\','    ( O  ___)==>',"     \\.___./"],
 sleepy:['       .---.','     .\' . . \`.','    /  __  .  \\','   (   O   ___)==>',"    \\ . .  . /","     '------'"],
 curly:['     @~@~@','   .@ . . @.','  (@  . .  @)','  (  O   ___)==>',"   \\ .__.. /","    '-----'"],
 pom:['       .----.','      / .~~. \\','     ( (__/ . )',"      '.__.--'",'     / . . . \\','    ( O   ___)==>',"     \\.___./"],
};
const BODIES={
 pear:["         /'--.\\","       .' .vv. '\\",'     .\' .  .  . \\',"   .' . /vvvv\\ . \\",'  / .  ( [==] ) . |','<( . .  \\vvvv/ . . )',"  \\ . .  . . .  ./","   '._ . . . _.-'","      '-----'"],
 runner:["        /'=='.\\",'       / .vv.  |','      / . . .  |',"     / . /vv\\ .|",'    <( .([==]) .|','     |. .\\vv/ . |','     | . . . . /',"      \\ . . . /","       '-----'"],
 barrel:["       .-'==`-.","    .-' . . .  '-.",'   / . /vvvvvv\\ . \\','  | . ( [====] ) . |',' <|. . \\vvvvvv/ . .|','  | . . . . . . . |',"   \\ . . . . . . /","    '------------'"],
 pocket:["       .-'==`-.","    .-' . vv . '-.",'   / . ( [=] ) . \\',' <( . . \\vv/ . . )',"   \\ . . . . . ./","    '----------'"],
 teardrop:["            .-'==`-.","         .-' . . vv '.","     _.-' . /vvvv\\ . \\",' <~~( . . .( [===]) . |',"     \\ . . \\vvvv/ . ./","      '-._ . . . _.-'","          '-----'"],
 shaggy:["       /'=='.\\", "    _./ . vv. \\_",'  _/ . /vvvv\\ . \\_'," <( . ( [==] ) . .)> ",'  \\ . \\vvvv/ . . /','   \\/ . . . . \\/',"    '\\_.__._./'"],
 low:["           .-'==`-.","     _..--' . . .  '--.",'  <~( . . /vvvvvvvv\\ . \\','     | . ( [======] ) . )',"      \\ . \\vvvvvvvv/ . /","       '--------------'"],
};
export function guestDesign(p){
 const head=HEADS[p.head]||HEADS.round,body=BODIES[p.shape]||BODIES.pear;
 const headX=({low:8,runner:6,barrel:6,teardrop:9}[p.shape]??7);
 const neck=p.head==='longbill'?['            |  |']:p.shape==='runner'?['           /   |']:[];
 const art=[...head.map(r=>' '.repeat(headX)+r),...neck,...body,'            >    >'];
 // Neck and body meet at a different posture in each selected silhouette.
 return {id:p.id,art,crest:1,collar:head.length,feet:p.shape==='low'?[12,23]:p.shape==='runner'?[10,16]:[10,19],
   height:p.height,pace:p.pace,tints:p.palette,
   inkOverrides:{b:p.palette[0],g:p.palette[1],h:'#e9dfbd',j:p.palette[0],s:'#7d826d',w:p.palette[1],a:'#e4b76d',p:p.palette[2]},
 };
}

// Forty hand-held objects give occupations readable silhouettes at pond scale.
export const GUEST_PROPS={
 compass:['  .---.',' / N . \\','( W + E )',' \\ . S /',"  '---'"],
 plane:['     /|','  __/ |',' <___/\\','     \\|'],
 map:[' .----.---.',' | /\\ : ~|',' | x .: /|'," '----'--'"],
 flask:['   .--.','  _|==|_',' / . . |',' | TEA |'," '-----'"],
 shell:[' .-~~~~.','/ / / /|','\\_/_/_/','  \\_/'],
 chalkboard:[' .--------.',' | E=mc2? |',' |  <(o)  |'," '--------'"],
 apple:['   /',' .-^- .','(  .  )'," '---'"],
 abacus:[' .--------.',' |-o--oo--|',' |--oo--o-|',' |o---oo--|'," '--------'"],
 magnifier:[' .---.','( o:o )'," '---'\\",'       \\'],
 flasks:['  _    _',' |:|  |.|',' /:\\  / \\','(:.:)( . )'," '--' '--'"],
 brush:['   /|','  / |',' /__|','  ||','  ||'],
 pressed_flower:[' .---.---.',' | * : * |',' |/|\\: | |'," '---'---'"],
 gears:['  _o_',' /(@)\\_',' \\_o(@)|','     \\_/'],
 lily_brush:[' .------.',' | ~v~  |',' | (o)~ |'," '------'"],
 watering_can:['  .--.',' /    \\__','|:::::|_ \\','|:::::| \\_>'," '----'"],
 bubble_wand:['   .-.','  (   )',"   '-'",'    |',' .--|--.'],
 banana:['  _',' / \\','| . |','| . /'," \\_/"],
 yoyo:['  |','  |','  |',' (o)','  V'],
 ball:[' .---.','/ ./| \\','|/--+-|','\\ |/. /'," '---'"],
 pinwheel:[' \\ | /','-- @ --',' / | \\','   |','   |'],
 shutter_lantern:['  /\\',' .--.',' |#*|',' |#*|'," '=='"],
 mask:[' .----.',' |o  o|',' | __ |',' \\__/','   |'],
 puzzle:['   __',' _|_ |','|_ |_||','  |__|'],
 listening_shell:['   __',' /@  \\','| /@@|',' \\___/'],
 quill:['   /\\','  /:/',' /:/','/|/',' |'],
 sewing:[' /| /|','/_|/_|','|~~~~|','|/X/X|',"'----'"],
 tea_cup:['  ~ ~',' .---.',' | . |)',' \\___/',' ----'],
 sprout:[' \\ /',' (v)','  |',' .--.',' |::|'],
 first_aid:['  .--.',' .----.',' | +  |',' |____|'],
 letter:[' .------.',' |\\ <3 /|',' | \\ / |'," '------'"],
 cookie_tray:[' .----------.',' | (o) (o)  |',' | (o)  .   |'," '----------'"],
 jam:['  .====.','  |~~~~|','  |JAM |','  |::::|',"  '----'"],
 mushroom_basket:['  __/\\__',' (oo)(oo)',' /~~~~~~\\',' |X/X/X|'," '-----'"],
 pepper_mill:['   ___','  (___)','   | |','  / . \\',' (_____)'],
 teapot:['    ~','   _^_',' _/ . \\_','( | . | )',' \\___/>'],
 stopwatch:['   _',' .---.','/ | . \\','| +-- |'," '---'"],
 laces:[' \\  /','  \\/',' (  )',' /\\','/  \\'],
 trophy:[' _|==|_','( |  | )',' \\|__|/','   ||','  [__]'],
 clipboard:['  [==]',' |----|',' |v --|',' |v --|',' |__o_|'],
 rocket:['   /\\','  /oo\\','  |  |',' /|==|\\','   vv'],
 bread_bag:[' .------.',' |(===) |',' |(===) |',' | . . /'," '----'"],
 book:[' .----.----.',' | ~~ : ~~ |',' | ~~ : ~~ |'," '----'----'"],
 plush:[' ,o--o.','(  vv  )',' /|__|\\','  /  \\'],
 case:['   .--.',' .--------.',' | []  [] |',' | +   :  |'," '--------'"],
 rose:['  @~',' /|','/_|','  |'],
 buttons:[' .------.',' | @ o  |',' | o  @ |'," '------'"],
 pollen:[' .  *','  *  .',' . *  '],
 mug:[' .---.',' | :-|)',' |___|'],
};

export function propRows(p,t,active){
 const rows=(GUEST_PROPS[p.prop]||GUEST_PROPS.book).map(r=>r),phase=Math.floor(t*5)%8;
 if(!active)return rows;
 if(['book','map','pressed_flower','letter'].includes(p.prop)&&phase>3&&phase<7)return rows.map((r,y)=>y>0&&y<rows.length-1?r.replace(':','/').replace('~~',' /'):r);
 if(p.prop==='pinwheel')return phase%2?[' / | \\','-- + --',' \\ | /','   |','   |']:rows;
 if(p.prop==='abacus')return rows.map((r,y)=>y>0&&y<4&&phase%2?r.replace(/-o/g,'o-'):r);
 if(p.prop==='chalkboard'&&phase>4)return rows.map(r=>r.replace('E=mc2?','E=duck'));
 if(p.prop==='compass')return rows.map(r=>r.replace('+',['+','/','-','\\'][phase%4]));
 if(p.prop==='stopwatch')return rows.map(r=>r.replace('+--',['+--','+/ ','+| ','+\\ '][phase%4]));
 if(p.prop==='yoyo')return ['  |',...Array(phase%3).fill('  |'),' (o)','  V'];
 if(p.prop==='teapot'||p.prop==='tea_cup'||p.prop==='flasks')return rows.map((r,y)=>y===0?r.replaceAll('~',phase%2?'.':'~'):r);
 if(p.prop==='shutter_lantern'&&phase>3)return rows.map(r=>r.replace('#','*'));
 if(p.prop==='puzzle'&&phase>3)return rows.slice().reverse();
 if(p.prop==='gears')return rows.map(r=>r.replaceAll('@',phase%2?'*':'@'));
 if(p.prop==='first_aid'&&phase>3)return [' .----.',...rows.slice(1).map(r=>r.replace('+','*'))];
 if(p.prop==='case'&&phase>3)return [' .--------.',' | o o [] |'," '--------'",' | []  [] |'," '--------'"];
 if(p.prop==='buttons'&&phase>4)return rows.map(r=>r.replace('@',' '));
 if(p.prop==='lily_brush')return rows.map(r=>r.replace('~v~',phase%2?'~w~':'~v~').replace('(o)',phase%2?'(*)':'(o)'));
 if(p.prop==='clipboard'&&phase>4)return rows.map(r=>r.replace('__o','v_o'));
 return rows;
}
