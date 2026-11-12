// Read-only samples of the existing egg drawing, never an egg action score.
import {characterSprite} from '../client/ultra-characters.mjs';
import {DUCK_AGES} from '../client/duck-designs.mjs';
const pace=DUCK_AGES.find(a=>a.id==='egg').pace,rate=pace/4.5;
export function eggShellSampleTimes(){
 const times=new Set([0]),extrema=new Set();
 for(let phase=0;phase<8;phase++)times.add((phase+.5)/(5*rate));
 // The original idle offset is .1*sin(2*cycle). Sample true extrema until
 // both signs occur in every discrete shell phase, rather than approximating
 // the wobble from a finite wall-clock interval.
 for(let k=0;k<10000&&extrema.size<16;k++){
  const cycle=Math.PI/4+k*Math.PI/2,time=cycle/rate,c=characterSprite({stage:'egg',state:'idle',facing:true},time),sign=c.offsetY>0?'positive':'negative';
  const key=c.phase+':'+sign;if(!extrema.has(key)){extrema.add(key);times.add(time);}
 }
 if(extrema.size!==16)throw Error('Egg shell extrema sampling incomplete');
 return [...times].sort((a,b)=>a-b);
}
export function eggShellGeometry(character){
 if(character.rig!==null||character.grip!==null||character.bill!==null||character.clipped||character.scale!==.66)throw Error('Original egg anatomy changed');
 const shift=(character.offsetY||0)/1.5;
 const ink=[];character.art.forEach((row,y)=>[...row].forEach((ch,x)=>{if(ch!==' ')ink.push({x,y,w:1});}));
 const shell=character.fills.filter(f=>f.tone==='c'),bottom=Math.max(...shell.map(f=>f.y));
 function bounds(cells){const x=Math.min(...cells.map(c=>c.x))-character.anchorX,y=Math.min(...cells.map(c=>c.y))-character.groundRow+shift;return {x,y,w:Math.max(...cells.map(c=>c.x+c.w))-character.anchorX-x,h:Math.max(...cells.map(c=>c.y+1))-character.groundRow+shift-y};}
 return {body:bounds([...ink,...character.fills]),shell:bounds(shell),shell_base:bounds(shell.filter(f=>f.y===bottom))};
}
