// Browser-side assertions shared by the parameterized native evidence runner.
import {SceneCanvas} from '../client/ultra-renderer.mjs';
import {characterSprite} from '../client/ultra-characters.mjs';
import {castleGeometry,castleActorPhysical,sharedCastleRecord,sharedCastleSource,eggCaregiverScene,CASTLE_SCORES} from '../client/castle-care.mjs';
import {castleActiveWork,castleTransit,CASTLE_DIAL} from '../client/castle-air-geometry.mjs';
import {projectCastleWorld,castleArtWorld} from '../client/castle-projection.mjs';
import {actorPitches} from '../client/actor-projection.mjs';
import GEOMETRY from '../client/animation/castle-geometry.json' with {type:'json'};
import {AirMatrixCoverage,airFrameIdentity} from './castle-air-matrix-coverage.mjs';
import {airSessionEvidence} from './castle-air-session-evidence.mjs';
const check=(ok,label)=>{if(!ok)throw Error(label);};
const near=(a,b,label)=>check(Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<1e-7,label+': '+a+' != '+b);
export function replayNativeAir(frames,{manifest=null}={}){
 const sessionEvidence=airSessionEvidence(frames);frames=sessionEvidence.frames;
 check(Array.isArray(frames)&&(frames.length||manifest),'Native air frames required');
 const view=new SceneCanvas();view.effects.level='quiet';
 const matrix=manifest?new AirMatrixCoverage(manifest):null,variants=[],imageCounts={};
 if(matrix)for(const frame of frames)matrix.match(frame);
 const images={},bindings={},eggs=new Map();let finalActorChecks=0,cases=0,roots=0,contacts=0,observations=0,eggChecks=0,transits=0,baselineFrames=0;
 function bindingFor(s,outer,work){
  const {mode,cast,adapter,age}=airFrameIdentity(s),occurrence=outer.atomic?.occurrence_id||'atomic',key=[s._airMatrixCase||'',mode,age,adapter,cast,outer.id,outer.air_procedure?.attempt||'',occurrence].join('/');
  const binding=bindings[key]??={mode,age,cast,adapter,matrixCase:s._airMatrixCase||null,outer:outer.id,atomic:castleTransit(work)?null:work.id,occurrence,cases:0,phases:new Set(),effects:new Set()};binding.cases++;binding.phases.add(outer.physical.phase);return binding;
 }
 for(const [width,height]of [[1200,800],[1800,800],[900,1100]])for(const shifted of [false,true])for(const reduced of [false,true]){
  view.resize(width,height);
  const variant=width+'x'+height+'/camera:'+Number(shifted)+'/reduced:'+Number(reduced);variants.push(variant);
  for(const [index,source]of frames.entries()){
   const s=structuredClone(source);if(shifted)s.camera={...s.camera,x:s.camera.x+3,y:s.camera.y+2};if(reduced)s.motion=false;
   const original=JSON.stringify(s),outer=s.living?.plan?.carnival_work,time=index*.2;view.draw(s,time,.2);check(JSON.stringify(s)===original,'Native source mutated');
   if(!outer){
    const capture=s._airSessionCapture;
    if(capture){
     check(capture.phase==='done','Missing live session record');check(!view.world.objects.some(o=>o.carnivalRiders?.length),'Ended session retained staged actors');
     const home=view.world.objects.find(o=>o.instance===capture.shared.instance);
     for(const actor of [capture.operator,capture.observer].filter(Boolean)){
      const source=actor.actor==='cheese'?s.duck:[s.visitor,s.rareVisitor,s.storyActor].find(v=>v?.id===(actor.render_id||actor.actor));
      check(source,'Missing final actual actor');near(source.x,actor.root[0],'final source x');near(source.y,actor.root[1],'final source y');
      const model=view.world.characters.find(c=>actor.actor==='cheese'?c.cheese:c.profileId===actor.cast);
      check(model&&!model.performance,'Final actor retained mechanical pose');const pixel=projectCastleWorld(home.physicalCastle,actor.root,view.sx,view.sy),pitch=actorPitches(model,view.sx,view.sy);
      near(model.x*view.sx,pixel.x,'final display x');near(model.y*view.sy,pixel.y,'final display y');near(pitch.ch/pitch.cw,1.5,'final glyph aspect');finalActorChecks++;roots++;
     }
    }
    baselineFrames++;continue;
   }
   const work=castleActiveWork(outer),shared=sharedCastleRecord(outer);check(work,'Invalid native occurrence');if(outer.shared_physical)check(shared,'Invalid native role binding');
   const home=view.world.objects.find(o=>o.instance===s.living.plan.instance),members=home?.carnivalRiders;
   if(matrix){const entry=matrix.match(s);near(home?.physicalCastle?.origin?.[0],entry.center[0],'selected castle center x');near(home?.physicalCastle?.origin?.[1],entry.center[1],'selected castle center y');}
   // Solo approach is intentionally ordinary locomotion until the plan reaches
   // its activity. Assert the actually drawn model, without a staging proxy.
   if(!shared&&outer.physical_pilot&&s.living.plan.phase==='approach'&&outer.physical.phase==='approach'){
    check(!members?.length&&s._physicalEvent===undefined,'Approach acquired a staged effect');const cheese=view.world.characters.filter(c=>c.cheese);check(cheese.length===1,'Missing ordinary approaching Cheese');const c=cheese[0],p=projectCastleWorld(home.physicalCastle,outer.physical.root,view.sx,view.sy),pitch=actorPitches(c,view.sx,view.sy);
    near(s.duck.x,outer.physical.root[0],'approach source x');near(s.duck.y,outer.physical.root[1],'approach source y');near(c.x*view.sx,p.x,'ordinary approach display x');near(c.y*view.sy,p.y,'ordinary approach display y');near(pitch.ch/pitch.cw,1.5,'ordinary approach aspect');check(!c.performance&&!c.grip,'Approach invented control pose');
    bindingFor(s,outer,work);if(matrix)matrix.record(s,variant);roots++;cases++;continue;
   }
   check(members?.length===(shared&&shared.mode!=='egg-caregiver'?2:1),'Wrong mechanical actor count');
   const operator=members.find(m=>m.role==='a'),isEgg=shared?.mode==='egg-caregiver',guest=sharedCastleSource(s,shared),cast=shared?.operator.cast||'cheese',mode=isEgg?'egg':shared?.mode==='flight-observer'?'flight':shared?'shared':'solo';
   check(operator.actor===outer.physical.actor,'Wrong native operator');
   if(outer.physical.actor==='cheese'){near(s.duck.x,outer.physical.root[0],'source Cheese x');near(s.duck.y,outer.physical.root[1],'source Cheese y');}
   else{check(guest,'Missing actual visitor source');near(guest.x,outer.physical.root[0],'source guest x');near(guest.y,outer.physical.root[1],'source guest y');check(operator.character.profileId===cast,'Wrong visitor profile');}
   for(const member of members){
    const physical=castleActorPhysical(outer,member.role),g=castleGeometry(home,member,view.sx,view.sy),p=projectCastleWorld(home.physicalCastle,physical.root,view.sx,view.sy),pitch=actorPitches(g.character,view.sx,view.sy);
    check(g.authoritativeRoot,'Renderer owns actor root');near(g.character.x*view.sx,p.x,'displayed root x');near(g.character.y*view.sy,p.y,'displayed root y');near(pitch.ch/pitch.cw,1.5,'glyph aspect');roots++;
    if(member.watch){check(!g.tip&&!g.points.length&&!g.observation?.ready,'Observer acquired mechanical authority');check(!member.character.grip,'Observer acquired grip');}
    if(member.watch){const sourceActor=shared.mode==='flight-observer'?guest:s.duck;near(sourceActor.x,physical.root[0],'source watcher x');near(sourceActor.y,physical.root[1],'source watcher y');}
    if(physical.phase!=='hold'||s.living.plan.paused)check(!g.tip&&!g.points.length&&!g.observation?.ready,'Premature or paused mechanics');
   }
   if(isEgg){
    check(eggCaregiverScene(s),'Invalid original egg binding');const egg=view.world.characters.find(c=>c.cheese),r=shared.recipient,expected=characterSprite({...s.duck,motion:s.motion!==false,performance:null},s.motion===false?0:time);
    check(egg&&!egg.physicalCastleActor,'Egg staged as a mechanical actor');const ep=projectCastleWorld(home.physicalCastle,r.root,view.sx,view.sy);near(egg.x*view.sx,ep.x,'egg root x');near(egg.y*view.sy,ep.y,'egg root y');roots++;
    for(const key of ['art','fills','offsetY','phase','scale','facing','rig','grip','bill','performance'])check(JSON.stringify(egg[key])===JSON.stringify(expected[key]),'Original egg changed '+key);
    const key=shared.attempt,identity=JSON.stringify([r.token,r.root,r.facing]);if(eggs.has(key))check(eggs.get(key)===identity,'Egg moved within caregiver attempt');else eggs.set(key,identity);eggChecks++;
   }
   const adapter=airFrameIdentity(s).adapter,g=castleGeometry(home,operator,view.sx,view.sy),binding=bindingFor(s,outer,work);
   if(castleTransit(work)){check(!g.tip&&!g.points.length&&!g.observation,'Transit acquired effect authority');transits++;}
   else if(work.id==='castle_gauge_check'){
    check(!g.tip&&!g.points.length,'Gauge created mechanical hand bridge');if(g.observation?.ready)check(g.observation.eyes.length,'Closed eyes credited');
    if(outer.physical.observation_target){const [x,y]=CASTLE_DIAL.needle_origin,target=castleArtWorld(home.physicalCastle.origin,x,y,{center:true});near(outer.physical.observation_target[0],target[0],'needle native x');near(outer.physical.observation_target[1],target[1],'needle native y');}
   }
   if(s._physicalEvent!==undefined){
    const event=s._physicalEvent,spec=CASTLE_SCORES[work.id],effect=spec?.effects[event];check(effect&&work.events.includes(event),'Wrong consumed occurrence event');near(work.ride_elapsed,effect[0]*spec.duration,'consumed event clock');binding.effects.add(event);
    if(effect[1]==='inspection'){
     check(outer.physical.observation_ready===true&&outer.physical.contact_ready===false&&g.observation?.ready,'Read without actual observation readiness');check(g.observation.eyes.length,'Read without visible eyes');observations++;
    }else{
     check(outer.physical.contact_ready===true&&g.tip&&g.reachable,'Missing actual effect contact');const anchor=GEOMETRY.controls[outer.physical.station],target=castleArtWorld(home.physicalCastle.origin,anchor.x,anchor.y,{center:true}),pixel=projectCastleWorld(home.physicalCastle,target,view.sx,view.sy);
     near(outer.physical.target[0],target[0],'control native x');near(outer.physical.target[1],target[1],'control native y');near(g.tip.x,pixel.x,'contact pixel x');near(g.tip.y,pixel.y,'contact pixel y');contacts++;
    }
   }
   const selectedImage=!matrix||['castle_grill_clean','castle_gauge_check'].includes(work.id)&&(s._physicalEvent===undefined||s._physicalEvent===0||s._physicalEvent===1);
   if(selectedImage&&!shifted&&!reduced&&['cheese','friend:marco','friend:rocket','wise_owl','lost_duckling'].includes(cast)){
    const imageKey=[mode,adapter,cast.replace('friend:',''),s.duck.stage,outer.id,work.id,outer.physical.phase,s._physicalEvent??'travel',width+'x'+height].join('-');
    if((imageCounts[width]||0)<60&&!images[imageKey]){images[imageKey]=view.canvas.toDataURL();imageCounts[width]=(imageCounts[width]||0)+1;}
   }
   if(matrix)matrix.record(s,variant);
   cases++;
  }
 }
 const coverage=Object.fromEntries(Object.entries(bindings).map(([key,b])=>[key,{...b,phases:[...b.phases],effects:[...b.effects],allAtomicEffects:b.atomic?b.effects.size===CASTLE_SCORES[b.atomic].effects.length:null}]));
 return {images,cases,roots,finalActorChecks,sessions:sessionEvidence.sessions,contacts,observations,eggChecks,transits,baselineFrames,sourceFrames:frames.length,windowSizes:3,cameras:2,motionModes:2,coverage,...(matrix?{matrix:matrix.finish(variants)}:{}),scope:'native-snapshots-render-only'};
}
