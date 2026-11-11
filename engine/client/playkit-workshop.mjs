import {ObjectCanvas} from './object-canvas.mjs';
import BLUEPRINTS from './animation/playkit.json' with {type:'json'};
export {BLUEPRINTS as PLAYKIT_BLUEPRINTS};
const clamp=(n,a=0,b=1)=>Math.max(a,Math.min(b,n||0));
function poly(c,points,tone){
 const ys=points.map(p=>p[1]);for(let y=Math.ceil(Math.min(...ys));y<=Math.floor(Math.max(...ys));y++){
  const cuts=[];for(let i=0;i<points.length;i++){const a=points[i],b=points[(i+1)%points.length];if(a[1]!==b[1]&&y>=Math.min(a[1],b[1])&&y<Math.max(a[1],b[1]))cuts.push(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]));}
  cuts.sort((a,b)=>a-b);for(let i=0;i+1<cuts.length;i+=2)c.solid(Math.ceil(cuts[i]),y,Math.max(1,Math.floor(cuts[i+1])-Math.ceil(cuts[i])+1),1,tone);
 }for(let i=0;i<points.length;i++)c.line(...points[i],...points[(i+1)%points.length],null,'f');
}
function disc(c,p,v){
 const cx=28+v.travel*83,ry=7+Math.abs(v.tilt)*7,cy=p.h-4-ry-v.lift*36;
 c.ellipse(cx,cy,24,ry,'_','q',true);c.ellipse(cx,cy,20,Math.max(2,ry-2),'_','f');c.ellipse(cx,cy,15,Math.max(1,ry-4),'-','a');
 for(let i=0;i<12;i++){const a=i*Math.PI/6+v.turn;c.put(cx+Math.cos(a)*18,cy+Math.sin(a)*Math.max(2,ry-2),i%2?'|':':','s');}
 for(let yy=-4;yy<=4;yy+=2)for(let xx=-17;xx<=17;xx+=4)if(Math.abs(xx)>9||Math.abs(yy)>2)c.put(cx+xx,cy+yy,yy<0?':':'.','s');
 c.put(cx-8,cy,'P O N D / A I R','p');c.put(cx-3,cy+2,'(o)>','a');
 c.line(cx-17,cy+ry+1,cx+17,cy+ry+1,'_','k');
 return {entry:{x:15,y:p.h-3},contact:{x:cx-21,y:cy+1},center:{x:cx,y:cy},partner:{x:cx+21,y:cy+1}};
}
function rope(c,p,v){
 const y=p.h-16,coil=clamp(v.coil),cx=72,rx=52*(1-coil)+21*coil,ry=10+coil*3;
 for(let j=0;j<(coil>.65?4:2);j++){
  let last=null;for(let i=0;i<=150;i++){const a=i/150*Math.PI*2,x=cx+Math.cos(a)*(rx-j*4),yy=y+Math.sin(a)*(ry-j*2)+(coil<.65?Math.sin(a*2)*3:0);
   if(last)c.line(...last,x,yy,i%4<2?'/':'\\',i%4<2?'a':'b');last=[x,yy];}
 }
 for(const [x,angle]of [[cx-rx-10,-.15],[cx+rx+1,.15]]){c.line(x+5,y,x+5,y+8,':','a');c.rect(x,y+5,10,6,'b',true);for(let j=2;j<9;j+=2)c.line(x+j,y+6,x+j+angle*5,y+10,'|','a');c.put(x+3,y+8,'o','k');}
 c.put(48,p.h-2,'//  / /  //  / /  //','s');
 return {entry:{x:20,y:p.h-3},contact:{x:cx-rx-7,y:y+8},deck:{x:cx,y:p.h-5},partner:{x:cx+rx+6,y:y+8}};
}
function yoyo(c,p,v){
 const cx=37+v.travel*45,cy=p.h-30+v.drop*14;
 c.ellipse(cx+4,cy,15,12,'_','k',true);c.ellipse(cx,cy,15,12,'_','b',true);c.ellipse(cx-1,cy,11,9,':','a');c.ellipse(cx-1,cy,7,6,'o','q',true);for(let yy=-8;yy<=8;yy+=3)c.line(cx-9,cy+yy,cx+9,cy+yy,':','s');
 for(let i=0;i<8;i++){const a=i*Math.PI/4+v.turn;c.line(cx,cy,cx+Math.cos(a)*10,cy+Math.sin(a)*8,null,i%2?'a':'s');}
 c.ellipse(cx,cy,3,2,'o','k',true);c.put(cx-1,cy,'(+)','f');c.put(cx-5,cy-7,'DUCK','p');c.put(cx-4,cy+8,'WALK','p');
 if(!v.active){c.line(cx,cy-12,cx-8,cy-27,':','p');c.ellipse(cx-8,cy-29,5,3,'o','p');}
 return {entry:{x:12,y:p.h-3},contact:{x:cx,y:cy-12},axle:{x:cx+3,y:cy},center:{x:cx,y:cy}};
}
function bubble(c,x,y,size){const rx=3+size*2,ry=2+size*1.7;c.ellipse(x,y,rx,ry,'_','w');c.put(x-rx+2,y-ry+2,'/','p');c.put(x+rx-2,y+ry-1,"'",'q');}
function particles(c,p,s,x,y){for(const b of s.bubbles||[]){const age=clamp(b.age,0,8),xx=x+age*(4+b.lane*.5),yy=y-age*(4.5-b.lane*.3);if(xx<p.w-8&&yy>8)bubble(c,xx,yy,b.size);}}
function bubbler(c,p,v,s){
 const H=p.h,x=18,y=H-62,w=69;
 for(const xx of [x+4,x+w-15]){c.rect(xx,H-12,13,8,'k',true);c.line(xx+1,H-5,xx+11,H-5,'=','s');}
 c.rect(x,y,w,51,'g',true);for(let yy=y+4;yy<y+47;yy+=6)c.line(x+4,yy,x+w-5,yy,':','s');for(let xx=x+4;xx<x+w-2;xx+=9){c.put(xx,y+2,'o','a');c.put(xx,y+48,'o','a');}c.line(x+34,y+9,x+34,y+31,'|','a');c.put(x+26,y+34,'SOAP / AIR / WONDER','f');
 c.rect(x+6,y+6,26,27,'k',true);for(let xx=x+9;xx<x+31;xx+=4)c.line(xx,y+8,xx,y+30,'|','a');
 c.rect(x+6,y+43,16,9,'a',true);c.put(x+9,y+47,v.power>.5?'[I]':'[O]','k');c.put(x+28,y+39,'BUBBLE / CO.','p');c.put(x+30,y+44,'NO. 08','f');
 const cx=x+50,cy=y+18;c.ellipse(cx,cy,18,17,'o','a',true);c.ellipse(cx,cy,14,13,':','k',true);
 for(let i=0;i<6;i++){const a=i*Math.PI/3+s.phase;c.ellipse(cx+Math.cos(a)*9,cy+Math.sin(a)*8,4,3,'o','w');}c.put(cx-1,cy,'(+)','f');
 c.rect(x+24,y-8,35,7,'b',true);c.line(x+27,y-6,x+55,y-6,'~','w');c.line(x+5,y-1,x+5,y-8,'|','a');c.line(x+5,y-8,x+18,y-8,'_','a');c.line(x+18,y-8,x+18,y-1,'|','a');
 for(const [xx,yy]of [[x+2,y+2],[x+w-4,y+2],[x+2,y+48],[x+w-4,y+48]])c.put(xx,yy,'+','f');c.line(x+14,y+50,x+14,H-8,':','a');c.rect(x+6,H-9,18,6,'a',true);c.put(x+11,H-6,v.power>.5?'[I]':'[O]','k');particles(c,p,s,cx+12,cy-6);
 return {entry:{x:x,y:H-3},contact:{x:x+14,y:H-6},mouth:{x:cx,y:cy},partner:{x:x+w-6,y:H-12}};
}
function wand(c,p,v,s){
 const H=p.h,cx=29,cy=H-22;c.ellipse(cx,cy+10,17,5,'_','g',true);c.rect(cx-17,cy-13,35,24,'g',true);c.ellipse(cx,cy-13,17,5,'_','w',true);c.ellipse(cx,cy-13,12,3,'_','k',true);
 for(const x of [cx-12,cx+12])c.line(x,cy-8,x,cy+5,':','p');c.rect(cx-12,cy-5,25,12,'p',true);c.put(cx-9,cy,'POND / SOAP','d');c.put(cx-6,cy+4,'~ (o)> ~','d');
 if(v.held<.05){const x=49-v.dip*20,y=H-52+v.dip*26;c.line(x,y+8,cx+4,H-10,'/','a');c.ellipse(x,y,10,8,'o','a');c.ellipse(x,y,7,5,':','w');if(v.dip<.2)c.line(x-4,y-2,x+5,y+2,'~','q');}
 if(!v.active)particles(c,p,s,52,H-56);return {entry:{x:11,y:H-3},contact:{x:cx+4,y:H-10},mouth:{x:52,y:H-56}};
}
function pinwheel(c,p,v,s){
 const H=p.h,cx=55,cy=H-65,angle=s.phase+v.turn;c.beam(cx,cy+7,cx,H-5,5,'b');c.line(cx-1,cy+17,cx-1,H-8,':','a');c.ellipse(cx,H-6,14,3,'_','k');
 for(let i=0;i<4;i++){const a=angle+i*Math.PI/2,pt=(u,w)=>[cx+Math.cos(a)*u-Math.sin(a)*w,cy+Math.sin(a)*u+Math.cos(a)*w];poly(c,[pt(0,0),pt(26,-20),pt(26,12),pt(8,3)],['q','w','a','g'][i]);c.line(...pt(2,0),...pt(25,11),':','p');for(let k=1;k<5;k++)c.put(...pt(12+k*2,-6+k),'+',i%2?'a':'p');}
 c.ellipse(cx,cy,5,4,'o','k',true);c.put(cx-1,cy,'(+)','a');c.put(cx-12,H-17,'TWIRL / NO. 4','p');c.line(cx+5,cy+4,cx+5,H-11,':','p');c.put(cx+1,H-10,'[====]','a');
 return {entry:{x:30,y:H-3},contact:{x:cx+4,y:H-10},hub:{x:cx,y:cy}};
}
function boat(c,p,v){
 const H=p.h,cx=41+v.travel*65,cy=H-11,tilt=v.tilt*3;poly(c,[[cx-34,cy-9],[cx+34,cy-9+tilt],[cx+25,cy+8],[cx-23,cy+8]],'b');
 for(let n=0;n<4;n++){const y=cy-6+n*4;c.line(cx-30+n*2,y,cx+31-n*2,y,'_','a');for(let xx=cx-24;xx<cx+25;xx+=12)c.put(xx,y-1,'o','k');}
 c.ellipse(cx,cy-10,33,6,'_','a',true);c.ellipse(cx,cy-10,27,3,'_','k',true);c.line(cx-2,cy-13,cx-2,cy-61,'|','a');c.line(cx-4,cy-13,cx-4,cy-61,'|','b');
 const sail=clamp(v.sail),width=8+sail*24;poly(c,[[cx-1,cy-59],[cx+width,cy-18],[cx-1,cy-18]],'p');for(let y=cy-52;y<cy-19;y+=6)c.line(cx+1,y,cx+Math.max(1,(y-(cy-59))/41*width-2),y,':','s');
 c.put(cx+3,cy-29,'/o>','q');c.line(cx-3,cy-16,cx+width+3,cy-16,'_','b');c.line(cx-3,cy-55,cx-28,cy-10,':','p');c.line(cx-3,cy-55,cx+29,cy-10,':','p');
 c.put(cx-15,cy+2,'S.S. CRUMB','p');c.ellipse(cx+19,cy,3,2,'o','w');c.put(cx-22,cy-11,'[==]','b');c.line(cx-3,cy-55,cx-24,H-14,':','p');c.put(cx-27,H-14,'[===]','a');c.line(cx+23,H-14,cx+23,H-11,':','p');c.put(cx+20,H-11,'[===]','a');
 return {entry:{x:15,y:H-3},contact:{x:cx-22,y:H-12},rigging:{x:cx-24,y:H-14},deck:{x:cx,y:cy-10},partner:{x:cx+23,y:H-11}};
}
function board(c,p,v,s){
 const H=p.h,cx=p.w/2,cy=H-20,ry=12,rx=73;c.ellipse(cx,cy+3,rx,ry,'_','k',true);c.ellipse(cx,cy,rx,ry,'_','q',true);c.ellipse(cx,cy,rx-4,ry-3,'_','a');
 c.line(cx-rx+6,cy,cx+rx-6,cy,'=','b');c.line(cx-rx+11,cy-2,cx+rx-11,cy-2,':','f');
 for(let i=-54;i<=54;i+=9){const bend=9*Math.sqrt(1-(i/73)**2);c.line(cx+i,cy-bend,cx+i+7,cy+bend,'/','w');}
 c.ellipse(cx+24,cy,15,7,'_','p',true);c.rows(['  __',' (o)>',' /_)',' ~~~'],cx+19,cy-3,'d');c.put(cx-48,cy+1,'POND RIDER','p');c.put(cx-43,cy+5,'EST. / JUST NOW','p');
 for(let n=0;n<Math.min(24,s.waxes*6);n++)c.put(cx-16+(n*7%50),cy-5+(n*3%10),':','f');c.ellipse(cx-rx+7,cy,3,2,'o','k');c.line(cx-rx+7,cy,cx-rx+2,cy+15,':','p');c.ellipse(cx-rx+6,cy+15,5,2,'_','p');
 return {entry:{x:cx-rx,y:H-3},contact:{x:cx-20+v.walk*40,y:H-10},deck:{x:cx-rx+17+v.walk*110,y:cy-4},partner:{x:cx+50,y:H-10}};
}
const BUILDERS={disc,rope,yoyo,bubbler,wand,pinwheel,boat,board};
export function playkitSprite(base,item,time,{state={},pose={}}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;const s={phase:0,speed:0,bubbles:[],waxes:0,...state.playkit},v={travel:0,lift:0,turn:0,coil:0,power:0,dip:0,blow:0,walk:0,tilt:0,jump:0,drop:1,held:0,wide:0,sail:0,...s,...pose.playkit,active:Boolean(pose.playkit)};
 const c=new ObjectCanvas(p.w,p.h),anchors=BUILDERS[p.type](c,p,v,s);
 // Wear and damp marks remain on the actual material, not in its animation reserve.
 const cells=[];for(let y=0;y<p.h;y++)for(let x=0;x<p.w;x++)if(c.art[y][x]!==' ')cells.push([x,y]);
 for(const [amount,glyph,tone,stride]of [[state.wetness||0,"'",'w',37],[state.dirt||0,'.','s',53],[1-(state.condition??1),'/', 'k',71]])if(amount>.2)for(let n=0;n<Math.ceil(amount*18);n++){const at=cells[(n*stride+19)%cells.length];if(at)c.put(...at,glyph,tone);}
 const inks={b:'#cfa575',a:'#ebc978',f:'#f4dfae',s:'#859b91',k:'#526b65',p:'#e9dfbd',d:'#344b46',g:'#91cbb5',w:'#8ed5dc',q:'#edaca2'};
 const panels={b:'#57422f',a:'#695539',f:'#8b7552',s:'#3e5249',k:'#15392e',p:'#c6b68e',d:'#26483b',g:'#2e6557',w:'#2b6473',q:'#84493d'};
 return {...base,...c.finish(),construction:'playkit-v1',detail:true,detailScale:.62,blueprint:item.id,anchors,inks,panels,playkitState:s,sway:0,lift:0,animated:Boolean(pose.playkit)||s.speed>0||s.power>.5||s.bubbles.length>0,emissive:false};
}
