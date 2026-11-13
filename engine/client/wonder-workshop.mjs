// Wonder machines and garden curiosities, constructed from ASCII geometry.
// Every animated part reads saved native state (state.wonder) or the parts the
// current routine moves (pose.wonder.object). Nothing here changes the world.
import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/wonders.json' with {type:'json'};
export {BLUEPRINTS as WONDER_BLUEPRINTS};
const TAU=Math.PI*2,clamp=(n,a=0,b=1)=>Math.max(a,Math.min(b,Number.isFinite(n)?n:0));
const hash=(...v)=>{let h=2166136261;for(const c of v.join('|')){h^=c.charCodeAt(0);h=Math.imul(h,16777619);}return h>>>0;};

// ------------------------------------------------------------------ shared construction
function shadow(c,p,rx=p.w*.38){c.ellipse(p.w/2,p.h-2,rx,1.4,'_','k',false);}
function rivets(c,x,y,w,step=6,tone='y'){for(let i=x;i<=x+w;i+=step)c.put(i,y,'o',tone);}
function plate(c,x,y,w,h,tone='t',edge='k'){c.rect(x,y,w,h,edge,false);c.solid(x+1,y+1,w-2,h-2,tone);for(let j=y+2;j<y+h-1;j+=3)c.line(x+2,j,x+w-3,j,'-','s');}
function gear(c,cx,cy,r,a,tone='y'){
 c.ellipse(cx,cy,r,r*.7,'o',tone,true);c.ellipse(cx,cy,r*.45,r*.32,'O','k',false);
 for(let i=0;i<8;i++){const q=a+i*TAU/8;c.put(cx+Math.cos(q)*(r+1.4),cy+Math.sin(q)*(r+1)*.7,'#',tone);}
 c.put(cx,cy,'@','f');
}
function dial(c,cx,cy,r,value,tone='p'){
 c.ellipse(cx,cy,r,r*.65,'-','k',true);c.ellipse(cx,cy,r-1,(r-1)*.65,'.',tone,false);
 const q=Math.PI*(1.15-1.3*clamp(value));c.line(cx,cy,cx+Math.cos(q)*(r-1.5),cy-Math.sin(q)*(r-1.5)*.65,'*','r');c.put(cx,cy,'o','f');
}
function swirl(c,cx,cy,rx,ry,phase,density,tones=['v','c','l']){
 for(let ring=1;ring<=6;ring++){
  const q=ring/6,n=Math.round(10+ring*7*density);
  for(let i=0;i<n;i++){
   const a=phase*(1.6-q)+i/n*TAU+q*2.1,x=cx+Math.cos(a)*rx*q,y=cy+Math.sin(a)*ry*q;
   c.put(x,y,'.:*o@'[Math.min(4,Math.floor((1-q)*5*density+i%2))],tones[(ring+i)%tones.length]);
  }
 }
}
function stars(c,x0,y0,w,h,n,seed,t=0,tone='p'){
 for(let i=0;i<n;i++){const v=hash(seed,i),x=x0+v%w,y=y0+(v>>>9)%h,tw=Math.sin(t*2+i)>.6;c.put(x,y,tw?'*':v%3?'.':'+',tone);}
}
function tube(c,x,y,w,h,level,tone='w'){
 c.rect(x,y,w,h,'k');c.solid(x+1,y+1,w-2,h-2,'d');
 const top=y+h-1-Math.round((h-2)*clamp(level));if(level>.02)c.solid(x+1,top,w-2,y+h-1-top,tone);
 for(let j=Math.max(y+1,top);j<y+h-1;j+=2)c.put(x+1,j,'~',tone);
}
function cloud(c,cx,cy,r,tone='p'){
 for(const [dx,dy,rr] of [[-r*.7,0,r*.55],[0,-r*.25,r*.7],[r*.7,0,r*.55]])c.ellipse(cx+dx,cy+dy,rr,rr*.5,'(','p',true);
 c.line(cx-r*1.1,cy+r*.3,cx+r*1.1,cy+r*.3,'~',tone);
}
function lightning(c,x,y,len,tone='y'){let xx=x;for(let j=0;j<len;j++){xx+=(j%2?1:-1);c.put(xx,y+j,j%2?'/':'\\',tone);}c.put(xx,y+len,'*','f');}
function puddle(c,cx,cy,w,tone='w'){if(w<1)return;c.ellipse(cx,cy,w,Math.max(1,w*.18),'~',tone,true);c.put(cx-w*.4,cy,'-.-','f');}
function leaves(c,x0,y0,w,h,n,seed){for(let i=0;i<n;i++){const v=hash(seed,'leaf',i);c.put(x0+v%w,y0+(v>>>8)%h,'v*,'[v%3],'o');}}
function texture(c,x0,y0,x1,y1,inside,fn){
 for(let y=Math.floor(y0);y<=Math.ceil(y1);y++)for(let x=Math.floor(x0);x<=Math.ceil(x1);x++){if(!inside(x,y))continue;const g=fn(x,y);if(g){c.solid(x,y,1,1,g[2]||g[1]);c.put(x,y,g[0],g[1]);}}
}
const inEllipse=(cx,cy,rx,ry)=>(x,y)=>((x-cx)/rx)**2+((y-cy)/ry)**2<=1;
function mark(c,x,y,text,tone='p'){c.put(x-Math.floor(String(text).length/2),y,text,tone);}

