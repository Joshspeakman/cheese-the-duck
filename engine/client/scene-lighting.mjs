// Every world and portrait uses the simulation's actual time of day.
const clamp=(n,a=0,b=1)=>Math.min(b,Math.max(a,n));
const smooth=(a,b,n)=>{const t=clamp((n-a)/(b-a));return t*t*(3-2*t);};
export function mixColor(a,b,t){
  const rgb=hex=>hex.slice(1).match(/../g).map(v=>parseInt(v,16));
  const x=rgb(a),y=rgb(b);return '#'+x.map((v,i)=>Math.round(v+(y[i]-v)*clamp(t)).toString(16).padStart(2,'0')).join('');
}
export function sceneLight(scene){
  const value=Number(scene.hour??12),indoor=/cave|drain/i.test(scene.location||'');
  let hour=Number.isFinite(value)?value%24:12;if(hour<0)hour+=24;
  const phase=hour<5?'Late night':hour<7?'Dawn':hour<11?'Morning':hour<14?'Midday':hour<17?'Afternoon':hour<19?'Evening':hour<21?'Dusk':'Night';
  const night=hour<5||hour>=21;
  const sun=indoor?0:Math.round(smooth(5,9,hour)*(1-smooth(17,21,hour))*64)/64;
  const twilight=indoor?0:Math.round(Math.max(smooth(4.75,6.5,hour)*(1-smooth(7.25,9,hour)),smooth(16.5,18.5,hour)*(1-smooth(20,21.5,hour)))*32)/32;
  const storm=/storm/.test(scene.weather),cloudy=/cloud|rain|fog|snow|drizzle/.test(scene.weather);
  // Saturated midtones carry warm, luminous ASCII ink. No pale screen-wide wash.
  let groundFar='#4d6748',groundNear='#304a36',waterFar='#357b86',waterNear='#225364';
  if(scene.season==='fall'||scene.season==='autumn'){groundFar='#706746';groundNear='#4e4b33';}
  if(scene.biome==='forest'){groundFar='#456449';groundNear='#2a4636';}
  if(scene.biome==='swamp'){groundFar='#506348';groundNear='#3b4934';waterFar='#50786c';waterNear='#304e49';}
  if(scene.biome==='beach'){groundFar='#a09061';groundNear='#736741';waterFar='#3d8b91';waterNear='#245e72';}
  if(scene.biome==='mountains'){groundFar='#657772';groundNear='#414f50';}
  if(scene.biome==='urban'){groundFar='#5e6b59';groundNear='#414d40';}
  if(scene.season==='winter'){groundFar='#96ada6';groundNear='#607d7c';waterFar='#6c969b';waterNear='#41697b';}
  const tone=(nightColor,day,dusk)=>{
    let value=mixColor(mixColor(nightColor,day,sun),dusk,twilight*.55);
    if(cloudy||storm)value=mixColor(value,storm?'#354b55':'#526b6b',sun*(storm?.4:.24));
    return value;
  };
  return {hour,phase,night,sun,twilight,indoor,sunX:night?183:43+(hour-6)*10,
    skyTop:tone('#0c1828','#386c83','#59475e'),skyHorizon:tone('#1c3040','#6a8b87','#ad8059'),
    groundFar:tone('#21382e',groundFar,'#6d6440'),groundNear:tone('#182b25',groundNear,'#4b4c31'),
    waterFar:tone('#1c3b4b',waterFar,'#756b68'),waterNear:tone('#102938',waterNear,'#3a5869'),
    propSurface:tone('#102023','#3a5141','#564736'),outline:mixColor('#08131f','#172e28',sun)};
}
// Row colors are cached with the palette. Empty cells get actual ambient light,
// independent of the optional bloom/particles toggle.
export function ambientRows(light,height=112){
  if(light.indoor)return {land:Array(height).fill('#0c1c21'),water:Array(height).fill('#12313b')};
  const land=[],water=[];
  for(let y=0;y<height;y++){
    land.push(y<32?mixColor(light.skyTop,light.skyHorizon,y/32):
      y<55?mixColor(light.skyHorizon,light.groundFar,(y-32)/23):mixColor(light.groundFar,light.groundNear,(y-55)/(height-55)));
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

export function lightBand(light,x,y){
  if(light.indoor||light.sun===0)return 2;
  const distance=Math.abs(x-(light.sunX-(y-13)*.35));
  const sunlit=Math.max(0,1-distance/100);
  const canopy=y<40?0:Math.sin(x*.065+y*.025)*Math.sin(x*.029-y*.045)*.28;
  return Math.round(clamp(.28+sunlit*.55+canopy,0,1)*4);
}
export function ambientSwatches(light,rows){
  const colors={};
  for(const surface of ['land','water'])colors[surface]=Array.from({length:5},(_,band)=>rows[surface].map(color=>{
    if(band<2)return mixColor(color,light.outline,(2-band)*.075*light.sun);
    return mixColor(color,surface==='water'?'#80b6ae':'#b3a86d',(band-2)*.055*light.sun);
  }));
  return colors;
}
