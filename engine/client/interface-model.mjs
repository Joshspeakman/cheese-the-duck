// Keep the authored text and styles. Only terminal box scaffolding is replaced.
export const plain = runs => runs.map(run=>run[0]).join('');
const box = /^[\s+|=\-─━═│┃║┌┐└┘├┤┬┴┼╔╗╚╝╠╣╦╩╬]+$/u;
export function documentRows(lines, columns=112, preserveArt=false) {
  const rows=[];
  for(const runs of lines){
    const cells=runs.flatMap(([text,fg,bg,flags])=>Array.from(text,char=>({char,fg,bg,flags})));
    const text=cells.map(c=>c.char).join('');
    if(!preserveArt && text.trim() && box.test(text) && /[-=─━═]/u.test(text)) { rows.push({kind:'rule',text,cells:[]}); continue; }
    // Strip a matched enclosing box, never prose, arrows or artwork.
    let start=0,end=cells.length;
    const first=text.search(/\S/),last=text.trimEnd().length-1;
    if(!preserveArt && first>=0 && /[│║|]/u.test(cells[first].char) && /[│║|]/u.test(cells[last].char) && last>first){start=first+1;end=last;}
    while(end>start && cells[end-1].char===' ')end--;
    const content=cells.slice(start,end);
    const value=content.map(c=>c.char).join('');
    const selected=/^\s*(?:->|>>|>|→|►|▶|❯)\s*\S/u.test(value);
    const heading=/^\s*(?:={2,}|-{2,}|\[=\])\s*\S/.test(value) || (/[A-Z]{3}/.test(value)&&value.trim()===value.trim().toUpperCase()&&!selected);
    // Soft wrapping on word boundaries, retaining every character and style.
    let part=content.slice();
    if(!part.length)rows.push({kind:'blank',text:'',cells:[]});
    while(part.length){
      let count=Math.min(columns,part.length);
      if(part.length>columns){const space=part.slice(0,columns).map(c=>c.char).lastIndexOf(' ');if(space>columns*.55)count=space+1;}
      const segment=part.splice(0,count);
      rows.push({kind:selected?'selected':heading?'heading':'text',text:segment.map(c=>c.char).join(''),cells:segment});
    }
  }
  while(rows[0]?.kind==='blank'||rows[0]?.kind==='rule')rows.shift();
  while(rows.at(-1)?.kind==='blank'||rows.at(-1)?.kind==='rule')rows.pop();
  return rows;
}
export function cropDocument(lines){
  const nonempty=lines.filter(row=>plain(row).trim());
  const indent=Math.min(...nonempty.map(row=>plain(row).search(/\S/)));
  if(!Number.isFinite(indent)||indent<=0)return lines;
  return lines.map(row=>{let remove=indent;return row.map(([text,...style])=>{const n=Math.min(remove,Array.from(text).length);remove-=n;return [Array.from(text).slice(n).join(''),...style];}).filter(run=>run[0]);});
}
export function documentTitle(modal) {
  if(modal.title!=='MENU')return modal.title.replace(/^[^\w]+|[\]\s]+$/gu,'');
  const rows=documentRows(modal.lines);
  const title=rows.find(row=>row.text.trim())?.text.trim()||'Pond journal';
  return title.replace(/^[=\-+\s]+|[=\-+\s]+$/g,'');
}
export function themeFor(title) {
  const value=title.toLowerCase();
  if(/confirm|reset|erase|error|unsaved|wrong/.test(value))return 'warning';
  if(/shop|invent|trad|item|craft|build|decor/.test(value))return 'workshop';
  if(/setting|audio|display|keybind/.test(value))return 'settings';
  if(/garden|world|area|weather|explor|fish|treasure/.test(value))return 'world';
  if(/trick|game|race|catch|chase|memory|festival|challeng|celebration|interact/.test(value))return 'play';
  if(/diary|scrap|photo|journal|life|dream|secret|collect/.test(value))return 'journal';
  if(/talk|message|friend/.test(value))return 'talk';
  return 'duck';
}
export function menuWindow(menu, count) {
  const start=Math.max(0,Math.min(menu.selected-Math.floor(count/2),menu.items.length-count));
  return {start,items:menu.items.slice(start,start+count)};
}
export function clamp(value,min,max){return Math.max(min,Math.min(max,value));}
