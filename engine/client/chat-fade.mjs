// Conversation visibility follows speech, not the world's event-log traffic.
export class ChatFade {
 constructor(now=0){this.lastSpeech=now;this.lastAttention=now;this.delay=14000;this.duration=1600;this.opacity=1;}
 wake(now){this.lastAttention=now;this.opacity=1;}
 spoke(now){this.lastSpeech=now;this.wake(now);}
 update(now,{held=false,reducedMotion=false}={}){
  if(held){this.wake(now);return 1;}
  const elapsed=Math.max(0,now-Math.max(this.lastSpeech,this.lastAttention)-this.delay);
  this.opacity=reducedMotion?(elapsed>0?0:1):1-Math.min(1,elapsed/this.duration);
  return this.opacity;
 }
}
