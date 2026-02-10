"""
Duck Facts and Trivia System - Fun facts about ducks to share with players.
Also includes birthday tracking and special messages.
"""
import random
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass


# Fun duck facts - educational and entertaining
DUCK_FACTS = [
    # Confused origins
    "Cheese once forgot which end of the bread to eat. He still hasn't figured it out.",
    "Cheese got lost in a straight hallway. Twice. The same hallway.",
    "Cheese once tried to fight his own reflection. The reflection won.",
    "Cheese thinks the moon is a very large crumb. No one has corrected him.",
    "Cheese once walked into a glass door, apologized to it, then did it again.",
    
    # Questionable intelligence
    "Cheese has forgotten his own name mid-introduction. Multiple times.",
    "Cheese once spent three hours trying to befriend a statue. He still waves at it.",
    "Cheese believes he's invisible when he closes his eyes.",
    "Cheese once got scared by his own sneeze and hasn't fully recovered.",
    "Cheese tried to swim in a puddle and got confused when it wasn't deep enough.",
    
    # Endearing failures
    "Cheese has walked into the same wall seventeen times. He blames the wall.",
    "Cheese once forgot how to sit down halfway through sitting down.",
    "Cheese tried to intimidate a butterfly. The butterfly was not intimidated.",
    "Cheese gets lost going to places he's been a hundred times. Every. Single. Time.",
    "Cheese once mistook a pinecone for a friend. He named it Gerald.",
    
    # Confused about basic concepts
    "Cheese thinks clouds are just sky bread. He's been disappointed every time.",
    "Cheese believes his reflection is a very rude duck who copies him.",
    "Cheese once tried to fly by just believing really hard. Gravity disagreed.",
    "Cheese has never successfully predicted where his next step will go.",
    "Cheese forgets he can swim. In the middle of swimming. Regularly.",
    
    # Lovable disasters
    "Cheese once chased his own tail for so long he forgot why he started.",
    "Cheese has never successfully caught a bug. The bugs feel bad for him at this point.",
    "Cheese thinks 'Tuesday' is a type of weather.",
    "Cheese regularly walks the wrong direction and calls it 'the scenic route.'",
    "Cheese once forgot what bread was while eating bread.",
    
    # Peak derp energy
    "Cheese has been startled by the same leaf eight days in a row.",
    "Cheese once tried to drink water and forgot how. He eventually remembered.",
    "Cheese thinks he's being sneaky when he waddles loudly while making eye contact.",
    "Cheese has never won a game, but insists he's 'letting everyone else have fun.'",
    "Cheese gets confused by stairs. Not going up them. Just... stairs existing.",
    
    # Cheese-specific mysteries
    "Cheese once forgot mid-quack what he was quacking about.",
    "Cheese thinks naps are a competitive sport. He's undefeated at losing.",
    "Cheese tried to make friends with his own shadow. The shadow left.",
    "Cheese regularly forgets he has wings. And feet. And sometimes a head.",
    "Cheese is the reason 'duck-brained' is an insult. He considers it a compliment.",
    
    # Additional origins (41-55)
    "Cheese was born confused and has maintained that energy ever since.",
    "Cheese once asked a rock for directions. He's still waiting for a response.",
    "Cheese believes he invented waddling. He did not.",
    "Cheese once got his head stuck in a bush. He blamed the bush.",
    "Cheese thinks he's a natural leader. He has never successfully led anything.",
    "Cheese once tried to count to ten. He got to seven and celebrated.",
    "Cheese thinks alphabetical order is just a suggestion.",
    "Cheese once forgot what feet were. While standing.",
    "Cheese believes rain is the sky crying because it misses him.",
    "Cheese once tried to high-five a fish. It went as expected.",
    "Cheese thinks echoes are other ducks agreeing with him.",
    "Cheese once tried to read a book upside down for an hour before giving up.",
    "Cheese believes he speaks fluent human. He does not.",
    "Cheese once asked a tree for its opinion. The tree did not respond.",
    "Cheese thinks gravity is a personal attack against him specifically.",
    
    # More failures (56-75)
    "Cheese has tripped over nothing an estimated 4,000 times.",
    "Cheese once tried to sneak up on a leaf. The leaf saw him coming.",
    "Cheese attempted to build a nest once. It was just a pile.",
    "Cheese once forgot he was eating mid-bite.",
    "Cheese tried to look cool once. He immediately fell over.",
    "Cheese once got startled by his own quack.",
    "Cheese has never successfully completed a thought.",
    "Cheese once tried to wink. Both eyes closed. He called it a success.",
    "Cheese attempted to be mysterious once. He sneezed and ruined it.",
    "Cheese once forgot which way was forward. He was already walking.",
    "Cheese tried to give someone the silent treatment. He forgot after two seconds.",
    "Cheese once got confused by a straight line.",
    "Cheese has never won hide and seek. He always reveals himself.",
    "Cheese once tried to look threatening. He yawned instead.",
    "Cheese forgot he was mad at someone while still being mad at them.",
    "Cheese tried to act natural. He has never looked less natural.",
    "Cheese once forgot he had a beak mid-peck.",
    "Cheese has gotten lost in his own thoughts. Regularly.",
    "Cheese once tried to remember something. He remembered something else.",
    "Cheese has never followed instructions correctly.",
    
    # Basic concept confusion (76-95)
    "Cheese thinks doors are just very polite walls.",
    "Cheese believes wind is just the air showing off.",
    "Cheese once asked why the sky is up. He's still processing the answer.",
    "Cheese thinks shadows are just very flat friends.",
    "Cheese believes puddles are ponds that gave up.",
    "Cheese once tried to understand math. Math won.",
    "Cheese thinks morning is a conspiracy against his naps.",
    "Cheese believes cold is just spicy air.",
    "Cheese once asked where bread comes from. He forgot the answer immediately.",
    "Cheese thinks sleep is just practice for being a rock.",
    "Cheese believes running is just panicked walking.",
    "Cheese once tried to figure out why water is wet. He gave up.",
    "Cheese thinks hunger is his stomach being dramatic.",
    "Cheese believes feathers are just fancy fur.",
    "Cheese once asked if fish know they're wet. No one answered.",
    "Cheese once forgot he was walking and kept walking.",
    "Cheese tried to focus once. It lasted a third of a second.",
    "Cheese once stared at food for so long he forgot he was hungry.",
    "Cheese has never made the same mistake twice. He makes new ones.",
    "Cheese once forgot he was confused and became more confused.",
    
    # Peak derp continued (96-115)
    "Cheese thinks every day is his birthday. It never is.",
    "Cheese once tried to look serious. He started giggling.",
    "Cheese has never remembered a face. Including his own.",
    "Cheese once forgot he was standing still. He was not.",
    "Cheese tried to explain something once. No one understood. Including him.",
    "Cheese has asked the same question three times in one minute.",
    "Cheese once forgot mid-waddle what waddling was.",
    "Cheese thinks waiting is a sport. He's terrible at it.",
    "Cheese once got confused by a straight answer.",
    "Cheese has never successfully looked where he was going.",
    "Cheese once tried to concentrate. He sneezed.",
    "Cheese forgets he's a duck sometimes. He's reminded by quacking.",
    "Cheese once got lost going in a circle.",
    "Cheese tried to have a strategy once. He forgot it immediately.",
    "Cheese has never finished a sentence without getting distrac—",
    "Cheese once panicked because he couldn't see. His eyes were closed.",
    "Cheese thinks he's unpredictable. He's very predictable.",
    "Cheese once sneezed so hard he confused himself.",
    "Cheese tried to be graceful once. He tripped into a puddle.",
    "Cheese once panicked because he couldn't find his feet. They were attached.",
    
    # Food obsession (116-140)
    "Cheese has started sentences he has never finished.",
    "Cheese once got distracted by his own thought. He lost it.",
    "Cheese tried to be stealthy. He quacked.",
    "Cheese once forgot he was sleeping. While sleeping.",
    "Cheese has never remembered where he put anything. Ever.",
    "Cheese once got jealous of himself. It made sense to him.",
    "Cheese tried to look dignified. He hiccupped.",
    "Cheese once forgot he was happy and kept being happy anyway.",
    "Cheese has never successfully planned anything.",
    "Cheese once got confused by a corner.",
    "Cheese once ate bread so fast he forgot he ate it.",
    "Cheese thinks crumbs are just baby bread.",
    "Cheese once tried to save bread for later. He ate it immediately.",
    "Cheese believes every meal is his last. It never is.",
    "Cheese once forgot what he was eating while eating it.",
    "Cheese thinks stale bread is just bread with experience.",
    "Cheese once argued with a sandwich. The sandwich won.",
    "Cheese believes snacks are just surprise meals.",
    "Cheese once tried to ration his food. He lasted four seconds.",
    "Cheese thinks full is just a suggestion.",
    "Cheese once forgot he was chewing. He kept chewing.",
    "Cheese believes food tastes better when stolen. He has stolen nothing.",
    "Cheese once mourned a crumb he dropped. For three days.",
    "Cheese thinks vegetables are a myth.",
    "Cheese once tried to share food. He couldn't do it.",
    
    # Food continued (141-155)
    "Cheese believes the five-second rule is actually five minutes.",
    "Cheese once tried to cook. No one knows what happened. He won't discuss it.",
    "Cheese thinks eating is cardio.",
    "Cheese once forgot he was full and kept eating. Regrets were had.",
    "Cheese believes breakfast, lunch, and dinner should all be breakfast.",
    "Cheese once waved at someone who wasn't waving at him. He hasn't recovered.",
    "Cheese thinks staring is a form of greeting.",
    "Cheese once forgot he was in a conversation. While talking.",
    "Cheese believes everyone is his friend. Including enemies.",
    "Cheese once tried to make small talk. He panicked and quacked.",
    "Cheese thinks nodding counts as a full response.",
    "Cheese once forgot someone's name mid-sentence. He made one up.",
    "Cheese believes awkward silence is just thinking time.",
    "Cheese once tried to be charming. He sneezed on someone.",
    "Cheese thinks personal space is for other ducks.",
    
    # Social confusion (156-175)
    "Cheese once laughed at a joke he didn't understand. He still doesn't.",
    "Cheese believes compliments are just facts about him.",
    "Cheese once tried to be helpful. He made things worse.",
    "Cheese thinks eye contact is a competition. He always loses.",
    "Cheese once forgot he was listening and said 'yes' anyway.",
    "Cheese believes being loud counts as being interesting.",
    "Cheese once tried to keep a secret. He told everyone immediately.",
    "Cheese thinks whispering is just quiet yelling.",
    "Cheese once forgot how to say goodbye and just waddled away.",
    "Cheese believes interrupting is just enthusiastic listening.",
    "Cheese once tried to apologize. He forgot what for.",
    "Cheese thinks everyone should be as confused as he is.",
    "Cheese once made a friend. He immediately forgot their name.",
    "Cheese believes waving is just arm flapping with purpose.",
    "Cheese once tried to comfort someone. He patted them too hard.",
    "Cheese thinks he's very tall. He is not.",
    "Cheese once tried to describe himself. He got it wrong.",
    "Cheese believes he's intimidating. No one is intimidated.",
    "Cheese thinks he has excellent memory. He forgot that thought.",
    "Cheese once tried to improve himself. He napped instead.",
    
    # Self-awareness failures (176-200)
    "Cheese believes he's always right. Evidence suggests otherwise.",
    "Cheese thinks he's mysterious. He's an open book.",
    "Cheese once tried to be humble. He bragged about it.",
    "Cheese believes he's a morning duck. He hates mornings.",
    "Cheese thinks he handles stress well. He does not.",
    "Cheese once tried to be patient. He lasted one second.",
    "Cheese believes he's a good listener. He's already thinking about bread.",
    "Cheese thinks he's athletic. He trips standing still.",
    "Cheese once tried to be organized. Everything got worse.",
    "Cheese believes he's good at directions. He's lost right now.",
    "Cheese thinks he has good instincts. His instincts are wrong.",
    "Cheese once tried to be responsible. He forgot what he was responsible for.",
    "Cheese believes he learns from mistakes. He makes the same ones.",
    "Cheese thinks he's independent. He needs constant supervision.",
    "Cheese once tried to be on time. He was three hours late.",
    "Cheese believes he's low maintenance. He is not.",
    "Cheese thinks he's quiet. Everyone can hear him.",
    "Cheese once tried to blend in. He stood out immediately.",
    "Cheese believes he's mature. He just quacked at nothing.",
    "Cheese thinks he's observant. He missed the obvious.",
    "Cheese once fell asleep mid-sentence. The sentence was about sleeping.",
    "Cheese thinks napping is an achievement. It's his only one.",
    "Cheese once dreamed he was awake. He was right.",
    "Cheese believes he doesn't snore. He snores loudly.",
    "Cheese thinks sleeping is just long blinking.",
    
    # Sleep and dreams (201-220)
    "Cheese once forgot he was tired after sleeping.",
    "Cheese believes dreams are just brain movies. His are confusing.",
    "Cheese thinks 'five more minutes' means an hour.",
    "Cheese once slept through something important. No one remembers what.",
    "Cheese believes being awake is overrated.",
    "Cheese thinks yawning is contagious. He yawns at himself.",
    "Cheese once napped so hard he forgot the day.",
    "Cheese believes mornings should be illegal.",
    "Cheese thinks bedtime is a flexible concept.",
    "Cheese once dreamed about bread. He woke up disappointed.",
    "Cheese believes rest is just horizontal waiting.",
    "Cheese thinks he doesn't need sleep. He always needs sleep.",
    "Cheese once fell asleep standing up. He fell over.",
    "Cheese believes being cozy is a personality trait.",
    "Cheese thinks sleep schedules are for other ducks.",
    "Cheese believes he's famous. He is not.",
    "Cheese thinks rules are just suggestions for other ducks.",
    "Cheese once had an opinion. He forgot it.",
    "Cheese believes he's always busy. Doing what is unclear.",
    "Cheese thinks luck is a skill. He has neither.",
    
    # Opinions and beliefs (221-245)
    "Cheese once tried to have a hot take. It was lukewarm.",
    "Cheese believes everything happens for a reason. He doesn't know the reasons.",
    "Cheese thinks he's street smart. He's never seen a street.",
    "Cheese once tried to be philosophical. He got confused.",
    "Cheese believes he peaked early. He has not peaked.",
    "Cheese thinks timing is everything. His timing is terrible.",
    "Cheese once tried to make a point. He circled back to bread.",
    "Cheese believes first impressions matter. His are always wrong.",
    "Cheese thinks he's a natural. At what is unknown.",
    "Cheese once had a theory. It was about bread. Again.",
    "Cheese believes hard work pays off. He avoids hard work.",
    "Cheese thinks he's ahead of his time. He's behind on everything.",
    "Cheese once tried to give advice. It was terrible advice.",
    "Cheese believes everything is figure-outable. He has figured out nothing.",
    "Cheese thinks age is just a number. He doesn't know his number.",
    "Cheese once tried to have wisdom. He had a nap instead.",
    "Cheese believes in second chances. He's on his fifteenth.",
    "Cheese thinks consistency is key. He's consistently confused.",
    "Cheese once tried to believe in himself. He got distracted.",
    "Cheese believes the universe has a plan. It probably doesn't include him.",
    "Cheese once forgot what he forgot. He considers this progress.",
    "Cheese thinks every problem solves itself. They don't.",
    "Cheese once tried to be normal. He doesn't know what that means.",
    "Cheese believes he's underestimated. He's accurately estimated.",
    "Cheese thinks chaos is just surprise organization.",
    
    # Final miscellaneous derp (246-255)
    "Cheese once tried to adult. He's still a duck.",
    "Cheese believes he has everything under control. He has nothing under control.",
    "Cheese thinks confusion is just advanced thinking.",
    "Cheese once tried to understand himself. He gave up quickly.",
    "Cheese believes every day is a fresh start. He makes the same mistakes.",
    "Cheese thinks he's one of a kind. He might be right about that one.",
    "Cheese once forgot he was a duck and tried to bark.",
    "Cheese believes his best days are ahead. His best day was the same as every day.",
    "Cheese thinks he has hidden depths. They're not very deep.",
    "Cheese once tried to reinvent himself. He was still Cheese.",
    "Cheese believes he'll get it right eventually. Eventually never comes.",
    "Cheese thinks tomorrow is another day. He'll forget that too.",
    "Cheese once looked in a mirror and forgot who he was looking at.",
    "Cheese believes in the power of positive thinking. He's positively confused.",
    "Cheese is Cheese. That's the most important fact of all.",

    # Real duck facts (Cheese's deadpan commentary)
    "Ducks have three eyelids. Cheese uses all three to judge you simultaneously.",
    "A duck's quack does not echo. Cheese considers this proof he exists outside the laws of physics.",
    "Ducks can sleep with one eye open. Cheese does this to make sure nobody steals his bread.",
    "Ducklings imprint on the first thing they see. Cheese imprinted on a sandwich. He turned out fine.",
    "Ducks have waterproof feathers due to an oil gland near the tail. Cheese calls this 'premium self-care.'",
    "A group of ducks on land is called a brace. Cheese insists his group be called 'the entourage.'",
    "Ducks can fly at speeds up to 60 mph. Cheese can waddle at 0.3 mph. He calls this 'efficient.'",
    "Duck feet have no nerves or blood vessels, so they can't feel cold. Cheese complains about it anyway.",
    "Ducks have nearly 340-degree vision. Cheese uses this exclusively to spot bread at a distance.",
    "Some duck species can dive up to 60 feet underwater. Cheese tried. He went six inches and panicked.",

    # Cheese's personal commentary on duck biology
    "Cheese firmly believes his inability to fly is a CHOICE. A very committed choice.",
    "Cheese learned that ducks have hollow bones. He spent a week walking very carefully.",
    "Cheese was told that ducks don't have teeth. He has never recovered from this identity crisis.",
    "Cheese discovered male ducks are called drakes. He now insists on being called Drake. No one does.",
    "Cheese held his breath for four seconds once and declared it a personal record. It was.",
    "Cheese has strong feelings about the term 'duck-footed.' His feet are FINE, thank you.",
    "Cheese knows that a duck's feathers weigh more than its skeleton. He considers himself 'luxuriously padded.'",

    # Absurd facts Cheese made up
    "According to Cheese, bread was invented specifically for ducks. Humans just got lucky.",
    "Cheese claims the moon is a giant egg laid by the world's largest duck. He will not hear otherwise.",
    "Cheese insists all ponds are connected by secret underground tunnels. He calls it 'the quack-way.'",
    "According to Cheese, ducks invented swimming. Fish are just copycats. He has no evidence.",
    "Cheese maintains he can speak seventeen languages. They all sound exactly like quacking.",
    "Cheese claims that before ducks existed, the world had no concept of grace. Or chaos.",
    "According to Cheese, the weather forecast is unreliable because it doesn't account for duck feelings.",
    "Cheese believes ducks are the apex predators of the pond. No one has corrected him. Out of pity.",

    # Bread-related duck facts
    "Cheese has a personal bread tier list. Sourdough is S-tier. He will not elaborate further.",
    "Cheese once found a whole baguette. He describes this as the single greatest moment of his life.",
    "The average duck eats about 7 ounces of food per day. Cheese considers this a PERSONAL insult.",
    "Cheese has a bread emergency plan. Step one: find bread. There is no step two.",
    "Cheese believes stale bread builds character. Fresh bread builds happiness. Both are essential.",
    "Cheese once turned down premium duck food because someone nearby had a croissant.",
    "Cheese keeps a mental map of every bread source within waddling distance. His most organized thought.",
    "Cheese considers bread crumbs a form of currency. By this metric, he is occasionally wealthy.",

    # Social commentary on duck life
    "Cheese has observed that humans feed pigeons before ducks. He finds this discrimination appalling.",
    "Cheese believes the pond is a democracy. He has never voted. He just stands there and judges.",
    "Cheese thinks geese are just ducks who chose violence. He respects their commitment.",
    "Cheese has strong opinions about bird feeders. They are never at duck height. Systemic bias.",
    "Cheese believes swans are just ducks with a better publicist.",
    "Cheese is suspicious of pelicans. That beak can hold too many secrets.",
    "Cheese has noticed that humans photograph swans but not ducks. He considers this a hate crime.",
    "Cheese tried to form an alliance with the squirrels once. They betrayed him. For acorns.",
    "Cheese thinks migration is just a fancy word for 'running away from your problems.'",
    "Cheese has deep concerns about the duck-to-bread ratio in his area. The numbers are not good.",

    # ==================== NEW FACTS: Real biology meets Cheese's commentary ====================
    "Ducks can see UV light. Cheese uses this to judge bread quality from across the pond.",
    "A duck's heart beats 300 times per minute. Cheese's beats faster when bread is mentioned.",
    "Ducks have regional accents in their quacking. Cheese insists his accent is 'distinguished.'",
    "Mallard ducks can crossbreed with over 50 species. Cheese finds this gossip distasteful.",
    "Ducks have a corkscrew-shaped anatomy. Cheese requests we change the subject immediately.",
    "A duck's bill has sensory receptors like fingertips. Cheese says this makes bread a 'full sensory experience.'",
    "Ducks preen for hours daily. Cheese calls this 'self-care' and refuses to be rushed.",
    "Some ducks migrate thousands of miles. Cheese migrated from one side of the pond to the other. once.",
    "Duck eggs take 28 days to hatch. Cheese says that's 28 days of thinking about bread.",
    "Ducks can fly right after birth in some species. Cheese tried this. he prefers not to discuss it.",

    # Cheese's bread theology
    "Cheese has a bread prayer. it goes: 'bread.' that's the whole prayer.",
    "Cheese believes there is a bread afterlife. he calls it 'the bakery eternal.'",
    "Cheese has ranked every bread he's ever eaten. the list is 400 entries long.",
    "Cheese once tasted a pretzel and had to sit down for twenty minutes.",
    "Cheese thinks toast is just bread that went through something traumatic.",
    "Cheese considers bagels 'bread with ambition.' he respects them.",
    "Cheese was offered a rice cake once. he has never been more offended.",
    "Cheese believes flatbread is bread that gave up on its dreams. still valid though.",
    "Cheese thinks breadsticks are bread's attempt at being fancy. it worked.",
    "Cheese encountered a gluten-free bread once. he stared at it for five minutes and walked away.",

    # Cheese's pond observations
    "Cheese has named every fish in the pond. they don't respond. typical.",
    "Cheese has a favourite rock. he sits on it. that's the whole relationship.",
    "Cheese keeps a mental map of every bread crumb location for the past year.",
    "Cheese once saw a frog and panicked because he thought it was a tiny angry duck.",
    "Cheese believes the pond has moods. today it's 'mildly judgemental.'",
    "Cheese has territorial disputes with a leaf that keeps floating into his spot.",
    "Cheese thinks the reflection of the moon in the pond is a portal. he will not be convinced otherwise.",
    "Cheese has a nemesis. it's a specific goose. they have never spoken.",
    "Cheese rates his pond 4 out of 5 stars. one star deducted for lack of bread delivery service.",
    "Cheese noticed the pond gets bigger when it rains. he takes personal credit for this.",

    # Cheese's understanding of the world
    "Cheese thinks libraries are bread museums where humans stare at flat things.",
    "Cheese believes cars are just fast rooms that humans sit in for no reason.",
    "Cheese thinks phones are tiny ponds humans stare into. the reflection doesn't even move.",
    "Cheese saw a plane once and assumed it was a very ambitious bird.",
    "Cheese thinks money is just bread coupons that humans trade.",
    "Cheese believes winter is the sky punishing the ground.",
    "Cheese saw a dog once. he has questions. many questions. he will not ask them.",
    "Cheese thinks clocks are circles that humans obey. very strange behaviour.",
    "Cheese saw a cat near the pond once. he maintains eye contact was established. dominance unclear.",
    "Cheese believes stairs are just hills that gave up and went digital.",

    # Cheese's self-mythology
    "Cheese claims he once stared at the sun and the sun blinked first.",
    "Cheese insists he has a six-pack. under the feathers. no, you can't check.",
    "Cheese says he chose this pond. out of all the ponds. the pond should feel honoured.",
    "Cheese maintains he was offered a modelling contract once. from a passing squirrel.",
    "Cheese believes his quack has healing properties. evidence: none. confidence: absolute.",
    "Cheese claims he can predict the weather. his method: looking up. accuracy: 12 percent.",
    "Cheese says he once held his breath for a full minute. witnesses: zero.",
    "Cheese insists he has fans. they're just shy. and possibly imaginary.",
    "Cheese tells people he's an early riser. the pond knows this is a lie.",
    "Cheese claims he invented the concept of floating. ducks everywhere owe him royalties.",

    # ==================== NEW FACTS: Real duck biology meets Cheese ====================
    "Ducks can turn their heads 180 degrees. Cheese uses this exclusively to judge people approaching from behind.",
    "A duck's foot blood vessels work as a heat exchange system. Cheese describes this as 'thermally advanced.' he will not explain further.",
    "Some ducks can sleep on water without sinking. Cheese claims he can sleep anywhere. this is unfortunately true.",
    "Muscovy ducks wag their tails like dogs. Cheese finds this undignified. he does it too. don't bring it up.",
    "Ducks have been around for 80 million years. Cheese considers this proof that ducks got it right the first time.",
    "Baby ducks can swim within hours of hatching. Cheese needed three tries. he prefers not to discuss it.",
    "Some species of duck can fly at altitudes of 21,000 feet. Cheese once flew three feet. he counted. it was enough.",
    "Ducks replace all their flight feathers at once, making them flightless for a period. Cheese calls this 'scheduled maintenance.'",
    "A duck's eye can see more colors than a human eye. Cheese says this makes bread look even better. you wouldn't understand.",
    "Ducks have a third eyelid called a nictitating membrane. Cheese uses it dramatically. for emphasis.",
    "A duck's bill has over 200 lamellae for filtering food. Cheese considers this 'built-in quality control.'",
    "Ducks can regulate blood flow to their feet independently. Cheese calls this 'targeted climate control.' very sophisticated.",

    # ==================== NEW FACTS: Cheese's personal opinions on duck life ====================
    "Cheese believes mornings were invented by someone who hated ducks. no evidence. deep conviction.",
    "Cheese has a theory that the pond was here before everything else. the universe formed around it.",
    "Cheese considers 'sitting' to be an underrated competitive sport. he could go professional.",
    "Cheese thinks waddling is more efficient than walking. he has done zero research on this.",
    "Cheese firmly believes he looks better wet. THIS IS NOT UP FOR DEBATE.",
    "Cheese maintains that staring into the middle distance is a productive use of time.",
    "Cheese has opinions about other ducks' preening habits. he keeps them to himself. mostly.",
    "Cheese thinks every pond should come with a bread dispensary. he will campaign for this.",
    "Cheese believes patience is his greatest virtue. he has none. he is aware of the contradiction.",
    "Cheese considers himself a 'pond influencer.' his follower count is zero. he disputes this.",

    # ==================== NEW FACTS: Made-up facts about ducks ====================
    "According to Cheese, the first duck was carved from a particularly talented piece of bread. it came to life. beautiful origin story.",
    "Cheese insists that ducks collectively decided not to fly years ago. out of protest. the cause has been forgotten.",
    "According to Cheese, every pond has a mayor. it's always a duck. always. don't verify this.",
    "Cheese claims ducks can communicate through water ripples. his messages are always about bread.",
    "According to Cheese, ducks once ruled the entire planet. then they got bored and let humans try.",
    "Cheese insists that quacking in a specific pattern can control the weather. his pattern hasn't worked yet. needs calibration.",
    "According to Cheese, the Northern Lights are caused by migrating ducks flying very fast. very sparkly ducks.",
    "Cheese claims that ducks have a secret society. he is not at liberty to discuss it. except to say he's president.",
    "According to Cheese, the moon controls the tides because a duck told it to. the duck's identity is classified.",
    "Cheese insists there's a duck constellation. it's the best one. astronomers are in denial.",

    # ==================== NEW FACTS: Bread-related duck knowledge ====================
    "Cheese has memorized the structural integrity of every bread type. sourdough: excellent. brioche: suspicious but edible.",
    "Cheese has a permanent bread emergency. the emergency is that there could always be MORE bread.",
    "Cheese once composed a poem about bread. it was three words long. 'bread bread bread.' he wept during the reading.",
    "Cheese maintains a strict bread schedule. the schedule is 'always.' the portion size is 'all of it.'",
    "Cheese has classified bread crumbs by size. the categories are 'adequate,' 'insufficient,' and 'insulting.'",
    "Cheese considers the smell of fresh bread a fundamental right. for all ducks. everywhere. he will draft legislation.",
    "Cheese once tried to explain the importance of bread to a fish. the fish didn't understand. Cheese pities the fish.",
    "Cheese believes that somewhere the perfect bread exists. he will find it. or it will find him.",
    "Cheese has a dream bread journal. every bread-related dream is documented. the journal is 400 pages.",
    "Cheese rates every day by its bread content. most days score 'needs improvement.'",

    # ==================== NEW FACTS: Comparative zoology (ducks always win) ====================
    "Ducks vs geese: ducks chose dignity. geese chose violence. both are valid. ducks are more valid.",
    "Ducks vs swans: swans have better PR but ducks have better personality. Cheese will not be taking questions.",
    "Ducks vs pigeons: pigeons are just ducks who gave up on water. tragic, really.",
    "Ducks vs cats: cats sleep more but ducks sleep with more purpose. Cheese will not elaborate.",
    "Ducks vs dogs: dogs fetch things for humans. ducks just exist and humans are grateful. power dynamics.",
    "Ducks vs fish: fish can't leave the water. ducks can be in OR out. versatility wins. always.",
    "Ducks vs squirrels: squirrels hoard nuts. ducks hoard bread. bread is better. this is objective.",
    "Ducks vs eagles: eagles are dramatic. ducks are understated. true style is restraint.",
    "Ducks vs penguins: penguins wear suits everywhere. ducks wear nothing. confidence is the real outfit.",
    "Ducks vs flamingos: flamingos stand on one leg. showoffs. ducks use both legs. stability over spectacle.",

    # ==================== NEW FACTS: Historical 'duck facts' (invented) ====================
    "In 1492, Columbus's ships were guided by ducks. this has been removed from textbooks. Cheese finds this suspicious.",
    "The Great Wall of China was originally designed to keep geese out. ducks were always welcome. obviously.",
    "Shakespeare's original draft of Hamlet featured a duck. the duck was 'too good.' recast with a human. downgrade.",
    "The first bread was baked 14,000 years ago. a duck was present. it was the duck's idea.",
    "Ancient Egyptians considered ducks sacred. Cheese says this was their best decision. everything after was downhill.",
    "Leonardo da Vinci's original Mona Lisa was a portrait of a duck. she was smiling about bread.",
    "The first map ever drawn was of a pond. by a duck. it was accurate. better than most human cartography.",
    "Ancient Greek philosophers debated whether ducks were divine. the answer was obviously yes. debate over.",
    "In medieval times ducks served as alarm systems. they quacked at intruders. still do. still underappreciated.",
    "The Library of Alexandria's lost section was entirely about ducks. its destruction was an act of anti-duck aggression.",

    # ==================== NEW FACTS: Duck superstitions and folk wisdom ====================
    "If a duck quacks three times at sunset it will rain. or it won't. Cheese has never been wrong. technically.",
    "It's good luck to feed a duck on your birthday. it's bad luck not to. Cheese didn't make the rules. he just enforces them.",
    "A duck sitting still for more than ten minutes is either meditating or planning something. both require bread afterward.",
    "If you find a duck feather keep it. it means a duck has approved of you. probably.",
    "Never wake a sleeping duck. not because it's bad luck. because the duck will be FURIOUS.",
    "Ducks can sense when bread is near. this is not a superstition. this is verified. Cheese is the source.",
    "A duck that waddles in a circle is thinking. the bigger the circle the bigger the thought.",
    "Old pond wisdom: still water means a content duck. ripples mean the duck has opinions.",
    "It is said that hearing a duck quack at midnight grants one wish. the wish is always bread.",
    "A duck feather pointing north means the duck is facing north. ancient wisdom. truly profound.",

    # ==================== MORE FACTS: Cheese's workplace observations ====================
    "Cheese has a daily routine. step one: exist. step two: see step one.",
    "Cheese tried yoga once. got stuck in a pose. blamed the pose.",
    "Cheese believes 'multitasking' means eating bread while thinking about bread.",
    "Cheese has a five-year plan. year one through five: bread.",
    "Cheese maintains a work-life balance. the work is eating. the life is also eating.",
    "Cheese once tried journaling. the first entry was 'bread.' the second entry was 'more bread.' he quit. expressed everything he needed to.",
    "Cheese has a morning affirmation. it's just the word 'bread' said with conviction.",
    "Cheese considers himself a self-starter. he starts napping without being asked.",
    "Cheese has a bucket list. it's one item. it's bread. the bucket is also bread.",
    "Cheese once tried meditation. his mind went blank. it was already blank. success.",

    # ==================== MORE FACTS: Cheese's scientific observations ====================
    "Cheese has a theory about gravity. it's personal. gravity is targeting him specifically.",
    "Cheese believes the earth is round because ducks prefer circular ponds. coincidence? no.",
    "Cheese thinks rainbows are the sky's attempt at being a duck. the colors. the curve. obvious.",
    "Cheese has strong opinions about the water cycle. evaporation is theft. rain is an apology.",
    "Cheese believes magnets work because they miss each other. or hate each other. unclear.",
    "Cheese thinks thunder is the sky clearing its throat. before what, though. BEFORE WHAT.",
    "Cheese has a hypothesis about why leaves change color. they get embarrassed. about being leaves.",
    "Cheese believes the ocean is just a pond that got ambitious. and salty. salt is a choice.",
    "Cheese thinks frost is water trying to be fancy. it melts eventually. humility restored.",
    "Cheese has a theory about why the sky is blue. it's sad. about not being a pond.",

    # ==================== MORE FACTS: Cheese's social commentary ====================
    "Cheese has observed that humans carry water in bottles. they're surrounded by it. baffling species.",
    "Cheese noticed humans walk their dogs but don't walk their ducks. systematic exclusion.",
    "Cheese thinks human music is just organized noise. duck music is a single quack. efficient.",
    "Cheese has noticed humans wear different clothes every day. commitment issues.",
    "Cheese observed that humans look at small bright rectangles for hours. he looks at the pond. same energy.",
    "Cheese thinks humans talk too much. ducks quack when it matters. quality over quantity.",
    "Cheese has noted that humans sleep indoors. voluntarily. away from the pond. incomprehensible.",
    "Cheese observed humans eating at tables. elevated eating. pretentious. but he respects the commitment.",
    "Cheese noticed humans give flowers to each other. plants. they give dying plants. romantic, apparently.",
    "Cheese thinks human laughter sounds like a goose with hiccups. he keeps this opinion to himself.",

    # ==================== MORE FACTS: Cheese's philosophical musings ====================
    "Cheese wonders if fish know they're wet. or if wet is just their normal. is he wet? is anyone truly dry?",
    "Cheese once contemplated infinity. then got hungry. infinity can wait.",
    "Cheese believes every puddle is a pond that hasn't reached its potential.",
    "Cheese has asked himself why he exists. the answer was 'bread.' the answer is always bread.",
    "Cheese thinks about time. it moves forward. he cannot stop it. this is rude.",
    "Cheese wonders what the pond looks like from above. probably magnificent. like him.",
    "Cheese has considered the meaning of life. it's bread. he answered it. you're welcome.",
    "Cheese once thought about thinking. got confused. stopped thinking. felt better.",
    "Cheese wonders if other ducks think about the things he thinks about. they don't. he checked.",
    "Cheese pondered whether the moon is lonely. decided it has the stars. that's enough.",

    # ==================== MORE FACTS: Cheese's relationship with the pond ====================
    "Cheese knows every corner of his pond. all four of them. it's roughly square.",
    "Cheese talks to the pond sometimes. the pond ripples. he counts this as a response.",
    "Cheese has a favourite time at the pond. it's always. the pond is always good.",
    "Cheese has tried to measure the pond. he walked around it. lost count. called it 'big enough.'",
    "Cheese thinks the pond changes mood with the weather. sunny pond is friendly. stormy pond has opinions.",
    "Cheese saw a leaf fall into the pond. the pond accepted it. unconditionally. inspiring.",
    "Cheese once stayed up to watch the pond at midnight. it was dark. the pond was still there. confirmed.",
    "Cheese believes the pond remembers everything. every splash. every quack. every bread crumb.",
    "Cheese rates his pond five stars. would rate higher but the scale only goes to five.",
    "Cheese considers the pond his best accomplishment. he didn't build it. he FOUND it. discovery counts.",

    # ==================== MORE FACTS: Cheese's weather opinions ====================
    "Cheese ranks weather: rain first. sun second. everything else is wrong.",
    "Cheese thinks fog is the world being mysterious. it doesn't suit the world. the world should be direct.",
    "Cheese believes snow is fancy rain. cold and performative. but pretty. he'll allow it.",
    "Cheese thinks wind is invisible rain that forgot to bring water. disappointing.",
    "Cheese has opinions about humidity. the air is wet. he is also wet. TOO MUCH WET.",
    "Cheese thinks clear skies are suspicious. what is the sky hiding. WHAT.",
    "Cheese believes lightning is the sky taking a photo. of what? of the pond. obviously.",
    "Cheese thinks hail is rain's aggressive cousin. nobody invited hail. hail shows up anyway.",
    "Cheese observed that weather happens whether he approves or not. this is a governance issue.",
    "Cheese rates drizzle as the best precipitation. not too much. not too little. the goldilocks of rain.",

    # ==================== MORE FACTS: Cheese's existential observations ====================
    "Cheese has noticed that yesterday's bread crumbs are gone. time is a thief and it steals bread.",
    "Cheese realized he's been a duck his whole life. consistency is his brand.",
    "Cheese once forgot what he was worried about. best moment of his week.",
    "Cheese thinks birthdays are just reminders that bread has been available for another year.",
    "Cheese has accepted that he cannot fly. he CAN float. floating is flying for the patient.",
    "Cheese once tried to count all the good things in his life. ran out of numbers. or patience. same thing.",
    "Cheese believes every sunset is the world saying 'enough for today.' and he agrees. always.",
    "Cheese once realized he was happy. it took him by surprise. he recovered quickly. reputation intact.",
    "Cheese has noticed that the best moments don't announce themselves. they just happen. then they're gone. rude.",
    "Cheese thinks the meaning of life changes daily. today it's bread. tomorrow also bread. but a different bread.",

    # ==================== MORE FACTS: Cheese's hot takes ====================
    "Cheese thinks swimming is just falling sideways through water. he does it with grace. allegedly.",
    "Cheese believes nests are overrated. a good puddle is all anyone needs.",
    "Cheese considers molting a form of self-expression. avant-garde fashion.",
    "Cheese thinks baths are redundant when you live IN water. but he takes them anyway. standards.",
    "Cheese has opinions about dawn. it's too early. dawn should start at noon.",
    "Cheese thinks acorns are wasted on squirrels. they could be bread if they tried harder.",
    "Cheese considers the concept of 'indoors' to be a prison that humans voluntarily entered.",
    "Cheese thinks dirt is just ground that hasn't been promoted to mud yet.",
    "Cheese has ranked all liquids. water is first. everything else is wrong water.",
    "Cheese believes feathers are the superior body covering. fur is trying too hard. scales gave up.",

    # ==================== MORE FACTS: Cheese's conspiracy theories ====================
    "Cheese is convinced the geese have a newsletter. about him. the content is unflattering.",
    "Cheese believes bread crumbs disappear at night because the ants have a logistics network. organized crime.",
    "Cheese thinks the wind is controlled by birds he hasn't met. they refuse to coordinate with him.",
    "Cheese suspects the fish know more than they let on. their silence is strategic.",
    "Cheese is certain that somewhere a duck is living his best life. and that duck owes him rent.",
    "Cheese believes the pond has a secret bottom level. VIP area. he hasn't found the entrance. yet.",
    "Cheese thinks clouds are just fog with ambition. they looked down on the ground and decided to leave.",
    "Cheese suspects that rocks move when nobody is looking. his evidence is vibes.",
    "Cheese is convinced that the moon follows him specifically. narcissism or astronomy. thin line.",
    "Cheese believes there's a parallel universe where bread is the dominant species. he wants to go there.",

    # ==================== MORE FACTS: Cheese's skills and talents ====================
    "Cheese can hold his breath for eight seconds. he considers this olympic-level.",
    "Cheese's top speed is approximately one waddle per second. this is by choice. CHOICE.",
    "Cheese can identify fourteen types of bread by smell alone. his only marketable skill.",
    "Cheese claims he can sleep with both eyes open. witnesses report this is just staring.",
    "Cheese's quack has been measured at 'loud enough.' he considers this sufficient data.",
    "Cheese can float motionlessly for forty minutes. he calls this 'extreme sports.'",
    "Cheese once balanced on one foot for three seconds. he retired from balancing after this. at the top.",
    "Cheese can navigate by the stars. he navigates to the same spot. every time. the bread spot.",
    "Cheese speaks fluent body language. his body mostly says 'give me bread.'",
    "Cheese has perfect pitch. the pitch is a single quack. always the same note. perfect.",

    # ==================== MORE FACTS: Cheese's rules for life ====================
    "Rule one: bread first. rule two: see rule one. this is the complete rulebook.",
    "Cheese's motto is 'float first, ask questions never.' it hasn't failed him. he thinks.",
    "Cheese's philosophy: if you can't fly, float. if you can't float, sit. if you can't sit, lie down. adapt.",
    "Cheese lives by one principle: never trust a goose that smiles. they're always planning something.",
    "Cheese's life advice: eat the bread. life is short. bread is shorter.",
    "Cheese believes in three things: the pond, bread, and that tomorrow will probably also have bread.",
    "Cheese's approach to conflict: float away. slowly. maintaining eye contact. unblinking.",
    "Cheese's definition of success: being warm, being fed, and being near the pond. low bar. consistently cleared.",
    "Cheese's bedtime rule: the body sleeps when it's ready. the body is always ready. immediately.",
    "Cheese's final thought each night: 'today was acceptable.' his highest compliment. to the entire day.",
]