// ------------------------------------------------------------------ garden curiosities
function topiary(c,p,s,v,t){
 const g=clamp(s.growth),hide=clamp(v.hide),sway=Math.sin(t*1.3)*.5;
 plate(c,22,94,76,14,'b');c.line(24,94,96,94,'=','k');for(let x=28;x<94;x+=8)c.put(x,100,'|','s');
 c.solid(25,92,70,2,s.moisture>.4?'d':'n');c.line(26,92,94,92,s.moisture>.4?',':'.','m');c.beam(56,92,56,84,5,'b');
 // A hedge clipped into a sitting duck: body, tucked wing line, raised neck, head and flat bill.
 const body=inEllipse(54,72,36+g*2,13+g),neck=(x,y)=>y>=48&&y<=66&&Math.abs(x-(80+sway*(66-y)/26-(y-40)*.08))<=5+g,
  head=inEllipse(84+sway,42,12+g,7.5+g*.5),bill=(x,y)=>y>=41&&y<=44&&x>=95+sway&&x<=107+sway-(y-41),
  tail=(x,y)=>{const u=(60-y)/16;return u>=0&&u<=1&&Math.abs(x-(20-u*8-hide*2))<=4-u*2+g;},
  shape=(x,y)=>body(x,y)||neck(x,y)||head(x,y)||bill(x,y)||tail(x,y+hide*8);
 texture(c,8,22,112,86,shape,(x,y)=>{
  const h=hash('tp',x,y),edge=!shape(x-1,y)||!shape(x+1,y)||!shape(x,y-1)||!shape(x,y+1);
  if(edge)return [g>.6&&h%3===0?"'":'&','h','h'];
  const wing=Math.abs(((x-50)/26)**2+((y-70)/7)**2-1)<.12&&x>36&&x<74;
  return [wing?'~':'&%@&#&*'[h%7],wing?'s':h%5===0?'f':h%3===0?'s':'h','h'];
 });
 for(let i=0;i<Math.round(6+g*34);i++){const h=hash('sprig',i),a=h%628/100,big=h%2,cx=big?54:84,cy=big?72:34,rx=big?38:13,ry=big?14:8;c.put(cx+Math.cos(a)*(rx+1+g*2),cy+Math.sin(a)*(ry+1+g),"'`,;"[h%4],'h');}
 c.put(88+sway,40,'o','k');c.put(98+sway,42,'====','m');
 if(s.blossom>.3)for(let i=0;i<12;i++){const h=hash('bl',i);c.put(26+h%58,62+(h>>>7)%18,'o','q');}
 if(s.snow>.15){for(let x=22;x<=86;x++)if(hash('sn',x)%10<s.snow*10)c.put(x,59+Math.abs(Math.sin(x/7))*1.5,'~','i');for(let x=74;x<=96;x++)c.put(x+sway,34,'~','i');c.put(76+sway,47,'~~~','i');}
 return {entry:{x:60,y:110},contact:{x:72,y:64},bill:{x:102,y:43},tail:{x:18,y:54},rump:{x:26,y:66},head:{x:84,y:35},back:{x:54,y:62},flank:{x:40,y:76},roots:{x:58,y:98}};
}
function zen(c,p,s,v,t){
 // A low raked bed seen from the front: shallow rows, so Cheese works at its near edge.
 c.ellipse(14,20,6,2,'^','s',true);c.rows(['  _[]_ ',' |/  \\|','  |  | ','  |__| ',' /____\\'],7,22,'t',true);c.put(12,25,'o','e');
 const Y0=42,Y1=64,bed=(x,y)=>y>Y0&&y<Y1&&x>6&&x<133;
 plate(c,5,Y0,130,Y1-Y0+1,'n');c.line(5,Y0,134,Y0,'=','b');c.line(4,Y1,135,Y1,'=','b');c.line(5,Y0,2,Y1,'/','b');c.line(134,Y0,137,Y1,'\\','b');
 const pat=Math.round(s.pattern),raked=clamp(s.raked),sx=100,sy=52;
 texture(c,6,Y0+1,133,Y1-1,bed,(x,y)=>{
  const d=Math.hypot((x-sx)/2.4,(y-sy)*1.5);if(d<6)return null;let ch=null;
  if(pat===0)ch=(y+Math.round(Math.sin(x/6)*1.2))%2===0?'~':null;
  else if(pat===1)ch=Math.round(d)%3===0?(x<sx?'(':')'):null;
  else if(pat===2){const a=Math.atan2((y-sy)*1.5,(x-sx)/2.4);ch=Math.round(d-a*1.8)%4===0?(x<sx?'(':')'):null;}
  else ch=hash(x,y)%23===0?'.':null;
  if(ch&&hash('rk',x,y)%100<raked*100)return [ch,'p','n'];
  if(hash('pit',x,y)%100<(1-raked)*10)return ['.,'[hash(x,y)%2],'s','n'];
  return null;
 });
 c.ellipse(sx,sy,8,3.5,'#','t',true);c.put(sx-5,sy-2,'/~~~\\','f');c.put(sx-3,sy,'.:.','s');c.ellipse(sx,sy-4,4,1.5,'^','t',true);
 const pebble=[[40,50],[28,58],[62,56],[76,48]][Math.round(s.stone)%4],lift=clamp(v.pebble);
 c.ellipse(pebble[0],pebble[1]-lift*2,3,1.2,'o','t',true);c.put(pebble[0]-1,pebble[1]-lift*2-1,'__','f');
 if(s.leaves>.05)leaves(c,8,Y0+1,124,Y1-Y0-2,Math.round(s.leaves*30),'zen');
 if(s.calm>.2)for(let i=0;i<3;i++)c.put(60+i*6,36-Math.sin(t+i)*2,'~','l');
 return {entry:{x:70,y:70},contact:{x:70,y:60},bed_l:{x:30,y:58},bed_c:{x:70,y:58},bed_r:{x:116,y:58},stone:{x:100,y:54},ring_n:{x:100,y:47},ring_e:{x:118,y:54},ring_s:{x:100,y:60},pebble:{x:pebble[0],y:pebble[1]}};
}
function ice(c,p,s,v,t){
 const melt=clamp(s.melt),detail=clamp(s.detail),shine=clamp(s.shine);
 plate(c,30,100,52,12,'t');c.put(37,105,'[ SWAN - ICE ]','p');
 const sag=melt*12,bodyY=88+melt*3,head={x:76,y:34+sag},wingLift=(1-melt)*22;
 const body=inEllipse(54,bodyY,27-melt*5,8-melt*2);
 // Raised swan wings: the top edge rises toward the back and is scalloped with feathers.
 const wingTop=x=>bodyY-5-wingLift*Math.pow(Math.max(0,Math.sin(Math.PI*(x-30)/40)),.7)+(detail>.4?(x%4<2?0:1):0);
 const wing=(x,y)=>x>30&&x<70&&y>=wingTop(x)&&y<bodyY-2;
 const neckX=y=>head.x-6+Math.sin((y-head.y)/(bodyY-head.y)*Math.PI*1.1)*(7-melt*3);
 const neck=(x,y)=>y>head.y+3&&y<bodyY-3&&Math.abs(x-neckX(y))<=2.6-melt;
 const hd=inEllipse(head.x,head.y,5.5-melt*2,3.4-melt);
 const shape=(x,y)=>body(x,y)||wing(x,y)||neck(x,y)||hd(x,y);
 texture(c,24,head.y-5,92,bodyY+9,shape,(x,y)=>{
  const h=hash('ice',x,y),edge=!shape(x-1,y)||!shape(x+1,y)||!shape(x,y-1);
  if(edge)return [h%3?'.':':',h%9<shine*9?'f':'i','i'];
  if(wing(x,y)&&!body(x,y)&&detail>.25&&(x+y)%5===0)return ['>','f','i'];
  return [h%11===0?'*':h%3?' ':'.',h%9<shine*9?'f':'i','i'];
 });
 if(melt<.75){c.put(head.x+5,head.y,'>=','f');c.put(head.x,head.y-1,'o','k');}
 if(s.frost>.2)for(let i=0;i<Math.round(s.frost*26);i++){const h=hash('fr',i);const x=30+h%54,y=head.y+(h>>>8)%(bodyY-head.y+6);if(shape(x,y))c.put(x,y,'+','p');}
 if(melt>.1)for(let i=0;i<Math.round(melt*8);i++){const x=36+i*6,y=bodyY+8+((t*3+i)%3);c.put(x,y,"'",'w');}
 puddle(c,92,110,4+s.puddle*14);
 const tarp=Math.max(clamp(s.tarp),clamp(v.tarp_hold)*.8);
 if(tarp>.05){const top=Math.round(head.y-4+(1-tarp)*60);for(let y=top;y<100;y++){const half=8+(y-top)*.55;c.solid(64-half*.5-6,y,half+14,1,'p');c.put(58-half*.5,y,'/','b');c.put(70+half*.5,y,'\\','b');}
  c.line(58,top,74,top,'^','b');}
 return {entry:{x:56,y:118},contact:{x:62,y:84},flank:{x:40,y:Math.round(bodyY-2)},wing:{x:46,y:Math.round(wingTop(46))+3},neck:{x:Math.round(neckX(head.y+20)),y:head.y+20},breast:{x:78,y:bodyY},crown:{x:head.x,y:head.y-4},base:{x:56,y:100},puddle:{x:92,y:110}};
}
function sandcastle(c,p,s,v,t){
 const er=clamp(s.erosion),towers=Math.round(s.towers),damp=s.damp>.5?'o':'n';
 c.ellipse(66,80,58,12,'.',damp,true);for(let i=0;i<40;i++){const h2=hash('sand',i);c.put(10+h2%112,72+(h2>>>8)%14,'.:,'[h2%3],'s');}
 const moat=clamp(s.moat);if(moat>.03){c.ellipse(66,86,48,4,'~','w',false);if(moat>.3)c.ellipse(66,86,44,2.5,'~','w',false);}else c.ellipse(66,86,48,4,'.','s',false);
 c.ellipse(12,82,8,4,'.','n',true);c.put(8,79,'.:.:.','s');
 const wallH=Math.round(14*(1-er*.6));
 c.solid(30,70-wallH,72,wallH,damp);c.rect(30,70-wallH,72,wallH,'b');
 if(er<.5)for(let x=30;x<102;x+=4)c.put(x,69-wallH,'[]','b');else for(let x=32;x<100;x+=7)c.put(x,70-wallH,'~.','s');
 c.put(60,66,'|^^|','k');c.solid(61,67,2,3,'d');
 const slots=[[66,56,18,8],[38,62,12,5],[94,62,12,5],[50,58,10,4],[82,58,10,4]];
 for(let i=0;i<=Math.min(4,towers);i++){
  const [cx,base,h,r]=slots[i],hh=Math.round(h*(1-er*.5));if(i>0||towers>0){
  c.solid(cx-r,base-hh,r*2,hh,damp);c.line(cx-r,base-hh,cx-r,base,'|','b');c.line(cx+r-1,base-hh,cx+r-1,base,'|','b');
  if(er<.6)for(let x=cx-r;x<cx+r;x+=3)c.put(x,base-hh-1,'n','b');else c.put(cx-2,base-hh-1,'.~.','s');
  c.put(cx-1,base-hh+3,'[]','k');}
 }
 const tip=towers>0?{x:66,y:Math.round(56-18*(1-er*.5))-2}:{x:66,y:60-wallH};
 if(s.flag>.5||v.flagstick>.5){c.line(tip.x,tip.y,tip.x,tip.y-8,'|','k');c.put(tip.x+1,tip.y-8+Math.round(Math.sin(t*4)),'>>','r');}
 for(let i=0;i<5;i++){const h2=hash('shell',i);c.put(34+h2%64,64-(h2>>>8)%6,'@','q');}
 return {entry:{x:66,y:94},contact:{x:66,y:60},keep:{x:66,y:44},tip,wall_l:{x:36,y:62},wall_r:{x:96,y:62},moat_l:{x:24,y:85},moat_c:{x:66,y:89},moat_r:{x:108,y:85},sandpile:{x:12,y:82}};
}
function gong(c,p,s,v,t){
 for(const x of [10,92]){c.beam(x,22,x,120,5,'b');c.put(x-2,120,'[___]','k');}
 c.beam(6,18,98,18,4,'b');for(let x=4;x<=100;x++)c.put(x,13-Math.round(Math.sin((x-4)/96*Math.PI)*5),'_','r');c.put(46,7,'(@)','y');
 const ring=clamp(s.ring),shake=Math.sin(t*38)*ring*1.2,cx=52+shake,cy=80;
 c.line(36,20,cx-16,cy-18,'\\','p');c.line(68,20,cx+16,cy-18,'/','p');c.line(36,20,36,cy-20,':','p');c.line(68,20,68,cy-20,':','p');
 c.ellipse(cx,cy,30,20,'O','y',true);
 for(let r=3;r<=20;r+=3)c.ellipse(cx,cy,r*1.5,r,r%8===3?'-':'.',r%8===3?'a':'s',false);
 c.ellipse(cx,cy,7,4,'@','a',true);c.put(cx-1,cy,'()','f');
 for(let i=0;i<Math.round(s.shine*12);i++){const q=-2.3+i*.12;c.put(cx+Math.cos(q)*22,cy+Math.sin(q)*14,'*','f');}
 if(ring>.08)for(let k=1;k<=3;k++){const rr=31+k*3+Math.round(t*12%3);c.put(cx-rr,cy,'(','c');c.put(cx+rr,cy,')','c');c.put(cx-rr+2,cy-8,'(','c');c.put(cx+rr-2,cy-8,')','c');}
 if(s.muted>.5)c.rows(['.~~~~.','|    |',"'~~~~'"],cx-3,cy-3,'p',true);
 if(s.dust>.2)for(let i=0;i<Math.round(s.dust*20);i++){const h2=hash('gd',i);c.put(cx-24+h2%48,cy-20+(h2>>>8)%40,'.','s');}
 if(!(v.mallet>.1)){c.line(92,60,96,80,'|','b');c.ellipse(97,82,3,2,'@','q',true);}
 return {entry:{x:52,y:122},contact:{x:52,y:92},post_foot:{x:92,y:120},boss:{x:52,y:80},rim:{x:30,y:92},rim_r:{x:74,y:92},rim_low:{x:52,y:99}};
}

