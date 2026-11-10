"""The pond's named cast: one identity shared by dialogue, motion and Ultra art.

Names/relationship IDs are unchanged. Unknown/custom names retain the original
personality dialogue and receive a deterministic visual fallback.
"""
PROFILES = {}


def F(name, archetype, shape, head, colors, gear, prop, habit, bio, lines,
      height=80, pace=4, social=.45, radius=12):
    keys = ('greeting', 'returning', 'opening', 'main', 'story', 'personal', 'activity', 'gift', 'farewell')
    p = dict(id='friend:' + name.lower(), name=name, archetype=archetype, species='duck',
             shape=shape, head=head, palette=colors.split(), gear=gear.split(), prop=prop,
             habit=habit, bio=bio, height=height, pace=pace, social=social, radius=radius,
             voice=dict(zip(keys, lines)), rare=False)
    PROFILES[p['id']] = p


F('Marco','adventurous','pear','longbill','#c49c75 #c5bda0 #d9805f','hat_cowboy bandana','compass',
  'Stops to tap a compass, then confidently points the wrong way.',
  'A mud-booted pathfinder with an enormous bill, a patched bag and spectacularly unreliable confidence.',[
  'Cheese! Excellent. A local. Which way is north today?',
  'Found you again. Deliberately, this time. Mostly.',
  'I name every path I discover. This one is Marco Was Here Twice.',
  'The compass says north. My stomach says bakery. A difficult scientific disagreement.',
  'I once led an expedition straight back to its own picnic. Morale was exceptional.',
  'Getting lost is fine. Being lost without someone to tell about it is the rotten part.',
  'Come on, Cheese. We will take the scenic route, then admit it was an accident.',
  'For me? I will put it somewhere safe. I have a map of my safe places.',
  'Onward! If I come past again, pretend that was the plan.'],height=88,pace=3.7,radius=18)
F('Amelia','adventurous','runner','swept','#b7c6cf #e4d8bb #d46b58','sunglasses_aviator scarf_red','plane',
  'Squints into the wind, tests a paper glider, and catches it with her wing.',
  'A lean silver runner with swept-back feathers; a fearless pilot who gets airsick on swings.',[
  'Wind good. Visibility good. Landing dignity: we will see.',
  'Your pond looks lovely from above. Also extremely wet from below.',
  'I am testing a paper glider. The paper thinks it is a boat.',
  'Everyone asks about the flying. Nobody asks about the very important falling-with-intent.',
  'My first solo flight ended in a laundry basket. Five stars for the landing surface.',
  'I keep every failed glider. They tried something difficult. So did I.',
  'Be my ground crew? Your job is to shout when the tree gets close.',
  'Oh! That belongs in the lucky pocket, beside the emergency biscuit.',
  'Clear skies, Cheese. And forgiving bushes.'],height=91,pace=4.6,radius=19)
F('Columbus','adventurous','barrel','brow','#bba77f #788f87 #cf9563','hat_pirate','map',
  'Unfolds a map upside down and rotates himself instead of the paper.',
  'A broad, weather-beaten navigator with a severe brow and a deeply unserious sense of direction.',[
  'I have charted this pond. Unfortunately the ink was water-soluble.',
  'Ah, familiar shores. Familiar suspicious rock. Familiar Cheese.',
  'The blank bit on my map is either a mystery or where I spilled soup.',
  'Never trust a map with no coffee stains. It has not been anywhere.',
  'A snail once overtook my expedition. We made it our guide.',
  'I like returning to places more than discovering them. You can tell who missed you.',
  'Help me name that inlet. No, we already have three Little Shits Creek.',
  'A fine addition to the ship. The ship is currently a bucket.',
  'I sail at dawn. Unless the bucket leaks again.'],height=84,pace=3.1,radius=14)
F('Vasco','adventurous','low','sleepy','#8ba6aa #d3b894 #8cae76','sun_hat','flask',
  'Takes a tiny thermos break after every perfectly manageable journey.',
  'A low, long-bodied wanderer who treats a five-step stroll like a luxurious expedition.',[
  'Made it all the way here. Right, tea break.',
  'Same lovely pond. Same excellent place to sit down.',
  'My travel journal has four pages about this bench.',
  'An adventure needs danger, discovery, and somewhere sensible to put a cup.',
  'Crossed a desert once. A sandbox, technically. I still rationed the biscuits.',
  'People rush past lovely things. I am helping by being quite difficult to rush.',
  'Fancy an expedition to that patch of shade? We can stop halfway.',
  'You packed for me? That is a very advanced form of friendship.',
  'Safe travels. Or safe sitting. Equally respectable.'],height=68,pace=2.4,radius=8)
F('Marina','adventurous','teardrop','bob','#789dae #d9cabc #edba82','scarf_striped','shell',
  'Listens to a shell, taps a rhythm with one foot, and answers it quietly.',
  'A sleek blue shore duck with a blunt feather bob and a pocket full of imaginary sea reports.',[
  'The tide sent me. Well, a puddle did. Same department.',
  'Cheese! I brought news from the other side of the water. More water.',
  'This shell sounds like the sea. This one sounds like a very rude kettle.',
  'I collect shorelines. Difficult to carry home, but the pockets are free.',
  'I wrote a message in a bottle. It returned with a complaint about my handwriting.',
  'Sometimes I listen to empty shells just to have someone listen back.',
  'Walk the bank with me? We can judge the interesting stones.',
  'Oh, this one has a story. I can tell. I will make one up if necessary.',
  'See you when the water changes its mind.'],height=78,pace=3.8,radius=17)

