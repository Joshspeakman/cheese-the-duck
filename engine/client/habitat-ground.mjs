import GROUND from './animation/habitat-ground.json' with {type:'json'};
export function homeShore(x){
 const gx=24+x*192/20;
 return (GROUND.bank+Math.sin(gx*GROUND.waveA[0]+GROUND.seed)*GROUND.waveA[1]+Math.sin(gx*GROUND.waveB[0])*GROUND.waveB[1]-46)*12/47;
}
export function homeBankOnScreen(x,camera={x:0,y:0,w:132,h:42}){
 const wx=camera.x+(x-24)/192*camera.w;
 return 46+(homeShore(wx*20/132)*42/12-camera.y)/camera.h*47;
}
export function itemSurface(id){return GROUND.waterItems.includes(id)?'water':GROUND.eitherItems.includes(id)?'either':'land';}
export function surfaceFits(id,box,y){
 const surface=itemSurface(id);
 if(surface==='either')return true;
 for(let x=box.x;x<=box.x+box.w+.001;x+=box.w/32){
  if(surface==='land'&&y+.35>homeShore(x))return false;
  if(surface==='water'&&y-.35<homeShore(x))return false;
 }
 return true;
}