// ------------------------------------------------------------------ lights and skies
function aurora(c,p,s,v,t){
 const glow=clamp(s.glow),hue=s.hue,n=Math.round(s.ribbons),tones=hue<.33?['g','c','g']:hue<.66?['c','v','g']:['v','q','l'];
 if(glow>.05)for(let r=0;r<n;r++){
  const base=12+r*8,amp=4+r,ph=s.drift*TAU+r*1.3+t*.4;
  for(let x=8;x<124;x++){const y=base+Math.sin(x/11+ph)*amp+Math.sin(x/5+ph*1.7);for(let k=0;k<Math.round(1+glow*4);k++)if(hash(x,k,r)%10<glow*10)c.put(x,y+k,k===0?'~':'|:.'[k%3],tones[r%3]);}
 }
 c.line(66,70,40,104,'/','t');c.line(66,70,92,104,'\\','t');c.line(66,70,66,104,'|','t');
 c.ellipse(66,64,13,8,'(',glow>.3?'c':'t',true);c.ellipse(66,64,9,5,'o',glow>.3?'f':'s',false);c.put(64,64,glow>.3?'(*)':'(-)',glow>.3?'f':'k');
 c.rect(58,72,16,4,'k');c.put(60,73,'[====]','y');
 plate(c,30,96,72,10,'t');dial(c,88,100,5,(v.dial??hue));
 c.rect(36,97,10,6,'k');c.put(39,99,(v.switch??(s.power>.5?1:0))>.5?'ON':'--',(s.power>.5)?'g':'s');
 return {entry:{x:66,y:110},contact:{x:66,y:96},switch:{x:40,y:98},dial:{x:88,y:98},lens:{x:66,y:72}};
}
function rainbow(c,p,s,v,t){
 const arc=clamp(s.arc),mist=clamp(s.mist);
 if(arc>.05){const bands=['r','o','y','g','c','u','v'];for(let b=0;b<7;b++)for(let x=60;x<=122;x++){const q=(x-60)/62,y=60-Math.sqrt(Math.max(0,Math.sin(q*Math.PI)))*(30-b*1.4)+b*.4;if(hash(x,b)%10<arc*10)c.put(x,y,'=',bands[b]);}}
 if(mist>.05)for(let i=0;i<Math.round(mist*40);i++){const h2=hash('mist',i,Math.floor(t*3));c.put(84+h2%30,30+(h2>>>8)%20,'.:'[h2%2],'w');}
 for(const x of [16,46])c.beam(x,82,x,106,3,'b');plate(c,10,48,42,36,'y');tube(c,22,54,6,26,s.water);c.put(32,56,'H2O','k');rivets(c,12,50,38);
 c.ellipse(4,80,3,3,'O','k',false);c.line(4,80,4+Math.cos((v.crank||0)*TAU)*4,80+Math.sin((v.crank||0)*TAU)*3,'=','y');
 c.rect(22,106,18,3,'k');c.put(24,107,s.water>.3?'~~~~~~~~~~~~~~':'..............','w');for(let i=0;i<3;i++)c.put(30+i*3,86+((t*4+i*3)%18),"'",'w');
 c.line(46,52,84,40,'=','t');c.line(84,40,84,30,'|','t');c.rows(['<o>'],82,40,'y');
 const tilt=s.prism;c.rows([' /\\','/__\\'],92+Math.round(tilt*3),28,'c',true);c.line(84,30,94,30,'-','t');c.line(94,32,94,74,':','t');c.ellipse(94,76,3,2,'@','y',true);c.put(54,70,'(v)','r');
 return {entry:{x:60,y:110},contact:{x:40,y:70},tank:{x:30,y:66},drip:{x:31,y:107},crank:{x:6,y:80},prism:{x:96,y:30},prism_knob:{x:94,y:76},nozzle:{x:84,y:40},valve:{x:55,y:70}};
}
function weather(c,p,s,v,t){
 const set=Math.round(s.setting)%4,charge=clamp(s.charge);
 plate(c,20,70,96,52,'t');rivets(c,22,72,92,8);
 c.ellipse(68,48,30,20,'(','d',true);c.ellipse(68,48,30,20,'.','c',false);c.put(42,42,')','f');
 const inner=['sun','rain','snow','wind'][set];
 if(inner==='sun'){c.ellipse(68,44,6,4,'O','y',true);for(let i=0;i<8;i++){const a=i*TAU/8+t;c.put(68+Math.cos(a)*10,44+Math.sin(a)*6,'*','y');}}
 else{cloud(c,68,38,9);for(let i=0;i<8;i++){const x=58+i*3,y=46+((t*6+i*3)%10);c.put(x,y,inner==='rain'?'|':inner==='snow'?'*':'~',inner==='rain'?'w':inner==='snow'?'p':'c');}}
 c.line(100,22,100,10,'|','t');c.rows(['\\___/',' \\_/'],95,6,'t');c.put(98,20,'@@@','y');
 dial(c,52,88,7,set/3);mark(c,52,97,['SUN','RAIN','SNOW','WIND'][set],'p');
 for(let i=0;i<5;i++)c.put(30+i*4,84,i<charge*5?'#':'.','g');mark(c,38,82,'CHARGE','s');
 c.rect(84,92,14,8,'k');c.put(86,95,'::::','s');
 c.beam(12,92,12,72-(v.lever||0)*-6,2,'k');c.ellipse(12,72+(v.lever||0)*12,3,2,'@','r',true);
 c.ellipse(124,90,4,3,'O','k',false);c.line(124,90,124+Math.cos((v.crank||0)*TAU)*4,90+Math.sin((v.crank||0)*TAU)*3,'=','y');
 if(s.cloud>.05){cloud(c,68,10,8+s.cloud*4);if(set===1||set===2)for(let i=0;i<6;i++)c.put(58+i*4,16+((t*6+i)%4),set===1?"'":'*',set===1?'w':'p');}
 c.line(100,22,112,72,':','y');c.rect(108,72,8,6,'k');c.put(110,74,'(+)','y');
 if(s.bolt>.1){lightning(c,100,22,10);c.put(108,70,'*zt*','f');}
 return {entry:{x:68,y:126},contact:{x:68,y:90},dial:{x:52,y:88},crank:{x:124,y:90},lever:{x:12,y:76},coil:{x:100,y:20},terminal:{x:112,y:75},vent:{x:90,y:96}};
}

