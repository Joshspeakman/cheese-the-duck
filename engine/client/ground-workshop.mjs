import BLUEPRINTS from './animation/groundworks.json' with {type:'json'};
import {ObjectCanvas} from './object-canvas.mjs';
export {BLUEPRINTS as GROUND_BLUEPRINTS};
const clamp=n=>Math.max(0,Math.min(1,Number.isFinite(n)?n:0));
// A shallow trapezoid, with room for an exposed foundation and near-edge feet.
export function groundPoint(p,u,v){return {x:p.w*(.14+.72*u)+(u-.5)*p.w*.18*v,y:12+v*(p.h-30)};}
function polygon(c,vertices,tone,edge='k'){
 const ys=vertices.map(p=>p.y);
 for(let y=Math.ceil(Math.min(...ys));y<=Math.floor(Math.max(...ys));y++){
  const hits=[];for(let i=0;i<vertices.length;i++){const a=vertices[i],b=vertices[(i+1)%vertices.length];if((a.y<=y&&b.y>y)||(b.y<=y&&a.y>y))hits.push(a.x+(b.x-a.x)*(y-a.y)/(b.y-a.y));}
  hits.sort((a,b)=>a-b);for(let i=0;i+1<hits.length;i+=2){const x=Math.ceil(hits[i]),w=Math.floor(hits[i+1])-x+1;if(w>0)c.solid(x,y,w,1,tone);}
 }
 vertices.forEach((a,i)=>{const b=vertices[(i+1)%vertices.length];c.line(a.x,a.y,b.x,b.y,null,edge);});
}
function panel(c,p,u,v,w,h,tone,edge='k'){
 const ps=[[u,v],[u+w,v],[u+w,v+h],[u,v+h]].map(([x,y])=>groundPoint(p,x,y));polygon(c,ps,tone,edge);return ps;
}
function mark(c,p,u,v,text,tone){const q=groundPoint(p,u,v);c.put(q.x,q.y,text,tone);}
function curve(c,points,tone='f',glyph=null){for(let i=1;i<points.length;i++)c.line(points[i-1].x,points[i-1].y,points[i].x,points[i].y,glyph,tone);}
function route(c,p,points,tone='f',glyph=null){curve(c,points.map(([u,v])=>groundPoint(p,u,v)),tone,glyph);}
function foundation(c,p,tone='b'){
 panel(c,p,0,0,1,1,tone,'f');
 const a=groundPoint(p,0,1),b=groundPoint(p,1,1);
 polygon(c,[a,b,{x:b.x-2,y:b.y+5},{x:a.x+2,y:a.y+5}],'s');
 c.line(a.x+2,a.y+3,b.x-2,b.y+3,':','k');
}
function stone(c,p,u,v,ru,rv,index){
 const shapes=[[[-1,-.2],[-.7,-.85],[.25,-1],[.9,-.5],[1,.45],[.3,1],[-.65,.7]],[[-.9,-.5],[-.4,-1],[.5,-.8],[1,-.1],[.8,.7],[-.2,1],[-.8,.5]],[[-1,-.4],[-.5,-.9],[.7,-.7],[.9,.3],[.45,.8],[-.65,.9]]];
 const ps=shapes[index%3].map(([x,y])=>groundPoint(p,u+x*ru,v+y*rv));
 polygon(c,ps.map(a=>({x:a.x,y:a.y+3})),'s');polygon(c,ps,index%3?'b':'a','f');
 const q=groundPoint(p,u,v);c.put(q.x-3,q.y,'.. :','s').put(q.x-2,q.y-2,'--','f');
 if(ru>.07){
  route(c,p,[[u-ru*.65,v+rv*.2],[u-ru*.3,v+rv*.42],[u+ru*.5,v+rv*.33]],'s','~');
  route(c,p,[[u-ru*.5,v-rv*.55],[u,v-rv*.35],[u+ru*.7,v-rv*.4]],'a','-');
  route(c,p,[[u+ru*.4,v-rv*.6],[u+ru*.24,v],[u+ru*.47,v+rv*.47]],'s');
 }
 if(index%3===0)c.put(q.x+4,q.y+2,',;','l');
}
function masonry(c,p){
 if(['stepping','winding'].includes(p.style)){
  const uv=p.style==='stepping'?[[.22,.67],[.4,.5],[.6,.62],[.78,.4]]:[[.13,.67],[.31,.47],[.5,.57],[.69,.39],[.87,.55]];
  uv.forEach(([u,v],i)=>stone(c,p,u,v,.105,.14,i));return;
 }
 foundation(c,p,'s');
 if(p.style==='pebbles'){
  // Woven bands of river pebbles, separated by a hand-set darker border.
  for(let row=0;row<8;row++)for(let col=0;col<15;col++){
   const u=.035+col*.062+(row%2)*.018,v=.055+row*.122,q=groundPoint(p,u,v);
   const tone=col===0||col===14?'s':(row+col)%3?'b':'a';
   c.ellipse(q.x,q.y,3,1.6,'~',tone,true);c.put(q.x-1,q.y-1,'-','f').put(q.x,q.y+1,':','k');
  }return;
 }
 for(let row=0;row<5;row++)for(let col=0;col<8;col++){
  const u=.065+col*.123+(row%2)*.028,v=.11+row*.19;
  if(u<.95)stone(c,p,u,v,.05,.075,row*8+col);
 }
}
function tiles(c,p){
 foundation(c,p);const cols=p.style==='mosaic'?20:p.style==='slate'?4:5,rows=p.style==='mosaic'?13:4;
 for(let r=0;r<rows;r++)for(let k=0;k<cols;k++){
  const u=(k+.035)/cols,v=(r+.035)/rows,w=.93/cols,h=.93/rows;
  const tone=p.style==='checker'?((k+r)%2?'k':'f'):p.style==='mosaic'?['a','w','b','s','b'][(k+r*2)%5]:((k+r)%3?'b':'a');
  panel(c,p,u,v,w,h,tone,p.style==='checker'?'s':'f');
  if(p.style==='slate'){
   for(let i=0;i<4;i++)route(c,p,[[u+.015,v+h*(.15+i*.18)],[u+w*.35,v+h*(.19+i*.18)],[u+w*.86,v+h*(.16+i*.18)]],i%2?'a':'s',i%2?'-':'.');
   route(c,p,[[u+.02,v+h*.4],[u+w*.3,v+h*.5],[u+w*.8,v+h*.36]],'s','.');
   route(c,p,[[u+.015,v+h*.78],[u+w*.7,v+h*.8]],'a','-');
  }
  if(p.style==='marble'){
   const flip=(r+k)%2,a=flip?.8:.1,b=flip?.2:.78;
   const points=[[u+w*a,v+h*.1],[u+w*(a*.6+.2),v+h*.3],[u+w*.48,v+h*.54],[u+w*(b*.7+.1),v+h*.72],[u+w*b,v+h*.93]];
   route(c,p,points,'s');route(c,p,[points[2],[u+w*.62,v+h*.35],[u+w*.9,v+h*.38]],'a');
   route(c,p,points.map(([x,y])=>[x+w*.07,y]),'f','.');
   route(c,p,[[u+w*.1,v+h*.8],[u+w*.3,v+h*.72],[u+w*.36,v+h*.43]],'a','.');
  }
 }
 if(p.style==='mosaic'){
  // Fish medallion and a ring of individually set tesserae.
  const rim=Array.from({length:50},(_,i)=>groundPoint(p,.5+.27*Math.cos(i*Math.PI*2/50),.5+.33*Math.sin(i*Math.PI*2/50)));polygon(c,rim,'w','f');
  for(let row=0;row<7;row++)for(let col=0;col<8;col++){const u=.32+col*.05,v=.26+row*.08;if(((u-.5)/.25)**2+((v-.5)/.3)**2<1)mark(c,p,u,v,'+','s');}
  for(let i=0;i<50;i++){const a=i*Math.PI*2/50;mark(c,p,.5+.25*Math.cos(a),.5+.3*Math.sin(a),'#',i%2?'f':'a');}
  polygon(c,[[.34,.5],[.45,.36],[.6,.43],[.66,.33],[.66,.63],[.59,.55],[.45,.65]].map(([u,v])=>groundPoint(p,u,v)),'a','f');
  mark(c,p,.4,.48,'o','k');route(c,p,[[.47,.4],[.52,.5],[.47,.6]],'s');
  for(const v of [.44,.5,.56])mark(c,p,.54,v,')','s');
 }
}
function boards(c,p){
 foundation(c,p,'s');const rows=p.type==='plank'?1:5;
 for(let r=0;r<rows;r++){
  const v=r/rows+.018,h=.96/rows;panel(c,p,.01,v,.98,h,r%2?'b':'a','f');
  for(let line=0;line<3;line++){
   const y=v+h*(.23+line*.25),pts=[];
   for(let i=0;i<30;i++){const u=.025+i*.032;pts.push([u,y+Math.sin(i*.45+r)*h*.045]);}route(c,p,pts,line%2?'s':'f','~');
  }
  const knot=groundPoint(p,.3+(r%3)*.2,v+h*.5);c.ellipse(knot.x,knot.y,6,Math.max(1,h*(p.h-30)*.2),'~','s');c.put(knot.x-1,knot.y,'()','k');
  if(p.type==='wood')for(const u of [.06,.94])mark(c,p,u,v+h*.5,'(+)','k');
 }
 if(p.type==='plank'){
  const a=groundPoint(p,.96,.1),b=groundPoint(p,.99,.9);c.line(a.x,a.y,b.x,b.y,':','s');
  route(c,p,[[.82,.96],[.85,.8],[.88,.94]],'k');
 }
}
function clearFloor(c,p,s){
 foundation(c,p,p.type==='ice'?'w':'b');
 if(p.type==='glass'){
  // Metal posts, clear panes, and the darker under-frame are separate layers.
  for(const v of [.08,.5,.92])route(c,p,[[.03,v],[.97,v]],'s','=');
  for(const u of [.08,.5,.92])route(c,p,[[u,.03],[u,.97]],'s','|');
  for(const v of [.04,.52])for(const u of [.03,.52]){
   panel(c,p,u,v,.45,.43,'w','f');route(c,p,[[u+.08,v+.31],[u+.17,v+.14],[u+.23,v+.13]],'f','/');
   mark(c,p,u+.04,v+.04,'+','a');mark(c,p,u+.4,v+.36,'+','a');
  }
 }else{
  route(c,p,[[.1,.12],[.35,.4],[.3,.7],[.58,.86]],'f');
  route(c,p,[[.35,.4],[.62,.32],[.83,.51]],'a');
  route(c,p,[[.3,.7],[.13,.85]],'a');
  for(let i=0;i<25;i++){const u=.15+(i%5)*.17,v=.16+Math.floor(i/5)*.16;mark(c,p,u,v,i%4?'o':'.','s');}
  if(s.frost>.2)for(let i=0;i<16;i++)mark(c,p,.04+i*.06,.03+(i%2)*.035,'*','f');
 }
}
function softGround(c,p,s){
 foundation(c,p,p.type==='snow'?'f':'b');
 for(let row=0;row<8;row++){
  const pts=[];for(let i=0;i<42;i++){const u=.025+i*.023,v=.08+row*.12+Math.sin(i*.24+row)*.025;pts.push([u,v]);}
  route(c,p,pts,p.type==='snow'?(row%2?'a':'w'):(row%2?'s':'a'),p.type==='snow'?'~':'.');
 }
 if(p.type==='sand'){
  for(let row=0;row<12;row++)for(let col=0;col<27;col++)if((col*7+row*3)%8===0)mark(c,p,.025+col*.036,.03+row*.08,':','f');
  for(const line of s.furrows||[]){
   const a=line.u0??.31,b=line.u1??.79,v=clamp(line.v);
   // The pushed-up sandy rim distinguishes a fresh drawn groove from the
   // underlying wind ripples. Weathered marks lose their crisp bright edge.
   route(c,p,[[a,v],[b,v]],'k','_');
   if((line.life??1)>.35){
    route(c,p,[[a,clamp(v+.018)],[b,clamp(v+.018)]],'f','.');
    mark(c,p,b,clamp(v+.032),':','a');
   }
  }
  for(const [u,v]of [[.12,.2],[.78,.3],[.2,.8],[.87,.74]]){route(c,p,[[u-.05,v+.02],[u,v],[u+.07,v+.03]],'a','~');mark(c,p,u-.02,v+.06,': .','s');}
 }else{
  for(let i=0;i<20;i++)mark(c,p,.08+(i%7)*.13,.1+Math.floor(i/7)*.3,i%3?'*':'+','a');
  // Depth belongs to this decorative snow patch; melt changes its exposed base.
  if(s.powder<.3)for(let i=0;i<18;i++)mark(c,p,.08+(i%6)*.16,.12+Math.floor(i/6)*.3,',.','s');
 }
}
function wonders(c,p,s,motion){
 const phase=motion?s.phase||0:0;
 if(p.type==='cloud'){
  const puffs=[[.18,.22,24,8],[.47,.17,31,9],[.77,.24,25,8],[.26,.43,32,10],[.66,.45,39,12],[.13,.67,23,8],[.43,.72,36,10],[.8,.73,25,9]];
  for(const [i,[u,v,rx,ry]]of puffs.entries()){
   const q=groundPoint(p,u+Math.sin(phase*.4+i)*.018,v);
   c.ellipse(q.x,q.y,rx,ry,'~',i%3?'b':'a',true);
   const points=[];for(let j=0;j<35;j++){const a=j*.13,rad=1-j/42;points.push({x:q.x+Math.cos(a)*rx*.75*rad,y:q.y+Math.sin(a)*ry*.65*rad});}
   curve(c,points,'f','~');c.line(q.x-rx*.55,q.y+ry*.55,q.x+rx*.3,q.y+ry*.55,'~','w');
  }return;
 }
 foundation(c,p,p.type==='lava'?'k':'s');
 if(p.type==='rainbow'){
  for(let band=0;band<7;band++){
   const tone=String(band);for(let row=0;row<5;row++){const pts=[];for(let i=0;i<60;i++)pts.push([.02+i*.016,.06+band*.125+row*.02-Math.sin(i*Math.PI/59)*.04]);route(c,p,pts,tone,row%2?'~':'=');}
  }
  for(let i=0;i<7;i++)mark(c,p,.08+i*.14,.15+(i%3)*.27,'.','f');
 }else if(p.type==='lava'){
  // Black crust rafts divide channels of slow-moving molten ribbons.
  for(let j=0;j<6;j++){
   const pts=[];for(let i=0;i<50;i++)pts.push([.03+i*.019,.1+j*.15+Math.sin(i*.22+j+phase)*.036]);
   route(c,p,pts,'a','=');route(c,p,pts.map(([u,v])=>[u,v+.035]),'f','~');
  }
  for(let j=0;j<4;j++)for(let i=0;i<6;i++){const u=.08+i*.16,v=.15+j*.22;panel(c,p,u,v,.1,.08,'k','s');}
  for(let i=0;i<10;i++)mark(c,p,.08+i*.09,.05,'#','b');
 }else{
  const center=groundPoint(p,.5,.5);
  for(let arm=0;arm<3;arm++)for(let i=0;i<120;i++){
   const a=i*.09+arm*Math.PI*2/3+phase*.1,rad=.025+i*.003;
   const q=groundPoint(p,.5+Math.cos(a)*rad,.5+Math.sin(a)*rad*.85);c.put(q.x,q.y,i%13===0?'*':'.',arm===1?'a':'w');
  }
  c.ellipse(center.x,center.y,5,2,'~','f');c.put(center.x-1,center.y,'*','f');
  for(let i=0;i<36;i++)mark(c,p,.035+(i*17%90)/100,.03+(i*29%92)/100,i%5?'.':'+','f');
 }
}
export function groundSprite(base,item,t,{state={},pose={},motion=true}={}){
 const p=BLUEPRINTS[item.id];if(!p)return null;
 const c=new ObjectCanvas(p.w,p.h),s={powder:.75,frost:0,phase:0,tracks:[],furrows:[],...state.ground},v=pose.ground||{u:.5,v:1.1};
 if(p.type==='stones')masonry(c,p);else if(p.type==='tiles')tiles(c,p);else if(['wood','plank'].includes(p.type))boards(c,p);else if(['glass','ice'].includes(p.type))clearFloor(c,p,s);else if(['sand','snow'].includes(p.type))softGround(c,p,s);else wonders(c,p,s,motion);
 const covered=new Set();for(const a of c.fills)for(let x=a.x;x<a.x+a.w;x++)covered.add(x+','+a.y);
 for(let y=12;y<p.h-18;y++)for(let x=8;x<p.w-8;x++)if(covered.has(x+','+y)){
  if(state.dirt>.2&&(x*17+y*7)%Math.max(30,Math.floor(190-state.dirt*150))===0)c.put(x,y,',','s');
  if(s.frost>.2&&(x*11+y*13)%Math.max(25,Math.floor(170-s.frost*130))===0)c.put(x,y,'*','f');
 }
 for(const track of s.tracks||[]){
  const q=groundPoint(p,clamp(track.u),clamp(track.v)),rows={webbed:['\\|/',' v '],small:['v'],talon:['Y','|'],toad:['o.o',' V ']}[track.shape||'webbed']||['v'];
  c.rows(rows,q.x-Math.floor(rows[0].length/2),q.y,'s');
 }
 if(v.press>.1&&['sand','snow'].includes(p.type)){const q=groundPoint(p,v.u,v.v);c.put(q.x-2,q.y+1,'(vv)','s');}
 const inks={b:'#afa99a',a:'#d1c6ad',f:'#e5dbc2',s:'#666c66',k:'#303b38',w:'#79aeb2',l:'#839661','0':'#cf6b72','1':'#e0a05d','2':'#e8d77f','3':'#86bd86','4':'#71b9cc','5':'#8299ca','6':'#b09bc9'};
 const panels={b:'#5d6661',a:'#778178',f:'#bac2af',s:'#364b47',k:'#172e2d',w:'#335c69'};
 if(['wood','plank'].includes(p.type)){Object.assign(inks,{b:'#be9a64',a:'#d2b57d',f:'#ead29e',s:'#806443',k:'#443b2e'});Object.assign(panels,{b:'#725b3d',a:'#846b48',s:'#443b2f'});}
 if(p.type==='sand'){Object.assign(inks,{b:'#ceb77a',a:'#b7a16d',f:'#d5c391',s:'#968354',k:'#494733'});Object.assign(panels,{b:'#756643',s:'#514d35'});}
 if(p.type==='snow'||p.type==='ice'){Object.assign(inks,{b:'#d0e6df',f:'#e9f2e7',a:'#aecbcc',w:'#87b2bd',s:'#577d90',k:'#365463'});Object.assign(panels,{f:'#b7cecc',w:'#456f80',s:'#3c5965'});}
 if(p.type==='cloud'){Object.assign(inks,{b:'#c7d9d3',f:'#edf3dc',a:'#aac7ca',w:'#88aeb8'});Object.assign(panels,{b:'#789fa8',a:'#5d8896'});}
 if(p.type==='lava'){Object.assign(inks,{b:'#867866',s:'#5c5149',a:'#e19248',f:'#f3c16d'});Object.assign(panels,{k:'#302f2c',s:'#474039'});}
 if(p.type==='galaxy'){Object.assign(inks,{a:'#b7a1cf',w:'#7d9bbd',f:'#e1d8b5'});panels.s='#273341';}
 const foot=groundPoint(p,v.u,v.v),contact=groundPoint(p,clamp(v.u+.09),clamp(v.v-.12));
 return {...base,...c.finish(),construction:'ground-v1',detail:true,detailScale:.65,blueprint:item.id,floor:p.type!=='plank',anchors:{foot,contact},inks,panels,sway:0,lift:0,animated:Boolean(pose.ground)||['cloud','lava','galaxy'].includes(p.type),emissive:false};
}
