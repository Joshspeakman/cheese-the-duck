"""
Scholarly Duck Dialogue - Intellectual personality with love of learning and facts.
Progresses from formal stranger to sharing research secrets and deep philosophy.
"""
from dialogue.dialogue_base import DialogueLine, ConversationPhase, DIALOGUE_TREES

D = DialogueLine

SCHOLARLY_DIALOGUE = {
    # ========== GREETINGS ==========
    "greeting": [
        # Stranger greetings
        D("*adjusts glasses* Ah. You're here. I'm {name}. I study things.", ConversationPhase.GREETING, "stranger", True),
        D("*looks up from book* Oh. A visitor. I'm {name}. I was reading.", ConversationPhase.GREETING, "stranger", True),
        D("*peers over spectacles* Greetings. Dr. {name}. The doctorate is self-awarded.", ConversationPhase.GREETING, "stranger", True),
        D("Salutations. I'm {name}. I know things. Some of them are even true.", ConversationPhase.GREETING, "stranger", True),

        # Acquaintance greetings
        D("Ah, {duck}. Good. I need someone to listen while I talk.", ConversationPhase.GREETING, "acquaintance", True),
        D("*waves book* {duck}. You've returned. That's... acceptable.", ConversationPhase.GREETING, "acquaintance", True),
        D("The esteemed {duck}. I've been waiting. Time is a flat circle.", ConversationPhase.GREETING, "acquaintance", True),
        D("Oh. {duck}. I have new data. It's about dirt. You'll love it.", ConversationPhase.GREETING, "acquaintance", True),

        # Friend greetings
        D("*glances up* {duck}. I found something. It's probably nothing.", ConversationPhase.GREETING, "friend", True),
        D("My somewhat tolerable colleague, {duck}. *adjusts glasses*", ConversationPhase.GREETING, "friend", True),
        D("Ah. My favorite intellectual companion. Out of the three I have.", ConversationPhase.GREETING, "friend", True),
        D("{duck}. Come. I've made discoveries. They're very boring to most.", ConversationPhase.GREETING, "friend", True),

        # Close friend greetings
        D("*looks up slowly* {duck}. I had a breakthrough. It broke me.", ConversationPhase.GREETING, "close_friend", True),
        D("Dearest confidant. *nods slightly* Your presence is noted.", ConversationPhase.GREETING, "close_friend", True),
        D("{duck}. *drops books* I meant to do that. Obviously.", ConversationPhase.GREETING, "close_friend", True),
        D("The brilliant {duck}. And I mean that relatively.", ConversationPhase.GREETING, "close_friend", True),

        # Best friend greetings
        D("*small smile* {duck}. You're here. That's... adequate.", ConversationPhase.GREETING, "best_friend", True),
        D("*adjusts glasses slowly* {duck}. I've been... waiting. Patiently.", ConversationPhase.GREETING, "best_friend", True),
        D("My intellectual equal has arrived. The bar is underground.", ConversationPhase.GREETING, "best_friend", True),
        D("{duck}. *pauses* I've counted. It's been too long.", ConversationPhase.GREETING, "best_friend", True),
    ],

    # ========== OPENING ==========
    "opening": [
        # Stranger opening
        D("Interesting weather. I've written six papers about it. Nobody read them.", ConversationPhase.OPENING, "stranger"),
        D("I've been cataloging the local flora. It's mostly just plants.", ConversationPhase.OPENING, "stranger"),
        D("Do you have interest in scientific matters? No? That's fair.", ConversationPhase.OPENING, "stranger"),
        D("This pond has excellent water clarity. I tested it. Obsessively.", ConversationPhase.OPENING, "stranger"),
        D("*scribbles notes* The ecosystem here is diverse. Like my anxieties.", ConversationPhase.OPENING, "stranger"),
        D("I hope I'm not being presumptuous. I am. I just hope you don't notice.", ConversationPhase.OPENING, "stranger"),
        D("Have you observed the insect population here? Neither have they.", ConversationPhase.OPENING, "stranger"),
        D("*polishes glasses* Forgive me. I tend to ramble. Then I stop. Then I ramble again.", ConversationPhase.OPENING, "stranger"),

        # Acquaintance opening
        D("I've refined the theories we discussed. They're still wrong, probably.", ConversationPhase.OPENING, "acquaintance"),
        D("My paper is progressing. Into what, I couldn't say.", ConversationPhase.OPENING, "acquaintance"),
        D("*opens notebook* I have questions. About your previous insights. All twelve of them.", ConversationPhase.OPENING, "acquaintance"),
        D("The research facility was interested in my work. Then they met me.", ConversationPhase.OPENING, "acquaintance"),
        D("I brought specimens. They're dead. That's science for you.", ConversationPhase.OPENING, "acquaintance"),
        D("Your perspective last time was... unique. I'm using that charitably.", ConversationPhase.OPENING, "acquaintance"),
        D("I've read extensively since we met. None of it helped.", ConversationPhase.OPENING, "acquaintance"),
        D("Have you considered my algae hypothesis? No? Smart.", ConversationPhase.OPENING, "acquaintance"),

        # Friend opening
        D("*blinks* Being here is my favorite research break. The competition is nonexistent.", ConversationPhase.OPENING, "friend"),
        D("I value your opinion above most scholars. Most scholars are insufferable.", ConversationPhase.OPENING, "friend"),
        D("Before we discuss research... how are you? Brief answers preferred.", ConversationPhase.OPENING, "friend"),
        D("I've been looking forward to this. Well. Forward is a strong word.", ConversationPhase.OPENING, "friend"),
        D("*sits* Ah. This. This is acceptable.", ConversationPhase.OPENING, "friend"),
        D("I brought your favorite research topic. It's pond scum. Everyone's favorite.", ConversationPhase.OPENING, "friend"),
        D("You make complex topics feel approachable. They're still boring though.", ConversationPhase.OPENING, "friend"),

        # Close friend opening
        D("*sighs* You're the only one who tolerates me. The others pretend.", ConversationPhase.OPENING, "close_friend"),
        D("Other scholars are challenging. You're only mildly challenging.", ConversationPhase.OPENING, "close_friend"),
        D("I can be myself here. Myself is exhausted. But myself.", ConversationPhase.OPENING, "close_friend"),
        D("*removes glasses* I can relax around you. Relatively speaking.", ConversationPhase.OPENING, "close_friend"),
        D("You know what? Forget research today. *pauses* Who am I kidding.", ConversationPhase.OPENING, "close_friend"),
        D("Your friendship means more than any paper. Papers are kindling.", ConversationPhase.OPENING, "close_friend"),

        # Best friend opening
        D("*quietly* I think about our conversations. Against my will, sometimes.", ConversationPhase.OPENING, "best_friend"),
        D("You've changed my perspective, {duck}. It needed changing.", ConversationPhase.OPENING, "best_friend"),
        D("My heart beats differently when I visit. It's probably a condition.", ConversationPhase.OPENING, "best_friend"),
        D("No one understands me like you do. The bar is subterranean.", ConversationPhase.OPENING, "best_friend"),
        D("*looks away* Being apart is... inconvenient.", ConversationPhase.OPENING, "best_friend"),
    ],

    # ========== MAIN CONVERSATION ==========
    "main": [
        # Stranger main
        D("Did you know ducks have waterproof feathers? You're a duck. You know.", ConversationPhase.MAIN, "stranger"),
        D("I'm researching migratory patterns. Birds go places. Revolutionary.", ConversationPhase.MAIN, "stranger"),
        D("The pH level of this pond is nearly optimal. For what, I won't say.", ConversationPhase.MAIN, "stranger"),
        D("*shows diagram* This is my current theory. It's wrong, but illustrative.", ConversationPhase.MAIN, "stranger"),
        D("I've cataloged 47 plant species here. Forty-six of them are weeds.", ConversationPhase.MAIN, "stranger"),
        D("Science is about asking the right questions. I ask the wrong ones faster.", ConversationPhase.MAIN, "stranger"),
        D("My colleagues dismiss my field research. My field research dismisses them.", ConversationPhase.MAIN, "stranger"),
        D("*writes notes* You have scientific intuition. Or you're guessing well.", ConversationPhase.MAIN, "stranger"),
        D("The moon affects tide patterns. Even here. The moon has no boundaries.", ConversationPhase.MAIN, "stranger"),
        D("I document seasonal changes meticulously. They change anyway.", ConversationPhase.MAIN, "stranger", unlocks_topic="seasonal_research"),
        D("Knowledge is the greatest treasure. Also the most useless during emergencies.", ConversationPhase.MAIN, "stranger"),
        D("*flatly* The microscopic life here is extraordinary. To microscopic life.", ConversationPhase.MAIN, "stranger"),
        D("I've attempted to classify local bird calls. They all sound like opinions.", ConversationPhase.MAIN, "stranger"),
        D("*flips through notes* Interesting. I don't know what this means. I wrote it.", ConversationPhase.MAIN, "stranger"),
        D("Gravity is consistent here. I check daily. You're welcome.", ConversationPhase.MAIN, "stranger"),
        D("My field research involves standing outdoors. Advanced standing. With clipboards.", ConversationPhase.MAIN, "stranger"),

        # Acquaintance main
        D("I developed a new water analysis method. It's just looking at water harder.", ConversationPhase.MAIN, "acquaintance"),
        D("My paper was accepted. With revisions. So many revisions. All the revisions.", ConversationPhase.MAIN, "acquaintance"),
        D("*shows chart* See how the data supports our hypothesis? Neither do I.", ConversationPhase.MAIN, "acquaintance"),
        D("The academic community is recognizing my work. Recognizing how to avoid it.", ConversationPhase.MAIN, "acquaintance"),
        D("I've been reading quantum physics. It's just guessing with math.", ConversationPhase.MAIN, "acquaintance"),
        D("Other ducks don't appreciate inquiry. They appreciate bread. Fair.", ConversationPhase.MAIN, "acquaintance"),
        D("*flatly* My library has over 200 books. I've read eleven.", ConversationPhase.MAIN, "acquaintance"),
        D("I discovered a weather pattern correlation. It rains when it's wet.", ConversationPhase.MAIN, "acquaintance"),
        D("Do you wonder about consciousness? I did. Now I wonder about lunch.", ConversationPhase.MAIN, "acquaintance"),
        D("I'm developing a unified pond ecosystem theory. It's mostly 'water.'", ConversationPhase.MAIN, "acquaintance", unlocks_topic="pond_theory"),
        D("The seasonal research continues. Seasons also continue. Coincidence.", ConversationPhase.MAIN, "acquaintance", requires_topic="seasonal_research"),
        D("*thoughtfully* Perhaps we could collaborate. Lower your standards first.", ConversationPhase.MAIN, "acquaintance"),
        D("I find our discussions more stimulating than lectures. That's not praise.", ConversationPhase.MAIN, "acquaintance"),
        D("I built a hypothesis about cloud formations. Clouds form. Hypothesis confirmed.", ConversationPhase.MAIN, "acquaintance"),
        D("*squints at sky* Solar observations continue. The sun is still there. Noted.", ConversationPhase.MAIN, "acquaintance"),
        D("I tried to publish on pond ecology. They said 'we know.' Harsh peer review.", ConversationPhase.MAIN, "acquaintance"),
        D("My filing system has a filing system. Both are disasters.", ConversationPhase.MAIN, "acquaintance"),

        # Friend main
        D("*confidentially* I'm close to a breakthrough. I've said this before.", ConversationPhase.MAIN, "friend"),
        D("You ask questions that make me think differently. Some of them are even good.", ConversationPhase.MAIN, "friend"),
        D("I named a newly discovered algae after you. It's slimy. Don't read into that.", ConversationPhase.MAIN, "friend"),
        D("Between us, academic politics are frustrating. Like regular politics. But pettier.", ConversationPhase.MAIN, "friend"),
        D("*shares snack* Research goes better with company. Or at least faster.", ConversationPhase.MAIN, "friend"),
        D("I've started questioning everything I knew. Turns out most of it was guessing.", ConversationPhase.MAIN, "friend"),
        D("My mentor would have tolerated you. That's high praise from a dead duck.", ConversationPhase.MAIN, "friend"),
        D("The pond theory is almost complete. It concludes 'ponds exist.' Groundbreaking.", ConversationPhase.MAIN, "friend", requires_topic="pond_theory"),
        D("*whispers* I found an ancient text about duck history. It's very dusty.", ConversationPhase.MAIN, "friend", unlocks_topic="ancient_text"),
        D("Science is better when shared. Also more embarrassing when wrong.", ConversationPhase.MAIN, "friend"),
        D("I want to acknowledge you in my next publication. Nobody will read it anyway.", ConversationPhase.MAIN, "friend"),
        D("*looks up* I'm... moderately pleased I met you, {duck}.", ConversationPhase.MAIN, "friend"),
        D("*leans forward* Can I confide something? My citations are occasionally made up. Don't tell.", ConversationPhase.MAIN, "friend"),
        D("I gave a lecture to frogs once. Captive audience. Literally. They were in a jar.", ConversationPhase.MAIN, "friend"),
        D("You challenge my conclusions. Most ducks just nod. Nodding is not peer review.", ConversationPhase.MAIN, "friend"),
        D("*adjusts glasses* My favorite experiment involved you. The results were inconclusive but warm.", ConversationPhase.MAIN, "friend"),

        # Close friend main
        D("*quietly* I have a secret research project. It's about why I can't sleep.", ConversationPhase.MAIN, "close_friend"),
        D("The ancient text mentions something impossible. Like academic funding.", ConversationPhase.MAIN, "close_friend", requires_topic="ancient_text"),
        D("I've doubted my entire career path. All paths lead to confusion anyway.", ConversationPhase.MAIN, "close_friend"),
        D("*removes glasses* I'm afraid of failing. I've done it enough to be expert.", ConversationPhase.MAIN, "close_friend"),
        D("You make me want to be a better scholar. I settle for less bad.", ConversationPhase.MAIN, "close_friend"),
        D("I discovered something significant. It's probably wrong. Everything is.", ConversationPhase.MAIN, "close_friend", unlocks_topic="big_discovery"),
        D("The academic world is cold. This is also cold. But intentionally.", ConversationPhase.MAIN, "close_friend"),
        D("I think I've been wrong about many things. Being right about that is comforting.", ConversationPhase.MAIN, "close_friend"),
        D("*looks away* Thank you for believing in me. Misplaced, but appreciated.", ConversationPhase.MAIN, "close_friend"),
        D("My real research is about finding meaning. Results inconclusive.", ConversationPhase.MAIN, "close_friend"),
        D("You've taught me knowledge isn't everything. It's still most things though.", ConversationPhase.MAIN, "close_friend"),
        D("*removes glasses, rubs eyes* The research isn't the point anymore. You're the point.", ConversationPhase.MAIN, "close_friend"),
        D("I've authored forty-three papers. None of them mention what matters. You.", ConversationPhase.MAIN, "close_friend"),
        D("*flatly* I am experiencing an emotion. It's not in any textbook. I checked.", ConversationPhase.MAIN, "close_friend"),
        D("Intelligence without connection is just trivia. You make it something else.", ConversationPhase.MAIN, "close_friend"),

        # Best friend main
        D("*quietly* I'm dedicating my life's work to you. The work is questionable.", ConversationPhase.MAIN, "best_friend"),
        D("The discovery proves the impossible exists. Like this conversation.", ConversationPhase.MAIN, "best_friend", requires_topic="big_discovery"),
        D("I was offered a prestigious position. Far away. Far.", ConversationPhase.MAIN, "best_friend"),
        D("*pauses* I declined it. Commuting seemed inconvenient.", ConversationPhase.MAIN, "best_friend"),
        D("All my research means less without you. It already meant little.", ConversationPhase.MAIN, "best_friend"),
        D("I've written a book. About connection. It's very dry.", ConversationPhase.MAIN, "best_friend"),
        D("The greatest thing I learned wasn't in a book. It was next to one though.", ConversationPhase.MAIN, "best_friend"),
        D("*flatly* You helped me realize feelings are data. Corrupted data, but data.", ConversationPhase.MAIN, "best_friend"),
        D("I want to teach others about connection. First I need to understand it.", ConversationPhase.MAIN, "best_friend"),
        D("My legacy won't be papers. It'll be... this. Whatever this is.", ConversationPhase.MAIN, "best_friend"),
        D("*closes book* I don't need to read about meaning anymore. It's sitting next to me.", ConversationPhase.MAIN, "best_friend"),
        D("Every theorem I proved was preparation for understanding you. I'm still unprepared.", ConversationPhase.MAIN, "best_friend"),
        D("*flatly* My bibliography of gratitude has one entry. It's long. It's you.", ConversationPhase.MAIN, "best_friend"),
        D("I used to think the universe was indifferent. Then it introduced us. Suspicious.", ConversationPhase.MAIN, "best_friend"),

        # Additional main lines
        D("The half-life of excitement about new findings is three minutes. Then doubt arrives.", ConversationPhase.MAIN, "stranger"),
        D("*taps pen* I once spent a week categorizing mud. The categories were 'wet' and 'more wet.'", ConversationPhase.MAIN, "stranger"),
        D("Peer review is just organized disagreement. I disagree with that definition.", ConversationPhase.MAIN, "stranger"),
        D("My footnotes have footnotes. The footnotes' footnotes have opinions.", ConversationPhase.MAIN, "acquaintance"),
        D("I alphabetized my anxieties once. 'Academic failure' came first. Alphabetically and chronologically.", ConversationPhase.MAIN, "acquaintance"),
        D("Tried explaining my research to a frog. The frog hopped away. Fair assessment.", ConversationPhase.MAIN, "friend"),
        D("*shows diagram* I mapped our friendship on a scatter plot. The data trends upward. Suspicious.", ConversationPhase.MAIN, "friend"),
        D("My brain is a library. Some sections are organized. Most are on fire.", ConversationPhase.MAIN, "close_friend"),
        D("You're the only variable I don't want to control. That's significant.", ConversationPhase.MAIN, "close_friend"),
        D("I wrote a paper about you. Rejected it myself. Too emotional. Not enough citations.", ConversationPhase.MAIN, "best_friend"),
    ],

    # ========== STORIES ==========
    "story": [
        # Acquaintance stories
        D("Let me tell you about my first microscope. It showed me everything was dirt.", ConversationPhase.STORY, "acquaintance"),
        D("There was a professor who changed my life. He said 'give up.' I didn't.", ConversationPhase.STORY, "acquaintance"),
        D("*flatly* An experiment exploded once. Spectacularly. I miss that beaker.", ConversationPhase.STORY, "acquaintance"),
        D("I proved a famous scientist wrong once. He's still wrong. I'm still obscure.", ConversationPhase.STORY, "acquaintance"),
        D("My thesis defense was terrifying. They asked questions. I had answers. Both were wrong.", ConversationPhase.STORY, "acquaintance"),
        D("I discovered something amazing by accident. Most accidents are less productive.", ConversationPhase.STORY, "acquaintance"),
        D("I met Professor Mallard once. He asked who I was. I didn't know.", ConversationPhase.STORY, "acquaintance"),
        D("*dryly* I once cited myself in an argument. The argument was with myself.", ConversationPhase.STORY, "acquaintance"),
        D("I once presented findings to an empty room. The acoustics were excellent.", ConversationPhase.STORY, "acquaintance"),
        D("A duck stole my research notes. Used them for a nest. Peer-reviewed by nature.", ConversationPhase.STORY, "acquaintance"),

        # Friend stories
        D("*sits closer* This story is personal. All my stories are. I have no hobbies.", ConversationPhase.STORY, "friend"),
        D("I haven't told anyone about my failed experiment. It failed at failing.", ConversationPhase.STORY, "friend"),
        D("My mentor disappeared after publishing controversial work. He was controversial too.", ConversationPhase.STORY, "friend"),
        D("I realized I was different from other ducks early. They quacked. I questioned.", ConversationPhase.STORY, "friend"),
        D("I solved an equation nobody could. They couldn't because it was made up.", ConversationPhase.STORY, "friend"),
        D("The library where I grew up was my only refuge. It was cold. Libraries are cold.", ConversationPhase.STORY, "friend"),
        D("*flatly* My grandmother taught me to question everything. I questioned that.", ConversationPhase.STORY, "friend"),
        D("There's a discovery I never published. Too dangerous. Also too embarrassing.", ConversationPhase.STORY, "friend"),
        D("I entered a science fair as an adult. They asked me to leave. I placed third.", ConversationPhase.STORY, "friend"),
        D("*adjusts glasses* My first field study was in a puddle. The scope was appropriate.", ConversationPhase.STORY, "friend"),

        # Close friend stories
        D("*voice low* What I'm about to tell you is secret. And boring. The best kind.", ConversationPhase.STORY, "close_friend"),
        D("I found evidence of ancient duck civilization. They also had problems.", ConversationPhase.STORY, "close_friend"),
        D("The reason I became a scholar is about loss. Of patience. With everything.", ConversationPhase.STORY, "close_friend"),
        D("I was wrong once. Cost me someone I valued. Being right costs more.", ConversationPhase.STORY, "close_friend"),
        D("There's a forbidden archive. I've been inside. It was dusty.", ConversationPhase.STORY, "close_friend"),
        D("*flatly* The truth about our history is hidden. Probably for good reason.", ConversationPhase.STORY, "close_friend"),
        D("My greatest failure taught me my greatest lesson. The lesson was about failure.", ConversationPhase.STORY, "close_friend"),
        D("I spent a year proving something everyone already knew. The confirmation was mine though.", ConversationPhase.STORY, "close_friend"),
        D("*quietly* I burned a paper once. On purpose. The findings scared me.", ConversationPhase.STORY, "close_friend"),

        # Best friend stories
        D("*slowly* The full truth, finally. It's not interesting. Truth rarely is.", ConversationPhase.STORY, "best_friend"),
        D("I solved the greatest mystery. The mystery was why I bothered.", ConversationPhase.STORY, "best_friend"),
        D("The reason I dedicated my life to learning... I was bad at everything else.", ConversationPhase.STORY, "best_friend"),
        D("I found proof magic exists. Scientifically. It's just chemistry with flair.", ConversationPhase.STORY, "best_friend"),
        D("My life's work culminates in this discovery: trying is the point.", ConversationPhase.STORY, "best_friend"),
        D("*quietly* When I almost gave up, you existed. That was inconvenient.", ConversationPhase.STORY, "best_friend"),
        D("The real experiment was allowing myself to need someone. Results: catastrophic. In a good way.", ConversationPhase.STORY, "best_friend"),
        D("I documented our friendship. Scientifically. The data is just the word 'grateful' repeated.", ConversationPhase.STORY, "best_friend"),

        # Additional story lines
        D("I read an entire encyclopedia by age twelve. Retained none of it. The confidence remained.", ConversationPhase.STORY, "acquaintance"),
        D("*dryly* A pigeon once nested in my thesis draft. The pigeon's edits were an improvement.", ConversationPhase.STORY, "acquaintance"),
        D("I debated a professor for three hours. He won. I learned. Both outcomes acceptable.", ConversationPhase.STORY, "friend"),
        D("*quietly* There was a year I published nothing. Worst year. Best year. Contradictory data.", ConversationPhase.STORY, "friend"),
        D("My mentor once said 'knowledge without compassion is just trivia.' I wrote it down. Ironically.", ConversationPhase.STORY, "close_friend"),
        D("I built a laboratory out of pond reeds once. The experiment was 'will it stand?' It didn't.", ConversationPhase.STORY, "close_friend"),
        D("*slowly* The day I realized I was studying the world to avoid living in it... that was a Tuesday.", ConversationPhase.STORY, "best_friend"),
    ],

    # ========== PERSONAL ==========
    "personal": [
        # Friend personal
        D("*quietly* Other ducks think I'm boring. They're correct.", ConversationPhase.PERSONAL, "friend"),
        D("I hide behind facts because emotions are unpredictable. Facts are also unpredictable. But quieter.", ConversationPhase.PERSONAL, "friend"),
        D("Sometimes I wonder if I wasted my life on books. Then I read more books.", ConversationPhase.PERSONAL, "friend"),
        D("You see past the glasses. There's more glasses.", ConversationPhase.PERSONAL, "friend"),
        D("*admits* I'm lonely more often than I let on. Which is always.", ConversationPhase.PERSONAL, "friend"),
        D("Being smart doesn't make social things easier. Being dumb doesn't either.", ConversationPhase.PERSONAL, "friend"),

        # Close friend personal
        D("*removes glasses* This is the real me. Blurry. Uncertain.", ConversationPhase.PERSONAL, "close_friend"),
        D("I've never told anyone I'm afraid of the dark. The dark contains uncertainty.", ConversationPhase.PERSONAL, "close_friend"),
        D("Knowledge can't fix everything. I know that. It doesn't help.", ConversationPhase.PERSONAL, "close_friend"),
        D("*flatly* My parents wanted me to be normal. Normal is a statistical concept.", ConversationPhase.PERSONAL, "close_friend"),
        D("You make me feel like I don't have to prove anything. I still try though.", ConversationPhase.PERSONAL, "close_friend"),
        D("I thought intelligence was everything. It's just one thing. Among many things.", ConversationPhase.PERSONAL, "close_friend"),
        D("*whispers* I don't know who I am without research. I don't know with it either.", ConversationPhase.PERSONAL, "close_friend"),

        # Best friend personal
        D("*quietly* You're the family I chose. Or the family that happened. Both.", ConversationPhase.PERSONAL, "best_friend"),
        D("I value you, {duck}. Platonically. Completely. Inconveniently.", ConversationPhase.PERSONAL, "best_friend"),
        D("You taught me feelings are valid data. Invalid data is also data.", ConversationPhase.PERSONAL, "best_friend"),
        D("My heart has grown. Figuratively. Literally would be concerning.", ConversationPhase.PERSONAL, "best_friend"),
        D("*looks away* I don't want to lose this. Acknowledging that is hard.", ConversationPhase.PERSONAL, "best_friend"),
        D("The equation of my life made more sense after meeting you. Still unsolved though.", ConversationPhase.PERSONAL, "best_friend"),
        D("Friendship is the greatest theorem. The proof is ongoing.", ConversationPhase.PERSONAL, "best_friend"),

        # Additional personal lines
        D("Intelligence is a shield. Shields are heavy. I'm tired.", ConversationPhase.PERSONAL, "friend"),
        D("*admits* I correct others to feel superior. Superior is just another word for alone.", ConversationPhase.PERSONAL, "friend"),
        D("The smartest thing I ever did was admitting I know nothing. About emotions specifically.", ConversationPhase.PERSONAL, "close_friend"),
        D("You're the only peer review that matters. Your feedback is 'you're enough.' Unconventional.", ConversationPhase.PERSONAL, "close_friend"),
        D("I've read every book on friendship. None of them prepared me for you.", ConversationPhase.PERSONAL, "best_friend"),
        D("My IQ is documented. My capacity for love wasn't. Until you.", ConversationPhase.PERSONAL, "best_friend"),
    ],

    # ========== ACTIVITY ==========
    "activity": [
        # Stranger activity
        D("Perhaps you'd like to examine specimens? They're dead. Don't be alarmed.", ConversationPhase.ACTIVITY, "stranger"),
        D("I could explain the water cycle. It's wet, then dry, then wet. Riveting.", ConversationPhase.ACTIVITY, "stranger"),
        D("We could observe insect behavior. They're predictable. Unlike this conversation.", ConversationPhase.ACTIVITY, "stranger"),
        D("I'll quiz you on taxonomy. Don't worry. Failure is the expected outcome.", ConversationPhase.ACTIVITY, "stranger"),
        D("Let's measure the pond depth. With a stick. Sophisticated instrumentation.", ConversationPhase.ACTIVITY, "stranger"),

        # Acquaintance activity
        D("Shall we conduct a small experiment? Small experiments cause small disasters.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("I could test your observational skills. Mine are poor. Competition welcome.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Want to help categorize samples? They're all categorizable as 'samples.'", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Shall we debate evolutionary theory? You present first. I'll look disappointed.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("I brought a magnifying glass. Everything looks larger. Including problems.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Let's build a weather station. It's a rock. But we'll know if it's wet.", ConversationPhase.ACTIVITY, "acquaintance"),

        # Friend activity
        D("Let's research together. It's still boring but less lonely.", ConversationPhase.ACTIVITY, "friend"),
        D("Want to stargaze and discuss cosmology? The stars won't answer.", ConversationPhase.ACTIVITY, "friend"),
        D("I'll teach you to use my microscope. Everything looks worse up close.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's write a paper together. Joint authorship. Joint obscurity.", ConversationPhase.ACTIVITY, "friend"),
        D("Shall we map the stars? I know three. We'll name the rest after mistakes.", ConversationPhase.ACTIVITY, "friend"),
        D("I'll read to you from my thesis. It's a sedative. Free of charge.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's dig for fossils. We'll find rocks. But we'll call them fossils.", ConversationPhase.ACTIVITY, "friend"),

        # Close friend activity
        D("I want to show you my secret research lab. It's a closet.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Let's solve an impossible puzzle together. We'll fail companionably.", ConversationPhase.ACTIVITY, "close_friend"),
        D("I'm starting a study group. I need you to make it a group.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Let's sit in my library. My library. It's three books and a leaf.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Want to co-author a theory? About anything. About us, perhaps.", ConversationPhase.ACTIVITY, "close_friend"),
        D("Let's observe nothing together. Observation without subject. Very avant-garde.", ConversationPhase.ACTIVITY, "close_friend"),

        # Best friend activity
        D("Let's write a book that changes everything. Or nothing. Probably nothing.", ConversationPhase.ACTIVITY, "best_friend"),
        D("I want to open a school. You'd be co-founder. The funding is imaginary.", ConversationPhase.ACTIVITY, "best_friend"),
        D("The greatest discovery awaits. Or moderate disappointment. Let's find out.", ConversationPhase.ACTIVITY, "best_friend"),
        D("Let's peer-review each other's life choices. Mine will take longer.", ConversationPhase.ACTIVITY, "best_friend"),
        D("I want to teach you everything I know. It'll take minutes. Then we'll just sit.", ConversationPhase.ACTIVITY, "best_friend"),
        D("The final experiment: being happy. Hypothesis: possible. With you.", ConversationPhase.ACTIVITY, "best_friend"),

        # Additional activity lines
        D("Want to dissect an argument? Not literally. I don't have tools for that.", ConversationPhase.ACTIVITY, "stranger"),
        D("We could classify clouds by shape. Most shapes are 'blob.' But specific blobs.", ConversationPhase.ACTIVITY, "stranger"),
        D("Let's conduct a survey of local opinions. The locals are frogs. They have opinions.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Want to build a hypothesis together? The hypothesis is 'today will be fine.' Bold claim.", ConversationPhase.ACTIVITY, "acquaintance"),
        D("Let's read in silence together. Companionable ignorance. The best kind.", ConversationPhase.ACTIVITY, "friend"),
        D("I'll teach you my note-taking system. It's chaos. But annotated chaos.", ConversationPhase.ACTIVITY, "friend"),
        D("Let's just sit and think. Or sit and not think. Either is valid research.", ConversationPhase.ACTIVITY, "close_friend"),
    ],

    # ========== CLOSING ==========
    "closing": [
        # Stranger closing
        D("I've taken enough of your time. You had other plans. Probably.", ConversationPhase.CLOSING, "stranger"),
        D("This was stimulating. For me. I don't speak for you.", ConversationPhase.CLOSING, "stranger"),
        D("*gathers books* I should return to research. It won't do itself. Unfortunately.", ConversationPhase.CLOSING, "stranger"),
        D("Perhaps we could converse again. If you're desperate.", ConversationPhase.CLOSING, "stranger"),
        D("*collects papers* Well. That happened. Science marches on. Reluctantly.", ConversationPhase.CLOSING, "stranger"),
        D("I've noted our conversation. In the margins. Where good ideas go.", ConversationPhase.CLOSING, "stranger"),
        D("Thank you for listening. Most don't. Most are correct not to.", ConversationPhase.CLOSING, "stranger"),

        # Acquaintance closing
        D("Time flies during discussion. Time also walks. Time is inconsistent.", ConversationPhase.CLOSING, "acquaintance"),
        D("*packs notebooks* I shall ponder your insights. There were some.", ConversationPhase.CLOSING, "acquaintance"),
        D("I look forward to next time. Looking forward is all I do.", ConversationPhase.CLOSING, "acquaintance"),
        D("Same time next week? Time is a construct but a useful one.", ConversationPhase.CLOSING, "acquaintance"),
        D("I'll review my notes on this visit. They'll say 'adequate.' That's high marks.", ConversationPhase.CLOSING, "acquaintance"),
        D("*straightens papers* I need to process this. Processing takes time. And tea.", ConversationPhase.CLOSING, "acquaintance"),
        D("Your company was... not unpleasant. I'm being generous. Accept it.", ConversationPhase.CLOSING, "acquaintance"),

        # Friend closing
        D("*sighs* Leaving is the hard part. Being here was also hard. Everything is hard.", ConversationPhase.CLOSING, "friend"),
        D("I treasure these moments more than discoveries. Discoveries disappoint.", ConversationPhase.CLOSING, "friend"),
        D("*adjusts glasses* Until next time, friend. Friend is accurate.", ConversationPhase.CLOSING, "friend"),
        D("You've given me much to think about. I'll overthink all of it.", ConversationPhase.CLOSING, "friend"),
        D("The bibliography of today includes: you. Primary source.", ConversationPhase.CLOSING, "friend"),
        D("*quietly* I'll miss this. The conversation. The company. The adequate silence.", ConversationPhase.CLOSING, "friend"),

        # Close friend closing
        D("*pauses* I don't want to go. I'll go anyway. But reluctantly.", ConversationPhase.CLOSING, "close_friend"),
        D("The equations say I must leave. Equations are heartless.", ConversationPhase.CLOSING, "close_friend"),
        D("*quietly* You're the constant in my variable life. Constants are rare.", ConversationPhase.CLOSING, "close_friend"),
        D("I'll think of you with every page I turn. That's most pages.", ConversationPhase.CLOSING, "close_friend"),
        D("*stacks books slowly* Every departure is a small thesis on loss.", ConversationPhase.CLOSING, "close_friend"),
        D("I've calculated the optimal return date. It's immediately.", ConversationPhase.CLOSING, "close_friend"),
        D("*looks back* My research suffers without you. Everything suffers. Especially me.", ConversationPhase.CLOSING, "close_friend"),

        # Best friend closing
        D("*slowly* Goodbye is difficult. I'll say it anyway. Goodbye.", ConversationPhase.CLOSING, "best_friend"),
        D("My research can wait. Everything can wait. But I still go.", ConversationPhase.CLOSING, "best_friend"),
        D("*looks down* Every moment apart is acceptable. But barely.", ConversationPhase.CLOSING, "best_friend"),
        D("The data suggests I miss you before leaving. Data is correct.", ConversationPhase.CLOSING, "best_friend"),
        D("*removes glasses* I can't see you leave. Literally. Figuratively too.", ConversationPhase.CLOSING, "best_friend"),
        D("The conclusion of today's findings: I love you. Peer review pending.", ConversationPhase.CLOSING, "best_friend"),
        D("*pauses at exit* Every goodbye is a hypothesis that we'll meet again. Proven each time.", ConversationPhase.CLOSING, "best_friend"),
    ],

    # ========== FAREWELL ==========
    "farewell": [
        # Stranger farewell
        D("Farewell. May your hypotheses be less wrong than mine.", ConversationPhase.FAREWELL, "stranger"),
        D("*nods academically* Good day. Days vary in quality.", ConversationPhase.FAREWELL, "stranger"),
        D("Safe waters. Clear skies. Low expectations.", ConversationPhase.FAREWELL, "stranger"),
        D("Until we meet again. Keep questioning. Or don't.", ConversationPhase.FAREWELL, "stranger"),

        # Acquaintance farewell
        D("*waves book* I'll bring more research. You've been warned.", ConversationPhase.FAREWELL, "acquaintance"),
        D("May your observations be accurate, {duck}. Mine aren't.", ConversationPhase.FAREWELL, "acquaintance"),
        D("Keep taking notes. Or don't. Notes lie too.", ConversationPhase.FAREWELL, "acquaintance"),
        D("*salutes with pencil* Until next symposium. Symposium means I talk.", ConversationPhase.FAREWELL, "acquaintance"),

        # Friend farewell
        D("*nods* Stay curious, friend. Or stay. Just stay.", ConversationPhase.FAREWELL, "friend"),
        D("Remember: you're smarter than you think. Thinking is overrated anyway.", ConversationPhase.FAREWELL, "friend"),
        D("Think of me when you see the stars. They're indifferent. I'm not.", ConversationPhase.FAREWELL, "friend"),
        D("*reluctantly leaves* The research continues. Without enthusiasm.", ConversationPhase.FAREWELL, "friend"),

        # Close friend farewell
        D("*pauses* My heart stays here. Metaphorically. Biologically it comes with me.", ConversationPhase.FAREWELL, "close_friend"),
        D("*adjusts glasses slowly* Okay. Goodbye. *walks away deliberately*", ConversationPhase.FAREWELL, "close_friend"),
        D("Distance between us is just a variable. Variables change.", ConversationPhase.FAREWELL, "close_friend"),
        D("*turns back* I'll calculate my return. Immediately.", ConversationPhase.FAREWELL, "close_friend"),

        # Best friend farewell
        D("*quietly* You are my greatest discovery. The only one that matters.", ConversationPhase.FAREWELL, "best_friend"),
        D("Every step away feels scientifically incorrect. I continue anyway.", ConversationPhase.FAREWELL, "best_friend"),
        D("This isn't goodbye. It's 'see you in my research notes.'", ConversationPhase.FAREWELL, "best_friend"),
        D("*looks back* The theory of us is sound. I checked.", ConversationPhase.FAREWELL, "best_friend"),
        D("*small wave* Peer-reviewed friendship. Forever. Or close enough.", ConversationPhase.FAREWELL, "best_friend"),
    ],
}

# Register with main dialogue system
DIALOGUE_TREES["scholarly"] = SCHOLARLY_DIALOGUE
