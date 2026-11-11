// Authoring source: low-control scores plus ordered, purposeful work procedures.
// Both the native simulation and renderer consume the same expanded artifact.
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
const root=new URL('./client/animation/',import.meta.url);
const read=name=>JSON.parse(fs.readFileSync(new URL(name,root),'utf8'));
const controls=read('castle-controls.json'),procedures=read('castle-procedures.json');
const scores={...controls};
for(const [id,recipe]of Object.entries(procedures)){
 const parts=recipe.steps.map(key=>{if(!controls[key])throw Error('Unknown step '+key);return controls[key];});
 const gap=3,duration=parts.reduce((n,p)=>n+p.duration,0)+gap*(parts.length-1);
 const score={item:'bounce_house',label:recipe.label,station:parts[0].station,partner:parts[0].partner,duration,
  entryDuration:parts[0].duration*.14,track:[],effects:[],stations:[],partnerStations:[],segments:[],steps:recipe.steps,
  weatherSafe:parts.every(p=>p.weatherSafe),note:recipe.note};
 let clock=0;
 for(const [i,part]of parts.entries()){
  // Each resident walks to the next component; the work clock includes this.
  if(i)clock+=gap;
  const time=at=>(clock+at*part.duration)/duration;
  score.segments.push([time(0),time(1),recipe.steps[i],part.label]);
  for(const [at,pose]of part.track)score.track.push([time(at),pose]);
  for(const [at,key,value]of part.effects)score.effects.push([time(at),key,value]);
  for(const [at,station]of part.stations||[[0,part.station]])score.stations.push([time(at),station]);
  score.partnerStations.push([time(0),part.partner]);
  clock+=part.duration;
 }
 scores[id]=score;
}
const output=JSON.stringify(scores,null,2)+'\n',target=new URL('castle-care.json',root);
if(process.argv.includes('--check')){
 if(fs.readFileSync(target,'utf8')!==output)throw Error('Rebuild castle-care.json with node engine/build-castle-care.mjs');
}else fs.writeFileSync(target,output);
console.log(`${Object.keys(controls).length} controls + ${Object.keys(procedures).length} procedures: ${fileURLToPath(target)}`);