F('Einstein','scholarly','shaggy','tuft','#b4acb8 #e1dfcd #c5a0d8','glasses_nerd','chalkboard',
  'Chalks an equation, squints, then rubs out everything except the duck doodle.',
  'A frazzled, round professor with a storm of pale feathers and chalk on every available surface.',[
  'Cheese! Quick question. How many crumbs make a philosophical problem?',
  'I solved our last problem. Then found three smaller problems inside it.',
  'My feathers are not messy. They are expressing several competing hypotheses.',
  'Time is relative. Especially the five minutes before lunch.',
  'I proved I had lost my glasses while looking directly through them.',
  'I like being wrong around you. You make it less of a catastrophe.',
  'Stand there a moment. I need a control duck.',
  'Fascinating! I shall label it before I forget why I love it.',
  'Must dash. An idea is escaping through a hole in my attention.'],height=83,pace=3.2,radius=9)
F('Newton','scholarly','pear','small','#b48d6d #c7c0a1 #aab871','hat_beanie','apple',
  'Balances an apple on his head, looks proud, and catches the inevitable result.',
  'A bottom-heavy little thinker with a tiny head and the air of someone arguing with gravity.',[
  'Do you know why things fall, Cheese? I have several bruised opinions.',
  'Still here? Excellent. A stable reference point.',
  'This apple is essential equipment. It is also getting a bit pecked.',
  'The universe has rules. The apple refuses to explain them.',
  'My greatest experiment was ruined by an experimental snack.',
  'It is nice when someone stays to hear the explanation, even the terrible one.',
  'Catch this. For science. And because I am out of apples.',
  'Thank you! I promise not to drop it until I have measured it.',
  'I must go. Something is about to fall somewhere.'],height=75,pace=3.5,radius=10)
F('Ada','scholarly','runner','bob','#7d9f9d #e0c6a1 #d68b88','bow_tie_blue','abacus',
  'Slides abacus beads in a precise pattern and smiles at one deliberately wrong bead.',
  'A neat teal runner with a square bob, striped cuffs and a soft spot for gloriously useless inventions.',[
  'Hello, Cheese. I made a machine that counts hellos. That was one.',
  'Welcome back to the sequence. You are my favorite recurring event.',
  'I taught my abacus a joke. It is still calculating the timing.',
  'A bug is just a feature with a very bad alibi.',
  'I automated my morning routine. Now I have spare time to repair my morning routine.',
  'People think precise means cold. I remember how everyone takes their tea.',
  'Help me test this pattern? There are absolutely no explosions scheduled.',
  'You remembered! That is much nicer than a perfect calculation.',
  'Until next iteration, Cheese. That means see you soon.'],height=81,pace=4,radius=11)
F('Darwin','scholarly','barrel','longbill','#9eaa77 #d6c4a1 #cfaa70','hat_cowboy','magnifier',
  'Studies a beetle through a magnifier, then apologizes for staring.',
  'A mossy, broad-backed naturalist whose bill and pockets are both much larger than necessary.',[
  'Shh. That beetle is doing something completely ordinary. Extraordinary.',
  'Cheese! I see you have continued being a duck. Excellent data.',
  'I have named the beetle Percy. Peer review may object.',
  'Nature wastes nothing. Except my entire afternoon when a caterpillar is interesting.',
  'I followed a trail for hours. It was my own dropped sandwich.',
  'Small things deserve witnesses. Somebody should notice how hard they try.',
  'Sit very still with me. We are about to become part of the scenery.',
  'A specimen! Or a present. Both? How wonderfully efficient.',
  'Percy is leaving. I should see him safely across this enormous twig.'],height=87,pace=2.8,radius=13)
F('Curie','scholarly','pocket','wedge','#a0b7c5 #d8d4df #b8d18b','glasses_nerd','flasks',
  'Compares two softly fizzing flasks and shields the smaller one from the wind.',
  'A compact slate duck with a pointed crest, oversized sleeves and patient, mischievous eyes.',[
  'Hello, Cheese. Nothing in these bottles is supposed to explode.',
  'I brought the quiet experiment today. The noisy one has been grounded.',
  'That green glow is algae. The dramatic lighting was my idea.',
  'Safety goggles make every cup of tea feel like a discovery.',
  'I once spent a week identifying a mysterious powder. It was flour. Excellent flour.',
  'The best part of a discovery is finding someone who wants to see it.',
  'Hold this label. If the bottle changes color, look impressed.',
  'For my collection? Oh, I am going to be unbearable about this.',
  'Keep curious, Cheese. Keep your beak out of unlabelled jars.'],height=68,pace=3.6,radius=9)

F('Picasso','artistic','shaggy','swept','#d5be9e #b5ccd0 #de937d','hat_beret','brush',
  'Measures the horizon with a paintbrush, then paints a tiny moustache in the air.',
  'A wiry, paint-spattered duck with a slanted crest and a beret permanently on the verge of escape.',[
  'Do not move, Cheese. You look wonderfully inconvenienced.',
  'Ah! My favorite difficult subject returns.',
  'I painted the pond blue. Critics called it accurate. Devastating.',
  'Art should ask questions. Mine mostly asks where I put the brush.',
  'A painting sold once. The buyer thought it was a map. They are probably still lost.',
  'I make jokes about the work because saying I care is a bit terrifying.',
  'Pick a color. Any color. I will disagree affectionately.',
  'What a shape! What a texture! What an excellent friend!',
  'Stay interesting. A completely unreasonable thing to ask of a duck.'],height=79,pace=4.1,radius=13)
F('Frida','artistic','pear','curly','#b58f77 #d5b994 #e2a39f','flower_lei','pressed_flower',
  'Tucks a flower behind her crest and presses another carefully into a journal.',
  'A warm russet duck with heavy brows, a flowering crown and a patient, fearless stare.',[
  'There you are. The pond was getting too polite without you.',
  'I saved a page for you. Try not to eat it.',
  'That weed has more ambition than half the roses I know.',
  'Pretty is nice. Alive is better. Slightly muddy is usually both.',
  'I painted every crack in a broken pot. Now everyone asks where I bought it.',
  'Some days I make beautiful things. Some days making anything is enough.',
  'Find me the least perfect flower. That is the one with the story.',
  'You saw this and thought of me? That is the whole point of presents.',
  'Take up space, Cheese. You are allowed.'],height=82,pace=3.1,radius=9)
