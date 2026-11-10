// Ten new directions from the selected D / Velvet rogue. Preview-only art.
const lines=text=>text.slice(1,-1).split('\n');
const PAL=['#c79c79','#8dc6ad','#886a53','#edc86f','#a5cee2','#355c53'];
const TINTS={
 D1:['#c79c79','#8dc6ad','#8ac4e4'],D2:['#c9a887','#9acbb2','#a5cce1'],
 D3:['#bb977c','#a3cfb8','#93b8df'],D4:['#c39a79','#86bfa6','#91c3df'],
 D5:['#c5a68a','#94c6b8','#9bc7da'],D6:['#bd997a','#7cb79e','#8dbfda'],
 D7:['#c39b7e','#94cdb0','#93c9e5'],D8:['#cba080','#85c1a3','#a3d3e7'],
 D9:['#baa18a','#9dc5b9','#9ac5d5'],D10:['#cba27c','#8fc5aa','#94c6e4'],
};
export const OPTIONS=[
 {id:'D1',name:'Pocket mallard',note:'Closest to D, with a rounder cheek, a brighter eye and a soft little chest.',motion:'An easy waddle with a curious blink.',head:5,collar:5,feet:[17,23],height:78,pace:4.1,material:'Emerald / chestnut / sky blue',art:lines(String.raw`
                     .-----.
                   .' .:::..'.
                  / .: O  .___)==>
                  \ .:' .: __/
                   '.__.._.'
                      |===|
              __..---'::..'\
         _,.-'..::..____..:.'\
       <'..::.. .-'vvvvv'-.::.)
        \..::. / v v v v v\::|
         \..: ( [=======]  ):|
          \..: \_v_v_v_v_/::/
           '--..::....::..-'
                 '------'
                  _>  >_
`)},
 {id:'D2',name:'Puddle dumpling',note:'A little head on a broad, squashy belly; the roundest and most huggable silhouette.',motion:'A gentle side-to-side roll on tiny feet.',head:5,collar:5,feet:[14,23],height:74,pace:3.4,material:'Jade / warm biscuit / powder blue',art:lines(String.raw`
                       .---.
                     .'..::.'.
                    ( . O .__)==>
                     \..:.._/
                      '.__/
                       |==|
            __..-------'::'-.
        _.-'..::..::..::..::..'.
      <'...:: .--vvvvvvvv--. ::.\
       \.:: / v v v v v v v\ ::.)
       (.: ( [===========]  ):. |
        \:: \_v_v_v_v_v_v_/ ::./
         '---..::......::..---'
                  _>  >_
`)},
 {id:'D3',name:'Buttonbill',note:'A generous round head, a tiny golden bill and a neat little bean-shaped body.',motion:'Small eager steps and a quick bill chatter.',head:6,collar:6,feet:[16,22],height:77,pace:4.7,material:'Mint emerald / cocoa / cornflower',art:lines(String.raw`
                   .------.
                 .' .::::. '.
                / .:'    ':. \
               ( .:  O    .__)>
                \ :.   ..: _/
                 '._....._.'
                    |====|
                _.-'::..::'-.
             ,-'::.---vv---. :\
           <'.:: / v v v v  \::)
            \:: ( [======]  ):/
             \:: \_v_v_v_v_/ /
              '---..::::..---'
                  '----'
                  _> >_
`)},
 {id:'D4',name:'Bedhead buddy',note:'D with three soft unruly feathers, a little smile and a rounded, ruffled wing.',motion:'His loose forelock bounces after each step.',head:7,collar:7,crest:2,feet:[16,23],height:81,pace:4.3,material:'Forest jade / cinnamon / pale blue',art:lines(String.raw`
                     ,\ ,
                    .\|/'
                  .'----'.
                 / .:::.. '\
                ( .: O  .___)==>
                 \ ':.  .:_/
                  '.__.._.'
                     |===|
              __..--'::..'\
         _,.-'..:: .--vv--. '\
       <'.:: .:: / v v v v \:.)
        \.:: .: ( [======]  ):|
         '\:: .: \_v_v_v_v_/ /
           '--..::......::.-'
                  '-----'
                  _>  >_
`)},
 {id:'D5',name:'Shy little drake',note:'A tucked chin, puffed cheeks and a soft cream collar that nearly hides his neck.',motion:'A hesitant two-step and a small bashful head tuck.',head:6,collar:6,feet:[15,22],height:75,pace:3.7,material:'Soft teal / toasted cream / blue',art:lines(String.raw`
                    .----.
                  .'..::..'.
                 / .:'  ':. \
                ( .: O  .___)==>
                 \ '::..: _/
                .-'._.._.'-.
               /'==========''\
          _,.-'..:: .--vv--. ::\
        <'..:: .:: / v v v v\ ::)
         \::. .: ( [======] ): |
          \::. :: \_v_v_v_/ ::/
           '---..::......::.-'
                 '------'
                  _> >_
`)},
 {id:'D6',name:'Velvet loaf',note:'A low, comfy oval with a tiny upturned tail and feet barely peeking from his belly.',motion:'A lazy low waddle; the tail gives a little wag.',head:5,collar:5,loaf:true,feet:[16,24],height:70,pace:3.1,material:'Deep emerald / hazelnut / blue',art:lines(String.raw`
                        .----.
                      .' .::. '.
                     ( . O  .___)==>
                      \ .:: ._/
                       '.___/
                        |==|
           __..---------':.'-.
      _,.-' .:: .--vvvvvv--.::.'\
     <' .:: .::/ v v v v v v\::. )
      \ .:: .:( [=========] ): .|
       '\.:: .:\_v_v_v_v_v_/::./
         '---..__________..---'
                  _>   >_
`)},
 {id:'D7',name:'Bright-eyed bandit',note:'A friendly three-quarter face, two round eyes and a little bill over a plump chest.',motion:'A bouncy waddle with a delighted double blink.',head:6,collar:6,frontBill:[4,5],feet:[14,22],height:79,pace:4.8,material:'Jade / chestnut / blue satin',art:lines(String.raw`
                  .------.
                .' .::::. '.
               / .:'    ':. \
              ( .: O   O  :. )
               \:.  .===. .:/
                '._ '===' _.'
                  '======='
                .-'::..::'-.
              .':: .----. ::'.
             /:: / v vv v \ ::\
          < (.: ( [======] ) :.)
             \:: \_v_v_v_/ ::/
              '---..::::..--'
                   '----'
                  _>  <_
`)},
 {id:'D8',name:'Dewdrop duck',note:'A small velvet head above a pear-shaped belly, with scalloped feathers and a curled tail.',motion:'A soft spring in his step and a dainty tail flick.',head:5,collar:5,feet:[16,23],height:80,pace:4,material:'Emerald / warm copper / ice blue',art:lines(String.raw`
                     .----.
                   .' .::..'.
                  ( . O  .___)==>
                   \ .::.._/
                    '.___/
                     |===|
                  .-'::..'\
                .'..::..::'.
              .':: .-vvvv-. :\
          _,.'::: / v v v v\::)
         <_):.:: ( [======] ):|
            \.:: \_v_v_v_/ ::/
             '---..::..::..-'
                  '-----'
                   _> >_
`)},
 {id:'D9',name:'Sleepy puddleduck',note:'A soft half-lidded face, a pillowy belly and neatly tucked blue flight feathers.',motion:'A slow shuffle, sleepy blink and little yawn.',head:5,collar:5,sleepy:true,feet:[15,23],height:74,pace:2.8,material:'Sea green / cocoa cream / blue',art:lines(String.raw`
                     .----.
                   .' .::..'.
                  ( . -  .___)==>
                   \ .::.. _/
                    '.___.'
                      |==|
               __..--':::'-.
         _,.--'..:: .--vvv-. '\
       <'..:: .:: / v v v v \::)
        \::. :: ( [=======] ):|
         '\::. : \_v_v_v_v_/ /
           '--..::........--'
                 '------'
                  _>  >_
`)},
 {id:'D10',name:'Tiny captain',note:'A puffed little chest, a jaunty curl and a big friendly eye; proud without the stern look.',motion:'A miniature proud strut with a bobbing curl.',head:7,collar:7,crest:2,feet:[16,22],height:81,pace:4.5,material:'Emerald / warm caramel / sky blue',art:lines(String.raw`
                      ,--.
                     (,_ '
                   .-'---'.
                  / .::::. '\
                 ( .: O .___)==>
                  \ .::.. _/
                   '.___.'
                     |===|
                 _.-'::..'\
             _.-':: .-vvv-. '\
          <''..:: / v v v v\:.)
           \..: ( [======] ):|
            \..: \_v_v_v_/::/
             '---..::::..--'
                  '----'
                  _> >_
`)},
].map(o=>({palette:PAL,tints:TINTS[o.id],...o}));

