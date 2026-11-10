import {duckRig,DUCK_AGES} from './duck-rig.mjs';
// Original personalities, plumage, and signature accessories, rebuilt on the
// compact D10 skeleton. No visitor names, dialogue or relationships are changed.
const STYLES={
 adventurous:{tints:['#c6a074','#8fb59a','#b6d7a1'],gear:['hat_cowboy','bandana','backpack_tiny'],height:83},
 scholarly:{tints:['#aab4bb','#c2ccce','#8ebdd9'],gear:['glasses_nerd','scarf_winter'],height:80},
 artistic:{tints:['#d1c7b6','#e0d8c0','#c79cdb'],gear:['hat_beret','flower_lei'],height:78},
 playful:{tints:['#d9b767','#efcf88','#e99b93'],gear:['hat_party','bowtie_red'],height:72},
 mysterious:{tints:['#777586','#9297a2','#a69ace'],gear:['masquerade_mask','cape'],height:84},
 generous:{tints:['#cfb475','#ead391','#dda3b5'],gear:['bow_tie_pink'],height:80},
 foodie:{tints:['#ce9065','#e0ae7f','#ddd8bb'],gear:['hat_chef'],height:79},
 athletic:{tints:['#ae896a','#c6ae81','#e1a35c'],gear:['bandana'],height:86},
};
export const VISITOR_STYLES=STYLES;
export function visitorRig(duck,time=0){
 const style=STYLES[duck.personality]||STYLES.adventurous;
 const seed=[...(duck.name||'')].reduce((n,c)=>n+c.charCodeAt(0),0);
 const age=DUCK_AGES[5],art=age.art.slice();
 // Five distinct feather marks per personality make names recognizable in a flock.
 art[0]=['                      ,--.','                      /~-.','                       ,~.','                       /~','                      .--,'][seed%5];
 const activity=duck.activity||duck.state||'idle';
 const state=/reading|painting|giving/.test(activity)?'preening':/bounce|happy|exercise/.test(activity)?'dancing':activity;
 const gear=duck.id==='celebrity_duck'?['hat_crown','bow_tie_pink']:style.gear;
 const model=duckRig({...duck,state,cosmetics:Object.fromEntries(gear.map((id,i)=>[i,id]))},time+seed%5,{...age,...style,art});
 const {rig}=model,phase=model.phase,rows=model.art.map(r=>[...r]),tones=model.tones.map(r=>[...r]);
 // Hand-held occupations travel with the posed wing, not a floating portrait.
 const props={scholarly:[' .----.',' |~ ~ |',' |____|'],artistic:[' /|','(o:*.)',' \\__/'],foodie:[' .---.','(=o=o=)'," '---'"],generous:['  _+_',' |+ +|',' |___|'],adventurous:[' .--.',' |/\\|',' |__|'],athletic:[' o===o'],playful:[' .o.','( * )'," 'o'"],mysterious:['  .',' (*.)',"  ' "]};
 if(!/walking|swimming|sleeping/.test(model.action)){
  const lines=props[duck.personality]||[],x=rig.body.x+rig.body.w-4,y=rig.body.y+3+(phase%4===1?1:0);
  lines.forEach((line,j)=>[...line].forEach((c,i)=>{const xx=duck.facing===false?model.width-1-x-i:x+i;if(c!==' '&&rows[y+j]?.[xx]!==undefined){rows[y+j][xx]=c;tones[y+j][xx]='p';}}));
 }
 return {...model,art:rows.map(r=>r.join('')),tones:tones.map(r=>r.join('')),design:'d10-visitor',personality:duck.personality};
}