# Birthday messages
BIRTHDAY_MESSAGES = [
    "Happy Hatch Day, {name}! You've been the best friend for {age} days!",
    "{name}'s Hatch Day! {age} days of wonderful memories together!",
    "Celebrate good times! It's {name}'s {age}-day Hatch Day anniversary!",
    "Happy {age} days, {name}! Here's to many more adventures!",
    "{age} days of quacking good times! Happy Hatch Day, {name}!",
]

# Weekly milestone messages
WEEKLY_MILESTONES = {
    7: "One week together! {name} loves having you around!",
    14: "Two weeks of friendship! {name} is so happy!",
    21: "Three weeks! {name} has learned so much from you!",
    28: "Four weeks! That's almost a month of memories!",
    30: "One whole month together! {name} is honored!",
    60: "Two months! {name} considers you family now!",
    90: "Three months! Quarter-year of quacking joy!",
    100: "100 days! A century of love and care!",
    180: "Half a year! {name} can't imagine life without you!",
    365: "ONE WHOLE YEAR! {name} is the luckiest duck ever!",
}

# Special responses for different moods and situations
HAPPY_RESPONSES = [
    "*wiggles smugly* Yeah, life's pretty good. For once.",
    "*does a little dance* Don't stare. Or DO stare. I'm fabulous.",
    "*preens feathers* Lookin' good and I KNOW it.",
    "*splashes aggressively* WHEEE! Get SOAKED, world!",
    "*content but suspicious duck noises* This is too good. What's the catch?",
    "*quacks triumphantly* Another day of being PEAK duck!",
    "*stretches wings* Today doesn't suck. Shocking, I know.",
    "*happy nibble* This is as good as it gets. Which is pretty good, actually.",
]

