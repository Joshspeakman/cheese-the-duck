// The landscape stays finely etched; characters use compact, larger glyphs.
// These fallbacks follow Cheese's original three-line silhouette. Live gameplay
// supplies the authored animation frames through the scene snapshot.
export const DUCK = [' ___  ', '(o__)>', "/'__\\ "];
export const EGG = [' .-. ', '(   )', " 'o' "];
export const NEST = String.raw`
       __..--------..__
    .-'//,//,\\,\\,\\'-. 
   (//// .          . \\\\)
    '\\,\\,\\_//_//_//_/'
      '---========---'
`.slice(1, -1).split('\n');
export const DOCK = String.raw`
   |                           |
  _|___________________________|_
 /_|____|____|____|____|____|____|/|
/__|____|____|____|____|____|___/| |
|__|____|____|____|____|____|__/ | |
   |     :      |     :        | ~
   |  ~~~~  ~~~~|~~~~~   ~~~~~ | 
~~~|~~~~   ~~~~~|~~~~  ~~~~   ~~|~~~
`.slice(1, -1).split('\n');
export const CABIN = String.raw`
                 /\
                /::\
               /::::\
           ___/======\___
          /::/        \::\
         /__/___/\_____\__\
        |: |  _/  \_  | :|
        |: | |  __  | | :|
        |: | | |  | | | :|
        |__|_|_|__|_|_|__|
       /____/______\______\
      .:  ..  .  ..  .  ..:.
`.slice(1, -1).split('\n');
export const RUIN = String.raw`
       _.._                _.._
      |::::|__..------..__|::::|
      |:  :|: : : : : : :|:  :|
      |:[]:|    .----.   |:[]:|
      |:  :|   / .--. \  |:  :|
      |: ,:|  | |    | | |:, :|
      |:: :|  | |    | | | :::|
    __|____|__|_|____|_|_|____|__
   /____..___..__..____..____..__\
       .:.   , :: ,   .:.
`.slice(1, -1).split('\n');
export const BOAT = String.raw`
                  |\
                  | \
                  |  \
                  |___\
      __..________|________..__
      \   \  \  \ | / / /   /
       \____\__\__|/_/_/____/
   ~~~~'---..________..---'~~~~
`.slice(1, -1).split('\n');
export const LANTERN = String.raw`
       .-.
       | |
      /===\
      |(*)|
      | : |
      '==='
        |
        |
`.slice(1, -1).split('\n');
export const MUSHROOM = String.raw`
       _..---.._
     .' o  .  o '.
    / .  o   .  o \
   (_______________)
        |: :|
        | : |
      ._|___|_.
`.slice(1, -1).split('\n');
export const CRYSTAL = String.raw`
          /\
         / :\
     /\ / : :\
    / :|  :  | /\
   /:  | : : |/ :\
   | : |  :  | : |
   |  :| : : |:  |
    \ :|  :  | :/
     \_|__:_|_/
`.slice(1, -1).split('\n');
export const FLOWERS = String.raw`
     .-.       .-.        .-.
    ( @ )     ( @ )      ( @ )
     '-'/      '-'/       '-'/
    \ |/      \ |/       \ |/
     \|        \|         \|
  .,..|..,. .,..|..,.  ,..|..,.
`.slice(1, -1).split('\n');
export const BENCH = String.raw`
    |____________________|
    |__|__|__|__|__|__|__|
    |____________________|
   /____________________/|
   |  |              |  |
   |__|              |__|
`.slice(1, -1).split('\n');
export const WELL = String.raw`
          /\
        _/==\_
       /______\
       | |  | |
       | |--| |
       | |[]| |
     .-=======-.
     | [] [] []|
     |[] [] [] |
     '---------'
`.slice(1, -1).split('\n');

export function mirror(lines) {
  const pairs = {'/':'\\','\\':'/','(' : ')', ')':'(', '[':']', ']':'[','<':'>','>':'<'};
  const width = Math.max(...lines.map(l => l.length));
  return lines.map(line => [...line.padEnd(width)].reverse().map(c => pairs[c] || c).join(''));
}
export function duckArt(state, time, facing = true, stage = 'adult') {
  if (stage === 'egg') return EGG.slice();
  const baby = ['hatchling','duckling'].includes(stage);
  const teen = ['teen','juvenile'].includes(stage);
  const elder = ['elder','mature','legendary'].includes(stage);
  const phase = Math.floor(time * 5) % 2;
  let eye = 'o';
  if (/sleep|napping|bored/.test(state)) eye = '-';
  else if (/happy|love|petting|playing|proud|danc|excited/.test(state)) eye = '^';
  else if (/sad|sick|cold/.test(state)) eye = ';';
  else if (/scared|surpris|quack|sing|yawn/.test(state)) eye = 'O';
  else if (/angry/.test(state)) eye = '>';
  else if (/dizzy/.test(state)) eye = '@';
  else if (time % 6.1 > 5.9) eye = '-';
  const art = baby ? [' __ ', `(${eye}>)`, "/'\\)"] :
    teen ? [' _~_ ', `(${eye}_>)`, "/''\\_"] :
    elder ? [' ~___ ', `(${eye}==)>`, "/'==\\ "] : [' ___  ', `(${eye}__)>`, "/'__\\ "];
  if (/eating|pecking|hungry/.test(state) && phase === 0) art[1] = art[1].replace(')>','>.').replace('>)','>.');
  if (/walk|waddle|danc|playing|excited/.test(state)) art[2] = phase ? ' /__ ' : ' __\\ ';
  if (/flap|wav|stretch|danc/.test(state)) art[0] = phase ? '\\___/' : ' ___/';
  if (/swim|float|splash|diving/.test(state)) art[2] = baby ? '~~~~' : '~~~~~~';
  if (/sleep|napping/.test(state)) art[0] += phase ? 'z' : 'Z';
  if (/preen/.test(state)) art[1] = baby ? '(o<)' : '(o<_)>';
  return facing ? art : mirror(art);
}

export const ARCH = String.raw`
       ___..-------..___
     .'::/ / / / / /::'.
    /::/ / / / / / / /::\
   /::/ /__..---..__\ \::\
  |::| .'           '. |::|
  |::*|               |*::|
  |:*:|               |:*:|
  |::o|               |o::|
  |:*:|               |:*:|
 _|:::|_______________|:::|_
`.slice(1,-1).split('\n');
export const CLOCKTOWER = String.raw`
           /\
          /::\
         /====\
        | .--. |
        | |/o| |
        | '--' |
        |======|
        |::[]::|
        |: :: :|
        |::[]::|
        |: :: :|
      __|______|__
     | [] |  | [] |
     |____|__|____|
`.slice(1,-1).split('\n');
export const MILL = String.raw`
             __
           .'__'.
          /::::::\
         /========\
        | :    :  |
        | : [] :  |
        | :    :  |
        | : [] :  |
        | :    :  |
       /: : __ :  :\
      /___:|  |:____\
`.slice(1,-1).split('\n');
