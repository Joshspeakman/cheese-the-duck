// Expression only: eyes, brows, duck bill and reaction marks. No head contour,
// crest, neck or clothing competes with the emotion in this panel.
export function emotionPortrait(duck={},emotion={},time=0){
  const stage=duck.stage||'adult',mood=emotion.mood||duck.mood||'content';
  const action=String(emotion.action||duck.state||'').toLowerCase();
  const W=34,H=13,cells=Array.from({length:H},()=>Array(W).fill(' '));
  const tones=Array.from({length:H},()=>Array(W).fill('f'));
  const put=(text,x,y,tone='f')=>{for(const [i,c] of Array.from(text).entries())if(y>=0&&y<H&&x+i>=0&&x+i<W){cells[y][x+i]=c;tones[y][x+i]=tone;}};
  const phase=Math.floor(time*3)%8;
  if(stage==='egg'){
    put(phase%2?'?':'!',16,4,'a');
    put('...',15,8,'f');
  }else{
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
    put(left,10,5);put(right,22,5);
    // A broad upper bill, nostril and separate lower mandible read as a duck.
    put(' .---o------.',10,7,'a');
    put(bill==='==='?'(____________)':'(            )',10,8,'a');
    put(bill==='==='?" '----------'":' \\__________/',10,9,'a');
    if(mood==='sad'||mood==='miserable'){put(phase%2?'.':"'",10,6,'w');put(phase%2?"'":'.',22,6,'w');}
    if(mood==='grumpy'||mood==='petty'){put('\\',10,4);put(mood==='petty'?'~':'/',22,4);}
    if(mood==='ecstatic'&&!emote)emote='!!';
    if(mood==='dramatic'&&!emote)emote='?!';
    if(cheeks){put('~',8,6,'a');put('~',24,6,'a');}
    put(emote,1,phase%3===0?3:4,'a');

  }
  return {art:cells.map(row=>row.join('')),tones:tones.map(row=>row.join('')),width:W,anchorX:W/2,groundRow:H,scale:1,
    body:'#e9c67d',face:['mature','elder','legendary'].includes(stage)?'#f3eed4':'#ffe6a7',accent:'#f1a751',shade:'#9aa797',name:'',mood,action};
}
