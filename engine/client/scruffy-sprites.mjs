import { fitWearables,paintWearables } from './wearables.mjs';
// Shared ASCII rig. The live game selects approved variant B, Bedhead Bandit.
// A fixed character grid gives every animation a stable ground and head anchor.
export const STAGES = [
  {id:'egg',name:'Egg',age:'Before hatching',note:'A restless shell with a bad attitude inside.'},
  {id:'hatchling',name:'Hatchling',age:'0–3 days',note:'Tiny body, oversized eye, two unruly feathers.'},
  {id:'duckling',name:'Duckling',age:'3–14 days',note:'Round downy belly; the crest starts misbehaving.'},
  {id:'juvenile',name:'Juvenile',age:'14–30 days',note:'Compact feet, sharp crest, maximum trouble.'},
  {id:'young_adult',name:'Young adult',age:'30–90 days',note:'Lean body and a quick, cocky stride.'},
  {id:'adult',name:'Adult',age:'90–365 days',note:'Full scruffy silhouette; the original menace grown up.'},
  {id:'mature',name:'Mature',age:'1–2 years',note:'A broader belly, worn crest, and pale wing tips.'},
  {id:'elder',name:'Elder',age:'2–3 years',note:'Lower posture, silver scruff, slower stubborn steps.'},
  {id:'legendary',name:'Legendary',age:'3+ years',note:'Ancient menace: forked crest, star eye, wandering sparks.'},
];
export const VARIANTS = [
  {id:'A',name:'Original menace',note:'Closest to your pick: spiky crest, side-eye, pointed tail.',crest:['\\|/','\\|/','\\!/'],wing:'(___)'},
  {id:'B',name:'Bedhead bandit',note:'Swept, floppy feathers and a softer, rounder silhouette.',crest:['~\\//','~\\/_','~\\//'],wing:'(~~_)'},
  {id:'C',name:'Pond punk',note:'Tall swept spikes, lean chest, and a sharp little tail.',crest:['///|','//|/','///|'],wing:'(/_)'},
  {id:'D',name:'Pocket bruiser',note:'Short bill, low stance, broad belly, and tiny angry feet.',crest:['\\|,','\\!,','\\|,'],wing:'(____)'},
  {id:'E',name:'Crooked trouble',note:'An off-center crest, cocked head, and a double tail flick.',crest:['\\\\_','\\|_','\\\\_'],wing:'(,_/)'},
  {id:'F',name:'Feral fluff',note:'A wider crest, cheek tufts, and ragged outer feathers.',crest:['\\|\\//','\\\\|//','\\|/\\/'],wing:'(v_v)'},
];
export const ACTIONS = [
  {id:'idle',name:'Idle / side-eye',duration:3.2,frames:8,detail:'Breathing, blinking, a head glance, and a delayed crest flick.'},
  {id:'walking',name:'Waddle',duration:1,frames:8,detail:'Eight poses: alternating planted feet, passing step, body dip, and feather follow-through.'},
  {id:'flapping',name:'Wing flap',duration:1.2,frames:6,detail:'Fold, lift, spread, downstroke, and recovery; the body reacts to the wingbeat.'},
  {id:'eating',name:'Peck / chew',duration:1.6,frames:8,detail:'Anticipation, head reach, downward peck, open bill, crumbs, and a swallow.'},
  {id:'swimming',name:'Swim',duration:1.6,frames:8,detail:'A lower floating body, alternating paddles, and expanding ASCII ripples.'},
  {id:'hopping',name:'Hop',duration:1.2,frames:8,detail:'Crouch, push-off, tucked feet, flight, landing squash, and recovery.'},
  {id:'preening',name:'Preen',duration:2,frames:8,detail:'The head turns into the wing, nibbles feathers, then shakes the crest out.'},
  {id:'quacking',name:'Quack',duration:1.1,frames:6,detail:'Inhale, chin lift, open bill, chest pulse, and a trailing quack mark.'},
  {id:'sleeping',name:'Sleep',duration:4,frames:8,detail:'Tucked bill, crouched body, slow breathing, and rising sleep letters.'},
  {id:'dancing',name:'Victory dance',duration:1.6,frames:8,detail:'Alternating kicks, wing throws, a happy eye, and an extra scruffy crest bounce.'},
];
const W=40,H=25,CX=19,GROUND=21;
const HEADS={
  hatchling:[' .-.','(>_)>'],
  duckling:[' .---.','(> __)>'," '._/"],
  juvenile:[' .----.','( > __)==>', ' \\_  /'],
  young_adult:[' .----.','( > ___)==>', ' \\_   /'],
  adult:[' .-----.','( > ___)==>', ' \\_   /'],
  mature:[' .------.','( > ____)==>', ' \\__   /'],
  elder:[' .-----.','( - ___)==>', " '.__  /"],
  legendary:[' .-----.','( * ___)==>', ' \\_   /'],
};
const BODIES={
  hatchling:[' /()\\', ' \\__/'],
  duckling:[' /(__)\\', ' \\____/'],
  juvenile:[",-' '-\\",'< (__) )'," '-----'"],
  young_adult:[",--' '-'\\",'< (___) )'," '------'"],
  adult:[",--' '-'\\",'<  (___)  )'," '-------'"],
  mature:[",--'  '-'\\",'<  (____)  )'," \\_______/"],
  elder:[",--'  '--.",'< (___)   )'," '-------'"],
  legendary:[",--' '-'\\",'<  (===)  )'," '-------'"],
};
const FLAP=[[' /','(>',' \\'],['\\ /',' V ','   '],['\\  /',' \\/ ','    '],[' __','/ /',' V '],['  /',' / ','/_ '],[' /','(>',' \\']];
const mirrorChar=c=>({'/':'\\','\\':'/','(' : ')',')':'(','[':']',']':'[','<':'>','>':'<'}[c]||c);