F('Leonardo','artistic','runner','tuft','#bfa679 #b9c5ae #d3ad71','glasses_nerd backpack_tiny','gears',
  'Winds a little gear train; one stubborn cog spins the wrong way.',
  'A tall, uncombed tinkerer with rolled sleeves and too many half-finished marvels.',[
  'Cheese! I need an opinion and possibly a very small wrench.',
  'Remember the flying chair? We are calling it a sitting kite now.',
  'This invention saves time. Building it only took six months.',
  'It is nearly finished. That is my favorite stage. I have forty things there.',
  'I invented a self-stirring soup. It left the bowl and started a new life.',
  'Finishing things is frightening. While they are unfinished, they can still be perfect.',
  'Turn this handle. Gently. More gently than that look suggests.',
  'A component! A treasure! I have already thought of three bad ideas.',
  'Back to the workshop. Something in there just became a noise.'],height=94,pace=3.9,radius=12)
F('Monet','artistic','low','sleepy','#89a8a0 #cfc6b8 #b0bedb','sun_hat','lily_brush',
  'Dabs a little watercolor pad, pauses for the light, and nearly nods off.',
  'A broad, low-slung painter in soft pond colors with an impractically wide hat.',[
  'The light is lovely. Please tell it to stay while I find my brush.',
  'Same pond, different green. You understand.',
  'I have painted that lily seventeen times. It remains extremely unhelpful.',
  'The secret is to squint until the problem becomes atmosphere.',
  'A frog sat on my palette. Best landscape I made all summer.',
  'I keep painting here because it never asks me to hurry.',
  'Watch that reflection with me. We are being productive. Quietly.',
  'Oh, that color. I will remember this moment when I use it.',
  'I shall follow the light. At a very reasonable pace.'],height=70,pace=2.2,radius=7)
F('Georgia','artistic','teardrop','wedge','#c9ae90 #e3d1ad #db926a','spring_gardener_hat','watering_can',
  'Waters one small bloom and checks it from three very serious angles.',
  'A long, pale desert-colored duck with sharp feathers and surprising gentleness around seedlings.',[
  'Look at that flower, Cheese. No, really look. It is showing off.',
  'I came back to see what opened. You count, by the way.',
  'People say my flowers are too big. People are standing too far away.',
  'A small thing can take up your whole day if you finally pay attention.',
  'I carried a seed across a mountain. It grew in the pocket before we arrived.',
  'I do not need a crowded garden. Just a few things I know how to care for.',
  'Help me water this without giving it a personal monsoon.',
  'Thank you. I know exactly where this belongs. Beside something loved.',
  'Notice something small for me. Then tell me all about it.'],height=85,pace=3.4,radius=10)

F('Bubbles','playful','pocket','round','#e7c991 #ebdcb3 #8dc7d3','bow_tie_pink','bubble_wand',
  'Blows one enormous bubble, watches it pop, and looks personally betrayed.',
  'A round butter-yellow duck with tiny feet, enormous cheeks and no ability to whisper exciting news.',[
  'CHEESE! I found a bubble with your exact attitude!',
  'You are back! I saved you some air. It was inside bubbles.',
  'This bubble is called Gerald. Do not tell the actual Gerald.',
  'If bubbles are free, why am I so emotionally invested?',
  'I tried to take a bubble home. Longest sad walk of my life. Three steps.',
  'I like things that do not last. Gives you a reason to notice them now.',
  'Catch one on your beak! No, emotionally does not count.',
  'FOR ME? Wait. Let me do the delighted face properly.',
  'POP! That means goodbye in bubble. Probably.'],height=65,pace=4.7,social=.75,radius=11)
F('Giggles','playful','barrel','curly','#c4a4bd #e0c8c8 #deaa69','party_hat','banana',
  'Checks both ways before presenting a banana as if it is a priceless violin.',
  'A lavender, barrel-shaped comedian with corkscrew feathers and catastrophically good timing.',[
  'A duck walks into a pond. The pond says, finally, a professional.',
  'Cheese! New jokes. Same questionable delivery system.',
  'I am working on a silent joke. The reviews have been quiet.',
  'This banana is my understudy. Excellent peel for the role.',
  'I once made Professor Hoot snort tea. Still my finest academic achievement.',
  'Making people laugh is how I check they are still there with me.',
  'You be the straight duck. It will be a terrible strain, I know.',
  'Oh! A gift with no punchline. Those are my favorite, actually.',
  'Thank you, you have been a wonderful pond.'],height=79,pace=4.1,social=.8,radius=8)
F('Zippy','playful','runner','swept','#879ebc #b8d1cc #efa578','cap_sports','yoyo',
  'Walks a yo-yo, trips over absolutely nothing, and recovers with a bow.',
  'A narrow blue blur with a long swept crest, one untied lace and twelve simultaneous plans.',[
  'HiCheesehaveyouseenthis—right. Breathing. Hello.',
  'I am back! You may not have noticed the middle bit where I left.',
  'My yo-yo returns more reliably than my attention.',
  'Standing still is just walking very, very badly.',
  'I won a race to the wrong tree. Nobody can take that away from me.',
  'Sometimes I go fast so nobody notices I am not sure where to go.',
  'Race you to that reed! Walking race. I am developing range.',
  'Oh wow. I will cherish this at an appropriate velocity.',
  'Bye! Wait, one more—nope, gone!'],height=78,pace=6,social=.6,radius=20)
