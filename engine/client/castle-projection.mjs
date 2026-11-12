import GEOMETRY from './animation/castle-geometry.json' with {type:'json'};
// These are fixed native dimensions, independent of camera/window/aspect fit.
export const CASTLE_UNIT=.66*GEOMETRY.detail_scale;
const defaultCamera={x:0,y:0,w:132,h:42};
export function projectCastleWorld(projection,point,sx=1,sy=1){
 const c=projection.camera||defaultCamera;
 return {x:(24+(point[0]-c.x)*192/c.w)*sx,y:(46+(point[1]-c.y)*47/c.h)*sy};
}
export function castleArtWorld(origin,x,y,{center=false}={}){
 return [origin[0]+(x+(center ? .5 : 0)-GEOMETRY.width/2)*CASTLE_UNIT*132/192,
  origin[1]+(y+(center ? .5 : 0)-GEOMETRY.height)*CASTLE_UNIT*42/47];
}
export function castleArtFrame(home,sx,sy){
 if(!home.physicalCastle)return null;
 const p=home.physicalCastle,c=p.camera||defaultCamera,origin=projectCastleWorld(p,p.origin,sx,sy);
 const unit=CASTLE_UNIT*132/c.w*sx,uh=CASTLE_UNIT*42/c.h*sy;
 return {unit,uh,left:origin.x-GEOMETRY.width*unit/2,top:origin.y-GEOMETRY.height*uh,origin,
  ground:origin.y+(GEOMETRY.ground_row-GEOMETRY.height)*uh};
}
export {actorPitches as castleActorPitches} from './actor-projection.mjs';
