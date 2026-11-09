import { mirror } from './ultra-art.mjs';

// Expanded drawings of the original cast. Large faces and open interiors are
// deliberate; detail belongs in contours, wings, feet and signature accessories.
const lines = text => text.slice(1,-1).split('\n');
const CHEESE = lines(String.raw`
       .-------.
     .'         '.
    (   o         )__
     '.__     ___/==>
       / '------'\
      /  / .--.  \
     (  (  '--' ) )
      '\_'------'/'
        _/    \_
       /__\  /__\
`);
const BABY = lines(String.raw`
       , ,
      .---.
     ( o __)>
      '.__/
     / (__)\
     \_____/ 
       /_\
`);
const EGG = lines(String.raw`
      .---.
    .'     '.
   /   .     \
  (       .   )
   \   .     /
    '-------'
`);
const FRONT = lines(String.raw`
      .-----.
     /       \
    (  o . o  )
     \   v   /
    /)'-----'(\>
   / / .---. \ \
   \_\ '---' /_/
      '-----'
       /   \
     /__\ /__\
`);

function eyeFor(duck,t){
  const state=duck.state==='idle'?duck.mood||'idle':duck.state||'idle';
  if(/sleep|napping|bored/.test(state))return '-';
  if(/happy|love|petting|playing|proud|danc|excited/.test(state))return '^';
  if(/sad|sick|cold/.test(state))return ';';
  if(/scared|surpris|quack|sing|yawn/.test(state))return 'O';
  if(/angry/.test(state))return '>';
  if(/dizzy/.test(state))return '@';
  if(/think|curious/.test(state))return '.';
  return t%6.1>5.9?'-':'o';
}
function drawing(art,{face=[],accent=[],runs=[],scale=1.7,anchor=10}={}){
  const tones=art.map((row,y)=>Array(row.length).fill(face.includes(y)?'f':accent.includes(y)?'a':'b'));
  for(const [y,start,end,tone='a'] of runs)for(let x=start;x<Math.min(end,art[y]?.length||0);x++)tones[y][x]=tone;
  return {art,tones:tones.map(row=>row.join('')),scale,anchorX:anchor};
}
function flip(model){
  const width=Math.max(...model.art.map(row=>row.length));
  model.art=mirror(model.art);
  model.tones=model.tones.map(row=>[...row.padEnd(width,'b')].reverse().join(''));
  model.anchorX=width-1-model.anchorX;
  return model;
}

