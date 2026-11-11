// Freeze the actual simulation and every dynamically imported gameplay module.
import { execFileSync } from 'node:child_process';
import { mkdirSync, readdirSync, existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url)), root = path.dirname(here);
execFileSync(process.execPath,[path.join(here,'build-footprints.mjs')],{cwd:root,stdio:'inherit'});
mkdirSync(path.join(here, 'build'), { recursive: true });
const python = path.join(root, '.venv/bin/python');
const args = ['-m', 'PyInstaller', '--noconfirm', '--clean', '--onedir', '--name', 'cheese-simulation',
  '--distpath', path.join(here, 'build/simulation'), '--workpath', path.join(here, 'build/pyinstaller'),
  '--specpath', path.join(here, 'build'), '--paths', root];
for (const name of ['core','duck','world','dialogue','ui','audio','engine']) args.push('--collect-submodules', name);
for (const name of readdirSync(root)) if (/\.(wav|ogg|mp3|ico)$/.test(name)) args.push('--add-data', `${path.join(root,name)}:.`);
for (const name of ['assets','models']) if (existsSync(path.join(root,name))) args.push('--add-data', `${path.join(root,name)}:${name}`);
args.push('--add-data', `${path.join(here,'client/animation')}:engine/client/animation`);
const hasLocalAI = execFileSync(python, ['-c', "import importlib.util; print(bool(importlib.util.find_spec('llama_cpp')))"]).toString().trim() === 'True';
if (hasLocalAI) args.push('--collect-all', 'llama_cpp');
args.push(path.join(here, 'host.py'));
execFileSync(python, args, { cwd: root, stdio: 'inherit' });
execFileSync('sips', ['-s', 'format', 'png', '-z', '1024', '1024', path.join(root,'cheese.ico'), '--out', path.join(here,'build/icon.png')], { stdio: 'ignore' });