F('Bouncy','playful','pear','tuft','#d5ac7d #ebce94 #d6929b','bunny_slippers','ball',
  'Bounces a stitched ball, crouches with it, and wobbles after the catch.',
  'A pear-shaped peach duck with springy knees, fluffy slippers and a solemn devotion to silliness.',[
  'Boing. That was my entrance. I rehearsed it.',
  'Cheese! The ground still works. I checked with my face.',
  'This ball has a slow leak. We are both learning to pace ourselves.',
  'You cannot be dignified and airborne at the same time. I have tried.',
  'I bounced into a hedge once and came out with a better haircut.',
  'I practice the easy things until they feel like flying.',
  'One bounce each. No championship. Just the nice little thump.',
  'This deserves a happy bounce. Stand clear of the elbows.',
  'Land softly, Cheese. Especially after the good bits.'],height=73,pace=4.8,social=.65,radius=12)
F('Sunny','playful','teardrop','pom','#d9b47b #f0d699 #dd987b','flower_lei','pinwheel',
  'Coaxes a pinwheel with a tiny breath and cheers when the wind takes over.',
  'A honey-colored duck with a spectacular feather pompadour and optimism that has learned to be patient.',[
  'Morning, Cheese! Or afternoon with ambition. Either works.',
  'There is my favorite little weather system.',
  'The pinwheel is resting. It has a demanding career.',
  'A bad day can still contain a very good puddle.',
  'I once organized a sunrise party and slept through it. Everyone liked the quiet.',
  'I am not cheerful all the time. I just leave a little room for it to come back.',
  'Find the warmest patch of grass with me. Very serious research.',
  'You have made today noticeably better. Thank you.',
  'See you soon. You do not have to smile for me to be glad you are here.'],height=80,pace=3.7,social=.7,radius=12)

F('Shadow','mysterious','runner','wedge','#8894ac #a1b3ba #a8bd87','cape','shutter_lantern',
  'Opens a shuttered lantern just a crack and checks whether anyone noticed.',
  'A tall slate silhouette with a pointed crest; practices ominous entrances and secretly repairs birdhouses.',[
  'We meet at last. Again. The wording is difficult after the first time.',
  'I was never gone. Except briefly, for groceries.',
  'Every pond has secrets. This one has a surprisingly aggressive shopping list.',
  'I work in the shadows. Mostly because the glare gives me a headache.',
  'Someone left a repaired birdhouse outside your gate. Mysterious. Very mysterious.',
  'It is easier to do kind things when nobody makes a fuss about them.',
  'Keep watch. I am performing a covert act of tidying.',
  'You should not have. I am extremely glad you did. Tell no one.',
  'I vanish now. Please ignore the squeaky foot.'],height=91,pace=3.3,social=.25,radius=16)
F('Phantom','mysterious','barrel','bob','#ada3bd #d9ced8 #ccae79','hat_tophat','mask',
  'Raises a theatre mask, peeks over it, and performs a completely unnecessary bow.',
  'A broad lilac theatrical duck with a velvet-dark cape and an entrance for every occasion.',[
  'Behold! A visitor! Yes, it is me. The smoke budget was cut.',
  'The sequel arrives. Critics describe it as much the same duck.',
  'I am rehearsing a tragic monologue about an empty biscuit tin.',
  'Mystery is ninety percent lighting and ten percent not answering practical questions.',
  'I haunted a shed once. The owner asked if I could help with the shelves.',
  'The costume helps me say things I am too shy to say as myself.',
  'You take the dramatic pause. I will handle the dramatic everything else.',
  'A tribute! Oh. An actual thoughtful present. That is considerably better.',
  'Farewell, sweet pond! I will be just behind that tree if you need me.'],height=88,pace=3,social=.4,radius=10)
F('Enigma','mysterious','pocket','brow','#b5ac8d #c4c5ad #a2b9d1','monocle','puzzle',
  'Turns a little wooden puzzle, solves it, and immediately pretends it is still difficult.',
  'A square-browed pocket duck in muted olive; asks riddles but cannot keep a birthday secret.',[
  'What has two feet and too many questions? Hello.',
  'You found me. Admittedly I was standing in the usual place.',
  'I brought a puzzle. The first puzzle is where I put the instructions.',
  'The answer was friendship. Terrible riddle. Excellent answer.',
  'I hid a present so well I had to give the recipient a second present: an apology.',
  'Not everything needs solving. I am trying to learn that without making it a puzzle.',
  'Hold this piece. No, that is the whole puzzle. You solved it emotionally.',
  'How did you know? No, do not tell me. I like this mystery.',
  'Until the next question mark, Cheese.'],height=65,pace=3.5,social=.35,radius=9)
F('Whisper','mysterious','low','sleepy','#b5bbb7 #ddd9cf #a1c1b2','scarf_winter','listening_shell',
  'Leans toward a shell, answers with one quiet syllable, and folds the scarf closer.',
  'A small, long-bodied pearl-gray duck who collects pond sounds and never mistakes quiet for empty.',[
  'Hello, Cheese. I brought a quiet sort of hello.',
  'I recognized your footsteps. One determined little scuff.',
  'That reed makes a different sound when rain is coming.',
  'You can sit without talking. I am very good at the other half of that conversation.',
  'I recorded the dawn once. Mostly it was my own stomach.',
  'People talk over quiet things. Thank you for not doing that to me.',
  'Listen. There is a tiny sound hiding under the large one.',
  'Oh. You listened when I mentioned it. I will remember that.',
  'I will leave the quiet with you. There is plenty.'],height=64,pace=2.3,social=.3,radius=6)
F('Raven','mysterious','teardrop','swept','#82919e #a0aabd #ce9eaa','masquerade_mask','quill',
  'Writes one brooding line, crosses it out, and adds a tiny smiling duck.',
  'An ink-blue duck with a razor crest and a poet’s solemn face; writes secretly terrible limericks.',[
  'The pond broods. I brood. You appear to be looking for lunch.',
  'Another chapter. Same questionable protagonist. I mean me.',
  'I am writing about the abyss. It is the deep bit beside the dock.',
  'Nothing rhymes with orange. A personal attack on my sunset poem.',
  'My darkest poem was used to wrap a sandwich. The reader said it was moving.',
  'I write down ordinary days because losing them frightens me a little.',
  'Give me a word, Cheese. Preferably one with a manageable number of syllables.',
  'I shall commemorate this in verse. You may request the short version.',
  'May your night contain only the interesting kind of darkness.'],height=87,pace=3.6,social=.3,radius=13)

