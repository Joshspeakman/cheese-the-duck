// Printable-character construction tools. Geometry creates actual new ASCII ink;
// it never stretches an old bitmap or treats random texture as authored detail.
export class ObjectCanvas {
 constructor(w,h){this.w=w;this.h=h;this.art=Array.from({length:h},()=>Array(w).fill(' '));this.tones=this.art.map(r=>r.map(()=>'b'));this.fills=[];this.clipped=false;}
 put(x,y,text,tone='b'){x=Math.round(x);y=Math.round(y);for(const [i,c] of [...String(text)].entries()){if(c===' ')continue;if(x+i<0||x+i>=this.w||y<0||y>=this.h){this.clipped=true;continue;}this.art[y][x+i]=c;this.tones[y][x+i]=tone;}return this;}
 clear(x,y,w,h){for(let j=Math.max(0,Math.round(y));j<Math.min(this.h,Math.round(y+h));j++)for(let i=Math.max(0,Math.round(x));i<Math.min(this.w,Math.round(x+w));i++){this.art[j][i]=' ';this.tones[j][i]='b';}return this;}
 line(x0,y0,x1,y1,char=null,tone='b'){const steps=Math.ceil(Math.max(Math.abs(x1-x0),Math.abs(y1-y0)));const c=char||((y1===y0)?'-':x1===x0?'|':(x1-x0)*(y1-y0)>0?'\\':'/');for(let i=0;i<=steps;i++){const p=steps?i/steps:0;this.put(x0+(x1-x0)*p,y0+(y1-y0)*p,c,tone);}return this;}
 beam(x0,y0,x1,y1,width=3,tone='b'){const steps=Math.ceil(Math.max(Math.abs(x1-x0),Math.abs(y1-y0)));for(let i=0;i<=steps;i++){const p=steps?i/steps:0;this.solid(x0+(x1-x0)*p-width/2,y0+(y1-y0)*p,width,1,tone);}this.line(x0-width/2,y0,x1-width/2,y1,null,'f').line(x0+width/2-1,y0,x1+width/2-1,y1,null,'k');return this;}
 rect(x,y,w,h,tone='b',fill=false){if(fill)this.solid(x,y,w,h,tone);this.line(x,y,x+w-1,y,'-',tone).line(x,y+h-1,x+w-1,y+h-1,'-',tone).line(x,y,x,y+h-1,'|',tone).line(x+w-1,y,x+w-1,y+h-1,'|',tone);for(const [xx,yy] of [[x,y],[x+w-1,y],[x,y+h-1],[x+w-1,y+h-1]])this.put(xx,yy,'+',tone);return this;}
 solid(x,y,w,h,tone='b'){for(let j=0;j<h;j++)this.fills.push({x:Math.round(x),y:Math.round(y+j),w:Math.round(w),tone,opaque:true});return this;}
 ellipse(cx,cy,rx,ry,char='-',tone='b',fill=false){for(let y=Math.ceil(cy-ry);y<=Math.floor(cy+ry);y++){const q=1-((y-cy)/ry)**2;if(q<0)continue;const half=rx*Math.sqrt(q),left=Math.round(cx-half),right=Math.round(cx+half);if(fill)this.solid(left,y,right-left+1,1,tone);this.put(left,y,Math.abs(y-cy)>ry*.7?char:'(',tone);this.put(right,y,Math.abs(y-cy)>ry*.7?char:')',tone);if(Math.abs(y-cy)>ry*.86)this.line(left,y,right,y,char,tone);}return this;}
 rows(rows,x,y,tone='b',fill=false){rows.forEach((r,j)=>{if(fill){const first=r.search(/\S/),end=r.trimEnd().length;if(first>=0)this.solid(x+first,y+j,end-first,1,tone);}this.put(x,y+j,r,tone);});return this;}
 view(dx,dy){
  const view={finish:()=>this.finish()};
  for(const name of ['put','clear','line','beam','rect','solid','ellipse','rows'])view[name]=(...args)=>{
   const i=name==='rows'?1:0;args[i]+=dx;args[i+1]+=dy;
   if(name==='line'||name==='beam'){args[2]+=dx;args[3]+=dy;}
   this[name](...args);return view;
  };
  return view;
 }
 finish(){return {art:this.art.map(r=>r.join('')),tones:this.tones.map(r=>r.join('')),fills:this.fills,width:this.w,groundRow:this.h,anchorX:this.w/2,clipped:this.clipped};}
}