// ------------------------------------------------------------------ space and spectacle
function portal(c,p,s,v,t){
 const energy=clamp(s.energy),stab=clamp(s.stability),jit=(1-stab)*Math.sin(t*20)*1.5,cx=70+jit,cy=72;
 c.solid(10,120,120,8,'t');for(let x=12;x<128;x+=10)c.put(x,122,'[__]','s');
 for(let i=0;i<40;i++){const a=i/40*TAU,x=cx+Math.cos(a)*50,y=cy+Math.sin(a)*38;c.solid(x-3,y-1,7,3,'t');c.put(x-2,y,i%5===0?'[#]':'===','s');}
 const idle=Math.floor(t*2)%9;  // a dormant ring still glimmers, one rune at a time
 for(let i=0;i<9;i++){const a=-Math.PI/2+(i-4)*.38,x=cx+Math.cos(a)*50,y=cy+Math.sin(a)*38;c.put(x-1,y,'<'+('ABCDEFGHI'[i])+'>',i<=s.rune*2&&energy>.1?'g':i===idle&&t>0?'c':'p');}
 if(energy>.03)swirl(c,cx,cy,42,30,s.swirl*TAU+t*1.5,Math.min(1,energy*1.4));else{for(let y=cy-28;y<cy+28;y+=6)c.put(cx-2,y,'. .','s');}
 if(stab<.5)for(let i=0;i<6;i++){const h2=hash('crack',i);c.put(cx-46+h2%92,cy-50+(h2>>>8)%100,'/\\'[h2%2],'r');}
 plate(c,40,104,60,14,'t');for(let i=0;i<3;i++)c.put(48+i*18,110,'<'+'ACE'[i]+'>',energy>.1&&i<=s.rune?'g':'p');
 if(v.pebble>.5)c.put(30,108,'o','t');
 return {entry:{x:70,y:130},contact:{x:70,y:112},swirl_low:{x:70,y:96},rune_l:{x:22,y:72},rune_top:{x:70,y:34},rune_r:{x:118,y:72},console_l:{x:49,y:110},console_c:{x:67,y:110},console_r:{x:85,y:110},swirl:{x:70,y:72},ring_l:{x:24,y:96}};
}
function wormhole(c,p,s,v,t){
 const ap=clamp(s.aperture),spin=s.spin*TAU+t;
 stars(c,4,4,124,70,40,'wh',t,'p');
 for(let i=0;i<=30;i++){const q=i/30,x=36+q*64,y=74-Math.sin(q*Math.PI)*34-q*8;c.put(x,y,'.:*'[i%3],'l');c.put(x,y+2,'.','v');}
 for(const [cx,cy,r] of [[36,74,14],[100,66,12]]){
  c.ellipse(cx,cy,r,r*.8,'(','d',true);for(let k=0;k<4;k++)c.ellipse(cx,cy,r*(1-k*.22),r*.8*(1-k*.22),k%2?'.':'o',k%2?'v':'c',false);
  if(ap>.1)swirl(c,cx,cy,r*ap,r*.8*ap,spin,ap*.7,['l','v','c']);else c.ellipse(cx,cy,3,2,'-','s',true);
 }
 c.beam(24,100,24,116,3,'t');c.ellipse(24,96,9,6,'O','y',false);for(let i=0;i<6;i++){const a=i*TAU/6+ap*2;c.line(24,96,24+Math.cos(a)*8*(1-ap*.6),96+Math.sin(a)*5*(1-ap*.6),'-','y');}
 c.put(14,116,'[_______]','k');c.ellipse(34,108,2,1.5,'@','y',true);c.put(32,111,'<>','p');
 if(v.boat>.5)c.put(38,88,'\\_/','p');
 return {entry:{x:66,y:118},contact:{x:40,y:80},iris:{x:24,y:96},align_knob:{x:34,y:108},near:{x:36,y:80},far:{x:100,y:72}};
}
function blackhole(c,p,s,v,t){
 const spin=s.spin*TAU+t*.8,mass=clamp(s.mass),cont=clamp(s.containment),hum=clamp(s.hum);
 plate(c,26,84,60,30,'t');c.put(34,112,'[__________]','k');
 dial(c,56,96,8,1-cont);mark(c,56,106,cont<.3?'!! LEAK !!':'HORIZON OK',cont<.3?'r':'g');
 c.ellipse(56,48,32,22,'.','c',false);texture(c,24,26,88,70,inEllipse(56,48,31,21),(x,y)=>hash('bh',x,y)%17===0?['.','l','d']:[' ','d','d']);c.ellipse(56,48,32,22,'.','c',false);
 for(let i=0;i<80;i++){const a=spin+i/80*TAU,r=12+mass*8+(i%3)*2;c.put(56+Math.cos(a)*r*1.3,48+Math.sin(a)*r*.32,'~-=*'[i%4],i%2?'o':'y');}
 c.ellipse(56,48,6+mass*5,4+mass*3,'@','k',true);c.ellipse(56,48,6+mass*5,4+mass*3,'O','v',false);
 c.put(53,71,'[o]','y');
 for(const [x,y] of [[26,62],[86,62]]){c.rect(x-3,y-2,7,5,'k');c.put(x-1,y,'(+)',cont<.4?'r':'y');}
 c.line(24,62,88,62,'=','t');
 if(hum>.1)for(let k=0;k<3;k++)c.put(56-36-k*2,44,'(','v');
 if(v.leaf>.5)c.put(50,30,'v','o');
 return {entry:{x:56,y:114},contact:{x:56,y:80},glass_low:{x:56,y:69},port:{x:55,y:72},rim:{x:56,y:26},bolt_l:{x:26,y:62},bolt_r:{x:86,y:62},gauge:{x:56,y:94},glass:{x:72,y:24}};
}
function volcano(c,p,s,v,t){
 const pr=clamp(s.pressure),er=clamp(s.eruption),warm=clamp(s.warmth);
 for(let y=24;y<112;y++){const half=8+(y-24)*.72;c.solid(72-half,y,half*2,1,'t');c.put(72-half,y,'/','b');c.put(72+half,y,'\\','b');
  for(let x=72-half+2;x<72+half-1;x+=5)if(hash('rk',x,y)%4===0)c.put(x,y,'^.:'[hash(x,y)%3],'s');}
 c.ellipse(72,24,10,2.5,'~',pr>.6||er>.1?'e':'o',true);c.put(66,23,'v v v',er>.1?'f':'r');
 for(let i=0;i<4;i++){const y=50+i*14,x=72+(i%2?-1:1)*(10+i*4);c.put(x,y,warm>.4?'(*)':'(.)',warm>.4?'e':'s');}
 if(er>.05){for(let i=0;i<Math.round(er*30);i++){const h2=hash('lava',i),q=(h2%100)/100,side=h2%2?1:-1;c.put(72+side*q*30,24+q*60,'~',q<.4?'e':'r');}
  for(let i=0;i<Math.round(er*24);i++){const h2=hash('plume',i,Math.floor(t*4));c.put(60+h2%24,2+(h2>>>8)%20,'*@o.'[h2%4],h2%3?'e':'o');}}
 else if(pr>.5)for(let i=0;i<3;i++)c.put(70+i*2,18-((t*4+i)%6),'.','s');
 if(s.ash>.1)for(let i=0;i<Math.round(s.ash*40);i++){const h2=hash('ash',i);c.put(10+h2%124,96+(h2>>>8)%16,'.','s');}
 c.rows(['\\___/',' \\_/','  |'],14,88,'t',true);c.line(17,91,40,60,':','s');c.put(52,96,'(*)',warm>.4?'e':'s');c.line(110,92,128,92,'=','y');c.line(128,92,128,80,'|','y');dial(c,128,74,5,pr);c.ellipse(120,92,3,2,(v.valve||0)>.5?'X':'+','r',true);
 return {entry:{x:72,y:118},contact:{x:72,y:96},crater:{x:72,y:22},hopper:{x:16,y:89},vent_low:{x:53,y:96},valve:{x:120,y:90},slope_l:{x:40,y:80},slope_r:{x:104,y:80},base:{x:72,y:108}};
}
function tornado(c,p,s,v,t){
 const size=clamp(s.size),spin=clamp(s.spin),cov=Math.max(clamp(s.covered),clamp(v.cloth)*.9),mood=clamp(s.mood);
 plate(c,18,110,68,12,'b');c.line(16,110,88,110,'=','k');
 c.ellipse(52,62,30,32,'.','c',false);c.line(26,96,78,96,'_','c');c.ellipse(52,30,10,2,'=','k',true);c.put(44,34,'/      \\','c');
 const w0=4+size*9,drift=x=>Math.sin(t*2+x*3)*3*size;
 for(let y=36;y<96;y++){const q=(y-36)/60,half=w0*(1-q)+1.2,x=52+drift(q);
  for(let k=-half;k<=half;k+=1){const a=(k/half)*Math.PI/2+t*7*spin+y*.6;if(Math.cos(a)>.35)c.put(x+k,y,Math.sin(a)>0?'(':')',q<.3?'p':'l');}
  if(y%5===0)c.put(x-half-1,y,'~','s');}
 const fx=52+drift(0);c.put(fx-2,42,mood>.5?'^ ^':'o o','k');c.put(fx-1,44,mood>.5?'w':'-','k');
 if(s.debris>.05)for(let i=0;i<Math.round(s.debris*12);i++){const a=t*6*spin+i;c.put(52+Math.cos(a)*(w0+4),46+i*3.5,'v','o');}
 if(cov>.05){const top=Math.round(24+(1-cov)*40);for(let y=top;y<Math.min(98,top+70*cov);y++){const half=12+(y-top)*.3;c.solid(52-half,y,half*2,1,'q');c.put(52-half,y,'(','r');c.put(52+half,y,')','r');}c.put(46,top+2,'z z z','p');}
 return {entry:{x:52,y:122},contact:{x:52,y:84},funnel:{x:60,y:64},lid:{x:52,y:30}};
}
function antigravity(c,p,s,v,t){
 const f=clamp(s.field),dr=s.drift*TAU+t*.6;
 c.ellipse(62,102,52,10,'=','t',true);for(let x=16;x<110;x+=6)c.put(x,102,f>.3?'+':'.',f>.3?'c':'s');c.ellipse(62,102,52,10,'-','k',false);
 for(const [y,r,tilt] of [[24,22,.35],[50,30,.3],[74,38,.25]]){
  const lift=f*Math.sin(dr+y)*2;c.ellipse(62,y+lift,r,r*tilt,'o',f>.2?'y':'s',false);
  for(let i=0;i<6;i++){const a=dr*(y/24)+i;c.put(62+Math.cos(a)*r,y+lift+Math.sin(a)*r*tilt,'@','y');}
 }
 for(let i=0;i<Math.round(s.floaters);i++){const a=i*1.9+dr,h=f*(30+i*6);c.put(40+i*9,96-h+Math.sin(a)*2,'o','t');}
 if(f>.3)for(let i=0;i<10;i++)c.put(20+i*9,92-((t*10+i*5)%30),"'",'c');
 c.rect(6,98,10,8,'k');c.put(8,101,f>.4?'ON':'--',f>.4?'g':'s');
 return {entry:{x:62,y:118},contact:{x:62,y:96},switch:{x:10,y:100},plate:{x:62,y:98},ring_top:{x:62,y:24},ring_mid:{x:62,y:50},ring_low:{x:30,y:78}};
}
function forcefield(c,p,s,v,t){
 const sh=clamp(s.shield),charge=clamp(s.charge),rip=clamp(s.ripple);
 c.ellipse(74,114,62,4,'.','s',false);c.beam(74,112,74,72,5,'t');c.ellipse(74,68,7,5,'@',charge>.3?'c':'s',true);c.put(71,68,'(*)',charge>.3?'f':'k');
 for(let i=0;i<6;i++)c.put(70,78+i*5,'=@=','y');
 plate(c,54,100,40,12,'t');for(let i=0;i<5;i++)c.put(58+i*4,104,i<charge*5?'#':'.','g');c.rect(56,106,8,4,'k');c.put(58,107,sh>.5?'ON':'--','g');
 c.ellipse(90,104,3,2,'O','k',false);c.line(90,104,90+Math.cos((v.crank||0)*TAU)*3,104+Math.sin((v.crank||0)*TAU)*2,'=','y');
 if(sh>.05){for(let y=8;y<112;y++){const q=1-((112-y)/104)**2,half=66*Math.sqrt(Math.max(0,q));
   const glyph=(y%4===0)?'_':'/\\'[y%2];c.put(74-half,y,'(','c');c.put(74+half,y,')','c');
   if(y%6===0)for(let x=74-half+3;x<74+half-5;x+=6)if(hash(x,y)%10<sh*10)c.put(x+(y%12?3:0),y,'/\\_'[Math.round(x+y)%3],rip>.2&&Math.abs(y-60-Math.sin(t*6)*30)<6?'f':'l');}
  if(rip>.1){const ry=60+Math.sin(t*5)*20;c.line(14,ry,134,ry,'~','f');}
  for(let i=0;i<Math.round(rip*10);i++){const h2=hash('spark',i,Math.floor(t*4));const a=(h2%314)/100;c.put(74+Math.cos(a)*66,112-Math.sin(a)*104,'*','f');}}
 return {entry:{x:74,y:118},contact:{x:74,y:100},switch:{x:60,y:106},crank:{x:90,y:104},dome:{x:30,y:70}};
}
function arch(c,p,s,v,t){
 const glow=clamp(s.starlight),moss=clamp(s.moss),traced=Math.round(s.traced);
 for(const x of [20,130]){c.solid(x-10,40,20,88,'t');c.rect(x-10,40,20,88,'k');for(let y=46;y<126;y+=8)c.put(x-8,y,'=[]=[]=','s');}
 for(let i=0;i<=60;i++){const a=Math.PI-i/60*Math.PI,x=75+Math.cos(a)*55,y=46-Math.sin(a)*36;c.solid(x-6,y-2,12,5,'t');c.put(x-4,y,i%6?'====':'[##]','s');}
 c.ellipse(75,18,10,7,'O','y',true);const w=(s.align+(v.wheel||0))*TAU;for(let i=0;i<8;i++){const a=w+i*TAU/8;c.put(75+Math.cos(a)*8,18+Math.sin(a)*5,'*','f');}c.put(74,18,'@','k');
 const pts=[[26,40],[34,30],[44,22],[56,16],[94,16],[106,22],[116,30],[124,40]];
 for(const [i,[x,y]] of pts.entries())c.put(x,y,glow>.3?'*':'+',glow>.3?(i<=traced?'f':'y'):'s');
 for(let i=0;i<Math.min(traced,7);i++){const [x0,y0]=pts[i],[x1,y1]=pts[i+1];if(glow>.3)c.line(x0,y0+1,x1,y1+1,'.','v');}
 if(moss>.1)for(let i=0;i<Math.round(moss*40);i++){const h2=hash('moss',i);c.put((h2%2?12:122)+(h2>>>4)%14,60+(h2>>>8)%60,'"','m');}
 c.ellipse(28,100,6,4,'O','y',true);for(let i=0;i<6;i++){const a=w+i*TAU/6;c.put(28+Math.cos(a)*5,100+Math.sin(a)*3,'*','f');}c.line(28,96,28,46,':','y');
 for(const [i,[x,y]] of [[118,96],[122,104],[126,98],[120,110]].entries())c.put(x,y,glow>.3?'*':'+',glow>.3?(i<=traced?'f':'y'):'s');
 if(glow>.3)stars(c,40,52,70,60,Math.round(glow*20),'archsky',t,'v');
 return {entry:{x:75,y:130},contact:{x:75,y:100},wheel:{x:75,y:22},dial_low:{x:28,y:100},keystone:{x:75,y:12},stars_l:{x:34,y:30},stars_r:{x:116,y:30},stars_low_a:{x:118,y:96},stars_low_b:{x:126,y:98},stars_low_c:{x:120,y:110},pillar_l:{x:28,y:108},pillar_r:{x:122,y:108}};
}