F('Charity','generous','barrel','curly','#c4a592 #e0c4a5 #b0bfa4','scarf_striped','sewing',
  'Mends a tiny sock, holds it up to the light, and discovers a second hole.',
  'A broad, cinnamon-seamed duck with a knitting basket and an inability to leave a loose button alone.',[
  'Hello, love. Hold still. Your imaginary button is loose.',
  'There you are. I made too much again. A mysterious recurring accident.',
  'I knit while I think. You can tell the difficult thoughts by the lumpy bits.',
  'A patch is a thing deciding it is not finished being useful.',
  'I made a scarf for a snake once. We had to discuss where the neck ended.',
  'I am learning to let people help me too. Turns out that is part of kindness.',
  'Keep me company while I fix this. Company counts as helping.',
  'For me? Sit down. I need a moment to be looked after.',
  'Be kind to yourself, Cheese. I cannot be everywhere.'],height=83,pace=2.8,social=.75,radius=8)
F('Grace','generous','runner','bob','#a9b9bc #e5d8c5 #c4a5c9','pearl_necklace','tea_cup',
  'Balances a teacup, corrects her posture, and quietly rescues a spilled drop.',
  'A tall pearl duck with immaculate feathers and the diplomatic skill to call chaos a lively afternoon.',[
  'Cheese, darling. What a beautifully assertive mess.',
  'I hoped I would find you here. I brought the good cups.',
  'Etiquette is mostly making sure nobody feels foolish. The tiny spoon is optional.',
  'I do not gossip. I provide context with excellent refreshments.',
  'I hosted a formal tea during a thunderstorm. We drank from the rain-filled cups.',
  'Being composed is not the same as being fine. I appreciate when you ask.',
  'Tea? You may hold the cup however your wings manage.',
  'How thoughtful. I shall use it, not save it for a mythical better day.',
  'Look after your little corner of the world, darling.'],height=95,pace=2.9,social=.65,radius=8)
F('Blessing','generous','pear','round','#acb991 #d4d5b7 #dca387','spring_flower_crown','sprout',
  'Shelters a seedling in both wings and turns it gently toward the light.',
  'A soft sage-green duck with round cheeks, soil under the feathers and fierce faith in second chances.',[
  'Good to see you growing, Cheese. Even sideways counts.',
  'Your little patch has changed. So have you. Both quietly.',
  'This seedling was marked unlikely. I dislike that sort of label.',
  'Compost is a second chance with a very distinctive smell.',
  'I planted a whole bed upside down once. The plants sorted me out.',
  'I keep things alive because somebody once did that for me on a hard day.',
  'Let us give this small thing a better place to begin.',
  'I will take good care of it. You can come and check.',
  'See you soon. Drink some water. Yes, standing in it is different.'],height=77,pace=3,social=.6,radius=9)
F('Angel','generous','pocket','tuft','#c0cbcf #e9e0ce #d7a095','bow_tie_blue','first_aid',
  'Checks a little first-aid tin and applies a plaster to a scuffed toy.',
  'A tiny cloud-white duck with one feather sticking up and the stern tenderness of a village nurse.',[
  'Hello, Cheese. Any scrapes, worries, or suspiciously brave faces?',
  'Good, you are here. I can stop pretending I was not checking.',
  'This plaster has a star on it. Medically essential, obviously.',
  'Rest is not a prize you earn by falling over first.',
  'I once bandaged a scarecrow. He looked like he needed someone to fuss.',
  'I worry because I care. I am practicing doing the second part without so much first part.',
  'Sit with me a moment. That is the entire prescription.',
  'You took care of me. Oh. That is a rather lovely feeling.',
  'No heroic nonsense until after a snack.'],height=62,pace=3.9,social=.8,radius=7)
F('Heart','generous','teardrop','pom','#c79a9d #e5bfc0 #c4a77a','heart_glasses','letter',
  'Seals a letter, hesitates, and adds one more tiny heart to the envelope.',
  'A rose-colored duck with a soft quiff, an oversized satchel and handwritten notes for everyone.',[
  'Cheese! I wrote you a note. Then remembered I could just come say it.',
  'I kept the last nice thing you said. It fits in a very small envelope.',
  'I put too many stamps on letters so they feel encouraged.',
  'A love letter can just say I saved you the good seat.',
  'I mailed a letter to myself once. It was surprisingly nice to receive.',
  'I worry people do not know they matter. So I tell them. Sometimes twice.',
  'Help me think of something kind to write that is not unbearably mushy.',
  'Oh, you absolute sweetheart. I will be sentimental about this forever.',
  'You matter, Cheese. There. Delivered in person.'],height=81,pace=3.6,social=.85,radius=10)

F('Cookie','foodie','barrel','round','#c99d75 #e4c49c #ba9dce','hat_chef','cookie_tray',
  'Offers a tray, counts the biscuits, and notices a suspiciously beak-shaped gap.',
  'A flour-dusted round baker with oven-mitt wings and a laugh like a warm kitchen.',[
  'Fresh batch, Cheese. Quality control was ruthless. There are two left.',
  'I know that look. Yes, I brought them.',
  'A recipe is a suggestion written by someone who was not hungry enough.',
  'These are rustic. That means I dropped the tray and kept my confidence.',
  'My first cake was a doorstop. Excellent at that, honestly.',
  'Feeding someone is easier than saying I am glad they exist. Both count.',
  'Taste this and be honest. Kindly honest. I have feelings and a rolling pin.',
  'For the kitchen? Or for me? Oh, both. Lovely.',
  'Eat something proper later. Yes, more biscuits was your argument last time.'],height=85,pace=3,social=.7,radius=8)
