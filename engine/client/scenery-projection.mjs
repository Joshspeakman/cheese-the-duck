// Physical Home Pond scenery is authored in the original canonical grid.
// These conversions preserve its native extents under every display camera.
export const canonicalSceneryPoint=(x,y)=>[(x-24)*132/192,(y-46)*42/47];
export function projectSceneryCell(camera,x,y){
 const c=camera||{x:0,y:0,w:132,h:42};
 return {x:24+(x-24-c.x*192/132)*132/c.w,y:46+(y-46-c.y*47/42)*42/c.h,w:132/c.w,h:42/c.h};
}
export function nativeSceneryBounds(cells){
 const left=Math.min(...cells.map(c=>c[0])),top=Math.min(...cells.map(c=>c[1])),right=Math.max(...cells.map(c=>c[0]+1)),bottom=Math.max(...cells.map(c=>c[1]+1)),[x,y]=canonicalSceneryPoint(left,top);
 return {x,y,w:(right-left)*132/192,h:(bottom-top)*42/47};
}
