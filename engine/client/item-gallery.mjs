import {catalog,itemSprite,ItemPainter} from './ultra-items.mjs';

// A presentation-only art browser: no inventory or simulation commands.
export class ItemGallery {
  constructor(motion=()=>true){
    this.motion=motion;this.painter=new ItemPainter();this.page=0;this.drawn=[];
    const dialog=document.createElement('dialog');this.dialog=dialog;dialog.id='item-gallery';
    dialog.innerHTML=`<div class="gallery-head"><div><strong>THE POND CATALOG</strong><p>${catalog.length} items · Artwork preview only</p></div><button class="gallery-close" aria-label="Close item catalog">Close [Esc]</button></div><div class="gallery-filters"><label>Find an item <input type="search" placeholder="Hats, fountains, fish, treasures…"></label><label>Category <select aria-label="Item category"><option value="">All items</option></select></label><label class="gallery-still"><input type="checkbox"> Pause animation</label></div><div class="gallery-grid"></div><div class="gallery-pages"><button class="gallery-prev">Previous</button><span aria-live="polite"></span><button class="gallery-next">Next</button></div>`;
    document.body.append(dialog);
    this.grid=dialog.querySelector('.gallery-grid');this.search=dialog.querySelector('input[type=search]');this.select=dialog.querySelector('select');this.pause=dialog.querySelector('input[type=checkbox]');this.status=dialog.querySelector('[aria-live]');
    for(const value of [...new Set(catalog.map(item=>item.category))].sort()){
      const option=document.createElement('option');option.value=value;option.textContent=value[0].toUpperCase()+value.slice(1);this.select.append(option);
    }
    this.search.oninput=this.select.onchange=()=>{this.page=0;this.populate();};
    dialog.querySelector('.gallery-close').onclick=()=>dialog.close();
    dialog.querySelector('.gallery-prev').onclick=()=>{this.page--;this.populate();};
    dialog.querySelector('.gallery-next').onclick=()=>{this.page++;this.populate();};
    dialog.addEventListener('close',()=>{cancelAnimationFrame(this.raf);document.getElementById('world')?.focus();});
  }
  get open(){return this.dialog.open;}
  show(){this.dialog.showModal();this.populate();this.search.focus();this.tick(0);}
  populate(){
    const query=this.search.value.trim().toLowerCase(),category=this.select.value;
    const items=catalog.filter(item=>(!category||item.category===category)&&(!query||[item.name,item.description,item.rarity,...item.aliases].join(' ').toLowerCase().includes(query)));
    const pages=Math.max(1,Math.ceil(items.length/24));this.page=Math.max(0,Math.min(this.page,pages-1));this.grid.replaceChildren();this.drawn=[];
    for(const item of items.slice(this.page*24,this.page*24+24)){
      const card=document.createElement('article'),canvas=document.createElement('canvas'),title=document.createElement('h3'),description=document.createElement('p'),rarity=document.createElement('small');
      canvas.width=500;canvas.height=340;canvas.setAttribute('aria-label',item.name+' ASCII artwork');title.textContent=item.name;description.textContent=item.description;rarity.textContent=item.rarity+' / '+item.category;
      card.append(canvas,title,description,rarity);this.grid.append(card);this.drawn.push({canvas,item,card});
    }
    this.status.textContent=items.length?`${items.length} ${items.length===1?'item':'items'} · Page ${this.page+1} of ${pages}`:'No matching items';
    this.dialog.querySelector('.gallery-prev').disabled=this.page===0;this.dialog.querySelector('.gallery-next').disabled=this.page===pages-1;this.grid.scrollTop=0;
  }
  tick(time){
    if(!this.open)return;
    if(!this.lastTime||time-this.lastTime>=100){
      const motion=this.motion()&&!this.pause.checked;
      for(const {canvas,item,card} of this.drawn){
        const rect=card.getBoundingClientRect(),bounds=this.grid.getBoundingClientRect();if(rect.bottom<bounds.top||rect.top>bounds.bottom)continue;
        const ctx=canvas.getContext('2d'),model=itemSprite(item.id,time/1000,{motion}),cw=Math.min(16,440/(model.width+2),235/((model.art.length+2)*1.5));
        ctx.fillStyle='#10262c';ctx.fillRect(0,0,500,340);
        if(model.emissive){const gradient=ctx.createRadialGradient(250,170,0,250,170,150);gradient.addColorStop(0,model.accent+'25');gradient.addColorStop(1,model.accent+'00');ctx.fillStyle=gradient;ctx.fillRect(0,0,500,340);}
        this.painter.draw(ctx,model,250,285,cw);card.querySelector('small').style.color=model.rarity;
      }this.lastTime=time;
    }
    this.raf=requestAnimationFrame(t=>this.tick(t));
  }
}
