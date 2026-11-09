// Copies the game's source into desktop/game (the app's Python environment is made on first launch) and makes the icon.
import { chmodSync, cpSync, existsSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.dirname(here);
const out = path.join(here, 'game');
const skip = new Set(['.git', '.github', '.gitignore', '.venv', '.pytest_cache', '__pycache__', 'desktop', 'models', 'debian', 'docs', 'tests', 'StupidDuckCS', 'assets']);
rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });
for (const name of readdirSync(root))
  if (!skip.has(name)) cpSync(path.join(root, name), path.join(out, name), { recursive: true, filter: (src) => !src.includes('__pycache__') });
mkdirSync(path.join(here, 'build'), { recursive: true });
if (process.platform === 'darwin')
  execFileSync('sips', ['-s', 'format', 'png', '-z', '1024', '1024', path.join(root, 'cheese.ico'), '--out', path.join(here, 'build/icon.png')], { stdio: 'ignore' });
// npm doesn't run node-pty's install step here, which is what makes its prebuilt helper executable
for (const arch of ['darwin-arm64', 'darwin-x64']) { const helper = path.join(here, 'node_modules/node-pty/prebuilds', arch, 'spawn-helper'); if (existsSync(helper)) chmodSync(helper, 0o755); }
console.log('bundled the game into desktop/game');