F('Biscuit','foodie','low','small','#bda785 #d8c4a3 #c89f6d','beanie_striped','jam',
  'Unscrews a jam jar, tastes one careful dab, and screws it shut with great resolve.',
  'A short, long-backed toasted-brown duck with a tiny cap and the patience of a properly brewed cup.',[
  'All right, Cheese? Sit down. Nothing urgent survives a good snack.',
  'Same time, same crumbs. That is a tradition now.',
  'I have strong opinions about jam. I am sparing you most of them.',
  'Crunch is a mood. Crumble is a lifestyle.',
  'I once entered a baking contest by accident. I was looking for the queue to eat.',
  'Familiar things help on unfamiliar days. I like being one of your familiar things.',
  'We could share this. I have calculated a generous division. Twice.',
  'Ah, you know me. That is better than the actual present. Almost.',
  'Keep a crumb for later. Future you is usually hungry.'],height=63,pace=2.5,social=.5,radius=7)
F('Truffle','foodie','shaggy','brow','#a29185 #c6b69d #ba9c83','autumn_leaf_crown','mushroom_basket',
  'Sniffs a mushroom basket, rejects a leaf, then sniffs the leaf just in case.',
  'A shaggy earth-colored forager with a low brow and the solemnity of a tiny woodland detective.',[
  'Something smells interesting. Could be lunch. Could be that boot.',
  'Cheese. I remembered your scent. Pond, attitude, faint bread.',
  'This mushroom is for looking at. I am fond of staying alive.',
  'A good nose finds dinner. A good brain asks a second opinion.',
  'I tracked a magnificent aroma for a mile. It was my own lunch bag.',
  'The woods are quieter with company. Not silent-quiet. Safe-quiet.',
  'Come forage with me. We can admire everything and eat only the sensible bits.',
  'That is worth a proper sniff. High praise, in my family.',
  'Follow your nose. Ask your brain before biting.'],height=78,pace=3.2,social=.35,radius=16)
F('Pepper','foodie','runner','wedge','#a98981 #c2a092 #df9a72','bandana','pepper_mill',
  'Grinds one dramatic twist of pepper, sneezes, and blames the weather.',
  'A sharp little russet runner with pointed feathers, rolled cuffs and unreasonable confidence in seasoning.',[
  'Needs pepper. Hello, Cheese. That applies to the conversation too.',
  'Back for another serving of my delightful personality?',
  'A pinch means whatever you can defend afterward.',
  'Bland is not a flavor. It is a cry for help.',
  'I overspiced a soup once. We used it to settle a neighborhood argument.',
  'I talk loudly when I care. I am learning the difference between flavor and volume.',
  'Taste and advise. You may swear. It is useful feedback.',
  'Oh, you know how to season a friendship. Nicely done.',
  'Stay sharp. Drink water. Ignore my advice about chili quantities.'],height=80,pace=4.5,social=.6,radius=12)
F('Ginger','foodie','pear','curly','#d4a079 #e1bf92 #b5c597','scarf_winter','teapot',
  'Warms a little teapot between her wings and watches the steam make a spiral.',
  'A ginger pear-shaped duck with soft curls, oversized scarf ends and an emergency remedy for everything.',[
  'Come in, Cheese. Figuratively. We are both already outside.',
  'I had a feeling you could use something warm.',
  'This tea fixes almost everything. For the rest, there is sitting together.',
  'Steep for three minutes. Worrying at the pot does not make it faster.',
  'I invented a calming tea so effective I slept through the naming ceremony.',
  'I learned to make comfort when I could not always find it.',
  'Hold your cup in both wings. There. That is already a little better.',
  'What a warm little thought. I will keep it close.',
  'Go gently. The world is not improved by you rushing your tea.'],height=76,pace=2.7,social=.7,radius=8)

F('Dash','athletic','runner','small','#9aab92 #c4cba9 #db9e6e','cap_sports','stopwatch',
  'Times a stretch, checks the result, and rounds it down with a guilty glance.',
  'A lean green runner with a small neat head and a stopwatch that is suspiciously generous to its owner.',[
  'Cheese! Personal best on the way here. In the visiting-a-friend category.',
  'You ready? Good. Neither am I. Excellent starting conditions.',
  'I time everything. Except tea. Tea deserves privacy.',
  'Resting heart rate? Very competitive. I am winning at sitting.',
  'I trained for a marathon and accidentally entered a picnic. Best recovery day ever.',
  'I like having a finish line. Real life is annoyingly vague about those.',
  'One lap together. Your pace. I can learn something.',
  'A gift! I have no metric for this. Feels like a record, though.',
  'See you on the next lap. Or at the snack table.'],height=86,pace=5.6,social=.5,radius=19)
F('Sprint','athletic','teardrop','swept','#a99285 #bfc5b5 #d7ba78','bandana','laces',
  'Reties one enormous shoelace, tests it with a quick step, and reties the other.',
  'A low aerodynamic duck whose determined crest points forward while the rest of him is already leaving.',[
  'Quick hello, Cheese. Actually, no. Proper hello. I am practicing.',
  'Came the long way. It had fewer things I had already run past.',
  'These knots are aerodynamic. They also refuse to stay tied.',
  'There is fast, and there is knows-where-the-hell-they-are-going. I have one.',
  'I once outran a thunderstorm. Then waited in it because my friend was behind.',
  'Going slower for somebody is not losing. Took me a while to get that.',
  'Race to the next reed? Winner helps the other one find their breath.',
  'You thought of me while I was busy thinking about speed. Thank you.',
  'Catch you later. Not a challenge. Unless you want it to be.'],height=77,pace=6.2,social=.45,radius=21)
