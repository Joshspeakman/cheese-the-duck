// Design studies only. No game state or live character art is changed.
const art = text => text.slice(1,-1).split('\n');
export const OPTIONS = [
  {id:'A',name:'Bramble bandit',note:'A wind-torn crest, layered honey feathers, ragged tail and a sharp little side-eye.',material:'Honey / bracken / warm ivory',motion:'Uneven swagger; the crest and loose wing tips catch the breeze.',head:6,feet:[13,21],height:83,pace:4.6,
    palette:['#e4c888','#f5e5b9','#a98750','#d69543','#b7bb88','#655839'],
    art:art(String.raw`
                     , /,
                   ,\|// .
                  .-'"'-._
                 /'.::'..'\
                (.: > .:___)==>
                 \..::'  _/
               ,--'--.._/
         _,,.-'..,'::'..'\
       <\,:'.,-===-..:'.::)
        >'.:/ / / /\'.:.::|
       < .:( / / / /):'.::/
        '\.:\_/_/_/.:,../
          '-.::,::..__.-'
             '--'---'
              _>   >_
`)},
  {id:'B',name:'River pebble',note:'A tiny rounded river duck: silver down, a broad cheek, scalloped wings and feet tucked underneath.',material:'River silver / cream / slate',motion:'Soft rolling steps; cheek fluff trembles with a small contented blink.',head:7,feet:[12,20],height:76,pace:3.5,
    palette:['#c5c9b6','#f1ebcf','#8d9e9b','#dab06a','#b1c3c0','#52666b'],
    art:art(String.raw`
                   .,,.
                .-''..''-.
              .' .::..::. '.
             / .:.'    '.:. \
            ( .:  o   o  :. )
             \:.  .====. .:/
             /'.. '====' ..'\
           .'::'--....--'::'.
          /.: /'~~~~~~'\  :.\
         (.: / ) )  ( ( \ ::.)
         |::( ) ) .. ( ( ):.|
          \:.\_).::::.(_/.:/
           '.:..::::::..:.'
             '---.__.---'
               _>  <_
`)},
  {id:'C',name:'Reed runner',note:'A narrow, forward-leaning duck with a long swept brow, striped flight feathers and a spear of tail.',material:'Reed gold / oat / olive',motion:'Quick short-footed steps; the long brow and tail stream behind him.',head:8,feet:[18,24],height:86,pace:6.4,
    palette:['#cfbd7b','#eee1ad','#98915d','#d5a355','#c0c58c','#596143'],
    art:art(String.raw`
                        __,,
                    _.-'//'
                   /.:''"--.
                  (.: o .___)====>
                   \.:.\___/
                    |::' /
                    |:: /
                  ,-'::/
            __..-'..::'\
      __..-'..:..__..::..\
    <_///..: .-'/////\.:.|
       '---.( ///////):./
             \_////_/./
              '--.._-'
                 _>  >_
`)},
  {id:'D',name:'Velvet rogue',note:'A proper low mallard profile: emerald head, pale collar, chestnut chest and a blue wing flash.',material:'Deep teal / chestnut / blue',motion:'A deliberate strut; his blue flight feathers fan out when he shakes.',head:6,feet:[16,24],height:80,pace:3.8,
    palette:['#b98e69','#7eb9a5','#755c49','#ddb75b','#82b4c7','#334f4c'],
    art:art(String.raw`
                      .----.
                    .'::++::'.
                   /::++o+.___)===>
                   \::++++: _/
                    '._:::_/
                      |===|
               __..--'::.:'.
        _,..--'..:..::.:.::: \
      <\___..:-.________.:.:.|
        \::: / //////// \.:.|
         \::( [========] ):./
          \::\_////////_/./
           '--.::::::::.-'
                '------'
                 _>   >_
`)},
  {id:'E',name:'Butterbrick',note:'A squat, square little troublemaker with a huge flat bill, dense golden down and a blunt fan tail.',material:'Butter / toasted gold / amber',motion:'Low stomping steps; a broad bill chatters while his tiny tail flicks.',head:7,feet:[11,21],height:73,pace:4,
    palette:['#e8c577','#f5dfa3','#b89451','#dfa044','#cabc77','#7c693d'],
    art:art(String.raw`
                _..,,,.._
              .'::'''''::'.
             /:: .----. :::\
            |::. >  > .:___|____
            |:. .__________=====>
            '.__\___________/'
          .-':::---...---::'-.
       __/:::::.________.:::::\
      <==|:::: /  v  v  v\::::|
      <==|::: ( v  v  v  v):::|
       '-\:::: \_v__v__v_/:::/
          '---.:::::::::.---'
               '-------'
               _>    <_
`)},
  {id:'F',name:'Stormcrest',note:'An angular charcoal duck with a swept crest, pale cheek slash and sharp overlapping steel feathers.',material:'Blue slate / smoke / pale wheat',motion:'A twitchy double-step; the crest snaps and the long wing edges shiver.',head:7,feet:[15,23],height:84,pace:5.4,
    palette:['#9cabae','#d8d9c1','#667f88','#c9a36c','#b2c6c5','#405963'],
    art:art(String.raw`
                   /| ,/
                __/ |//
               <///'--._
                /::/'''.\
               (::: >  __)==>
                \::\__::/
                 '::\__/
          _..---'::::::'\
      __</////::::::_____\
      \_<<<:::.---'/////\|
        \_<<:( //// //// )
          \<:.\//_////_//
           \:::::____.-'
            '---'----'
                _>  >_
`)},
  {id:'G',name:'Marsh ghost',note:'An ivory duck with a graceful hooked neck, a tiny dark eye and fine, flowing wing engravings.',material:'Pale linen / sage shadow / sand',motion:'An unhurried glide of a waddle; the neck sways and fine feathers settle.',head:8,feet:[14,22],height:86,pace:2.8,
    palette:['#d9ddc4','#f1edd5','#a2b7a6','#cbb181','#bdcbb7','#627c72'],
    art:art(String.raw`
                       .-''-.
                      / .:' .\
                     ( . o ___)====>
                      \ ':. _/
                       | .:|
                      / .:'/
                    .' .:'/
             __..--' .::.'\
       _,.--' ..::' .:' .:.\
     <' ..::' .-'~~~~~-. .:.|
      \ .:' .' ~ ~ ~ ~ '.::|
       \ .:( ~ ~ ~ ~ ~  ):/
        '\:.'.________.'/'
          '---.______.-'
                _>  >_
`)},
  {id:'H',name:'Acorn rascal',note:'A small pointed cap of feathers, dark eye mask, speckled chest and rounded chestnut wings.',material:'Chestnut / russet / oat cream',motion:'A quick hop-step with a nose-first pause; his cap bounces once on landing.',head:7,feet:[12,19],height:76,pace:5.8,
    palette:['#c59c72','#e7cb9e','#937052','#d59d59','#b7a377','#574f3c'],
    art:art(String.raw`
                    /,
                  _/''\_
                .'//////'.
               / .-====-. \
              ( .| o  o|.__)==>
               \.'-====':/
               /'..::..'\
            .-'...::::...'-.
          .':: .-vvvv-. ::'.
         /::: / v v v v\ :::\
         \:::(v v v v v ):::/
          '\::\_v_v_v_/::/'
            '--..::::..--'
                '----'
                _> <_
`)},
  {id:'I',name:'Copper drifter',note:'A long, low duck with a rust-red head, etched bronze wings and three upturned tail plumes.',material:'Copper / bronze / deep umber',motion:'A low rocking waddle; the three tail feathers ripple one after another.',head:6,feet:[17,26],height:74,pace:3.7,
    palette:['#d0a16e','#e3b68c','#947551','#d3a757','#bbbd8f','#5a5340'],
    art:art(String.raw`
                         .--,,.
                       .'::'::'.
                      /.: o .___)===>
                      \:::..: _/
                       '---.:/
       /\ /\ /\       _/:::.'\
      <//<//<//__..--'..:::..:\
       \<<<:: .---====---. .::|
        \::: / //////////\ ::|
         \::( ////==///// ):./
          \::\_////////_/::/
           '--...______..-'
                  _>   >_
`)},
  {id:'J',name:'Mossback mischief',note:'A hunched pond veteran with bushy brows, moss-tinted feathers, a broad cheek and an untidy wing.',material:'Lichen / weathered gold / fern',motion:'A lopsided shuffle; his heavy eyebrow rises and the loose tail gives a delayed wag.',head:7,feet:[12,22],height:80,pace:3.2,
    palette:['#bdba83','#dfd4a4','#858b5c','#c6a069','#a4bc87','#4f6248'],
    art:art(String.raw`
                   _.,,._
                 .'//''\\'.
                /:. ____ .:\
               (.:. --- .___)====>
                \.:....::: /
               .-'::._____/\
           _.-' .:':::' .::.\
        ,<' .::' .-====-. .::)
       <//.:.:: / /v/ /v\ .:|
        <.:.:: ( /v/ /v/ )::/
         \:::.  \_/v/_v_/.:/
          '\::...:::....::/'
            '---..___..--'
                _>    >_
`)},
];

