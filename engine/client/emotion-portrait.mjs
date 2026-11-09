// A face close-up, based on the original two-eye emotion panel, with B's bedhead.
// This has its own expression animation; it never reuses the world body pose.
export function emotionPortrait(duck={},emotion={},time=0){
  const stage=duck.stage||'adult',mood=emotion.mood||duck.mood||'content';
  const action=String(emotion.action||duck.state||'').toLowerCase();
  const W=29,H=11,cells=Array.from({length:H},()=>Array(W).fill(' '));
  const tones=Array.from({length:H},()=>Array(W).fill('f'));
  const put=(text,x,y,tone='f')=>{for(const [i,c] of Array.from(text).entries())if(y>=0&&y<H&&x+i>=0&&x+i<W){cells[y][x+i]=c;tones[y][x+i]=tone;}};
  const phase=Math.floor(time*3)%8;
  if(stage==='egg'){
    ['    .----.','  .\'      `.',' /          \\','|            |','|            |',' \\          /',"  '--------'"].forEach((row,i)=>put(row,7,i+2));
    put(phase>=4?'/\\':phase>=2?'/':' .',14,5,'a');
    put(phase%2?'?':'.',24,2,'a');
  }else{
    const young=['hatchling','duckling'].includes(stage),old=['mature','elder','legendary'].includes(stage);
    ['     ._-------_.',"   .'           `.",'  /               \\',
     ' |                 |',' |                 |','  \\               /',
     "   '-.__     __.-'","        '---'"].forEach((row,i)=>put(row,3,i+2));
    const crests=young?[',,','\\,|',',,']:stage==='elder'?['~\\_','~\\_','~\\/']:['~\\//','~\\/_','~\\//'];
    put(crests[Math.floor(phase/3)%3],12,1,old?'f':'b');
    let [left,right]={ecstatic:['*','*'],happy:['^','^'],content:['-','-'],grumpy:['>','<'],sad:[';',';'],miserable:['T','T'],dramatic:['O','O'],petty:['>','.']}[mood]||['o','o'];
    let bill='===',emote='',cheeks=false;
    if(/eat|feed/.test(action)){left=phase%3?'^':'o';right=left;bill=phase%2?'=v=':'===';emote=phase%2?'. :':'.';}
    else if(/sleep|nap/.test(action)){left=right='-';emote=phase<4?'z':'Zz';}
    else if(/pet|love/.test(action)){left=right='^';cheeks=true;emote=phase%2?'<3':'+';}
    else if(/clean|bath|preen/.test(action)){left=right=phase%3?'^':'-';emote=phase%2?'o *':'* o';}
    else if(/play|danc|happy|excited/.test(action)){left='^';right=phase===3?'-':'^';emote=phase%2?'!':'*';}
    else if(/talk|quack|sing/.test(action)){bill=phase%2?'=O=':'===';emote=phase%2?'!':'.';}
    else if(/angry/.test(action)){left='>';right='<';emote='!';}
    else if(/scared|surpris/.test(action)){left=right='O';bill='=o=';emote='?!';}
    else if(Math.floor(time*4)%19===17){left=right='-';}
    put(left,8,5);put(right,18,5);
    put('>',13,6,'a');put(bill,12,7,'a');
    if(mood==='sad'||mood==='miserable'){put(phase%2?'.':"'",8,6,'w');put(phase%2?"'":'.',18,6,'w');}
    if(mood==='grumpy'||mood==='petty'){put('\\',8,4);put(mood==='petty'?'~':'/',18,4);}
    if(mood==='ecstatic'&&!emote)emote='!!';
    if(mood==='dramatic'&&!emote)emote='?!';
    if(cheeks){put('~',6,6,'a');put('~',20,6,'a');}
    if(old){put("'",6,5,'s');put("'",20,5,'s');}
    if(stage==='legendary'){put('*',10,0,'a');put('*',18,0,'a');}
    put(emote,24,phase%3===0?2:3,'a');
    const equipped=Object.values(duck.cosmetics||{}).join(' ');
    if(/glass/.test(equipped)){put('['+left+']',7,5,'a');put('['+right+']',17,5,'a');}
  }
  return {art:cells.map(row=>row.join('')),tones:tones.map(row=>row.join('')),width:W,anchorX:W/2,groundRow:H,scale:1,
    body:'#e9c67d',face:['mature','elder','legendary'].includes(stage)?'#f3eed4':'#ffe6a7',accent:'#f1a751',shade:'#9aa797',name:'',mood,action};
}