// ------------------------------------------------------------------ doors and machines
function timemachine(c,p,s,v,t){
 const flux=clamp(s.flux),door=Math.max(clamp(s.door),clamp(v.door)),shine=clamp(s.shine);
 c.solid(22,26,88,104,'y');c.rect(22,26,88,104,'k');rivets(c,24,28,84,7,'f');rivets(c,24,127,84,7,'f');
 for(let x=10;x<=122;x++)c.put(x,22-Math.round(Math.sin((x-10)/112*Math.PI)*8),'_','b');c.line(14,23,118,23,'=','k');
 c.ellipse(66,14,9,6,'O','p',true);c.ellipse(66,14,9,6,'o','k',false);const hh=t*.3;c.line(66,14,66+Math.cos(hh)*6,14+Math.sin(hh)*4,'-','k');c.line(66,14,66+Math.cos(hh*12)*4,14+Math.sin(hh*12)*3,'-','r');
 gear(c,36,48,6,t*2,'o');gear(c,96,48,6,-t*2,'o');
 const year=String(Math.round(s.year)).padStart(4,'0');c.rect(48,36,36,8,'k');c.solid(49,37,34,6,'d');for(const [i,d] of [...year].entries())c.put(52+i*8,40,'['+d+']','g');
 c.ellipse(66,84,22,30,'(','t',true);c.ellipse(66,84,22,30,'O','k',false);
 if(door>.05){c.ellipse(66,84,20*door,28,' ','d',true);for(let i=0;i<10;i++){const a=t*3+i;c.put(66+Math.cos(a)*14*door,84+Math.sin(a)*20,'.*'[i%2],'v');}}
 else{c.ellipse(66,84,12,16,'o','c',false);c.put(58,84,'(     )','f');}
 for(let i=0;i<Math.round(shine*8);i++)c.put(26+i*10,30+(i%3)*30,'*','f');
 c.line(100,30,120,30,'=','y');c.line(120,30,120,60,'|','y');
 c.beam(118,120,118,96-(v.lever||0)*-8,2,'k');c.ellipse(118,94+(v.lever||0)*10,3,2,'@','r',true);
 c.ellipse(10,100,5,4,'O','y',false);const k=(v.key||0)*Math.PI/2;c.line(10,100,10+Math.cos(k)*7,100+Math.sin(k)*4,'=','y');
 c.rect(84,104,22,12,'k');c.solid(85,105,20,10,'d');c.put(87,107,year.slice(-2)+' <>','g');c.ellipse(95,112,2,1.5,'@','r',true);c.line(66,44,95,104,':','y');c.put(30,122,'[====]','f');c.put(84,122,'[====]','f');
 if(flux>.05)for(let i=0;i<Math.round(flux*40);i++){const h2=hash('flux',i,Math.floor(t*6));c.put(14+h2%104,8+(h2>>>8)%120,'~*'[h2%2],h2%3?'c':'v');}
 return {entry:{x:66,y:134},contact:{x:66,y:110},counter:{x:66,y:40},year_knob:{x:95,y:110},clock:{x:66,y:14},door:{x:66,y:104},lever:{x:118,y:100},key:{x:10,y:100},brass_low:{x:36,y:122},brass_low_r:{x:90,y:122},pipe:{x:110,y:30}};
}
function booth(c,p,s,v,t){
 const door=Math.max(clamp(s.door),clamp(v.door)),lamp=clamp(s.lamp);
 c.ellipse(52,6,4,3,'(',lamp>.2?'f':'p',true);c.put(50,6,lamp>.2?'(*)':'(.)',lamp>.2?'y':'s');c.rows(['_______'],48,9,'k');
 c.solid(14,12,76,6,'u');c.rect(14,12,76,6,'k');c.solid(10,18,84,8,'u');c.rect(10,18,84,8,'k');c.solid(18,20,68,4,'k');mark(c,52,22,'BIGGER  INSIDE','p');
 c.solid(12,26,80,104,'u');c.rect(12,26,80,104,'k');c.line(52,26,52,130,'|','k');
 for(const x0 of [16,56]){for(const y0 of [32,60,86,108]){c.rect(x0,y0,32,y0===32?22:20,'k');if(y0===32)for(let i=0;i<3;i++){c.solid(x0+2+i*10,y0+2,8,8,'p');c.put(x0+4+i*10,y0+6,'+','k');}}}
 if(door>.05){const w=Math.round(36*door);c.solid(53,27,w,102,'d');for(let k=1;k<6;k++){const q=k/6;c.rect(53+w*q*.5,27+q*40,Math.max(2,w*(1-q)),Math.max(2,102-q*80),'v');}c.put(55,70,w>16?'~ vast ~':'','l');}
 c.put(58,100,'o','y');c.put(46,100,'o','y');c.line(88,10,90,104,':','y');c.put(89,105,'(o)','y');
 if(s.dust>.3)for(let i=0;i<Math.round(s.dust*20);i++){const h2=hash('bd',i);c.put(14+h2%76,28+(h2>>>8)%100,'.','s');}
 if(s.whoosh>.1)for(let i=0;i<3;i++){c.put(2,40+i*20,'(((','l');c.put(96,40+i*20,')))','l');}
 return {entry:{x:52,y:134},contact:{x:52,y:110},lamp:{x:52,y:6},chain:{x:90,y:105},sign:{x:52,y:22},door:{x:40,y:106},handle:{x:58,y:100},panel_low:{x:30,y:118},base:{x:52,y:126}};
}
function dimdoor(c,p,s,v,t){
 const door=Math.max(clamp(s.door),clamp(v.door)),dim=Math.round(s.dimension)%5;
 c.solid(10,124,92,8,'t');c.put(14,126,'[_______________]','s');
 c.rect(26,10,60,116,'k');c.solid(27,11,58,114,'d');
 const scene=[['p','*','v'],['w','~','c'],['q','o','y'],['e','^','r'],['k','@','v']][dim];
 if(door>.05){for(let y=12;y<124;y++)for(let x=28;x<84;x++){const h2=hash('dim',dim,x,y);if(h2%7===0)c.put(x,y,scene[1],scene[h2%3?0:2]);}
  if(dim===4){c.ellipse(56,60,10,6,'O','f',true);c.ellipse(56,60,4,4,'@','k',true);}}
 const w=Math.round(58*(1-door*.82));c.solid(28,12,w,112,'b');c.rect(28,12,w,112,'k');
 if(w>20){c.rect(32,18,w-8,40,'s');c.rect(32,64,w-8,52,'s');c.put(28+w-8,94,'(o)','y');}
 for(const y of [30,76,110])c.put(26,y,'[=','y');
 if(s.draft>.1)for(let i=0;i<4;i++)c.put(88+i*3,40+i*16+Math.sin(t*4+i)*2,'~','l');
 return {entry:{x:56,y:130},contact:{x:56,y:110},knob:{x:74,y:96},hinge_top:{x:28,y:30},hinge_mid:{x:28,y:76},hinge_low:{x:28,y:110},sill:{x:56,y:124},back:{x:92,y:100}};
}
function teleporter(c,p,s,v,t){
 const beam=clamp(s.beam),charge=clamp(s.charge),lens=clamp(s.lens);
 c.ellipse(54,102,40,9,'=','t',true);c.ellipse(54,102,32,7,'o',charge>.3?'c':'s',false);c.ellipse(54,102,22,4,'+',charge>.3?'c':'s',false);
 c.beam(14,100,14,20,3,'t');c.beam(94,100,94,20,3,'t');for(let x=14;x<=94;x++)c.put(x,18-Math.round(Math.sin((x-14)/80*Math.PI)*8),'=','t');
 c.ellipse(54,16,8,4,'O',lens>.5?'c':'s',true);c.put(52,16,'(@)',lens>.5?'f':'s');
 if(lens<.5)for(let i=0;i<4;i++)c.put(48+i*3,15,'.','s');
 if(beam>.05)for(let y=20;y<100;y++){if(hash('bm',y,Math.floor(t*8))%10<beam*9){c.put(46,y,':',  'c');c.put(62,y,':','c');c.put(52+Math.sin(y/3+t*9)*5,y,'*','f');}}
 c.solid(100,60,14,40,'t');c.rect(100,60,14,40,'k');for(let j=0;j<3;j++)c.put(102,64+j*5,'[][][]'.slice(0,5),j===s.target?'g':'s');for(let i=0;i<5;i++)c.put(102+i*2,84,i<charge*5?'#':'.','g');
 if(v.pebble>.5)c.put(52,98,'o','t');
 return {entry:{x:54,y:114},contact:{x:54,y:100},keypad:{x:104,y:84},pad:{x:54,y:100},sensor:{x:24,y:104},lens:{x:54,y:18}};
}
function robot(c,p,s,v,t){
 const bow=clamp(s.bow),wave=clamp(s.wave),bat=clamp(s.battery),rust=clamp(s.rust),lean=Math.round(bow*6);
 c.ellipse(50,124,26,4,'O','k',true);for(let x=28;x<74;x+=6)c.put(x,124,'(@)','s');
 c.solid(30,60+lean,40,58,'t');c.rect(30,60+lean,40,58,'k');rivets(c,32,62+lean,36,6);
 for(let i=0;i<3;i++){c.put(40,74+lean+i*8,'(o)',i===0?'r':i===1?'y':'g');c.put(54,74+lean+i*8,'[=]','s');}
 for(let i=0;i<4;i++)c.put(36+i*7,108+lean,i<bat*4?'##':'..','g');
 c.ellipse(50+lean,30+lean,18,16,'(','t',true);c.ellipse(50+lean,30+lean,18,16,'o','k',false);
 c.solid(36+lean,28+lean,28,6,'d');c.put(40+lean,30+lean,bat>.15?'[ o    o ]':'[ -    - ]',bat>.15?'c':'s');
 if(bat>.15)c.put(46+lean,38+lean,'\\__/','k');
 c.line(50+lean,14+lean,50+lean,8,'|','k');c.put(48+lean,6,'(*)',bat>.15?'r':'s');
 for(let i=0;i<Math.round(s.shine*6);i++)c.put(38+lean+i*3,20+lean,'*','f');
 if(rust>.15)for(let i=0;i<Math.round(rust*16);i++){const h2=hash('rust',i);c.put(32+h2%36,62+(h2>>>8)%50,'%','o');}
 c.line(30,66+lean,16,86,'=','t');c.line(16,86,24,100,'=','t');c.put(20,100,'[_____]','y');
 const ax=70,ay=66+lean,hx=ax+12,hy=wave>.1?ay-24-Math.sin(t*10)*3*wave:ay+18;c.line(ax,ay,hx,hy,'=','t');c.put(hx-1,hy,'(W)','y');
 c.rect(8,64,6,10,'k');c.put(4,68,'<-O',bat>.5?'y':'s');
 return {entry:{x:50,y:130},contact:{x:60,y:90},key:{x:8,y:68},elbow:{x:76,y:70+lean},knee:{x:44,y:112},hand:{x:hx,y:hy},dome:{x:50+lean,y:16+lean}};
}
function cloner(c,p,s,v,t){
 const holo=clamp(s.hologram),bub=clamp(s.bubbles);
 for(const cx of [28,116]){c.ellipse(cx,32,14,5,'=','t',true);c.ellipse(cx,104,16,6,'=','t',true);c.line(cx-14,32,cx-14,104,'|','c');c.line(cx+14,32,cx+14,104,'|','c');for(let y=36;y<102;y+=4)c.put(cx-13,y,':','l');}
 if(s.sample>.5){c.line(28,60,30,80,'|','p');c.put(26,58,'\\\\//','p');}
 if(holo>.05){const rows=['   __','  (o >','  /  )','\\/  /',' \\__/','  ||'];for(const [j,r] of rows.entries())if(hash('holo',j,Math.floor(t*6))%10<holo*10)c.put(108,62+j*5,r,'g');}
 plate(c,54,60,36,46,'t');c.ellipse(72,40,8,6,'O','c',true);c.put(70,40,'(+)','f');
 c.line(42,70,54,70,'=','y');c.line(90,70,102,70,'=','y');c.rect(66,66,12,6,'k');c.put(68,68,'[GO]','r');
 tube(c,64,78,4,20,.6,'g');tube(c,76,78,4,20,.6,'g');if(bub>.05)for(let i=0;i<5;i++){c.put(65,96-((t*12+i*4)%18),'o','f');c.put(77,96-((t*12+i*5)%18),'o','f');}
 c.ellipse(72,100,4,2,'X','r',true);
 return {entry:{x:72,y:122},contact:{x:72,y:96},pod_a:{x:28,y:70},button:{x:72,y:68},tube:{x:66,y:84},valve:{x:72,y:100}};
}
function transmog(c,p,s,v,t){
 const smoke=clamp(s.smoke),jam=clamp(s.jam);
 for(let y=4;y<26;y++){const half=24-(y-4)*.7;c.solid(40-half,y,half*2,1,'t');c.put(40-half,y,'\\','k');c.put(40+half,y,'/','k');}
 if(s.hopper>.5)c.put(36,10,'v v','o');
 plate(c,18,26,92,78,'t');rivets(c,20,28,88,8);
 gear(c,44,50,9,t*(1+smoke*3),'y');gear(c,66,62,6,-t*(1.5+smoke*4),'o');gear(c,90,46,7,t*2,'y');
 c.ellipse(60,84,12,8,'O','c',true);c.ellipse(60,84,12,8,'o','k',false);c.put(54,84,smoke>.2?'~?!~':'(  )','v');
 c.ellipse(100,80,4,3,'@',jam>.3?'r':'g',true);c.rect(20,86,16,8,'k');c.solid(21,87,14,6,'b');c.put(24,90,'[==]','y');if(s.hopper>.5)c.put(26,88,'v','o');
 c.ellipse(8,70,5,4,'O','k',false);c.line(8,70,8+Math.cos(t*smoke*4)*5,70+Math.sin(t*smoke*4)*3,'=','y');
 c.line(110,96,128,112,'\\','k');c.line(110,104,124,118,'\\','k');
 const out=Math.round(s.output);const art=[null,['(*)',' |'],['__','(o>','(_)'],['|_|','|__\\'],['_','c(_)']][out];
 if(art)c.rows(art,118,112-art.length,'q');
 if(smoke>.05)for(let i=0;i<Math.round(smoke*10);i++)c.put(80+i*3,22-((t*8+i*3)%18),'o@.'[i%3],'p');
 if(jam>.3)c.put(56,104,'~crumple~','p');
 return {entry:{x:68,y:122},contact:{x:68,y:104},hopper:{x:40,y:8},drawer:{x:28,y:90},crank:{x:8,y:70},chute:{x:118,y:108},panel:{x:60,y:96}};
}
function printer(c,p,s,v,t){
 const stack=clamp(s.stack),jam=clamp(s.jam),turn=(v.crank||0)*TAU+(s.runs||0);
 plate(c,24,36,72,60,'k');c.solid(26,38,68,56,'t');rivets(c,26,40,66,7,'y');
 for(const y of [52,60]){c.ellipse(60,y,30,3,'=','s',true);c.line(32,y,88,y,'-','k');}
 c.rows(['_____','|===|','|___|'],10,30,'p',true);c.line(16,38,30,48,'\\','p');
 c.ellipse(104,60,12,10,'O','k',false);for(let i=0;i<6;i++){const a=turn+i*TAU/6;c.line(104,60,104+Math.cos(a)*11,60+Math.sin(a)*9,'-','y');}c.put(103,60,'@','r');
 mark(c,60,44,'DUCK BUCKS CO.','y');
 for(let i=0;i<Math.round(stack*10);i++)c.put(86,96-i,'[$Q$]','g');
 c.rect(80,97,22,4,'k');
 if(jam>.3)c.put(54,58,'~^~^~','p');
 c.beam(30,96,30,108,3,'k');c.beam(90,96,90,108,3,'k');
 return {entry:{x:60,y:110},contact:{x:60,y:96},tray:{x:16,y:38},crank:{x:104,y:60},rollers:{x:60,y:56},stack:{x:90,y:92}};
}
function perpetual(c,p,s,v,t){
 const a=s.angle*TAU+t*s.speed*2;
 c.beam(58,56,40,112,3,'b');c.beam(58,56,76,112,3,'b');c.line(30,112,86,112,'=','k');c.put(28,114,'[___________]','s');
 c.ellipse(58,52,36,24,'o','y',false);c.ellipse(58,52,34,22,'.','s',false);
 for(let i=0;i<10;i++){const q=a+i*TAU/10,x=58+Math.cos(q)*34,y=52+Math.sin(q)*22;c.line(58,52,x,y,'.','s');
  const out=Math.cos(q)>0?1:0,wx=x+Math.cos(q+out*.6)*5,wy=y+Math.sin(q+out*.6)*4;c.line(x,y,wx,wy,'-','t');c.ellipse(wx,wy,2,1.5,'@','r',true);}
 c.ellipse(58,52,4,3,'O','k',true);c.put(57,52,'+','f');
 if(s.squeak>.3)c.put(66,44+Math.sin(t*9)*2,'eek','p');
 mark(c,58,8,'TURNS '+String(Math.floor(s.turns)).slice(-6),'g');
 return {entry:{x:58,y:118},contact:{x:58,y:96},rim:{x:40,y:72},axle:{x:58,y:52},stand:{x:46,y:96}};
}
function dna(c,p,s,v,t){
 const spin=clamp(s.spin),ph=t*(1+spin*12);
 c.rect(44,6,28,84,'k');c.solid(45,7,26,82,'d');c.line(44,6,72,6,'=','t');c.line(44,89,72,89,'=','t');
 for(let y=10;y<86;y++){const q=y/6+ph,x1=58+Math.sin(q)*9,x2=58+Math.sin(q+Math.PI)*9;c.put(x1,y,'o',Math.cos(q)>0?'g':'s');c.put(x2,y,'o',Math.cos(q)>0?'s':'q');if(y%4===0)c.line(Math.min(x1,x2)+1,y,Math.max(x1,x2)-1,y,'-','l');}
 const vt=['s','q','g','c','y'];
 for(const [x,val] of [[20,s.vial_a],[96,s.vial_b]]){c.rect(x-6,80,12,16,'k');tube(c,x-3,74,6,18,.7,vt[Math.round(val)%5]);c.put(x-5,96,'[__]','t');}
 plate(c,38,92,40,24,'t');c.rect(48,94,20,4,'k');c.put(50,95,'~~~~~~~~','p');if(s.printout>.5)for(let j=0;j<4;j++)c.put(52,98+j*2,'|'+'ATCG'[j].repeat(6)+'|','p');
 c.rect(54,104,8,4,'k');c.put(56,105,spin>.1?'ON':'--','g');
 return {entry:{x:58,y:122},contact:{x:58,y:110},vial_a:{x:20,y:84},vial_b:{x:96,y:84},switch:{x:58,y:106},slot:{x:58,y:96}};
}
function ray(c,p,s,v,t,item){
 const glow=clamp(s.glow),grow=item.id==='growth_ray',target=s.target;
 c.line(30,92,30,62,'|','k');c.line(30,62,16,92,'/','k');c.line(30,62,44,92,'\\','k');
 c.solid(10,44,46,14,'t');c.rect(10,44,46,14,'k');c.rows(['==<>==<>=='],12,48,grow?'g':'v');
 c.ellipse(60,51,6,6,'O',grow?'g':'v',true);c.line(64,51,72,51,'=','t');c.put(72,49,'<<',grow?'g':'v');
 dial(c,36,38,5,s.dial);c.rect(16,58,8,8,'k');c.put(18,61,'[]','y');c.put(26,56,'U','r');
 for(let i=0;i<5;i++)c.put(14+i*3,42,i<s.charge*5?'#':'.',grow?'g':'v');
 if(glow>.05)for(let x=76;x<92;x++)if(hash('beam',x,Math.floor(t*10))%10<glow*10)c.put(x,51+Math.sin(x/2+t*20)*1.5,'~',grow?'g':'v');
 c.line(96,92,96,84,'|','k');c.ellipse(96,84,10,2,'=','t',true);
 if(grow){const h=Math.round(4+(target-1)*12);c.line(96,82,96,82-h,'|','h');c.ellipse(96,80-h,3+h*.25,2+h*.2,'*','y',true);c.put(95,80-h,'@','o');}
 else{const r=Math.max(.6,target*3);c.ellipse(96,81,r,r*.6,'o','t',true);}
 return {entry:{x:56,y:94},contact:{x:56,y:80},pump:{x:20,y:60},dial:{x:36,y:38},trigger:{x:26,y:56},plate:{x:96,y:82}};
}
function lamp(c,p,s,v,t){
 const smoke=clamp(s.smoke),pol=clamp(s.polish);
 c.ellipse(50,76,30,5,'~','q',true);c.ellipse(50,76,30,5,'.','r',false);c.put(22,80,'(_________________)','r');
 texture(c,28,50,72,70,inEllipse(50,60,22,10),(x,y)=>[(x+y)%4===0?'/':y===60?'=':' ','a','y']);c.ellipse(50,60,22,10,'o','b',false);c.rows(['  _/=\\_','  \\___/'],43,46,'y',true);c.put(48,44,'(*)','a');
 for(let i=0;i<=16;i++){const q=i/16;c.put(70+q*20,58-q*12-Math.sin(q*3)*2,'=','y');}c.put(89,45,'o','b');
 for(let j=0;j<10;j++){const a=Math.PI/2+j/10*Math.PI;c.put(28+Math.cos(a)*6,60+Math.sin(a)*6,'(','y');}
 for(let i=0;i<Math.round(pol*10);i++){const h2=hash('lp',i);c.put(34+h2%32,54+(h2>>>8)%10,'*','f');}
 if(smoke>.05){for(let i=0;i<Math.round(smoke*24);i++){const q=i/24,x=90+Math.sin(q*9+t*2)*6-q*30,y=44-q*40;c.put(x,y,'@o.'[i%3],'v');}
  if(smoke>.5)c.rows(['  .--.',' ( ^^ )','  \\__/'],50,4,'l');}
 return {entry:{x:50,y:82},contact:{x:50,y:66},belly:{x:50,y:62},spout:{x:86,y:48}};
}
function cloak(c,p,s,v,t){
 const fold=clamp(s.folded),sh=clamp(s.shimmer),hid=clamp(v.cloak);
 c.beam(50,14,50,112,3,'b');c.line(32,114,68,114,'=','k');c.put(34,116,'/____\\  /____\\','b');c.rows(['_/~~~\\_'],46,10,'y');
 if(hid>.5){c.put(44,60,'(bare)','s');return {entry:{x:50,y:118},contact:{x:50,y:96},hem:{x:50,y:98},mid:{x:50,y:80},shoulder:{x:50,y:28},hook:{x:50,y:10}};}
 if(fold>.5){c.solid(36,48,28,10,'l');c.rect(36,48,28,10,'v');for(let y=50;y<57;y+=2)c.line(38,y,62,y,'~','c');}
 else for(let y=20;y<100;y++){const q=(y-20)/80,half=10+q*20+Math.sin(t*2+y/7)*1.5*sh;
  for(let x=50-half;x<50+half;x++){const h2=hash('ck',Math.round(x),y,Math.floor(t*3));if(h2%10<2+sh*4)c.put(x,y,'.:~'[h2%3],h2%4?'c':'l');}
  c.put(50-half,y,':','l');c.put(50+half,y,':','l');}
 return {entry:{x:50,y:118},contact:{x:50,y:96},hem:{x:50,y:98},mid:{x:50,y:80},shoulder:{x:50,y:28},hook:{x:50,y:10}};
}
function dreamcatcher(c,p,s,v,t){
 const sway=Math.sin(s.sway*TAU+t)*2,dreams=clamp(s.dreams),tangle=clamp(s.tangle);
 c.beam(48,8,48,128,3,'b');c.line(30,128,66,128,'=','k');c.line(48,8,62,8,'=','b');c.line(62,8,62+sway*.3,52,'|','p');
 const cx=62+sway,cy=72;
 c.ellipse(cx,cy,18,12,'o','b',false);c.ellipse(cx,cy,17,11,'-','q',false);
 for(let i=0;i<12;i++){const a=i*TAU/12;c.line(cx+Math.cos(a)*16,cy+Math.sin(a)*10.5,cx+Math.cos(a+2.4)*8,cy+Math.sin(a+2.4)*5,'.',tangle>.3&&i%3===0?'s':'p');}
 c.ellipse(cx,cy,7,4.5,'.','p',false);c.put(cx-1,cy,'(o)','y');
 if(tangle>.3)for(let i=0;i<Math.round(tangle*12);i++){const h2=hash('tg',i);c.put(cx-12+h2%24,cy-10+(h2>>>8)%20,'%','s');}
 for(let i=0;i<Math.round(dreams*14);i++){const h2=hash('dr',i),a=(h2%628)/100,r=4+(h2>>>8)%12;c.put(cx+Math.cos(a)*r,cy+Math.sin(a)*r*.65,Math.sin(t*3+i)>0?'*':'+','v');}
 const n=Math.round(s.feathers);for(let i=0;i<n;i++){const x=cx-10+i*(20/(n-1||1)),len=14+(i%2)*6,sw=Math.sin(t*1.5+i)*1.5;c.line(x,cy+12,x+sw,cy+12+len,'|','p');c.rows(['/|\\','\\|/','\\|/'],x+sw-1,cy+12+len,i===n-1&&n>3?'y':'p');c.put(x,cy+16,'o','q');}
 return {entry:{x:48,y:130},contact:{x:52,y:90},web:{x:cx-6,y:cy},web_r:{x:cx+8,y:cy},tassel:{x:cx,y:cy+24},hoop:{x:cx,y:cy-12}};
}
function dragonegg(c,p,s,v,t){
 const wob=clamp(s.wobble),inc=clamp(s.incubation),warm=clamp(s.warmth),emb=clamp(s.embers),tilt=Math.sin(t*9)*wob*2;
 c.ellipse(56,92,46,7,'#','t',true);for(let i=0;i<22;i++){const a=i/22*Math.PI;c.ellipse(56-Math.cos(a)*42,90+Math.sin(a)*3,4,1.6,'@','s',true);}
 for(let i=0;i<14;i++){const h=hash('em',i);c.put(20+h%72,88+(h>>>8)%5,emb>.3?'*':'.',emb>.3?(h%2?'e':'o'):'s');}
 if(warm>.3)for(let i=0;i<5;i++)c.put(36+i*10,40-((t*4+i*3)%8),'~','e');
 const cx=56+tilt,cy=60,egg=(x,y)=>{const dy=(y-cy)/(y<cy?26:22);return ((x-cx)/(y<cy?15:18))**2+dy*dy<=1;};
 texture(c,cx-19,cy-27,cx+19,cy+23,egg,(x,y)=>{
  const h=hash('scale',Math.round(x-tilt),y),edge=!egg(x-1,y)||!egg(x+1,y)||!egg(x,y-1)||!egg(x,y+1);
  if(edge)return ['.','k','r'];
  const row=y%3,scale=(Math.round(x-tilt)+(row===1?1:0))%3;
  return [scale===0?'v':row===0?'^':' ',h%9<s.shine*9?'f':(y<cy-8?'o':'r'),'r'];
 });
 if(warm>.4)for(let i=0;i<8;i++){const a=i/8*TAU;c.put(cx+Math.cos(a)*20,cy+Math.sin(a)*25,'.','e');}
 if(inc>.6){c.line(cx-6,cy-12,cx+2,cy-4,'/','k');c.line(cx+2,cy-4,cx-3,cy+4,'\\','k');}
 if(inc>.85){c.line(cx+6,cy-2,cx+11,cy+5,'\\','k');}
 if(inc>=.99){c.solid(cx-3,cy-8,6,3,'d');c.put(cx-2,cy-7,'(@)','y');c.put(cx-1,cy-5,'^^','f');}
 return {entry:{x:56,y:102},contact:{x:56,y:84},shell:{x:72,y:56},embers:{x:30,y:88}};
}

