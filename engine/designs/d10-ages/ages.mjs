import {OPTIONS as CUTE_OPTIONS,optionSprite as cuteSprite,drawStudy as drawCute} from '../cute-mallards/options.mjs';
const raw=s=>s.slice(1,-1).split('\n');
const ADULT=CUTE_OPTIONS.find(o=>o.id==='D10');
export const AGES=[
 {id:'egg',name:'Egg',age:'Before hatching',note:'A warm speckled shell. A tiny curled feather peeks through as he rocks.',height:34,pace:2,art:raw(String.raw`
     .---.
   .' .:. '.
  / .: .:. \
 ( .: .:. . )
  \ .: .:. /
   '------'
`)},
 {id:'hatchling',name:'Hatchling',age:'0–3 days',note:'Golden down, one tiny curl, an oversized eye and little tucked toes.',head:4,collar:4,crest:1,feet:[8,12],height:43,pace:5.3,tints:['#ddc58e','#edda9f','#d5d7b0'],inkOverrides:{j:'#bea36c',h:'#f4e6b9',s:'#a98a59',w:'#eddbad'},art:raw(String.raw`
           ,~.
          .--'.
         ( O __)>
          '._/
       .-'...'-.
     <( .(vv). )
       '\_.._/'
          > >
`)},
 {id:'duckling',name:'Duckling',age:'3–14 days',note:'A round downy belly and a stronger curl; the first blue feathers show at the wing.',head:5,collar:5,crest:2,feet:[11,15],height:55,pace:5,tints:['#d6bd8d','#d8cf94','#b2ced5'],inkOverrides:{j:'#ab9f67',h:'#ebdfad',s:'#a89060',w:'#e9d6a7'},art:raw(String.raw`
              ,~.
             (_ '
            .--'.
           ( O __)==>
            '.__/
           .-==-'\
        ,-'..vv..'\
      <( .( [==] ).)
        '\._vvvv_/'
           '----'
            > >
`)},
 {id:'juvenile',name:'Juvenile',age:'14–30 days',note:'A soft mottled green head, an emerging collar, and blue flight feathers among the down.',head:6,collar:6,crest:2,feet:[13,18],height:67,pace:4.8,tints:['#c4aa81','#b4c79a','#9fcadd'],inkOverrides:{j:'#9ba77a',h:'#d0d9b4'},art:raw(String.raw`
                 ,--.
                (,_ '
              .-'--'.
             / .::.. '\
            ( . O .___)==>
             '.__.._/'
                |==|
           _..-'::.'\
       <''..:: .-vv-. '\
        \..: ( [====] ):)
         \..: \_vvvv_/ /
          '---..::..--'
               > >
`)},
 {id:'young_adult',name:'Young adult',age:'30–90 days',note:'The emerald head and cream collar settle in; a leaner version of his grown-up silhouette.',head:7,collar:7,crest:2,feet:[15,20],height:76,pace:4.7,art:raw(String.raw`
                    ,--.
                   (,_ '
                 .-'---'.
                / .::::. '\
               ( .: O .___)==>
                \ .::.. _/
                 '.___.'
                   |===|
               _.-'::.'\
           _.-':: .-vv-. '\
        <''..:: ( [=====] ):)
         \..: .: \_v_v_v_/ /
          '---..:::::..--'
               '----'
                > >
`)},
 {...ADULT,id:'adult',name:'Adult',age:'90–365 days',note:'Your chosen D10 exactly: the jaunty curl, friendly eye, proud chest and compact feet.'},
 {id:'mature',name:'Mature',age:'1–2 years',note:'A fuller chest, softer belly, thicker curl and warm cream edging on his blue wing.',head:7,collar:7,crest:2,feet:[17,24],height:85,pace:4,tints:['#c4a382','#9cc7af','#a2c9df'],inkOverrides:{w:'#e7d7b6'},art:raw(String.raw`
                       ,---.
                      (,__ '
                    .-'----'.
                   / .:::::. '\
                  ( .: O  .___)==>
                   \ .:::.. _/
                    '.___..'
                      |====|
                __..-'::..'\
           _,.-'..:: .-vvvv-. '\
        <''..:: .: / v v v v \:.)
         \..::. : ( [=======] ):|
          \..:: .: \_v_v_v_v_/ /
           '---..::........--'
                 '------'
                  >   >
`)},
 {id:'elder',name:'Elder',age:'2–3 years',note:'A relaxed lower posture, silver cheek flecks and a soft fallen curl. Still recognizably Cheese.',head:7,collar:7,crest:2,feet:[16,23],height:80,pace:3,tints:['#baaa94','#b2caba','#b8d0d6'],inkOverrides:{j:'#d1d7c8',h:'#e4e4cf',w:'#ded8c1',s:'#9b8e77'},art:raw(String.raw`
                     ,---.
                    (,__ '
                  .-'----'.
                 / .:....: '\
                ( .: o  .___)==>
                 \ .:...: _/
                  '.___..'
                .-'|====|'\
          __..-'..:: .-vv-. '\
       <''..:: .:: / v v v \:.)
        \..::. : ( [======] ):|
         \..:: .: \_v_v_v_/ /
          '---..::.......--'
                '------'
                 >   >
`)},
 {id:'legendary',name:'Legendary',age:'3+ years',note:'Silver-tipped emerald feathers, a looping pale curl and a bright familiar eye; the old pond legend.',head:7,collar:7,crest:2,feet:[17,23],height:85,pace:3.5,tints:['#c9b591','#bcd3bd','#c1dfdf'],inkOverrides:{j:'#d9dfc8',h:'#f0e6b8',w:'#e4d9b5',c:'#f3e8bf',p:'#b8dee3'},art:raw(String.raw`
                      ,---.
                     (,_ ,'
                   .-'----'.
                  / .:..::. '\
                 ( .: O  .___)==>
                  \ .:..:: _/
                   '.___..'
                     |====|
                __.-'::..'\
            _.-'..:: .-vvv-. '\
         <''..::. : / v v v \:.)
          \..:: . ( [======] ):|
           \..:: . \_v_v_v_/ /
            '---..::......--'
                  '-----'
                   >  >
`)},
].map(o=>({...ADULT,...o}));

