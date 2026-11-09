// Run with: engine/node_modules/.bin/electron engine/designs/cheese-options/export.cjs
// Exports a standalone browser gallery and PNGs. Does not start the simulation.
const { app, BrowserWindow } = require('electron');
const fs = require('node:fs'), path = require('node:path'), os = require('node:os');
const { pathToFileURL } = require('node:url');
const engine = path.resolve(__dirname, '../..');
const out = path.join(engine, 'artifacts', 'cheese-options');
app.setPath('userData', fs.mkdtempSync(path.join(os.tmpdir(), 'cheese-designs-')));
app.whenReady().then(async () => {
  const win = new BrowserWindow({show:false, webPreferences:{contextIsolation:true, sandbox:true, backgroundThrottling:false}});
  try {
    const { OPTIONS, optionSprite } = await import(pathToFileURL(path.join(__dirname, 'options.mjs')));
    if (OPTIONS.length !== 10 || new Set(OPTIONS.map(o => o.art.join('\n'))).size !== 10) throw Error('Expected 10 unique options');
    for (const option of OPTIONS) for (const pose of ['idle','happy','angry','walking','sleeping']) {
      const sprite = optionSprite(option, 0.3, pose);
      if (sprite.art.some((row,i) => !/^[\x20-\x7e]*$/.test(row) || row.length !== sprite.tones[i].length)) throw Error(`Invalid glyph or tone in option ${option.id}`);
    }
    await win.loadFile(path.join(__dirname, 'template.html'));
    const rendererURL = pathToFileURL(path.join(engine, 'client', 'ultra-renderer.mjs')).href;
    const sceneURL = pathToFileURL(path.join(engine, 'tests', 'scenes.mjs')).href;
    const background = await win.webContents.executeJavaScript(`(async()=>{
      const {SceneCanvas} = await import(${JSON.stringify(rendererURL)});
      const {scene} = await import(${JSON.stringify(sceneURL)});
      const canvas = new SceneCanvas(); canvas.resize(1200,560);
      const s = scene({motion:false}); s.duck.hidden = true;
      canvas.draw(s,2,1/30); return canvas.canvas.toDataURL('image/png');
    })()`);
    const template = fs.readFileSync(path.join(__dirname, 'template.html'), 'utf8');
    const options = fs.readFileSync(path.join(__dirname, 'options.mjs'), 'utf8').replace(/^export /gm, '');
    const draw = fs.readFileSync(path.join(engine, 'client', 'ultra-characters.mjs'), 'utf8').split('export function drawCharacter')[1];
    const gallery = fs.readFileSync(path.join(__dirname, 'gallery.mjs'), 'utf8').replace(/^import .*;\n/gm, '');
    const script = `(async()=>{const SCENE=${JSON.stringify(background)};\n${options}\nfunction drawCharacter${draw}\n${gallery}\n})();`;
    const html = template.replace('<!-- GALLERY_SCRIPT -->', `<script>${script}</script>`);
    fs.mkdirSync(out, {recursive:true});
    const file = path.join(out, 'Cheese - 10 design options.html'); fs.writeFileSync(file, html);
    await win.loadFile(file);
    await win.webContents.executeJavaScript(`new Promise((resolve,reject)=>{
      const deadline = Date.now()+5000;
      const poll = ()=>window.galleryReady?resolve():Date.now()>deadline?reject(Error('Gallery failed to load')):setTimeout(poll,25);poll();
    })`);
    await win.webContents.executeJavaScript(`(async()=>{
      const cards = [...document.querySelectorAll('.card')];
      for (const [i, card] of cards.entries()) {
        card.click();
        if (!document.getElementById('selection').textContent.startsWith(String(i+1).padStart(2,'0'))) throw Error('Card selection failed');
      }
      cards[8].click();
      await new Promise(r=>setTimeout(r,150));
      const before = document.getElementById('world').toDataURL();
      document.querySelector('[data-pose="happy"]').click();
      await new Promise(r=>setTimeout(r,150));
      if (before === document.getElementById('world').toDataURL()) throw Error('Expression preview did not change');
      document.getElementById('play').click();
      if (document.getElementById('play').getAttribute('aria-pressed') !== 'false') throw Error('Pause failed');
      document.getElementById('play').click(); document.querySelector('[data-pose="idle"]').click();
    })()`);
    const images = await win.webContents.executeJavaScript('window.exportOptions()');
    for (const [name, data] of Object.entries(images)) fs.writeFileSync(path.join(out, name+'.png'), Buffer.from(data.split(',')[1], 'base64'));
    console.log(JSON.stringify({result:'PASS', options:OPTIONS.length, images:Object.keys(images).length, gallery:file, out}));
    app.exit(0);
  } catch(error) { console.error(error); app.exit(1); }
});