F('Champion','athletic','barrel','pom','#b7a075 #d2bd93 #c7b875','bandana','trophy',
  'Polishes a cracked trophy and turns the crack proudly toward the light.',
  'A broad-chested golden duck with a heroic quiff and a trophy earned by finishing last with someone else.',[
  'Cheese! Good effort existing today. Strong fundamentals.',
  'There is the team. All two of us. Formidable.',
  'The trophy is cracked. That is where the extra character gets in.',
  'A champion thanks the duck who carried the water.',
  'My favorite medal is for a race I did not win. I stopped to help someone finish.',
  'I was not always confident. Sometimes the loud encouragement is for me too.',
  'Show me your best terrible stretch. Nobody is getting judged.',
  'This goes on the shelf with the important wins.',
  'Proud of you. You do not need a reason every time.'],height=94,pace=3.8,social=.75,radius=12)
F('Victor','athletic','pear','brow','#a1a9b8 #c5c9cc #d9a17b','glasses_nerd','clipboard',
  'Checks a training clipboard, whistles silently, and adds a snack break.',
  'A sturdy gray coach with heavy eyebrows, a whistle and a schedule containing suspiciously generous rests.',[
  'Morning assessment: you are a duck. Promising start.',
  'Good attendance, Cheese. I have drawn a little star.',
  'I scheduled spontaneity for later. We may move it forward if necessary.',
  'Hydrate, stretch, complain. In that order, ideally.',
  'I coached a snail once. Tremendous commitment. We are still on the warm-up.',
  'I make plans because surprises used to scare me. Nice ones still catch me out.',
  'Try one small improvement. Then we will celebrate a frankly disproportionate amount.',
  'This was not on the schedule. I am making room for it immediately.',
  'Rest is on the plan. Do not make me underline it.'],height=84,pace=3.4,social=.6,radius=11)
F('Rocket','athletic','pocket','tuft','#a2b8bf #ced7c1 #e18c6a','space_helmet','rocket',
  'Counts down on tiny toes, crouches for takeoff, then gives the ground a skeptical look.',
  'A compact blue daredevil with a huge helmet and plans that exceed the available duck.',[
  'Three, two, one—hello! Still working on the launch part.',
  'Mission control, I have returned with dirt on my face.',
  'The helmet is for safety. Also, I sound magnificent inside it.',
  'Gravity is a very persistent heckler.',
  'I built a rocket from reeds. It became an excellent whistle. Flexible objectives.',
  'I want to do something big. I am learning small brave things count first.',
  'Be mission control? Tell me when my idea becomes a bad idea.',
  'Oh! Official mission equipment. You are on the crew forever.',
  'To infinity! Or just past the bench. We will assess conditions.'],height=69,pace=5.2,social=.6,radius=17)


def R(key, name, species, shape, head, colors, gear, prop, habit, bio, lines,
      height=90, pace=3.5, radius=12):
    F(name, 'rare', shape, head, colors, gear, prop, habit, bio, lines, height, pace, .5, radius)
    p = PROFILES.pop('friend:' + name.lower())
    p.update(id=key, rare=True, species=species)
    PROFILES[key] = p


R('friendly_goose','Gerald the Goose','goose','goose','goose','#c6c8b4 #ece5cf #d89667','bandana','bread_bag',
  'Patrols with a proud long-necked march, puffs his chest, then offers an embarrassingly small loaf.',
  'A lanky neighborhood watch goose. Loud enough to be a landmark; soft enough to escort a beetle across a path.',[
  'HONK! Neighborhood inspection. You look suspiciously excellent.',
  'Gerald returns! The pond has passed its preliminary honk assessment.',
  'Gerald brought a loaf. It used to be larger. Travel is hungry work.',
  'A goose must protect the little ones. Also the picnic. Especially both together.',
  'Gerald once chased his own reflection out of a puddle. Very effective policing.',
  'Butterflies make Gerald nervous. So much confidence. So little goose.',
  'Come patrol with Gerald. We will check on everybody and pretend it is official.',
  'For Gerald? HONK. That was the quiet emotional honk.',
  'Gerald is needed elsewhere. Probably. Keep being worth a loud entrance.'],height=106,pace=3.6,radius=18)
R('wise_owl','Professor Hoot','owl','owl','owl','#b7a28a #e1d1b6 #c2abdb','','book',
  'Shuffles a feathered wing, turns a page with a talon and peers over crooked spectacles.',
  'A tuft-eared owl in a frayed academic shawl. Knows everything except where he left the bookmark.',[
  'Hoo. I have brought wisdom. And a book to check whether it is correct.',
  'My dear Cheese. Still asking difficult questions by merely existing.',
  'These spectacles are for reading. The second pair is for finding the first.',
  'A footnote is where an author hides a second, less supervised author.',
  'I once lectured a tree stump for twenty minutes. Excellent listener. Poor notes.',
  'Knowing a great deal does not stop you feeling foolish. It gives the feeling better vocabulary.',
  'Turn the page with me. Slowly. There is a pressed biscuit in chapter four.',
  'How thoughtful. I shall write your name inside. In the good handwriting.',
  'Remember to question authority. Particularly if it is wearing my hat.'],height=97,pace=2.5,radius=8)
R('lost_duckling','Pip the Duckling','duckling','pocket','small','#e1c995 #eddda7 #d79c92','scarf_red','plush',
  'Takes three brave little steps, looks back for Cheese, and hugs a lopsided toy frog.',
  'A tiny fluffy duckling with an oversized knitted scarf and a toy frog that is braver than he is.',[
  'Hi. My frog says this pond is safe. Is he right?',
  'Cheese! I found you without getting lost! Well. Only a tiny bit.',
  'This is Captain Ribbit. He is in charge of being brave when I am tired.',
  'I practiced a big quack. It came out as a squeak with plans.',
  'I walked all the way to the tall reed by myself. Somebody should put up a sign.',
  'Can I stay beside you until I remember how to be brave again?',
  'Watch my little jump? Captain Ribbit is watching too, but he is biased.',
  'For me? Captain says thank you. I say it louder. THANK YOU.',
  'Bye, Cheese. I know the way back now. That is my favorite thing to know.'],height=52,pace=4.8,radius=5)