export const ACTIONS=[['idle','Breathe & blink'],['walking','Waddle'],['ruffle','Fluff feathers'],['quack','Quack']];
export function ageSprite(age,t=0,action='idle',facing=true){
  if(age.id!=='egg')return cuteSprite(age,t,action,facing);
  const width=24,height=17,art=Array.from({length:height},()=>Array(width).fill(' '));
  const phase=Math.floor(t*2)%8,dx=[0,0,-1,0,1,0,-1,0][phase];
  const put=(s,x,y)=>[...s].forEach((c,i)=>{if(c!==' ')art[y][x+i]=c;});
  age.art.forEach((row,y)=>put(row,5+dx,7+y));
  if(phase>=3&&phase<=6){put(phase<5?'/':'/\\',11+dx,9);if(phase>=5)put(',~.',10+dx,6);}
  return {art:art.map(r=>r.join('')),tones:art.map(r=>r.map(()=> 'c').join('')),width,anchorX:12,groundRow:13,cell:age.height/9,offsetY:0};
}
export function drawAge(ctx,age,t,action,x,ground,cell,facing=true,lighting='day'){
  if(age.id!=='egg')return drawCute(ctx,age,t,action,x,ground,cell,facing,lighting);
  const m=ageSprite(age,t,action,facing),ch=cell*1.5,left=x-m.anchorX*cell,top=ground-m.groundRow*ch;
  ctx.save();ctx.font=`600 ${ch}px Menlo,monospace`;ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.fillStyle=lighting==='day'?'#41452e':'#223d3b';ctx.fillText('..,,:::::,,..',x,ground+cell*.6);
  for(let y=0;y<m.art.length;y++){
    const row=m.art[y],a=row.search(/\S/),b=row.trimEnd().length;if(a<0)continue;
    ctx.fillStyle=lighting==='day'?'#9b916c':'#687e70';ctx.fillRect(left+(a+.3)*cell,top+y*ch,(b-a-.6)*cell,ch+.3);
    for(let i=a;i<b;i++){if(row[i]===' ')continue;ctx.fillStyle='.:'.includes(row[i])?'#bcb58b':'#eee2b3';ctx.fillText(row[i],left+(i+.5)*cell,top+(y+.5)*ch,cell*1.12);}
  }
  ctx.restore();return m;
}
