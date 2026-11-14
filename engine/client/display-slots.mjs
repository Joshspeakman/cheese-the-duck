// Where displayed things stand inside each display host, in the host drawing's own
// cells: [x centre, base row]. Lowest shelf first (display fills bottom-up).
export const DISPLAY_SLOTS={
 trophy_case:[[22,61],[48,61],[74,61],[22,42],[48,42],[74,42],[22,23],[48,23]],
 cabinet:[[18,53],[30,53],[52,53],[64,53],[78,53],[18,32],[30,32],[52,32],[64,32],[78,32]],
};
// Pixel placement of slot i on a drawn host (same projection as repertoire geometry).
export function slotPoint(home,i,sx,sy){
 const s=DISPLAY_SLOTS[home.id]?.[i];if(!s)return null;
 const unit=sx*home.scale*(home.detailScale||1),hh=unit*1.5,left=home.x*sx-home.width*unit/2,top=home.y*sy-home.art.length*hh;
 return {x:left+s[0]*unit,y:top+(s[1]+1)*hh,unit};
}
