import test from 'node:test';
import assert from 'node:assert/strict';
import {characterSprite} from '../client/ultra-characters.mjs';
import {performancePose,PERFORMANCES} from '../client/performances.mjs';
import {GUEST_CAST} from '../client/guest-cast.mjs';
import {guestWalkingTime} from '../scripts/export-castle-guest-metrics.mjs';
import METRICS from '../client/animation/castle-guest-metrics.json' with {type:'json'};
import {specialSharedCastleFixture} from './castle-shared-fixtures.mjs';
import {LivingWorld} from '../client/ultra-world.mjs';
import {displayCamera} from '../client/actor-projection.mjs';
import {castleGeometry,CASTLE_SCORES,castlePose} from '../client/castle-care.mjs';
const species=['friendly_goose','wise_owl','mysterious_crow','grumpy_toad'];
function ink(c){for(const f of c.rig.feet){const x=c.facing?f.x:c.width-1-f.x;assert.equal(c.art[f.y]?.[x],'_',`${c.profileId} foot ${x},${f.y}`);}}
test('species pads are actual drawn underscores through all eight true walking phases and both facings',()=>{
 for(const cast of species){const profile=GUEST_CAST[cast],phases=new Set(),travel=METRICS.casts[cast].travel;
  for(const facing of [true,false])for(let phase=0;phase<8;phase++){
   const c=characterSprite({castId:cast,state:'walking',facing},guestWalkingTime(profile,phase),true);phases.add(c.phase);assert.equal(c.phase,phase);assert.equal(c.rig.feet.length,cast==='grumpy_toad'?4:2);ink(c);
   for(const f of c.rig.feet){const x=(facing?f.x:c.width-1-f.x)+.5-c.anchorX,y=f.y+.5-c.groundRow;assert(travel.feet.some(p=>p[0]===x&&p[1]===y));}
   const b=c.rig.supportBody,x=(facing?b.x:c.width-b.x-b.w)-c.anchorX,y=b.y-c.groundRow;assert(x>=travel.body.x&&x+b.w<=travel.body.x+travel.body.w);assert(y>=travel.body.y&&y+b.h<=travel.body.y+travel.body.h);
  }
  assert.equal(phases.size,8);
 }
 assert.equal(METRICS.casts.butterfly_fairy,undefined);assert.deepEqual(characterSprite({castId:'butterfly_fairy'},0,true).rig.feet,[]);
});
test('species pads follow performance torso translations and individual lifts without changing local body metadata',()=>{
 let negative=false,positive=false;
 for(const cast of species)for(const facing of [true,false])for(const motion of [true,false])for(const [id,spec]of Object.entries(PERFORMANCES))for(const frame of spec.a){
  const performance={kind:id,role:'a',progress:frame.at,motion},pose=performancePose(performance);if(!pose)continue;
  negative ||= pose.b<-.5;positive ||= pose.b>.5;
  const c=characterSprite({castId:cast,facing,performance},0,true);ink(c);assert.equal(c.rig.drawnBody.y,Math.round(c.rig.body.y+pose.b));
  for(const f of c.rig.feet){const lift=f.foot?pose.r:pose.l;assert.equal(f.y,Math.round(39-lift-Math.max(0,pose.b)+pose.b));}
 }
 assert(negative&&positive,'must exercise negative and positive body translation');
});
test('four species retain grounded pads and actual grip ink at every shared control contact',()=>{
 for(const cast of species)for(const [id,metrics]of Object.entries(METRICS.casts[cast].routines))for(const [index,metric]of metrics.entries())for(const motion of [true,false])for(const facing of [true,false]){
  const s=specialSharedCastleFixture(cast,'rare',id,index,{motion}),work=s.living.plan.carnival_work,c=characterSprite({castId:cast,facing,performance:{kind:'carnival',routine:work,role:'a',motion}},0,true);ink(c);assert(c.rig.feet.every(f=>f.y===39));assert.equal(c.art[c.grip.y]?.[c.grip.x],facing?')':'(');assert.equal(c.scale,metric.scale);
  const sx=5,sy=800/112,world=new LivingWorld(),result=world.render({...s,camera:displayCamera(s.camera,sx,sy)},0,0),home=result.objects.find(o=>o.id==='bounce_house'),operator=home.carnivalRiders.find(m=>m.role==='a'),g=castleGeometry(home,operator,sx,sy);assert(g.reachable&&g.tip);assert.equal(operator.character.profileId,cast);assert(Math.abs(g.tip.x-g.target.x)<1e-8&&Math.abs(g.tip.y-g.target.y)<1e-8);
 }
});
test('species support encloses actual head and torso fills throughout held scores in both facings',()=>{
 for(const cast of species)for(const id of ['castle_start','castle_door_open','castle_hose_stow'])for(let step=0;step<=100;step++)for(const facing of [true,false])for(const motion of [true,false]){
  const s=specialSharedCastleFixture(cast,'rare',id),w=s.living.plan.carnival_work;w.clock=w.ride_elapsed=step/100*CASTLE_SCORES[id].duration;w.physical.station=castlePose({id,stage:'service',clock:w.clock,ride_elapsed:w.clock}).station;
  const c=characterSprite({castId:cast,facing,performance:{kind:'carnival',routine:w,role:'a',motion}},0,true),b=METRICS.casts[cast].travel.body;ink(c);
  for(const f of c.fills.filter(f=>['b','g'].includes(f.tone))){const x=f.x-c.anchorX,y=f.y-c.groundRow;assert(x>=b.x&&x+f.w<=b.x+b.w,cast+' head/torso horizontal clearance');assert(y>=b.y&&y+1<=b.y+b.h,cast+' head/torso vertical clearance');}
 }
});
