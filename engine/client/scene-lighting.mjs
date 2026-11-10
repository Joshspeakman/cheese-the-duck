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
  let groundFar='#77763f',groundNear='#4b552a',waterFar='#1d647e',waterNear='#123b59',foliage='#153c2c';
  if(scene.season==='fall'||scene.season==='autumn'){groundFar='#827348';groundNear='#5c522e';foliage='#4d2d22';}
  if(scene.biome==='forest'){groundFar='#657044';groundNear='#46572f';}
  if(scene.biome==='swamp'){groundFar='#737345';groundNear='#4e552c';waterFar='#205c67';waterNear='#133b4e';}
  if(scene.biome==='beach'){groundFar='#a09061';groundNear='#736741';waterFar='#216f8c';waterNear='#124568';}
  if(scene.biome==='mountains'){groundFar='#7d8273';groundNear='#555d51';}
  if(scene.biome==='urban'){groundFar='#7d7758';groundNear='#57533d';}
  if(scene.season==='winter'){groundFar='#a7b6ad';groundNear='#7f948c';waterFar='#356984';waterNear='#20465f';foliage='#294a44';}
  const tone=(nightColor,day,dusk,overcast)=>{
    let value=mixColor(mixColor(nightColor,day,sun),dusk,twilight*.55);
    if(cloudy||storm)value=mixColor(value,overcast,sun*(storm?.3:.16));
    return value;
  };
  return {hour,phase,night,sun,twilight,indoor,sunX:night?183:43+(hour-6)*10,
    skyTop:tone('#10172f','#3e7cae','#70536d','#647f99'),skyHorizon:tone('#253852','#8bb9c3','#c19170','#8098a5'),
    groundFar:tone('#353421',groundFar,'#74633d','#626047'),groundNear:tone('#22281b',groundNear,'#51482b','#4e5336'),
    waterFar:tone('#073148',waterFar,'#254b68','#244f69'),waterNear:tone('#08263e',waterNear,'#17374f','#1b3d59'),
    foliage:tone('#10231c',foliage,'#38301e','#294134'),wood:tone('#211912','#3b281e','#38251c','#47372d'),
    outline:mixColor('#08131f','#172e28',sun)};
}
// Row colors are cached with the palette. Empty cells get actual ambient light,
// independent of the optional bloom/particles toggle.
export function ambientRows(light,height=112){
  if(light.indoor)return {land:Array(height).fill('#0c1c21'),water:Array(height).fill('#12313b'),foliage:Array(height).fill('#12271e'),wood:Array(height).fill('#271f18')};
  const land=[],water=[],foliage=[],wood=[];
  for(let y=0;y<height;y++){
    land.push(y<32?mixColor(light.skyTop,light.skyHorizon,y/32):
      y<55?mixColor(light.skyHorizon,light.groundFar,(y-32)/23):mixColor(light.groundFar,light.groundNear,(y-55)/(height-55)));
    water.push(mixColor(light.waterFar,light.waterNear,clamp((y-52)/(height-52))));
    foliage.push(mixColor(light.foliage,light.outline,clamp(y/height)*.15));
    wood.push(mixColor(light.wood,'#16120f',clamp(y/height)*.12));
  }
  return {land,water,foliage,wood};
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
  const sunlight={land:'#b3a86d',water:'#5c9ab5',foliage:'#507143',wood:'#88613e'};
  for(const surface of Object.keys(rows))colors[surface]=Array.from({length:5},(_,band)=>rows[surface].map(color=>{
    if(band<2)return mixColor(color,light.outline,(2-band)*.075*light.sun);
    return mixColor(color,sunlight[surface],(band-2)*.055*light.sun);
  }));
  return colors;
}
