// Expanded drawings of the original NPC cast.
const lines = text => text.slice(1,-1).split("\n");
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

function drawing(art,{face=[],accent=[],runs=[],scale=1.7,anchor=10}={}){
  const tones=art.map((row,y)=>Array(row.length).fill(face.includes(y)?'f':accent.includes(y)?'a':'b'));
  for(const [y,start,end,tone='a'] of runs)for(let x=start;x<Math.min(end,art[y]?.length||0);x++)tones[y][x]=tone;
  return {art,tones:tones.map(row=>row.join('')),scale,anchorX:anchor};
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
