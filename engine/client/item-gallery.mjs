import {catalog,itemSprite,ItemPainter} from './ultra-items.mjs';
import {wearableCatalog,wearableSpec} from './wearables.mjs';
import {characterSprite,drawCharacter} from './ultra-characters.mjs';
import {STAGES,ACTIONS} from './scruffy-sprites.mjs';

// A presentation-only art browser: no inventory or simulation commands.
export class ItemGallery {
  constructor(motion=()=>true){
    this.motion=motion;this.painter=new ItemPainter();this.page=0;this.drawn=[];
    const dialog=document.createElement('dialog');this.dialog=dialog;dialog.id='item-gallery';
    dialog.innerHTML=`<div class="gallery-head"><div><strong>THE POND CATALOG</strong><p>${catalog.length} items · Artwork preview only</p></div><button class="gallery-close" aria-label="Close item catalog">Close [Esc]</button></div><div class="gallery-filters"><label>Find an item <input type="search" placeholder="Hats, fountains, fish, treasures…"></label><label>Category <select aria-label="Item category"><option value="">All items</option></select></label><label class="gallery-still"><input type="checkbox"> Pause animation</label></div><div class="gallery-grid"></div><div class="gallery-pages"><button class="gallery-prev">Previous</button><span aria-live="polite"></span><button class="gallery-next">Next</button></div>`;
    document.body.append(dialog);
    this.grid=dialog.querySelector('.gallery-grid');this.search=dialog.querySelector('input[type=search]');this.select=dialog.querySelector('select');this.pause=dialog.querySelector('input[type=checkbox]');this.status=dialog.querySelector('[aria-live]');
    const controls=document.createElement('div');controls.className='gallery-filters';
    controls.innerHTML='<label>Preview <select class="gallery-mode"><option value="art">Item artwork</option><option value="wear">Wearables on Cheese</option></select></label><label class="gallery-fit" hidden>Age <select class="gallery-age"></select></label><label class="gallery-fit" hidden>Action <select class="gallery-action"></select></label><label class="gallery-fit" hidden>Facing <select class="gallery-facing"><option value="right">Right</option><option value="left">Left</option></select></label>';
    this.grid.before(controls);this.mode=controls.querySelector('.gallery-mode');this.age=controls.querySelector('.gallery-age');this.action=controls.querySelector('.gallery-action');this.facing=controls.querySelector('.gallery-facing');
    for(const stage of STAGES)this.age.add(new Option(stage.name,stage.id));this.age.value='adult';
    for(const action of ACTIONS)this.action.add(new Option(action.name,action.id));this.action.value='walking';
    this.mode.onchange=()=>{this.page=0;this.categories();this.populate();controls.querySelectorAll('.gallery-fit').forEach(label=>label.hidden=this.mode.value!=='wear');};
    this.categories();
    this.search.oninput=this.select.onchange=()=>{this.page=0;this.populate();};
    dialog.querySelector('.gallery-close').onclick=()=>dialog.close();
    dialog.querySelector('.gallery-prev').onclick=()=>{this.page--;this.populate();};
    dialog.querySelector('.gallery-next').onclick=()=>{this.page++;this.populate();};
    dialog.addEventListener('close',()=>{cancelAnimationFrame(this.raf);document.getElementById('world')?.focus();});
  }
  get open(){return this.dialog.open;}
  entries(){return this.mode.value==='wear'?wearableCatalog.map(item=>({...item,category:wearableSpec(item.id).slot,aliases:[]})):catalog;}
  categories(){
    this.select.replaceChildren(new Option('All items',''));
    for(const value of [...new Set(this.entries().map(item=>item.category))].sort())this.select.add(new Option(value[0].toUpperCase()+value.slice(1),value));
  }
  show(){this.dialog.showModal();this.populate();this.search.focus();this.tick(0);}
  populate(){
    const query=this.search.value.trim().toLowerCase(),category=this.select.value;
    const wearing=this.mode.value==='wear';
    this.dialog.querySelector('.gallery-head p').textContent=wearing?`${wearableCatalog.length} fitted wearables · Try-on preview only`:`${catalog.length} items · Artwork preview only`;
    const items=this.entries().filter(item=>(!category||item.category===category)&&(!query||[item.id,item.name,item.description,item.rarity,...item.aliases].join(' ').toLowerCase().includes(query)));
    const pages=Math.max(1,Math.ceil(items.length/24));this.page=Math.max(0,Math.min(this.page,pages-1));this.grid.replaceChildren();this.drawn=[];
    for(const item of items.slice(this.page*24,this.page*24+24)){
      const card=document.createElement('article'),canvas=document.createElement('canvas'),title=document.createElement('h3'),description=document.createElement('p'),rarity=document.createElement('small');
      canvas.width=500;canvas.height=340;canvas.setAttribute('aria-label',item.name+(wearing?' fitted on Cheese':' ASCII artwork'));title.textContent=item.name;description.textContent=wearing?wearableSpec(item.id).motion:item.description;rarity.textContent=item.rarity+' / '+item.category;
      card.append(canvas,title,description,rarity);this.grid.append(card);this.drawn.push({canvas,item,card});
    }
    this.status.textContent=items.length?`${items.length} ${items.length===1?'item':'items'} · Page ${this.page+1} of ${pages}`:'No matching items';
    this.dialog.querySelector('.gallery-prev').disabled=this.page===0;this.dialog.querySelector('.gallery-next').disabled=this.page===pages-1;this.grid.scrollTop=0;
  }
  tick(time){
    if(!this.open)return;
    if(!this.lastTime||time-this.lastTime>=100){
      const motion=this.motion()&&!this.pause.checked;
      for(const entry of this.drawn){
        const {canvas,item,card}=entry;
        const rect=card.getBoundingClientRect(),bounds=this.grid.getBoundingClientRect();if(rect.bottom<bounds.top||rect.top>bounds.bottom)continue;
        const ctx=canvas.getContext('2d');
        ctx.fillStyle='#10262c';ctx.fillRect(0,0,500,340);
        if(this.mode.value==='wear'){
          const duck={stage:this.age.value,state:this.action.value,facing:this.facing.value==='right',cosmetics:{preview:item.id}},key=[duck.stage,duck.state,duck.facing].join(':');
          // Fit the whole animation, not its current frame, so the preview stays
          // large enough to inspect without zooming in and out on each step.
          if(entry.fitKey!==key){
            let left=40,right=0,top=25,bottom=0;
            for(let frame=0;frame<16;frame++){
              characterSprite(duck,frame*.4).art.forEach((line,y)=>{for(let x=0;x<line.length;x++)if(line[x]!==' '){left=Math.min(left,x);right=Math.max(right,x);top=Math.min(top,y);bottom=Math.max(bottom,y);}});
            }
            entry.fit={cx:(left+right+1)/2,cy:(top+bottom+1)/2,w:right-left+1,h:bottom-top+1};entry.fitKey=key;
          }
          const model=characterSprite(duck,motion?time/1000:0),fit=entry.fit,cw=Math.min(28,440/(fit.w+2),270/((fit.h+2)*1.5));
          drawCharacter(ctx,{...model,scale:1,x:250/cw+model.anchorX-fit.cx,y:170/cw+(model.groundRow-fit.cy)*1.5},cw,cw,'#10262c');
          card.querySelector('small').style.color=wearableSpec(item.id).color;continue;
        }
        const model=itemSprite(item.id,time/1000,{motion}),cw=Math.min(16,440/(model.width+2),235/((model.art.length+2)*1.5));
        if(model.emissive){const gradient=ctx.createRadialGradient(250,170,0,250,170,150);gradient.addColorStop(0,model.accent+'25');gradient.addColorStop(1,model.accent+'00');ctx.fillStyle=gradient;ctx.fillRect(0,0,500,340);}
        this.painter.draw(ctx,model,250,285,cw);card.querySelector('small').style.color=model.rarity;
      }this.lastTime=time;
    }
    this.raf=requestAnimationFrame(t=>this.tick(t));
  }
}
