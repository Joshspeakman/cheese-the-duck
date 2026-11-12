// Expand the visible native extent around the requested center. The playfield
// still fills the canvas, while fixed native rig cells retain their 1:1.5 art.
export function displayCamera(camera={x:0,y:0,w:132,h:42},sx=1,sy=1){
 const ratio=42*sy/(132*sx*1.5),w=Math.max(camera.w,camera.h/ratio),h=Math.max(camera.h,camera.w*ratio);
 return {x:camera.x+(camera.w-w)/2,y:camera.y+(camera.h-h)/2,w,h};
}
// World Cheese uses one fixed native rig grid before, during and after activity.
// Visitors/catalogue-only sprites retain the previous presentation until adopted.
export function actorPitches(character,sx,sy){
 const c=(character.physicalActorProjection||character.physicalCastleActor)?.camera;
 return c?{cw:character.scale*132/c.w*sx,ch:character.scale*42/c.h*sy}:{cw:character.scale*sx,ch:character.scale*sx*1.5};
}
export function hasPhysicalActorProjection(character){return Boolean(character.physicalActorProjection||character.physicalCastleActor);}
