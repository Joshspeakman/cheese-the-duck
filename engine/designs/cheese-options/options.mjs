// Design studies only. These do not replace the live character renderer.
const lines = text => text.slice(1, -1).split('\n');
export const ORIGINAL = [' ___ ', '(o__)>', "/'__\\"];
export const OPTIONS = [
  {
    id: 1, name: 'Classic expanded',
    description: 'The original profile, with a folded wing and little webbed feet.',
    face: [0, 1, 2], eye: [1, 5],
    art: lines(String.raw`
    .-----.
   ( o ____)==>
    \_    /
    / '--'\
   / (__)  \
   \______/
     /  \
    ^^  ^^
`),
  },
  {
    id: 2, name: 'Round pond duck',
    description: 'A low, plump body with a small head, soft belly, and tail.',
    face: [0, 1, 2], eye: [1, 9],
    art: lines(String.raw`
        .---.
       ( o __)==>
   .----\  /
 .'   .--'  \
/    (___)   |
\           /
 '--------'
    _/  \_
`),
  },
  {
    id: 3, name: 'Tall duck',
    description: 'An upright neck and a pear-shaped body for a proud waddle.',
    face: [0, 1, 2], eye: [1, 9],
    art: lines(String.raw`
        .---.
       ( o __)==>
        |  /
        |  |
  ,-----'  |
 /   .--.  |
 \  (___)  /
  '-------'
     /  \
    ^^  ^^
`),
  },
  {
    id: 4, name: 'Low swimmer',
    description: 'A long floating silhouette, little tail, and trailing ripples.',
    face: [0, 1, 2], eye: [1, 8], water: true,
    art: lines(String.raw`
       .----.
      ( o ___)==>
   .---\   /
 _/   __'  '--.
 \   (___)    /
  '----------'
 ~~~  ~~~  ~~~
`),
  },
  {
    id: 5, name: 'Big head, tiny feet',
    description: 'A tuft, an oversized face, and a small round body.',
    face: [1, 2, 3], eye: [2, 6],
    art: lines(String.raw`
       ,,
    .------.
   (  o  __)==>
    '.___.'
    /(__) \
    \_____/
     /_ _\
`),
  },
  {
    id: 6, name: 'Grumpy slouch',
    description: 'A half-lidded stare and a heavy, relaxed belly.',
    face: [0, 1, 2, 3], eye: [2, 6], defaultEye: '-',
    art: lines(String.raw`
      ______
    .'      '.
   (  -   __)==>
    '.___/ /
   .-'    '--.
  /  (___)    \
  '-----------'
      _/ \_
`),
  },
  {
    id: 7, name: 'Mallard profile',
    description: 'A recognizable duck outline with a collar, tail, and long wing.',
    face: [0, 1, 2], eye: [1, 11],
    art: lines(String.raw`
          .----.
         / o ___)==>
         \___  /
          |==|
    __.--'   '--.
  <'   .----.    \
   \  (______)   /
    '----------'
        _/ \_
`),
  },
  {
    id: 8, name: 'Scruffy little menace',
    description: 'A messy crest, sharp side-eye, and an uneven swagger.',
    face: [1, 2, 3], eye: [2, 7], defaultEye: '>',
    art: lines(String.raw`
        \|/
      .-----.
     ( > ___)==>
      \_   /
   ,--' '-'\
  <  (___)  )
   '-------'
      /  >_
`),
  },
  {
    id: 9, name: 'Face to face',
    description: 'Both eyes, a broad bill, folded wings, and a round chest.',
    face: [0, 1, 2, 3, 4], eyes: [[1, 8], [1, 11]],
    art: lines(String.raw`
       .----.
     .' o  o '.
    (   ____   )
     \ <____> /
      '------'
     / (____) \
    (          )
     '--------'
       /_  _\
`),
  },
  {
    id: 10, name: 'Compact classic',
    description: 'A clean, chunky version of the original with just one wing.',
    face: [0, 1], eye: [1, 4],
    art: lines(String.raw`
   .------.
  ( o _____)>
   /'    '\
  /  (__)  \
  '--------'
     ^  ^
`),
  },
];

export function optionSprite(option, time = 0, pose = 'idle') {
  const art = [...option.art], step = Math.floor(time * 4) % 2;
  let eye = pose === 'happy' ? '^' : pose === 'angry' ? '>' : pose === 'sleeping' ? '-' : option.defaultEye || 'o';
  if (pose !== 'sleeping' && time % 5 > 4.8) eye = '-';
  for (const [row, col] of option.eyes || [option.eye])
    art[row] = art[row].slice(0, col) + eye + art[row].slice(col + 1);
  if (pose === 'walking' && step && !option.water) {
    const row = art.length - 1;
    art[row] = art[row].replaceAll('^^', '>_').replaceAll('_/', '_>').replaceAll('^', '>');
  }
  if (option.water && step) art[art.length - 1] = '  ~~  ~~~~  ~~';
  if (pose === 'sleeping') art[0] += step ? '  Z' : '  z';
  const tones = art.map((row, y) => {
    const colors = Array(row.length).fill(option.face.includes(y) ? 'f' : 'b');
    const beak = row.indexOf('==>');
    if (beak >= 0) for (let x = beak; x < row.length; x++) colors[x] = 'a';
    if (option.id === 9 && (y === 2 || y === 3)) for (let x = 7; x < 13; x++) colors[x] = 'a';
    if (option.id === 10 && y === 1) colors[row.length - 1] = 'a';
    if (y === art.length - 1) colors.fill(option.water ? 'w' : 'a');
    return colors.join('');
  });
  const width = Math.max(...art.map(row => row.length));
  return { art, tones, width, anchorX: Math.max(...option.art.map(row => row.length)) / 2,
    scale: 1, body: '#f0d28e', face: '#ffe9b3', accent: '#f3ad56', shade: '#baa078', name: '' };
}
