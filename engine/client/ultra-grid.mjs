import { sceneLight,mixColor } from './scene-lighting.mjs';
export const W = 240, H = 112;
export const M = Object.freeze({ambient:0,foliage:1,wood:2});
export const C = Object.freeze({bg:0,sky:1,cloud:2,far:3,hill:4,leafDark:5,leaf:6,leafLight:7,
  barkDark:8,bark:9,barkLight:10,groundDark:11,ground:12,grass:13,waterDark:14,water:15,
  waterLight:16,glint:17,flower:18,goldDark:19,gold:20,goldLight:21,orange:22,ink:23,
  white:24,mist:25,star:26,berry:27,crystal:28,ice:29,lamp:30,shadow:31});
export const clamp = (n,a,b) => Math.min(b, Math.max(a,n));
export const lerp = (a,b,t) => a+(b-a)*t;
export function hash(x,y=0,seed=0) {
  let h = Math.imul(x | 0, 374761393) + Math.imul(y | 0, 668265263) + Math.imul(seed | 0, 1442695041);
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  return ((h ^ (h >>> 16)) >>> 0) / 4294967295;
}
export function seedOf(str) { let n = 0; for (const c of str) n = Math.imul(n,31) + c.charCodeAt(0) | 0; return n; }
export class Grid {
  constructor(w=W,h=H) { this.w=w;this.h=h;this.chars=new Uint8Array(w*h);this.colors=new Uint8Array(w*h);this.materials=new Uint8Array(w*h); }
  clear() {this.chars.fill(32);this.colors.fill(0);this.materials.fill(M.ambient);}
  put(x,y,ch,color,material=M.ambient) {
    x=Math.round(x);y=Math.round(y);
    if (x<0||y<0||x>=this.w||y>=this.h) return;
    const c=typeof ch==='number'?ch:ch.charCodeAt(0);
    this.chars[y*this.w+x]=c>=32&&c<=126?c:63;this.colors[y*this.w+x]=color;this.materials[y*this.w+x]=material;
  }
  text(x,y,str,color,material=M.ambient) { for(let i=0;i<str.length;i++)this.put(x+i,y,str[i],color,material); }
  art(x,y,lines,color,flip=false) {
    for(let j=0;j<lines.length;j++)for(let i=0;i<lines[j].length;i++) {
      const ch=lines[j][i]; if(ch!==' ')this.put(x+i,y+j,ch,typeof color==='function'?color(ch,i,j):color);
    }
  }
  line(x1,y1,x2,y2,char,color,material=M.ambient) {
    const n=Math.ceil(Math.max(Math.abs(x2-x1),Math.abs(y2-y1)));
    for(let i=0;i<=n;i++) this.put(lerp(x1,x2,i/Math.max(1,n)),lerp(y1,y2,i/Math.max(1,n)),char,color,material);
  }
  ellipse(cx,cy,rx,ry,char,color,fill=true) {
    for(let y=Math.floor(cy-ry);y<=cy+ry;y++)for(let x=Math.floor(cx-rx);x<=cx+rx;x++) {
      const d=((x-cx)/rx)**2+((y-cy)/ry)**2;
      if(d<=1&&(fill||d>.72))this.put(x,y,char,color);
    }
  }
}
export function palette(scene) {
  const p=['#0c1c21','#20363c','#728784','#354c54','#496356','#173a30','#426c43','#9bad66',
    '#3c3529','#796343','#bda57b','#263e35','#52634a','#97a575','#163b4b','#36717d',
    '#74a7a5','#c2d9bd','#d8ad9b','#9c6b26','#e0b64e','#ffe3a0','#ed963e','#171d21',
    '#f2e5ca','#637a7e','#d9e4d7','#a96473','#a6b5d4','#9fd1d4','#edbc70','#09171a'];
  const b=scene.biome;
  if(b==='swamp'){p[6]='#54634b';p[7]='#a7aa70';p[15]='#486b60';p[16]='#81a692';}
  if(b==='beach'){p[11]='#514f3b';p[12]='#9b936d';p[13]='#d6c59b';p[15]='#328c99';}
  if(b==='mountains'){p[5]='#233f43';p[6]='#457070';p[12]='#78868a';p[13]='#bcc7bc';}
  if(b==='urban'){p[11]='#3c4546';p[12]='#697a72';p[13]='#a6b29b';}
  if(scene.season==='fall'){p[6]='#966d43';p[7]='#d8aa66';p[13]='#a89762';}
  if(scene.season==='winter'){p[6]='#688c8d';p[7]='#c7d8d1';p[12]='#7f9e9e';p[13]='#cedbd5';}
  const light=sceneLight(scene),day=p.slice();
  Object.assign(day,{0:light.groundNear,1:'#7fa8c4',2:'#e3e8da',3:'#597687',4:'#48685c',5:'#3e7045',6:'#76a852',7:'#b6d97e',
    8:'#775237',9:'#c29561',10:'#edc189',11:'#939052',12:'#c3ba78',13:'#e2cf87',14:'#437f9a',15:'#75b6d1',16:'#c3e4ee',17:'#f4df9d'});
  if(scene.biome==='beach'){day[11]='#a29061';day[12]='#f1dba1';day[13]='#fff0ca';}
  if(scene.season==='fall'||scene.season==='autumn'){day[5]='#96562d';day[6]='#dd9146';day[7]='#f7c074';day[12]='#c3b177';}
  if(scene.season==='winter'){day[11]='#709b9a';day[12]='#e7eddd';day[13]='#fbffe9';}
  // Grass is a quiet, detailed ground plane. Keep the brighter cream and gold
  // values for characters, flowers and the occasional sun-catching blade.
  if(light.grassy){
    day[C.groundDark]='#405d37';day[C.ground]='#637d4f';day[C.grass]='#8c9e66';
    if(scene.season==='fall'||scene.season==='autumn'){
      day[C.groundDark]='#3f5636';day[C.ground]='#627348';day[C.grass]='#88965c';
    }
  }
  const daylight=light.sun;
  const dusk=light.twilight>0;
  if(dusk){p[1]='#423440';p[2]='#bd937c';p[3]='#665168';p[17]='#efbf8b';}
  if(daylight<.1){p[0]='#080f1d';p[1]='#162336';p[2]='#536079';p[17]='#859ebc';}
  // Keep night legible, with luminous daylight ink over the lit sky and terrain.
  const shade=Math.round((.7+.3*daylight)*8)/8;
  return p.map((hex,i)=>{
    let shaded=hex;
    if(![0,1,2,17,19,20,21,22,24,26,28,30].includes(i)){
      const a=hex.slice(1).match(/../g).map(v=>parseInt(v,16));
      shaded='#'+a.map((v,j)=>Math.round(v*shade+(1-shade)*(j===2?9:0)).toString(16).padStart(2,'0')).join('');
    }
    return mixColor(shaded,day[i],daylight);
  });
}