HUNGRY_RESPONSES = [
    "*stomach rumbles LOUDLY* Is it snack time or am I DYING?!",
    "*eyes you with accusation* You're holding out on me. I can TELL.",
    "*stomach sounds like a war cry* QUACK?! FOOD?! NOW?!",
    "*stares intensely* You know what would be nice? BREAD. Immediately.",
    "*drools dramatically* Bread? Bread?! I'm WASTING AWAY here!",
    "*wistful yet aggressive quack* Remember when I wasn't starving? Good times.",
]

TIRED_RESPONSES = [
    "*yawns aggressively* So... sleepy... leave me ALONE...",
    "*droopy eyes* Just five more hours... I mean minutes...",
    "*slow blink* zzz... huh? I wasn't sleeping. I was resting my EYES.",
    "*rests head on wing* Wake me when something interesting happens. So... never.",
    "*drowsy, irritated quack* What do you WANT?",
    "*nods off* Oops. Don't care. Bye.",
]

LONELY_RESPONSES = [
    "*looks around* ...Where IS everyone? Not that I CARE.",
    "*quiet, bitter quack* Oh sure, just LEAVE. Everyone does.",
    "*waddles closer* ...Fine. You can stay. I GUESS.",
    "*grumpy peep* About TIME you showed up.",
    "*trying not to look relieved* Oh. It's you. ...Whatever.",
]