export function scruffySprite(variantId='A',stage='adult',action='idle',time=0,facing=true,appearance={}){
  const variant=VARIANTS.find(v=>v.id===variantId)||VARIANTS[0];
  const stageIndex=Math.max(0,STAGES.findIndex(s=>s.id===stage));
  stage=STAGES[stageIndex].id;
  const animation=ACTIONS.find(a=>a.id===action)||ACTIONS[0];
  const ageSpeed=stage==='elder'?.72:stage==='hatchling'?1.18:1;
  const cycle=(time*ageSpeed/animation.duration)%1;
  const phase=Math.floor(cycle*animation.frames), p8=Math.floor(cycle*8);
  const cells=Array.from({length:H},()=>Array(W).fill(' '));
  const colors=Array.from({length:H},()=>Array(W).fill('b'));
  let clipped=false,inks={},rig=null,wearablePlan=null;
  function put(text,x,y,tone='b'){
    x=Math.round(x);y=Math.round(y);
    for(let i=0;i<text.length;i++){
      if(text[i]===' ')continue;
      if(x+i<0||x+i>=W||y<0||y>=H){clipped=true;continue;}
      cells[y][x+i]=text[i];colors[y][x+i]=tone;
    }
  }
  const group=(art,x,y,tone='b')=>art.forEach((line,row)=>put(line,x,y+row,tone));
  let offsetX=0,offsetY=0;
  if(stage==='egg'){
    const wobble=[0,0,-1,0,1,0,-1,0][p8];
    const crack=['',' .',' /',' \\','/\\','/\\','/\\',''][p8];
    const egg=['  .---.',' /     \\','(       )',' \\     /',"  '---'"];
    group(egg,CX-4+wobble,GROUND-5,'f');
    if(crack)put(crack,CX-1+wobble,GROUND-3,'a');
    if(p8===5||p8===6)put(variant.id==='C'?'//':variant.id==='F'?'\\|/':',,',CX-1+wobble,GROUND-6,'a');
    put(p8===2?' .':'  .',CX-5,GROUND+1,'s');
  }else{
    const baby=stageIndex<3,old=stageIndex>=6,elder=stage==='elder';
    let head=[...HEADS[stage]],body=[...BODIES[stage]];
    const baseBodyX=CX-(baby?2:5);
    let bodyX=baseBodyX,bodyBottom=variant.id==='B'?GROUND-1:GROUND-(baby?1:2)-(stage==='juvenile'?1:0);
    const feet=[];
    let headX=CX-(baby?1:2),bodyDy=0,headDy=0,headDx=0,crestDx=0;
    let eye=appearance.eye||(stage==='hatchling'?'o':elder?'-':stage==='legendary'?'*':'>');
    if(action==='idle'){
      headDx=[0,0,0,1,1,0,0,0][p8]; crestDx=[0,0,0,0,1,1,0,0][p8];
      if(p8===6)eye='-';
      offsetY=Math.sin(cycle*Math.PI*2)*.07;
    }
    if(variant.id==='B'&&!baby){
      head[0]=' ._----.';
      body[1]=stage==='young_adult'?'( (~~_) )':'(  (~~_)  )';body[2]=stage==='young_adult'?" '-----'":" '-------'";
    }
    if(variant.id==='C'&&!baby){
      head[1]=head[1].replace('(','/');body[1]='<< (/_) )';
      body[2]=" '-----'";headX++;
    }
    if(variant.id==='D'){
      head[1]=head[1].replace('==>','>');
      if(!baby){head[0]=' .----.';body[1]=stage==='young_adult'?'( (____)  )':'(  (____)   )';body[2]=stage==='young_adult'?" '-------'":" '---------'";bodyX--;bodyBottom++;}
    }
    if(variant.id==='E'&&!baby){head[0]=' .--~--.';body[1]='<< (,_/)  )';}
    if(variant.id==='F'){
      head[0]=head[0].replace('.','~');
      if(!baby){body[1]='<~ (v_v)  >';body[2]=" 'v-----v'";}
    }
    if(old&&!baby)body[1]=body[1].replace(/\([^)]*\)/,stage==='legendary'?'(===)':'(==_)');
    if(action==='walking'||action==='dancing'){
      bodyDy=[0,-1,-1,0,0,-1,-1,0][p8];headDy=[0,0,-1,-1,0,0,-1,-1][p8];
      headDx=[0,1,1,0,0,-1,-1,0][p8];crestDx=[-1,0,1,1,0,0,-1,-1][p8];
      if(action==='dancing'){eye='^';bodyDy--;headDy--;}
      offsetX=Math.sin(cycle*Math.PI*2)*.14;
    }
    if(action==='flapping'){
      bodyDy=[0,0,-1,-1,0,0][phase];headDy=bodyDy;
      crestDx=[0,-1,-1,0,1,0][phase];eye=phase===2?'^':eye;
    }
    if(action==='hopping'){
      bodyDy=[0,1,-1,-3,-4,-2,1,0][p8];headDy=bodyDy;eye=p8===3||p8===4?'O':eye;
      headDx=[0,0,0,1,1,1,0,0][p8];crestDx=[0,-1,-1,-1,0,1,1,0][p8];
    }
    if(action==='swimming'){
      bodyDy=1;headDy=1;headDx=[0,0,1,1,0,0,-1,-1][p8];
      offsetY=Math.sin(cycle*Math.PI*2)*.12;
    }
    if(action==='eating'){
      headDx=[0,-1,1,3,3,2,0,0][p8];headDy=[0,-1,0,2,3,1,0,0][p8];
      crestDx=[0,0,-1,-1,0,1,0,0][p8];eye=p8===3||p8===4?'o':eye;
    }
    if(action==='preening'){
      headDx=[0,0,-1,-2,-2,-1,0,0][p8];headDy=[0,0,1,2,2,1,0,0][p8];
      if(p8>=2&&p8<=5)head[1]=baby?'(<_)': '(<_  > )';
      if(p8===6)crestDx=2;
    }
    if(action==='quacking'){
      headDy=[0,-1,-1,-1,0,0][phase];headDx=[-1,0,1,1,0,0][phase];
      eye=phase===2||phase===3?'O':eye;
      if(phase===2||phase===3)body[1]=body[1].replace('___','~~~');
    }
    if(action==='sleeping'){
      eye='-';headDy=2;headDx=-1;bodyDy=1;
      head[1]=baby?'(-~)': '( - <__)';
      offsetY=Math.sin(cycle*Math.PI*2)*.1;
    }
    // Body and wings form independent layers; the head never drags a held pose.
    const bodyY=bodyBottom-body.length+1+bodyDy;
    const headY=bodyBottom-body.length-head.length+1+headDy;
    // Stretch the neck through anticipation poses so a lifted head stays attached.
    const jawY=headY+head.length-1;
    for(let y=jawY+1;y<bodyY;y++){
      const blend=(y-jawY)/(bodyY-jawY);
      put('|',headX+1+headDx*(1-blend),y,'f');
      put('/',headX+(baby?3:6)+headDx*(1-blend),y,'f');
    }
    group(body,bodyX,bodyY);
    if(action==='flapping'||action==='dancing'){
      const wing=FLAP[action==='dancing'?[0,1,2,3,2,1,0,4][p8]:phase];
      group(wing,bodyX-2,bodyY-1,'f');
      group(wing.map(line=>[...line].reverse().map(mirrorChar).join('')),bodyX+body[1].length-1,bodyY-1,'f');
    }
    if(old)put(stage==='legendary'?'===':'==',bodyX+4,bodyY+1,'f');
    // Two independent feet: contact, passing, lift, extension, and opposite contact.
    if(!['swimming','sleeping'].includes(action)){
      const footY=GROUND,feetX=CX-(baby?1:2);
      const leg=(text,x,y,anchor)=>{
        feet.push({x,y});
        const from=bodyBottom+bodyDy;
        for(let row=from+1;row<y;row++){
          const dx=x+.5-anchor,px=anchor+dx*(row-from)/(y-from);
          put(dx<-.4?'/':dx>.4?'\\':'|',px,row,'a');
        }
        put(text,x,y,'a');
      };
      if(action==='walking'||action==='dancing'){
        const left=[[-1,0,'/_'],[0,0,'|_'],[1,-1,'>_'],[1,-1,'_>'],[1,0,'_>'],[0,0,'|_'],[-1,0,'/_'],[-1,0,'/_']][p8];
        const right=[ [1,0,'_>'],[0,0,'|_'],[-1,0,'_\\'],[-1,0,'_\\'],[-1,0,'_\\'],[0,0,'|_'],[1,-1,'<_'],[1,-1,'<_']][p8];
        leg(left[2],feetX+left[0],footY+left[1]-(action==='dancing'?1:0),feetX);
        leg(right[2],feetX+(baby?2:3)+right[0],footY+right[1]-(action==='dancing'?1:0),feetX+(baby?2:3));
        if(p8===0||p8===4)put(p8===0?' .':'. ',bodyX-2,GROUND+1,'s');
      }else if(action==='hopping'&&p8>=2&&p8<=5){
        leg('/_',feetX,footY+bodyDy,feetX);leg('_\\',feetX+2,footY+bodyDy,feetX+3);
      }
      else{
        leg('/_',feetX,footY,feetX);leg('_\\',feetX+(baby?2:3),footY,feetX+(baby?2:3));
      }
    }else if(action==='swimming'){
      const ripples=[' ~~~   ~~','~~   ~~~~',' ~~~~  ~~','~~  ~~~  ~',' ~~~  ~~~~','~~   ~~  ~',' ~~~~   ~~','~~  ~~~~ '];
      put(ripples[p8],bodyX-2,GROUND+1,'w');put(p8<4?'>_':'_<',CX+1,GROUND,'a');
      put(p8%2?' ~~':'~~ ',bodyX+9,GROUND+2,'w');
    }else put(' _  _ ',CX-2,GROUND,'a');
    // Head comes last so pecking and tucked sleep poses overlap the wing cleanly.
    head[1]=head[1].replace(/[>*o-](?=[ _])/,eye);
    const crest=stage==='hatchling'?',,':stage==='duckling'?'\\,|':elder?'~\\_':
      stage==='mature'?variant.crest[1]:stage==='legendary'?'*'+variant.crest[p8%3]+'*':variant.crest[Math.floor((p8+1)/3)%3];
    for(const [row,line] of head.entries()){
      const start=line.search(/\S/),y=headY+row;
      for(let x=headX+headDx+start;x<headX+headDx+line.length;x++){
        if(x>=0&&x<W&&y>=0&&y<H){cells[y][x]=' ';colors[y][x]='f';}
      }
    }
    group(head,headX+headDx,headY,'f');
    put(crest,headX+2+crestDx,headY-1,old?'f':'b');
    // Expose posed anatomical anchors to fitted clothing. The feet remain at
    // their true contacts while the belly now sits just one cell above them.
    rig={small:baby,stage,action,phase:p8,
      head:{x:headX+headDx+1,y:headY,w:head[0].trim().length,h:head.length},
      faceBounds:{x:headX+headDx,y:headY,w:Math.max(...head.map(row=>row.length)),h:head.length},
      eye:{x:headX+headDx+Math.max(1,head[1].indexOf(eye)),y:headY+1,char:eye},
      crest:{x:headX+2+crestDx,y:headY-1,w:crest.length},
      neck:{x:headX+headDx+1,y:headY+head.length,w:baby?2:3},
      body:{x:bodyX,y:bodyY,w:Math.max(...body.map(row=>row.length)),h:body.length},feet};
    wearablePlan=fitWearables(rig,appearance.cosmetics,time);
    if(appearance.emote)put(appearance.emote,headX+headDx+head[0].length+2,headY-1,'a');
    const bill=head[1].match(/(==>|>)[ ]*$/);
    if(bill){
      const bx=headX+headDx+head[1].length-bill[0].length,by=headY+1;
      const open=(action==='quacking'&&(phase===2||phase===3))||(action==='eating'&&[3,4,5].includes(p8));
      put(bill[0],bx,by,'a');
      if(open)put('\\_',bx,by+1,'a');
    }
    if(action==='eating'){
      if(p8>=2&&p8<=5)put(p8<4?' . :':'.  *',headX+headDx+head[1].length,headY+2,'a');
      put(p8<4?' . .':p8<6?' .':'',CX+8,GROUND+1,'a');
    }
    if(action==='sleeping')put(['z','z','z','Z','Z','Z','z','z'][p8],headX+10+(p8%3),headY-2-Math.floor(p8/3),'f');
    if(action==='quacking'&&(phase===2||phase===3||phase===4))put(phase===4?"'":'!',headX+headDx+head[1].length+2,headY,'a');
    if(action==='hopping'&&p8===6)put("' .   . '",bodyX-1,GROUND+1,'s');
    if(stage==='legendary'){
      const sparks=[[CX-8,GROUND-8],[CX+9,GROUND-10],[CX-6,GROUND-12],[CX+7,GROUND-6]];
      const [x,y]=sparks[Math.floor(p8/2)];put(p8%2?'+':'*',x,y,'a');
    }
    const submerged=appearance.diving&&p8>=2&&p8<=5;
    if(!submerged){clipped=paintWearables(cells,colors,rig,wearablePlan)||clipped;inks=wearablePlan.inks;}
    if(submerged){
      for(let y=0;y<H;y++){cells[y].fill(' ');colors[y].fill('b');}
      group([' \\ /','  /\\',' (__)'],CX-2,GROUND-3,'a');
      put(p8%2?'~~~  ~~~~':' ~~~~~~~ ',CX-5,GROUND+1,'w');
      put(p8<4?' o':'  .',CX+3,GROUND+2,'w');
    }
  }
  if(!facing){for(let y=0;y<H;y++){cells[y]=cells[y].reverse().map(mirrorChar);colors[y].reverse();}offsetX=-offsetX;}
  return {art:cells.map(row=>row.join('')),tones:colors.map(row=>row.join('')),width:W,anchorX:facing?CX:W-1-CX,
    inks,rig,wearables:wearablePlan?.items.map(item=>item.id)||[],
    scale:1,body:stage==='hatchling'?'#f7da83':'#e9c67d',face:stageIndex>=6?'#f3eed4':'#ffe6a7',accent:'#f1a751',shade:'#7a8f83',
    name:'',offsetX,offsetY,phase,frames:animation.frames,cycle,clipped};
}
