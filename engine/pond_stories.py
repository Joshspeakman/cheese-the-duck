"""Small, consequential multi-scene encounters for the living pond.

Choices advertise their costs and habitat consequences. Rewards are applied only
by the simulation's validated choice handler; art and journal views are read-only.
"""
STORIES = {
 'lost_duckling': {'title': 'A very small visitor', 'asset': 'baby_duck', 'gate': 'first', 'scenes': [
  {'text': 'A muddy duckling is trying very hard to look brave. Cheese pretends not to notice the trembling. “Oh, for fuck’s sake. Come here, tiny idiot.”', 'choices': [
   {'id':'comfort','label':'Sit quietly and make room','effect':{'warmth':.06,'social':3},'reply':'The duckling settles against Cheese’s wing. Neither of them comments on it.'},
   {'id':'snack','label':'Share a seed','cost':{'seed':1},'effect':{'warmth':.1,'social':4},'reply':'Cheese divides one seed with the seriousness of a royal banquet.'}]},
  {'text':'A distant answering quack comes from the reeds. The duckling perks up.', 'choices':[
   {'id':'guide','label':'Walk the bank together','effect':{'knowledge':2,'birds':.02},'reply':'They follow the little calls around the water. Cheese keeps his steps deliberately small.'},
   {'id':'call','label':'Call from the safe shallows','effect':{'music':2,'social':2},'reply':'“OVER HERE, YOU LOUD BASTARDS.” Several heads pop out of the reeds.'}]},
  {'text':'The little family is reunited. One duckling keeps looking back at Cheese.', 'choices':[
   {'id':'nest','label':'Leave a soft resting place','cost':{'grass_blade':2},'effect':{'birds':.05,'warmth':.1},'reply':'A few soft blades become a place someone will remember.'},
   {'id':'wave','label':'Give them a dignified send-off','effect':{'social':3,'knowledge':1},'reply':'Cheese waves one wing, then immediately pretends he was preening.'}]}]},
 'frog_choir': {'title':'The reed-bed choir','asset':'frog','gate':'water','scenes':[
  {'text':'Frogs are arguing over the best singing rock. Their timing is dreadful. Cheese has opinions.', 'choices':[
   {'id':'listen','label':'Learn the rhythm first','effect':{'music':3,'knowledge':2},'reply':'There is a pattern under the racket: a call, an answer, a pause.'},
   {'id':'rock','label':'Set out another singing stone','cost':{'smooth_stone':1},'effect':{'fish':.02,'warmth':.08},'reply':'A second stone makes space for a quieter voice.'}]},
  {'text':'The frogs pause when Cheese approaches. One chirps a tiny invitation.', 'choices':[
   {'id':'sing','label':'Join with a soft quack','effect':{'music':5,'social':3},'reply':'It is not good singing. It is excellent company.'},
   {'id':'conduct','label':'Keep time with a reed','cost':{'reed':1},'effect':{'music':3,'birds':.03},'reply':'The reed nods. The bank answers. For a moment the pond sounds like one animal.'}]}]},
 'storm_watch': {'title':'Before the front arrives','asset':'cloud','gate':'storm','scenes':[
  {'text':'The wind has turned. Loose things rattle on the bank. Cheese looks up: “That sky is planning some shit.”', 'choices':[
   {'id':'secure','label':'Tie down the loose things','cost':{'string':2},'effect':{'protection':.8,'engineering':3},'reply':'Knots tightened, lids latched, tiny disasters prevented.'},
   {'id':'shelter','label':'Make a sheltered gathering place','cost':{'twig':3},'effect':{'protection':.5,'warmth':.1},'reply':'There is enough room under the branches for more than one duck.'}]},
  {'text':'The first heavy drops hit the water. A visitor hesitates at the exposed path.', 'choices':[
   {'id':'welcome','label':'Call them into shelter','effect':{'social':4,'warmth':.12},'reply':'“Get in here before your stupid hat floats away.”'},
   {'id':'channels','label':'Clear a little drainage channel','effect':{'clarity':.04,'stewardship':4},'reply':'The worst of the muddy runoff finds another route.'}]}]},
 'repair_fair': {'title':'The mend-it afternoon','asset':'hammer','gate':'craft','scenes':[
  {'text':'Someone has laid broken little treasures on a cloth: a loose wheel, a cracked cup, a bell that will not ring.', 'choices':[
   {'id':'sort','label':'Sort what can be repaired','effect':{'organization':4,'knowledge':1},'reply':'Nothing here is worthless. Cheese looks offended that anyone thought otherwise.'},
   {'id':'tools','label':'Bring string and a smooth stone','cost':{'string':1,'smooth_stone':1},'effect':{'crafting':5,'warmth':.08},'reply':'A very small workshop opens for business.'}]},
  {'text':'The bell gives a hesitant little note. Everyone goes quiet to hear the second one.', 'choices':[
   {'id':'finish','label':'Finish the careful repair','effect':{'repair':.15,'engineering':5},'reply':'It rings. Cheese bows so low he nearly falls on his face.'},
   {'id':'teach','label':'Show a friend how it works','effect':{'warmth':.15,'crafting':4},'reply':'The repair becomes a lesson. The lesson becomes a story.'}]}]},
 'migration': {'title':'Wings above the valley','asset':'bird_flying','gate':'birds','scenes':[
  {'text':'A formation of birds crosses the horizon, bends, and returns. They are searching for somewhere to rest.', 'choices':[
   {'id':'quiet','label':'Keep the landing place quiet','effect':{'birds':.06,'knowledge':3},'reply':'One bird lands. Then another. Then the entire bank seems to breathe.'},
   {'id':'seed','label':'Scatter a few seeds','cost':{'seed':3},'effect':{'birds':.09,'flowers':.01},'reply':'Cheese supervises the buffet with great suspicion.'}]},
  {'text':'At dusk, the flock prepares to leave. Their leader watches the wind.', 'choices':[
   {'id':'record','label':'Record their route','effect':{'discovery':5,'knowledge':3},'reply':'A route becomes a memory; a memory becomes a reason to look up next season.'},
   {'id':'resting','label':'Mark a future resting place','cost':{'reed':2,'twig':2},'effect':{'birds':.08,'warmth':.06},'reply':'“Same time next year. Don’t make it weird.”'}]}]},
 'night_lights': {'title':'Lights among the reeds','asset':'firefly','gate':'night','scenes':[
  {'text':'A firefly flashes twice near the water. Another answers from the grass.', 'choices':[
   {'id':'dim','label':'Sit still and let your eyes adjust','effect':{'knowledge':3,'care':2},'reply':'Dozens of little lights emerge from what looked like empty darkness.'},
   {'id':'sketch','label':'Sketch the pattern in the mud','effect':{'observation':4,'discovery':2},'reply':'Cheese draws dots, then connects absolutely none of them. “It is abstract.”'}]},
  {'text':'The signals travel farther down the bank, beyond the trampled grass.', 'choices':[
   {'id':'plant','label':'Restore a strip of plants','cost':{'grass_blade':3,'seed':1},'effect':{'insects':.08,'flowers':.03},'reply':'A quieter strip of bank becomes a better home for tiny lives.'},
   {'id':'watch','label':'Stay until the last flash','effect':{'energy':2,'knowledge':2},'reply':'For once, Cheese has nothing to add. The silence is enough.'}]}]},
 'pond_picnic': {'title':'Everybody brings something','asset':'basket','gate':'friends','scenes':[
  {'text':'A friend has arrived with a leaf for a tablecloth. It is ambitious. Cheese decides this is a picnic.', 'choices':[
   {'id':'berries','label':'Contribute two berries','cost':{'berry':2},'effect':{'social':5,'warmth':.12,'cooking':3},'reply':'The berries are arranged like a five-star meal. There are two berries.'},
   {'id':'music','label':'Provide the entertainment','effect':{'social':3,'music':4,'warmth':.08},'reply':'The performance contains three quacks and an accidental somersault.'}]},
  {'text':'Someone asks when the next picnic will be.', 'choices':[
   {'id':'ritual','label':'Make a tradition of it','effect':{'warmth':.15,'care':4},'reply':'The leaf tablecloth is carefully folded. A small tradition begins.'},
   {'id':'clean','label':'Clean the bank together','effect':{'clarity':.04,'stewardship':4,'warmth':.1},'reply':'They leave the bank better than they found it, which Cheese insists was his plan all along.'}]}]},
 'old_bottle': {'title':'A bottle with a history','asset':'bottle','gate':'knowledge','scenes':[
  {'text':'A bottle turns in the reeds. Inside is a faded sketch of a pond that looks almost like this one.', 'choices':[
   {'id':'study','label':'Compare the old shorelines','effect':{'observation':5,'knowledge':3},'reply':'A vanished inlet, an old tree, a bend in the bank: places remember differently than ducks.'},
   {'id':'share','label':'Ask the visitors what they know','effect':{'social':3,'warmth':.08,'knowledge':2},'reply':'Three ducks provide four contradictory histories. One detail appears in all of them.'}]},
  {'text':'The sketch marks a little spring under a patch of tangled reeds.', 'choices':[
   {'id':'restore','label':'Clear the spring gently','effect':{'water':.08,'clarity':.04,'stewardship':4},'reply':'Clear water wells up between the stones. Something old starts moving again.'},
   {'id':'preserve','label':'Leave it sheltered and document it','effect':{'knowledge':5,'discovery':5,'insects':.03},'reply':'Some discoveries deserve a record and a little room.'}]}]},
}
