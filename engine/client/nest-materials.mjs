// Read-only physical bedding. The native simulation owns every value here.
const defaults={left:.22,right:.28,brace:0,mend:0,plump:.5,hollow:.2,width:.5,
 feather:0,leaf:0,twig:1,grit:.6,crumbs:.35,pebble:0,acorn:0,petals:0,
 snow:0,frost:0,groove:0,braid:.25};
export function nestMaterials(state={}){
 const source=state.nest||{},out={};
 for(const [key,value]of Object.entries(defaults))out[key]=Number.isFinite(source[key])?Math.max(0,Math.min(1,source[key])):value;
 return out;
}
export function drawNestMaterials(c,p,s,pose,cx,cy,rx){
 const moving=pose?.show>=.12?pose.prop:null;
 const straw=p.nest==='gold'?'a':'f',fibre=p.lining==='velvet'?'q':'c';
 // Real loose ends settle into the weave when tucked; subsequent visits see it.
 for(const [side,key]of [[-1,'left'],[1,'right']]){
  const x=cx+side*(rx-7),loose=(1-s[key])*6;
  c.line(x,cy+2,x+side*loose,cy-2-loose/2,side<0?'/':'\\',straw);
  if(s[key]>.7)c.put(x-2,cy+1,'><><',straw);
 }
 if(s.brace>.5)c.line(cx+1,cy+1,cx+15,cy-4,'/','f');
 if(s.mend>.5){c.put(cx-13,cy+2,'/X/X/','f');c.put(cx-12,cy+3,'V-V','b');}
 if(s.braid>.5)for(let i=-9;i<=9;i+=3)c.put(cx+i,cy+4,p.nest==='gold'?'(o)':'><','f');
 if(s.twig>.02&&moving!=='twig'&&moving!=='fork'){
  c.line(cx+3,cy-3,cx+18,cy-6,'_','b');c.line(cx+11,cy-4,cx+15,cy-8,'/','f');
 }
 if(moving!=='feather'){
  const x=s.feather>.5?cx-12:12,y=s.feather>.5?cy-4:cy-9;
  c.rows(s.feather>.5?['__..--/','/:/:/ ',"'--'  "]:['  /',' /:','//'],x,y,fibre);
 }
 if(moving!=='leaf'){
  if(s.leaf>.5)c.put(cx+4,cy-1,'/;/','g');
  else c.rows(['  .---.',' /; / /'," '---'"],p.w-16,cy-10,'g');
 }
 if(s.grit>.02&&moving!=='pebble')for(let i=0;i<Math.ceil(s.grit*5);i++)c.put(cx-7+i*4,cy-3+i%2,'.','s');
 if(moving!=='pebble')c.rows([' .-.','(.:)'," '-'"],s.pebble>.5?cx+rx-6:cx+7,s.pebble>.5?cy+6:cy-4,'s');
 if(moving!=='crumbs')for(let i=0;i<Math.ceil(s.crumbs*8);i++)c.put(cx-5+i*3,cy-2+i%2,i%2?'.':'o','a');
 if(s.acorn>.02&&moving!=='acorn')c.rows(['_#_','(o)',"'v'"],cx-14,cy-3,'a');
 if(moving!=='petals')for(let i=0;i<Math.ceil(s.petals*6);i++)c.put(cx-15+i*5,cy-5+i%3,'<>','q');
 if(s.groove>.2)for(let i=0;i<Math.ceil(s.groove*5);i++)c.put(cx-5+i*2,cy-1+Math.round(Math.sin(i)),"'",'s');
 // Sparse deposits expose the joinery instead of whitening the entire nest.
 for(let i=0;i<Math.floor(s.snow*18);i++)c.put(cx-rx+5+i*(rx*2-10)/18,cy+2+(i%3),'*','c');
 for(let i=0;i<Math.floor(s.frost*10);i++)c.put(cx-rx+6+i*(rx*2-12)/10,cy+5,'+','w');
}