export function cheeseDrawing(duck,t){
  const stage=duck.stage||'adult',state=duck.state||'idle',phase=Math.floor(t*6)%4;
  if(stage==='egg')return drawing(EGG.slice(),{face:[1,2,3],scale:1.7,anchor:8});
  const baby=['hatchling','duckling'].includes(stage),teen=['juvenile','teen'].includes(stage);
  const art=(baby?BABY:CHEESE).slice();
  const eye=eyeFor(duck,t);
  art[2]=art[2].replace('o',eye);
  if(stage==='duckling')art[0]='       __';
  if(teen)art[0]='       .--~_~--.';
  if(['elder','mature','legendary'].includes(stage)){
    art[1]="     .'  ~~~    '.";
    art[6]="     (  (  ===  ) )";
  }
  if(stage==='legendary')art[0]='     * .-------. *';
  if(/walk|waddle|danc|playing|excited/.test(state)){
    if(baby)art[6]=phase%2?'      /_>':'        <_\\';
    else {
      art[8]=phase%2?'        _/     _':'         _    \\_';
      art[9]=phase%2?'       /__>  _/  ':'       _/   <__\\';
    }
  }
  if(/flap|wav|stretch|danc|excited/.test(state)){
    if(baby)art[4]=phase<2?'   \\/ (__)\\/':'     / (__)\\';
    else if(phase<2){
      art[5]='   \\ \\ / .--. \\ / /';
      art[6]="    \\_\\(  '--' )/_/";
    }else art[6]="    / / (  '--' ) \\ \\";
  }
  if(/eating|pecking|hungry/.test(state)&&phase<2){
    art[2]=baby?`     ( ${eye} __)> .`:`    (   ${eye}    ____)> .`;
    if(!baby)art[3]="     '.__    \\__/  .";
  }
  if(/preen/.test(state))art[2]=baby?`     ( ${eye}<__)`:`    (   ${eye} <____  )`;
  if(/swim|float|splash/.test(state)){
    art[art.length-2]=baby?'    ~~~~~~~~':'     ~~~-.____.-~~~';
    art[art.length-1]=baby?(phase<2?'      ~~~~':'     ~~  ~~'):(phase<2?'       ~~~--~~~':'      ~~--~~--~~');
  }
  if(/diving/.test(state)){
    const dive=phase<2?['    \\ /','     \\|/','    ~~~~~~~~','  ~~  o  ~~']:['      o','   ~~~  ~~~','     ~~~~~'];
    return drawing(dive,{accent:[0,1],runs:[[2,0,30,'w'],[3,0,30,'w']],scale:1.7,anchor:7});
  }
  if(/sleep|napping/.test(state))art[0]+='  '+(phase<2?'z':'Z');
  if(/love|petting/.test(state))art[0]+=' <3';
  if(/quack|sing|yawn/.test(state)&&phase<2)art[2]+=' !';
  if(/scared|angry/.test(state))art[0]+=' !';
  if(/think|curious/.test(state))art[0]+=' ?';
  if(/clean|shak|splash/.test(state)&&phase%2===0){art[1]="  '"+art[1].slice(3)+" '";}

  let face=[1,2,3],accent=[art.length-2,art.length-1];
  let runs=baby?[[2,9,13]]:[[2,19,22],[3,17,22],[6,10,15,'s']];
  if(/swim|float|splash/.test(state))runs.push([art.length-2,0,30,'w'],[art.length-1,0,30,'w']);
  const cosmetics=Object.values(duck.cosmetics||{}).join(' ');
  if(/glass/.test(cosmetics))art[2]=art[2].replace(eye,`[${eye}]`);
  if(/scarf|bow|tie/.test(cosmetics)){art[baby?3:4]=baby?"      ><==/":"       /'-><----'\\";accent.push(baby?3:4);}
  if(/hat|crown|cap|beret/.test(cosmetics)){
    const hat=/crown/.test(cosmetics)?['       \\V/V/V/','       [=====]']:
      /party|wizard/.test(cosmetics)?['          *','         /:\\','        /___\\']:
      /chef/.test(cosmetics)?["       .-.-.-.",'      (_______)','       |_____|']:
      /beret/.test(cosmetics)?['          @',"       .-'==='."]:['        .----.','        |    |','      __|____|__'];
    art.unshift(...hat.map(line=>baby?line.slice(2):line));face=face.map(y=>y+hat.length);
    accent=[...hat.map((_,i)=>i),...accent.map(y=>y+hat.length)];
    runs=runs.map(([y,...rest])=>[y+hat.length,...rest]);
  }
  const model=drawing(art,{face,accent,runs,scale:baby?1.9:teen?1.55:1.7,anchor:baby?8:11});
  return duck.facing===false?flip(model):model;
}

function originalExpression(duck,t){
  const source=(duck.art||[]).join('\n');
  const face=(source.match(/\(([^)]+)\)/)||[])[1]||'o.o';
  const eyes=[...face].filter(c=>'oO^?<>;-'.includes(c));
  let left=eyes[0]||'o',right=eyes[eyes.length-1]||left;
  if(t%7>6.8){if('oO'.includes(left))left='-';if('oO'.includes(right))right='-';}
  return {source,left,right,happy:face.includes('^')||face.includes('w')};
}