export const ACTIONS=[['idle','Breathe & blink'],['walking','Waddle'],['ruffle','Fluff feathers'],['quack','Quack']];
const mirror=c=>({'/':'\\','\\':'/','(' :')',')':'(','<':'>','>':'<','[':']',']':'['}[c]||c);
export function optionSprite(option,t=0,action='idle',facing=true){
  const original=option.art,width=Math.max(...original.map(r=>r.length))+10,height=original.length+6;
  const cells=Array.from({length:height},()=>Array(width).fill(' ')),tones=Array.from({length:height},()=>Array(width).fill('b'));
  const phase=Math.floor(t*option.pace)%4,walk=action==='walking',ruffle=action==='ruffle',quack=action==='quack';
  const blink=t%5.3>4.95||(option.id==='D7'&&t%5.3>4.55&&t%5.3<4.7);
  for(let y=0;y<original.length-1;y++){
    const row=original[y],first=row.search(/\S/),last=row.trimEnd().length-1;
    let bill=row.indexOf(')==');bill=bill>=0?bill+1:row.indexOf(')>')>=0?row.indexOf(')>')+1:100;
    if(option.frontBill?.includes(y))bill=row.indexOf('===');
    const wing=row.indexOf('['),wingEnd=row.indexOf(']');
    for(let x=0;x<row.length;x++){
      let ch=row[x];if(ch===' ')continue;
      const eye=y<option.head&&('oO'.includes(ch)||(option.sleepy&&y===2&&ch==='-'));
      if(eye&&blink)ch='-';
      if(quack&&y<option.head&&x>=bill&&phase%2)ch=ch==='='?'~':ch;
      let dx=ruffle?(y<option.head?[0,1,0,-1][phase]:y>option.collar?[0,-1,0,1][phase]:0):0;
      let dy=walk&&phase===1?-1:0;
      if(option.crest&&y<option.crest)dx+=[0,1,0,-1][Math.floor(t*3)%4];
      if(option.id==='D5'&&action==='idle'&&t%5.3>3.7&&y<option.head)dy++;
      if(option.loaf&&x<10&&y>option.collar)dy+=Math.floor(t*3)%2?-1:0;
      if(option.id==='D8'&&x<15&&y>8)dx+=Math.floor(t*3)%2?-1:0;
      if(ruffle&&ch==='v'&&y>option.collar&&phase%2)ch='~';
      const xx=x+5+dx,yy=y+3+dy;cells[yy][xx]=ch;
      let tone=y<option.collar?'g':'b';
      if(':.'.includes(ch))tone=y<option.collar?'j':(x+y)%3?'s':'b';
      if(y>option.collar&&'/v~'.includes(ch)&&x>first+3&&x<last-2)tone='w';
      if(x===first||x===last||ch==="'")tone=y<option.collar?'h':'b';
      if(y===option.collar)tone='c';
      if(wing>=0&&x>=wing&&x<=wingEnd)tone='p';
      if(eye)tone='e';
      if(y<option.head&&x>=bill&&(!option.frontBill?.includes(y)||x<bill+3))tone='a';
      tones[yy][xx]=tone;
    }
  }
  // Belly and toes meet directly; the smaller shape keeps no exposed shin.
  const fy=height-4;
  for(const [i,foot] of option.feet.entries()){
    const dx=walk?[0,i?-1:1,0,i?1:-1][phase]:0,lifted=walk&&((phase===1&&i===0)||(phase===3&&i===1));
    [...(lifted?'>':i?'>_':'_>')].forEach((ch,j)=>{cells[fy-(lifted?1:0)][foot+5+dx+j]=ch;tones[fy-(lifted?1:0)][foot+5+dx+j]='a';});
  }
  const anchor=(Math.min(...option.feet)+Math.max(...option.feet))/2+6;
  return {art:cells.map(r=>(facing?r:[...r].reverse().map(mirror)).join('')),tones:tones.map(r=>(facing?r:[...r].reverse()).join('')),
    inks:{b:option.tints[0],g:option.tints[1],j:'#65a58d',h:'#b1dcc4',s:'#937152',a:'#efc46a',w:'#dbbfa0',c:'#f0ead2',p:option.tints[2],e:'#172b25'},width,anchorX:facing?anchor:width-anchor,groundRow:fy+.8,cell:option.height/(original.length*1.5),offsetY:action==='idle'?Math.sin(t*2)*.1:0};
}