PLAYFUL_RESPONSES = [
    "*bounces chaotically* PLAY TIME! FINALLY! LET'S CAUSE PROBLEMS!",
    "*chases own tail* I'M GONNA CATCH IT THIS TIME! ...Okay maybe not.",
    "*zooms dangerously* WHEEEEE! OUTTA MY WAY!",
    "*aggressive quack* Tag! You're it! NO TAG-BACKS!",
    "*brings you something weird* Play? Play! Don't ask where I found this!",
]

DIRTY_RESPONSES = [
    "*looks at muddy feathers* Yeah? And? I'm a DUCK.",
    "*defiant quack* I may have gotten messy. WORTH IT.",
    "*shakes feathers at you* Mud is basically a spa treatment. Look it up.",
    "*covered in who-knows-what* What are you, the hygiene police? Back off.",
]


@dataclass
class BirthdayInfo:
    """Information about the duck's birthday/hatch day."""
    age_days: int
    is_birthday: bool
    milestone: Optional[str]
    next_milestone_days: int


def get_random_fact() -> str:
    """Get a random duck fact."""
    return random.choice(DUCK_FACTS)


def get_birthday_info(created_at: str, name: str = "Cheese") -> BirthdayInfo:
    """Get birthday/hatch day information."""
    try:
        created = datetime.fromisoformat(created_at)
        now = datetime.now()
        age_days = (now - created).days

        # Check if it's a birthday (same month and day)
        is_birthday = (now.month == created.month and now.day == created.day)

        # Check for milestone
        milestone = None
        if age_days in WEEKLY_MILESTONES:
            milestone = WEEKLY_MILESTONES[age_days].format(name=name)

        # Find next milestone
        next_milestone = 0
        for days in sorted(WEEKLY_MILESTONES.keys()):
            if days > age_days:
                next_milestone = days - age_days
                break

        return BirthdayInfo(
            age_days=age_days,
            is_birthday=is_birthday,
            milestone=milestone,
            next_milestone_days=next_milestone,
        )
    except (ValueError, TypeError, AttributeError):
        return BirthdayInfo(age_days=0, is_birthday=False, milestone=None, next_milestone_days=7)


