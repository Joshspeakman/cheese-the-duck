export const BIOMES = ['pond','forest','meadow','garden','riverside','beach','swamp','mountains','urban'];
export const LOCATIONS = ['Home Pond','Mushroom Grove','Sunny Meadow','Vegetable Patch','Waterfall','Shipwreck Cove','Misty Marsh','Crystal Cave','Park Fountain'];
export function scene(overrides={}) {
 return {biome:'pond',location:'Home Pond',season:'spring',hour:15,weather:'sunny',intensity:.7,
 motion:true,particles:true,weatherEffects:true,camera:{x:0,y:0,w:132,h:42},
 duck:{name:'Cheese',x:65,y:24,facing:true,state:'idle',stage:'adult',cosmetics:{}},
 items:[],structures:[],visitor:null,interaction:null,...overrides};
}