// Merge per-cell fills into horizontal runs. Later fills paint over earlier ones,
// so a run only absorbs the cell immediately to its right when nothing drawn in
// between could be covered differently: identical pixels, far fewer rectangles.
function mergeFills(fills){
 const grid=new Map();
 for(const f of fills)for(let x=f.x;x<f.x+f.w;x++)grid.set(f.y*4096+x,f.tone+(f.opaque?'!':''));
 const rows=new Map();
 for(const [k,tone] of grid){const y=Math.floor(k/4096),x=k-y*4096;if(!rows.has(y))rows.set(y,[]);rows.get(y).push([x,tone]);}
 const out=[];
 for(const [y,cells] of [...rows].sort((a,b)=>a[0]-b[0])){
  cells.sort((a,b)=>a[0]-b[0]);let run=null;
  for(const [x,tone] of cells){
   if(run&&run.x+run.w===x&&run.key===tone){run.w++;continue;}
   if(run)out.push({x:run.x,y,w:run.w,tone:run.tone,opaque:run.opaque});
   run={x,w:1,key:tone,tone:tone.replace('!',''),opaque:tone.endsWith('!')};
  }
  if(run)out.push({x:run.x,y,w:run.w,tone:run.tone,opaque:run.opaque});
 }
 return out;
}
const BUILDERS={topiary,zen,ice,sandcastle,gong,aurora,rainbow,weather,portal,wormhole,blackhole,volcano,tornado,antigravity,forcefield,arch,timemachine,booth,dimdoor,teleporter,robot,cloner,transmog,printer,perpetual,dna,ray,lamp,cloak,dreamcatcher,dragonegg};
const INKS={b:'#c9a071',a:'#e8c27a',f:'#f6f0d8',s:'#93a39e',k:'#5f6f6a',p:'#e9e3cc',d:'#2c3440',g:'#9ef0a8',q:'#f0a4bc',w:'#8fd7ea',l:'#c4b4f0',e:'#ffb347',y:'#e8c46a',v:'#b58cf2',c:'#8ce9f0',h:'#6fb36a',i:'#cdeff6',m:'#8fb86a',n:'#e6cf9a',o:'#e8955a',r:'#e86f6f',t:'#a7b4b8',u:'#6f9fe0'};
const PANELS={b:'#4a3a2a',a:'#5a4528',f:'#5e5a4a',s:'#2c3834',k:'#141c1c',p:'#5a5648',d:'#0c1018',g:'#1e4a2a',q:'#5a2a3a',w:'#1e4a5a',l:'#3a3256',e:'#5a3216',y:'#5a4a22',v:'#3a2456',c:'#1a4a50',h:'#1f3f20',i:'#3a5a64',m:'#2a3a1e',n:'#6a5a3a',o:'#5a3220',r:'#5a2020',t:'#36403f',u:'#1c3260'};
// Construction is memoized on everything it reads, and motion is stepped at 6 fps
// (like the legacy item phases), so an unchanged frame reuses its sprite and the
// painter's raster cache; a busy garden of wonders stays inside the frame budget.
const MEMO=new Map();
export function wonderSprite(base,item,time,{state={},pose={},motion=true}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const s={};for(const [k,[d,lo,hi]] of Object.entries(p.fields))s[k]=clamp(Number(state.wonder?.[k]??d),lo,hi);
 // Each wonder steps on its own phase so their rebuilds spread across frames.
 // Idle motion steps at 3 fps like legacy items; the wonder being worked steps at 6.
 const v={...(pose.wonder?.object||{})},fps=pose.wonder?6:3,offset=(hash(item.id)%97)/97,t=motion?(Math.floor(time*fps+offset)-offset)/fps:0;
 const key=item.id+'|'+t+'|'+JSON.stringify(s)+'|'+JSON.stringify(v)+'|'+(state.dirt>.35?1:0);
 let built=MEMO.get(key);
 if(built){MEMO.delete(key);MEMO.set(key,built);}
 else{built=construct(p,item,s,v,t,state);MEMO.set(key,built);if(MEMO.size>256)MEMO.delete(MEMO.keys().next().value);}
 return {...base,...built,anchors:built.anchors};
}
function construct(p,item,s,v,t,state){
 const c=new ObjectCanvas(p.w,p.h);
 shadow(c,p);
 const anchors=BUILDERS[p.type](c,p,s,v,t,item);
 if(state.dirt>.35)for(const x of [p.w*.3,p.w*.5,p.w*.7])c.put(x,p.h-6,'.:','s');
 const glows=['aurora','portal','wormhole','blackhole','volcano','forcefield','arch','teleporter','cloner','timemachine','dreamcatcher','dragonegg'].includes(p.type);
 const fin=c.finish();fin.fills=mergeFills(fin.fills);
 return {...fin,construction:'wonder-v1',detail:true,detailScale:.62,blueprint:item.id,anchors,inks:INKS,panels:PANELS,sway:0,lift:0,
  animated:true,emissive:glows&&(s.glow>.2||s.energy>.2||s.starlight>.3||s.eruption>.1||s.shield>.5||s.beam>.1||s.hologram>.2||s.flux>.1||s.dreams>.3||s.warmth>.5||s.aperture>.3||s.mass>0)};
}
