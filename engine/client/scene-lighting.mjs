// Visual time only. Auto follows the simulation; overrides never alter its clock.
export const LIGHTING_MODES=['auto','day','dusk','night'];
const clamp=(n,a=0,b=1)=>Math.min(b,Math.max(a,n));
const smooth=(a,b,n)=>{const t=clamp((n-a)/(b-a));return t*t*(3-2*t);};
export function mixColor(a,b,t){
  const rgb=hex=>hex.slice(1).match(/../g).map(v=>parseInt(v,16));
  const x=rgb(a),y=rgb(b);return '#'+x.map((v,i)=>Math.round(v+(y[i]-v)*clamp(t)).toString(16).padStart(2,'0')).join('');
}
export function lightingScene(scene,mode='auto'){
  const hour={day:12,dusk:18.5,night:23}[mode];
  return hour===undefined?scene:{...scene,hour};
}
export function sceneLight(scene){
  const hour=((Number(scene.hour??12)%24)+24)%24,indoor=/cave|drain/i.test(scene.location||'');
  const sun=indoor?0:Math.round(smooth(5.5,9,hour)*(1-smooth(17,20.5,hour))*64)/64;
  const twilight=indoor?0:Math.round(Math.max(smooth(4.75,6.5,hour)*(1-smooth(7.25,9,hour)),smooth(16.5,18.5,hour)*(1-smooth(20,21,hour)))*32)/32;
  const storm=/storm/.test(scene.weather),cloudy=/cloud|rain|fog|snow|drizzle/.test(scene.weather);
  let groundFar='#a2b77b',groundNear='#6f945a',waterFar='#88c4c5',waterNear='#438c9a';
  if(scene.season==='fall'||scene.season==='autumn'){groundFar='#c4ba83';groundNear='#9c975c';}
  if(scene.biome==='forest'){groundFar='#85a879';groundNear='#52794e';}
  if(scene.biome==='swamp'){groundFar='#8eaa80';groundNear='#667c52';waterFar='#8eb6a2';waterNear='#547c6f';}
  if(scene.biome==='beach'){groundFar='#e6d8ab';groundNear='#c4ae7e';waterFar='#8bd4d0';waterNear='#418fa7';}
  if(scene.biome==='mountains'){groundFar='#bdc7ba';groundNear='#8b9b93';}
  if(scene.biome==='urban'){groundFar='#b6bdaa';groundNear='#8b9e86';}
  if(scene.season==='winter'){groundFar='#e3e9d9';groundNear='#b4cdc7';waterFar='#b9dfe0';waterNear='#81b5c4';}
  const tone=(night,day,dusk)=>{
    let value=mixColor(mixColor(night,day,sun),dusk,twilight*.66);
    if(cloudy||storm)value=mixColor(value,storm?'#627d85':'#a0b8b7',sun*(storm?.38:.27));
    return value;
  };
  return {sun,twilight,indoor,
    skyTop:tone('#101e31','#70b4d5','#826c93'),skyHorizon:tone('#253e50','#d6e7cd','#f0bc88'),
    groundFar:tone('#29433a',groundFar,'#a99869'),groundNear:tone('#20372e',groundNear,'#73784f'),
    waterFar:tone('#244a5b',waterFar,'#ad9f94'),waterNear:tone('#173849',waterNear,'#577c8b'),
    propSurface:mixColor('#102023','#335443',sun),outline:mixColor('#0b1a24','#25473b',sun)};
}
// Row colors are cached with the palette. Empty cells get actual ambient light,
// independent of the optional bloom/particles toggle.
export function ambientRows(light,height=112){
  if(light.indoor)return {land:Array(height).fill('#0c1c21'),water:Array(height).fill('#12313b')};
  const land=[],water=[];
  for(let y=0;y<height;y++){
    land.push(y<43?mixColor(light.skyTop,light.skyHorizon,y/43):
      y<58?mixColor(light.skyHorizon,light.groundFar,(y-43)/15):mixColor(light.groundFar,light.groundNear,(y-58)/(height-58)));
    water.push(mixColor(light.waterFar,light.waterNear,clamp((y-52)/(height-52))));
  }
  return {land,water};
}

export function luminance(hex){
  const [r,g,b]=hex.slice(1,7).match(/../g).map(v=>{const s=parseInt(v,16)/255;return s<=.04045?s/12.92:((s+.055)/1.055)**2.4;});
  return r*.2126+g*.7152+b*.0722;
}
export function contrastRatio(a,b){const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);}
export function readableInk(ink,background,minimum=3.25){
  if(contrastRatio(ink,background)>=minimum)return ink;
  const dark='#102f30',light='#f0f5de',target=contrastRatio(dark,background)>contrastRatio(light,background)?dark:light;
  // Quantized ink shades keep the glyph atlas bounded across the row gradient.
  for(let step=1;step<=16;step++){
    const color=mixColor(ink,target,step/16);if(contrastRatio(color,background)>=minimum)return color;
  }
  return target;
}
