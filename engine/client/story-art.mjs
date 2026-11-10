import {characterSprite} from './ultra-characters.mjs';
import {eventModel} from './event-art.mjs';

// Story characters use the same articulated feather/face/prop rigs as guests.
// They retain their own story identity and never become a friendship reward.
export function storyModel(story,actor={},time=0,motion=true){
 const t=motion?time:0;
 const model=story.id==='lost_duckling'
  ?characterSprite({...actor,id:'story:lost_duckling',castId:'lost_duckling',name:'Little visitor',stage:'duckling',state:actor.state||'signature'},t,true)
  :eventModel({id:story.id,asset:story.asset,...actor},t,motion);
 return {...model,id:'story:'+story.id,story:true,event:true,visitor:false};
}