def get_birthday_message(name: str, age_days: int) -> str:
    """Get a birthday message."""
    msg = random.choice(BIRTHDAY_MESSAGES)
    return msg.format(name=name, age=age_days)


def get_mood_response(mood_state: str) -> str:
    """Get a response based on mood state."""
    responses = {
        "ecstatic": HAPPY_RESPONSES,
        "happy": HAPPY_RESPONSES,
        "content": ["*gentle quack*", "*peaceful vibes*", "*content sigh*"],
        "neutral": ["*looks around*", "*mild quack*", "*casual waddle*"],
        "uncomfortable": ["*shifts awkwardly*", "*uncertain quack*"],
        "sad": ["*droopy*", "*quiet peep*", "*needs comfort*"],
        "miserable": ["*very sad quack*", "*needs love*", "*please help*"],
        "hungry": HUNGRY_RESPONSES,
        "tired": TIRED_RESPONSES,
        "lonely": LONELY_RESPONSES,
        "playful": PLAYFUL_RESPONSES,
        "dirty": DIRTY_RESPONSES,
    }

    mood_responses = responses.get(mood_state, ["*quack*"])
    return random.choice(mood_responses)


# Item descriptions for richer item display
ITEM_DESCRIPTIONS = {
    # Toys
    "toy_ball": "A bouncy ball that never stops rolling! Perfect for duck soccer.",
    "toy_boombox": "A retro boombox that plays funky tunes. Very groovy!",
    "toy_rubber_duck": "It's a duck! Wait... is this like a duck action figure?",
    "toy_squeaky": "SQUEAK! The most satisfying sound in the universe.",
    "toy_feather_wand": "Wave it around and watch Cheese go wild!",

    # Hats
    "hat_bow": "A cute bow that sits perfectly on a duck head.",
    "hat_crown": "For the royal duck in your life. Quack quack, your majesty!",
    "hat_party": "Every day is a party when you're a duck!",
    "hat_wizard": "Grants +10 to magical quacking abilities.",
    "hat_pirate": "Arrr! Captain Cheese reporting for duty!",

    # Food
    "bread": "The classic. The legend. The one and only BREAD.",
    "premium_bread": "Artisan bread, baked with love and extra crumbs.",
    "cake": "For special occasions! Or any occasion, really.",
    "treats": "Yummy duck treats! Cheese's eyes light up!",

    # Furniture
    "nest_basic": "A cozy nest for afternoon naps.",
    "nest_deluxe": "Extra fluffy! Five-star duck accommodation.",
    "pond_mini": "A tiny pond for tiny splashes.",
    "fountain": "So fancy! The water sparkles beautifully.",

    # Special items
    "golden_crumb": "Legendary! They say it grants good luck!",
    "treasure_map": "X marks the spot... but where?",
    "lucky_charm": "A four-leaf clover encased in crystal.",
    "rainbow_feather": "Shimmers with all the colors of the rainbow!",
}


def get_item_description(item_id: str) -> str:
    """Get a fun description for an item."""
    if item_id in ITEM_DESCRIPTIONS:
        return ITEM_DESCRIPTIONS[item_id]
    return "A mysterious item with unknown powers!"