export function drawStudy(ctx,option,t,action,x,ground,cell,facing=true,lighting='day'){
  const m=optionSprite(option,t,action,facing),ch=cell*1.5,left=x-m.anchorX*cell,top=ground-m.groundRow*ch+m.offsetY*cell;
  const day=lighting==='day',dusk=lighting==='dusk';
  ctx.save();ctx.textAlign='center';ctx.textBaseline='middle';ctx.font=`600 ${ch}px Menlo,monospace`;
  ctx.fillStyle=day?'#353d2a':dusk?'#292e2c':'#132a2d';ctx.fillText('..,,:::::::::,,..',x,ground+cell*.8,cell*21);
  for(let y=0;y<option.art.length+2;y++){
    const row=m.art[y],a=row.search(/\S/),b=row.trimEnd().length;if(a<0)continue;
    const head=y<option.collar+3,base=option.tints[head?1:0].match(/\w\w/g).map(v=>parseInt(v,16));
    const featherLight=.5+.14*(1-y/m.art.length),strength=featherLight*(day?1:dusk?.83:.62);
    ctx.fillStyle='rgb('+base.map((v,i)=>Math.round(v*strength+([7,12,6][i])+(!day&&i===2?13:0))).join(',')+')';
    ctx.fillRect(left+(a+.3)*cell,top+y*ch,(b-a-.6)*cell,ch+.4);
  }
  ctx.lineJoin='round';
  for(let y=0;y<m.art.length;y++)for(let col=0;col<m.art[y].length;col++){
    const glyph=m.art[y][col];if(glyph===' ')continue;
    const tone=m.tones[y][col],px=left+(col+.5)*cell,py=top+(y+.5)*ch;
    ctx.strokeStyle=day?'#385247':'#173d3b';ctx.lineWidth=Math.max(.5,cell*.13);ctx.strokeText(glyph,px,py,cell*1.12);
    let ink=m.inks[tone];if(!day&&tone!=='e'){const rgb=ink.match(/\w\w/g).map(v=>parseInt(v,16)),blend=dusk?[206,158,116]:[128,181,193],amount=dusk?.12:.23;ink='rgb('+rgb.map((v,i)=>Math.round(v*(1-amount)+blend[i]*amount)).join(',')+')';}
    ctx.fillStyle=ink;ctx.fillText(glyph,px,py,cell*1.12);
    // A tiny ASCII catchlight gives the larger O an alert, gentle expression.
    if(tone==='e'&&glyph==='O'){ctx.font=`600 ${ch*.5}px Menlo,monospace`;ctx.fillStyle='#f3f1da';ctx.fillText('.',px-cell*.1,py-ch*.16);ctx.font=`600 ${ch}px Menlo,monospace`;}
  }
  ctx.restore();return m;
}
