// Cosmetic drift integrates the native wind vector. It never changes weather,
// object clocks or saves. Bearings point INTO the wind, like the copper vane;
// airborne leaves and precipitation travel the opposite way.
const finite=(n,fallback)=>Number.isFinite(n)?n:fallback;
export const wrap=(n,size)=>((n%size)+size)%size;
export function windVector(scene){
 const e=scene.living?.ecology||{},heading=wrap(finite(e.wind_heading,0),1),strength=Math.max(0,Math.min(1,finite(e.wind,.2)));
 const a=heading*Math.PI*2;
 return {x:-Math.cos(a)*strength,y:-Math.sin(a)*strength,strength,heading};
}
export class WeatherDrift {
 constructor(){this.x=0;this.y=0;this.location=null;this.vector={x:0,y:0,strength:0,heading:0};}
 update(scene,dt,exposed=true){
  if(scene.location!==this.location){this.x=0;this.y=0;this.location=scene.location;}
  this.vector=exposed?windVector(scene):{x:0,y:0,strength:0,heading:0};
  // A stalled window resumes from its old particles, without jumping through
  // hours of drift. Small regular steps integrate identically at 30/60/120 Hz.
  const step=scene.motion===false?0:Math.max(0,Math.min(.25,finite(dt,0)));
  this.x+=this.vector.x*step;this.y+=this.vector.y*step;
  return this;
 }
}