export const ACTIONS=[['idle','Breathe & blink'],['walking','Waddle'],['ruffle','Ruffle feathers'],['quack','Quack']];
const mirrorChar=c=>({'/':'\\','\\':'/','(' :')',')':'(','<':'>','>':'<','[':']',']':'['}[c]||c);
export function optionSprite(option,t=0,action='idle',facing=true){
  const original=option.art,width=Math.max(...original.map(r=>r.length))+10,height=original.length+6;
  const cells=Array.from({length:height},()=>Array(width).fill(' ')),tones=Array.from({length:height},()=>Array(width).fill('b'));
  const phase=Math.floor(t*option.pace)%4,walk=action==='walking',ruffle=action==='ruffle',quack=action==='quack';
  const blink=t%5.3>5.02,headShift=ruffle?[0,1,-1,0][phase]:0;
  for(let y=0;y<original.length-1;y++){
    const row=original[y],first=row.search(/\S/),last=row.trimEnd().length-1;
    for(let x=0;x<row.length;x++){
      let ch=row[x];if(ch===' ')continue;
      const bill=option.id==='B'&&[5,6].includes(y)?row.indexOf('===='):row.indexOf(')==')>=0?row.indexOf(')==')+1:row.indexOf('====>')>=0?row.indexOf('====>')-1:100;
      const eye=y<option.head&&('oO'.includes(ch)||ch==='>'&&x<bill);
      if(eye&&blink)ch='-';
      if(quack&&y<option.head&&x>=bill&&phase%2)ch=ch==='='?'~':ch;
      let dx=y<option.head?headShift:ruffle&&y>option.head&&y<original.length-3?[0,-1,1,0][phase]:0;
      let dy=walk&&phase===1?-1:0;
      if(['A','C','F'].includes(option.id)&&y<2)dx+=[0,1,0,-1][Math.floor(t*3)%4];
      if(option.id==='H'&&y<3&&walk&&phase===2)dy--;
      if(option.id==='E'&&x<10&&y>=7&&y<=10)dx+=phase%2?-1:0;
      if(option.id==='I'&&x<15&&y>=5&&y<8)dy+=(Math.floor(t*4+x/3)%3===0?-1:0);
      if(option.id==='D'&&ruffle&&y>8&&ch==='/'&&phase%2)ch='\\';
      if(option.id==='J'&&y===3&&ch==='-'&&(quack||t%7>6.5))ch='^';
      if(option.id==='B'&&quack&&y===5&&ch==='=')ch=phase%2?'o':'=';
      const xx=x+5+dx,yy=y+3+dy;
      cells[yy][xx]=ch;
      let tone=y<option.head?'f':'b';
      if(':.'.includes(ch))tone=(x+y)%3?'s':'b';
      if('/v)'.includes(ch)&&y>option.head&&x>first+4&&x<last-2)tone='w';
      if(x===first||x===last||ch==="'")tone='h';
      if(eye||y<option.head&&ch==='>'&&x<bill)tone='e';
      if(y<option.head&&x>=bill)tone='a';
      if(option.id==='D'&&y===5)tone='h';
      if(option.id==='D'&&y===10&&x>12&&x<25)tone='p';
      if(option.id==='H'&&y<4)tone='s';
      if(option.id==='H'&&y===4&&x>15&&x<23&&!eye)tone='d';
      if(option.id==='J'&&y===3&&ch==='-')tone='e';
      tones[yy][xx]=tone;
    }
  }
  const fy=height-3;
  for(const [i,foot] of option.feet.entries()){
    const dx=walk?[0,i?-1:1,0,i?1:-1][phase]:0;
    const lifted=walk&&((phase===1&&i===0)||(phase===3&&i===1));
    const glyph=lifted?'>':i?' >_':'_> ';
    if(!lifted){cells[fy-1][foot+6+dx]='|';tones[fy-1][foot+6+dx]='a';}
    [...glyph].forEach((ch,j)=>{cells[fy-(lifted?1:0)][foot+5+dx+j]=ch;tones[fy-(lifted?1:0)][foot+5+dx+j]='a';});
  }
  if(ruffle&&phase===1){cells[5][2]="'";cells[9][width-2]='`';tones[5][2]='s';tones[9][width-2]='s';}
  const anchor=(Math.min(...option.feet)+Math.max(...option.feet))/2+6;
  const [body,face,shade,accent,wing,dark]=option.palette;
  return {art:cells.map(r=>(facing?r:[...r].reverse().map(mirrorChar)).join('')),tones:tones.map(r=>(facing?r:[...r].reverse()).join('')),
    inks:{b:body,f:face,s:shade,a:accent,w:wing,h:face,e:'#272d26',d:dark,p:'#86c3d8'},body,face,shade,accent,width,anchorX:facing?anchor:width-anchor,
    groundRow:fy+.7,scale:1,cell:option.height/(original.length*1.5),offsetY:action==='idle'?Math.sin(t*2+option.id.charCodeAt(0))*.14:0};
}

