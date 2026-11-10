import { sceneLight,mixColor } from './scene-lighting.mjs';

// A small window onto the same hour, weather and season as the actual pond.
export function portraitEnvironment(ctx,scene,x,y,w,h,time){
  const light=sceneLight(scene),clock=scene.motion===false?0:time;
  const gradient=ctx.createLinearGradient(0,y,0,y+h);
  const stops=light.indoor?[[0,'#132d37'],[1,'#233d43']]:
    [[0,light.skyTop],[.58,light.skyHorizon],[.72,light.groundFar],[1,light.waterNear]];
  for(const [at,color] of stops)gradient.addColorStop(at,color);
  // Reuse this exact gradient inside Cheese's silhouette so there is no flat
  // backing or row banding at fractional Retina/UI scales.
  const background=()=>gradient;
  ctx.save();ctx.beginPath();ctx.rect(x,y,w,h);ctx.clip();
  ctx.fillStyle=gradient;ctx.fillRect(x,y,w,h);
  ctx.font='12px Menlo, monospace';ctx.textBaseline='middle';ctx.textAlign='left';
  if(light.indoor){ctx.fillStyle='#9bb9cd';ctx.fillText('/\\',x+15,y+h*.5);ctx.fillText('/|\\',x+w-36,y+h*.7);}
  else if(light.night){
    ctx.fillStyle='#bed4d9';
    for(const [u,v,c] of [[.06,.12,'+'],[.26,.09,'.'],[.68,.14,'*'],[.92,.25,'+'],[.86,.45,'.']])ctx.fillText(c,x+u*w,y+v*h);
    ctx.fillStyle='#ece6b8';ctx.fillText(')',x+w*.1,y+h*.28);
  }else{
    ctx.fillStyle=light.twilight>.4?'#e9bf83':'#f3dfa2';
    if(!/rain|storm|fog/.test(scene.weather||''))ctx.fillText(light.twilight>.4?'(_)' : '\\|/',x+w*.06,y+h*.22);
    ctx.fillStyle=mixColor(light.skyHorizon,'#d4dfcd',.5);
    ctx.fillText('~~--~~',x+14+Math.sin(clock*.2)*3,y+h*.12);
    ctx.fillText('.--~~',x+w-58+Math.sin(clock*.17)*2,y+h*.28);
  }
  ctx.fillStyle=mixColor(light.groundFar,'#abc291',.35);
  for(let i=0;i<4;i++){ctx.fillText('/|',x+6+i*9,y+h-12-(i%2)*7);ctx.fillText('|\\',x+w-40+i*9,y+h-10-((i+1)%2)*7);}
  ctx.restore();return {light,background};
}
