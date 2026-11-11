import score from './animation/nest-routines.json' with {type:'json'};
import {ObjectCanvas} from './object-canvas.mjs';

export const NEST_ROUTINES=score.routines;
export const NEST_IDS=['basic_nest','cozy_nest','deluxe_nest','nest_premium','golden_nest'];
export const NEST_MARGIN={x:8,y:18};
const rest={x:0,y:0,b:0,w:0,l:0,r:0,gape:0,tail:0,u:0,v:0,px:0,py:0,turn:0,show:0,press:0,straw:0,blanket:0,pillow:0,eye:null,mark:''};
const numeric=Object.keys(rest).filter(k=>typeof rest[k]==='number');
export function nestPose(routine,motion=true){
 const spec=NEST_ROUTINES[routine?.id];if(!spec)return null;
 const p=motion?Math.max(0,Math.min(1,(routine.elapsed??0)/spec.duration)):.5;
 let a=spec.track[0],b=spec.track.at(-1);
 for(let i=1;i<spec.track.length;i++)if(p<=spec.track[i].at){a=spec.track[i-1];b=spec.track[i];break;}
 a={...rest,...a};b={...rest,...b};let u=(p-a.at)/Math.max(.001,b.at-a.at);u=u*u*(3-2*u);
 const pose={...rest};for(const key of numeric)pose[key]=a[key]+(b[key]-a[key])*u;
 pose.eye=u<.5?a.eye:b.eye;pose.mark=u<.5?a.mark:b.mark;
 const grip=Math.max(0,...(spec.grips||[]).map(([a,b])=>Math.max(0,Math.min(1,(p-a)/.04,(b-p)/.04))));
 return {...pose,id:routine.id,progress:p,prop:spec.prop,label:spec.label,grip};
}

// Loose materials are actual ASCII parts of the nest, with their own path and
// orientation. They share the simulation clock with the actor's bill and wing.
export function nestForeground(p,pose,anchors){
 const c=new ObjectCanvas(p.w+NEST_MARGIN.x*2,p.h+NEST_MARGIN.y).view(NEST_MARGIN.x,NEST_MARGIN.y);if(!pose||pose.show<.12)return c.finish();
 const cx=anchors.seat.x+pose.px,cy=anchors.seat.y+pose.py-3;
 const turn=Math.round(pose.turn),strength=pose.show;
 const line=(ax,ay,bx,by,g='/',tone='f')=>c.line(cx+ax,cy+ay,cx+bx,cy+by,g,tone);
 const rows=(a,tone='f')=>c.rows(a,cx-Math.floor(Math.max(...a.map(r=>r.length))/2),cy-Math.floor(a.length/2),tone);
 switch(pose.prop){
  case 'twig':case 'fork':{
   const angle=pose.turn*.65,dx=Math.cos(angle)*7,dy=Math.sin(angle)*3;
   line(-dx,-dy,dx,dy,Math.abs(dy)<1?'_':dy>0?'\\':'/');
   line(1,0,4,dy-3,'/','b');c.put(cx-3,cy,'o','b');
   if(pose.prop==='fork')line(-4,2,5,-3,'/','b');break;
  }
  case 'strand':case 'braid':{
   const g=pose.prop==='braid'?(p.nest==='gold'?'(o)':'><'):(p.nest==='twig'?'/':'~');
   for(let i=-8;i<8;i+=2)c.put(cx+i,cy+Math.sin(i*.4+pose.turn)*2,g,i%4?'b':'f');break;
  }
  case 'fibres':for(let i=0;i<7;i++){const dx=(i-3)*3,dy=Math.sin(i*1.9+pose.turn)*2;c.put(cx+dx,cy+dy,(i+turn)%2?'/':'\\',p.lining==='velvet'?'q':'f');}break;
  case 'tracks':for(let i=0;i<=Math.min(4,Math.max(0,turn));i++){const a=i*Math.PI/2;c.put(anchors.seat.x+Math.cos(a)*10,anchors.seat.y+Math.sin(a)*2,'v','s');}break;
  case 'feather':rows(turn%2?['   /','  /:',' /:/','//','/']:['  __..--/',' /:/:/:/ ',"'-----'  "],'c');break;
  case 'leaf':rows(turn%2?[' .-.','/;/|','|//','|/']:['  __.._',' /; / /',"'----'"],'g');break;
  case 'pebble':rows(turn%2?[' .-.','(.:)'," '-' "]:[' .--.','( .: )'," '--'"],'s');break;
  case 'acorn':rows(turn%2?[' _#_','(:::)'," \\_/ "]:[' _=_','(###)','( . )'," '-' "],'a');break;
  case 'crumbs':for(let i=0;i<6;i++)c.put(cx+(i-2)*3,cy+(i%3)-1,i%2?'.':'o','a');break;
  case 'petals':for(let i=0;i<5;i++)c.put(cx+(i-2)*4,cy+Math.sin(i+pose.turn)*3,i%2?'<>':',','q');break;
  case 'snow':for(let i=0;i<7;i++)c.put(cx+(i-3)*3,cy+Math.sin(i+pose.turn)*4,i%2?'*':'.','c');break;
  case 'frost':rows(turn?['. :  .'," ' * "]:['_/|\\_'," '*:'"],'w');break;
  case 'beetle':rows(turn%2?[' /\\','(oo)'," /\\"]:['\\ /','(oo)','/ \\'],'k');break;
  case 'firefly':rows(strength>.7?[' .|.','-o-','  |']:[' . ',' o '],'l');break;
  case 'drop':rows(turn?[". ' .",' ~_~ ']:["'",'o'],'w');break;
  case 'drops':for(let i=0;i<3;i++)c.put(cx+(i-1)*3,cy+i*2,"'",'w');break;
  case 'breath':if(strength>.4)rows(strength>.75?[' .~.','  ~']:['.~'],'c');break;
  case 'dream':rows(turn%2?['. o .',' ~^~']:[' o . ',' ~v~'],'w');break;
  case 'air':rows(turn%2?[' ~~~ >','  ~ >']:[' ~~ >',' ~~~ >'],'w');break;
  case 'groove':for(let i=0;i<=Math.min(3,turn);i++)c.put(cx+i*2,cy+Math.round(Math.sin(i)),"'",'s');break;
 }
 return {...c.finish(),contact:{x:cx+NEST_MARGIN.x,y:cy+NEST_MARGIN.y}};
}