R('traveling_merchant','Marco the Merchant','duck','barrel','longbill','#bd936f #c9b889 #c398c7','hat_tophat','case',
  'Sets down a many-pocketed case, snaps it open and polishes one absolutely ordinary pebble.',
  'A squat traveling salesman with a battered stovepipe hat, striped waistcoat and a fondness for hopeless bargains.',[
  'Cheese! Fine wares, questionable provenance, impeccable customer service.',
  'My favorite customer! A statement I make to very few ducks at once.',
  'This pebble is unique. So is every pebble. I prefer not to mention the second bit.',
  'The price includes a story. The story may include further prices.',
  'I sold a hole once. The buyer wanted somewhere to put a fence post. Honest business.',
  'I remember every place that lets me sit down without asking what I am selling.',
  'Have a look. You do not have to buy anything. That bit is sincere.',
  'A gift with no invoice? You are making me reconsider my entire profession.',
  'May your pockets be full and your regrets reasonably priced.'],height=85,pace=2.8,radius=11)
R('celebrity_duck','Sir Quackington III','duck','runner','pom','#b7b7ca #e3d6bc #dbad70','hat_crown cape','rose',
  'Sweeps a velvet cape into a grand bow, checks for an audience, then smiles shyly when noticed.',
  'An elegant, long-necked actor with an extravagant crown, a battered rehearsal rose and very ordinary stage fright.',[
  'Your pond is graced by—oh, it is you, Cheese. May I just sit for a minute?',
  'The triumphant return! Slightly less triumphant knees today.',
  'This crown is heavier than my entire first apartment. It was a bucket.',
  'Applause is lovely. Someone remembering how you take your tea is better.',
  'My first audience was three frogs. Two left. The third was a stone.',
  'Sometimes I worry they love the feathers and not the duck inside them.',
  'Rehearse a bow with me? Yours may contain more contempt. It is a valid interpretation.',
  'For the actual me? Oh. That is unexpectedly moving.',
  'Until we meet again. No fanfare necessary. A little would be nice.'],height=100,pace=2.9,radius=10)
R('mysterious_crow','Corvus the Crow','crow','crow','crow','#929bac #b3bfd1 #c4ad7c','','buttons',
  'Hops sideways, checks a button collection and hides the shiniest one under a patched wing.',
  'A scruffy charcoal crow with one bent tail feather, silver buttons and the manners of a suspicious antique dealer.',[
  'Nice pond. Anything shiny here legally unattended?',
  'Cheese. I returned the spoon. A spoon. Let us not dwell on details.',
  'This button has history. Mostly being a button, but it did that very well.',
  'I do not steal. I relocate things into a more appreciative social environment.',
  'I once traded a ring for a sandwich. Best investment of my life. Terrible resale value.',
  'I bring you odd little things because I am not very good at bringing myself.',
  'Judge these buttons. Be cruel. They need honest criticism.',
  'You picked this for me? I will hide it somewhere better than the others.',
  'Keep one eye on the sky. And one on the cutlery.'],height=83,pace=4.4,radius=16)
R('butterfly_fairy','Flutter','butterfly','butterfly','butterfly','#b8a2cc #e8c5d7 #aad5bc','','pollen',
  'Hovers in little figure-eights, fans patterned wings and shakes pollen from one offended antenna.',
  'A tiny theatrical pollinator with lace-edged wings, mismatched antenna curls and strong opinions about flowers.',[
  'Darling, your air is lovely. A little humid. Very flattering to the wings.',
  'Cheese! I followed the flowers. Then the unmistakable atmosphere of you.',
  'This pollen is everywhere. I am a magical being and also a lint problem.',
  'Metamorphosis is glamorous after the bit where you become soup.',
  'I once landed on a painted flower. Charming conversation. Terrible refreshments.',
  'Being delicate does not mean I have not survived a very strange amount.',
  'Hold still. You have a speck of ordinary on you. There, improved.',
  'Oh! I shall make room in my impossibly small luggage.',
  'Bloom outrageously, Cheese. Even if it annoys someone.'],height=66,pace=4.6,radius=18)
R('grumpy_toad','Grumble the Toad','toad','toad','toad','#9fa47c #c1bd93 #c1a07b','','mug',
  'Settles his broad belly, sips from a chipped acorn mug and performs one profoundly dissatisfied hop.',
  'A squat, wart-speckled toad with heavy lids and a hand-knitted vest he claims to hate but never removes.',[
  'Hmph. Moved my nice damp rock. By which I mean I moved. Still annoying.',
  'You again. Good. Someone sensible to complain near.',
  'This mug says cheerful. I have registered a complaint with the acorn.',
  'Too sunny for a drizzle. Too dry for a proper misery. Make up your mind, weather.',
  'Someone knitted me this vest. It is hideous. Touch it and lose a finger.',
  'I come here because you do not tell me to cheer up. Makes me almost cheerful.',
  'Sit. We can dislike the same cloud. Efficient use of company.',
  'Hmph. That is... annoyingly thoughtful. Thank you. Once.',
  'I am leaving. Do not make it a thing. Save my damp bit.'],height=66,pace=2.7,radius=7)

BY_NAME = {p['name'].casefold(): p for p in PROFILES.values()}


def guest_profile(name_or_id):
    return PROFILES.get(name_or_id) or BY_NAME.get(str(name_or_id).casefold())


def guest_line(name_or_id, section, duck_name='Cheese'):
    profile = guest_profile(name_or_id)
    line = profile['voice'].get(section, '') if profile else ''
    return line.replace('Cheese', duck_name)


if __name__ == '__main__':
    import json
    from pathlib import Path
    target = Path(__file__).resolve().parents[1] / 'engine/client/guest-cast.mjs'
    target.write_text('// Generated from world/guest_cast.py. Shared names, art direction and voice.\n'
                      + 'export const GUEST_CAST=' + json.dumps(PROFILES, ensure_ascii=False, separators=(',', ':')) + ';\n')
    print(f'Exported {len(PROFILES)} named guests')