export function visitorDrawing(duck,t){
  const personality=duck.personality||'adventurous',phase=Math.floor(t*4)%4;
  const {source,left,right,happy}=originalExpression(duck,t);
  const art=FRONT.slice();
  art[2]=`    (  ${left} . ${right}  )`;
  let hat=[],accent=[],runs=[],face=[1,2,3];
  if(personality==='adventurous'){
    hat=['        /\\',"     __/^^\\__",'    /________\\'];
    art[4]="    /)'--v--'(\\>";
    art[5]='   / /  /|   \\ \\]';
    art[6]='   \\_\\ [o]  /_/|';
    art[7]="      '-----'  [_]";
    runs=[[4,8,10],[5,8,11],[6,7,10],[5,16,18],[6,16,18],[7,15,18]];
  }else if(personality==='scholarly'){
    hat=["       .---.",'      /_____\\'];
    art[2]=`    ( [${left}]-[${right}] )`;
    art[4]="    /)'--:--'(\\>";
    art[5]='   / / .--.--.\\ \\';
    art[6]=phase<2?'   \\_\\|==|  |/_/':'   \\_\\|  |==|/_/';
    art[7]="      '---^---'";
    accent=[5,6,7];runs=[[2,6,13],[4,9,10]];
  }else if(personality==='artistic'){
    hat=['          @',"      .--'---.","     (________)"];
    art[4]="    /)'--~--'(\\>";
    art[5]='   / / .---. \\ \\  /';
    art[6]='   \\_\\( o.o)/_/--/';
    art[7]="      '-----'   /";
    runs=[[4,8,11],[6,8,13],[5,19,21],[6,16,20],[7,16,18]];
  }else if(personality==='playful'){
    hat=[phase%2?'       --@--':'         @|', '       __|__', '      /_____\\'];
    art[3]=happy?'     \\  w  /':'     \\  v  /';
    art[8]='      d/   \\b';art[9]='     (__) (__)';
    accent=[8,9];
  }else if(personality==='mysterious'){
    hat=['        /\\',"       /..\\",'      /____\\'];
    art[1]='     / .---. \\';
    art[2]=`    ( |${left} _ ${right}| )`;
    art[3]='     \\|___|/';
    art[4]="    /)'-----'(\\>";
    art[5]='   / /   :   \\ \\';
    art[6]='   \\_\\__:_ _/_/';
    art[7]='      ~--~--~';art[8]=phase%2?'      ~~  ~~':'       ~~ ~~';art[9]='';
    runs=[[2,6,13]];
  }else if(personality==='generous'){
    hat=['        <3'];
    art[4]="    /)'--><-'(\\>";
    art[5]='   / / .---. \\ \\ .--+--.';
    art[6]='   \\_\\ \\_/ /_/--|  |  |';
    art[7]="      '-----'    '--+--'";
    runs=[[4,8,11],[5,17,25],[6,17,25],[7,17,25]];
  }else if(personality==='foodie'){
    hat=["       .-.-.-.",'      (       )','       |=====|'];
    art[4]="    /)'-----'(\\>";
    art[5]='   / / |===| \\ \\';
    art[6]=source.includes('~@')||source.includes('nom')?'   \\_\\|___|/_/ (@)':'   \\_\\|___|/_/';
    art[7]="      '-----'";
    runs=[[5,7,12,'f'],[6,7,12,'f'],[6,17,21]];
  }else if(personality==='athletic'){
    hat=['       ====='];
    art[1]='     /=======\\~';
    art[4]="    /)'-----'(\\>";
    art[5]=source.includes('\\/')?' \\ / / .---. \\ \\ /':'   / / .---. \\ \\';
    art[8]=phase%2?'      /     |':'      |     \\';
    art[9]=phase%2?'     /__>  /__\\':'     /__\\  <__\\';
    runs=[[1,6,14],[5,5,7],[5,13,15]];
  }
  if(happy){art[3]='     \\  v  /';art[0]+=' !';}
  if(personality==='generous'&&(source.includes('[#]')||source.includes('[*]'))){
    art[6]=art[6].replace('|  |  |','| [#] |');
  }else if(source.includes('[#]')||source.includes('[*]')){
    art[5]+=' .-+-.';art[6]+=' | # |';art[7]+=" '-+-'";
    runs.push([5,17,30],[6,17,30],[7,17,30]);
  }
  // The original waddle alternates feet. Preserve that cue without changing the face.
  if(source.includes("'' ''")||source.includes('" " ~]')){
    art[8]=phase%2?'       /    _':'       _    \\';
    art[9]=phase%2?'     /__>  __ ':'      __  <__\\';
  }
  const hatCount=hat.length;
  art.unshift(...hat);
  face=face.map(y=>y+hatCount);
  accent=[...hat.map((_,i)=>i),...accent.map(y=>y+hatCount),art.length-2,art.length-1];
  runs=runs.map(([y,...rest])=>[y+hatCount,...rest]);
  return drawing(art,{face,accent,runs,scale:1.5,anchor:9});
}