export function drawStudy(ctx,option,t,action,x,ground,cell,facing=true,lighting='day'){
  const m=optionSprite(option,t,action,facing),ch=cell*1.5,left=x-m.anchorX*cell,top=ground-m.groundRow*ch+m.offsetY*cell;
  const day=lighting==='day',dusk=lighting==='dusk';
  ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';ctx.font=`600 ${ch}px Menlo,monospace`;
  // Fine ASCII contact shadow ties his feet to the terrain.
  ctx.fillStyle=day?'#353d2a':dusk?'#292e2c':'#132a2d';
  ctx.fillText('..,,:::::::::::,,..',x,ground+cell*.9,cell*24);
  // Tinted feather mass under the ASCII engraving, with a continuous silhouette.
  // Each duck keeps its own material; upper feathers catch more sky light.
  for(let y=0;y<m.art.length-3;y++){
    const row=m.art[y],a=row.search(/\S/),b=row.trimEnd().length;if(a<0)continue;
    const base=option.palette[y<option.head+3?1:0].match(/\w\w/g).map(v=>parseInt(v,16));
    const amount=day?.46:dusk?.36:.25,sky=day?[24,29,20]:dusk?[30,24,22]:[20,37,43];
    ctx.fillStyle='rgb('+base.map((v,i)=>Math.round(v*amount+sky[i])).join(',')+')';
    ctx.fillRect(left+(a+.3)*cell,top+y*ch,(b-a-.6)*cell,ch+.5);
  }
  ctx.globalAlpha=1;ctx.lineJoin='round';
  for(let y=0;y<m.art.length;y++)for(let col=0;col<m.art[y].length;col++){
    const glyph=m.art[y][col];if(glyph===' ')continue;
    const tone=m.tones[y][col],px=left+(col+.5)*cell,py=top+(y+.5)*ch;
    ctx.strokeStyle=day?'#454c35':'#172e32';ctx.lineWidth=Math.max(.5,cell*.14);ctx.strokeText(glyph,px,py,cell*1.12);
    let ink=m.inks[tone]||m.body;
    if(!day){const rgb=ink.match(/\w\w/g).map(v=>parseInt(v,16)),blend=dusk?[206,150,108]:[121,175,187],amount=dusk?.15:.27;ink='rgb('+rgb.map((v,i)=>Math.round(v*(1-amount)+blend[i]*amount)).join(',')+')';}
    ctx.fillStyle=ink;ctx.fillText(glyph,px,py,cell*1.12);
  }
  ctx.restore();return m;
}
