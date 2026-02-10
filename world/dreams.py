"""
Duck Dreams System - Dreams that play while the duck sleeps.
Dreams are influenced by recent activities, mood, and random chance.
"""
import random
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


class DreamType(Enum):
    """Types of dreams the duck can have."""
    ADVENTURE = "adventure"
    FLYING = "flying"
    FOOD = "food"
    FRIEND = "friend"
    NIGHTMARE = "nightmare"
    MEMORY = "memory"
    PROPHETIC = "prophetic"
    SILLY = "silly"
    PEACEFUL = "peaceful"


@dataclass
class Dream:
    """A single dream sequence."""
    dream_type: DreamType
    title: str
    scenes: List[str]
    mood_effect: int  # Effect on mood when waking
    special_reward: Optional[str] = None  # Rare item/bonus from dream
    xp_bonus: int = 0
    is_recurring: bool = False


# Dream sequences organized by type
DREAMS = {
    DreamType.ADVENTURE: [
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="The Great Bread Quest",
            scenes=[
                "Cheese is in a desert. It's made of bread. Sure.",
                "A mountain of sourdough loaves blocks the path.",
                "Cheese climbs it anyway. Takes about three hours.",
                "At the summit: more bread. Cheese is not surprised.",
                "Eats some. It's fine. Tastes like bread.",
                "Quest complete. Nothing has fundamentally changed.",
            ],
            mood_effect=10,
            xp_bonus=5,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="Pirate Duck",
            scenes=[
                "Cheese is on a boat. Cheese did not ask for this.",
                "The ocean is suspiciously calm. Too calm.",
                "A treasure map appears. The X is where Cheese is standing.",
                "Cheese digs. Finds a smaller boat. Okay.",
                "The smaller boat also has a treasure map.",
                "This is going to take a while.",
            ],
            mood_effect=8,
            xp_bonus=3,
            special_reward="treasure_map",
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="Space Duck",
            scenes=[
                "Cheese is in space now. Nobody explained how.",
                "There are stars. They're just... there.",
                "An alien duck waves. Cheese waves back. Professional courtesy.",
                "The moon is closer than expected. Smells like cheese.",
                "Not the duck. The other cheese. Dairy cheese.",
                "Cheese wakes up confused about identity.",
            ],
            mood_effect=12,
            xp_bonus=5,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="The Cave",
            scenes=[
                "There's a cave. Cheese enters. Standard procedure.",
                "It's dark. Cheese can still see somehow. Dream logic.",
                "A dragon appears. It's the size of a potato.",
                "The dragon asks for directions. Cheese doesn't know any.",
                "They sit in awkward silence for a while.",
                "Cheese leaves. The dragon stays. Life goes on.",
            ],
            mood_effect=7,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="The Desert of Mild Inconvenience",
            scenes=[
                "Cheese is in a desert. It's warm. Not dangerously warm. Just annoying.",
                "There's a cactus. It has a face. The face looks bored.",
                "Cheese walks for what feels like hours. It's been three minutes.",
                "An oasis appears. It's real. The water is lukewarm.",
                "A tumbleweed rolls past. It has places to be, apparently.",
                "Cheese sits down. The adventure is over. It was fine.",
            ],
            mood_effect=6,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="The Labyrinth",
            scenes=[
                "Cheese is in a maze. The walls are made of hedge. Classic.",
                "Left turn. Dead end. Right turn. Dead end. Straight. Believe it or not, dead end.",
                "A minotaur appears. It's also lost. They don't talk about it.",
                "Cheese finds the center. There's a sandwich. It's adequate.",
                "The maze dissolves. Cheese is standing in a field now.",
                "That was a lot of effort for a sandwich. Worth it though.",
            ],
            mood_effect=8,
            xp_bonus=4,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="Cheese and the Volcano",
            scenes=[
                "There's a volcano. Cheese is climbing it. Nobody asked Cheese to.",
                "The rocks are warm. Cheese's feet are warm. Everything is warm.",
                "At the top: lava. It looks exactly like lava. No surprises here.",
                "The volcano rumbles. Cheese rumbles back. Establishing dominance.",
                "A phoenix flies out. It nods at Cheese. Professional respect.",
                "Cheese descends. Adds 'survived volcano' to resume.",
            ],
            mood_effect=9,
            xp_bonus=5,
            special_reward="volcanic_pebble",
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="The Sunken City",
            scenes=[
                "The pond is deeper than expected. Much deeper.",
                "Cheese dives. There are buildings down here. Tiny ones.",
                "A fish in a top hat waves. 'Welcome to Atlantis,' it says. 'The pond version.'",
                "The streets are paved with smooth pebbles. Very walkable.",
                "A restaurant serves seaweed. Cheese declines. Not bread.",
                "Cheese surfaces. Checks the pond. Normal depth. Probably.",
            ],
            mood_effect=10,
            xp_bonus=4,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="The Library at the End",
            scenes=[
                "There's a library. It's at the end of everything. Literally.",
                "The books contain every fact ever known. Cheese opens one. It's about bread.",
                "Cheese opens another. Also bread. A pattern emerges.",
                "The librarian is an owl. Obviously. It judges silently.",
                "Cheese checks out seven books. All bread. The owl stamps them disapprovingly.",
                "Cheese wakes up wanting to read. The urge passes quickly.",
            ],
            mood_effect=8,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="Train to Nowhere",
            scenes=[
                "Cheese is on a train. It has no schedule. No destination.",
                "The scenery passes. Fields. Forests. More fields. A mountain with a face.",
                "A conductor asks for tickets. Cheese has no pockets. Or tickets.",
                "The conductor nods. 'That'll do.' Low standards. Cheese approves.",
                "The train stops. Cheese gets off. It's the pond. It was always the pond.",
                "Cheese wakes up unsure if he traveled far or not at all. Both feel true.",
            ],
            mood_effect=9,
            xp_bonus=3,
        ),
    ],
    DreamType.FLYING: [
        Dream(
            dream_type=DreamType.FLYING,
            title="Cloud Surfing",
            scenes=[
                "Cheese's wings work now. They usually don't. Suspicious.",
                "Flying is exactly as advertised. You go up.",
                "A cloud passes by. Cheese sits on it. It holds.",
                "Other birds fly past. They seem busy.",
                "Cheese is not busy. Cheese is sitting on a cloud.",
                "This is fine.",
            ],
            mood_effect=15,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.FLYING,
            title="Rainbow Rider",
            scenes=[
                "A rainbow appears. Cheese gets on it. As one does.",
                "It's a slide now. Cheese didn't consent to this.",
                "The colors blur together. Everything is briefly purple.",
                "At the bottom: a pot of corn. Not gold. Corn.",
                "Cheese eats some. It's fine.",
            ],
            mood_effect=20,
            xp_bonus=5,
            special_reward="rainbow_feather",
        ),
        Dream(
            dream_type=DreamType.FLYING,
            title="Just Falling",
            scenes=[
                "Cheese is falling. Not flying. Just falling.",
                "The ground approaches. Then recedes. Then approaches again.",
                "This has been happening for some time now.",
                "A passing bird asks if Cheese needs help.",
                "Cheese says no. Pride is important.",
                "Still falling. Might be falling forever. It's fine.",
            ],
            mood_effect=5,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FLYING,
            title="Migrating Nowhere",
            scenes=[
                "Cheese is flying in a V formation. Alone. It's a V of one.",
                "The other ducks didn't show. Classic. Unreliable.",
                "The scenery below changes. Fields. Cities. More fields.",
                "Cheese doesn't know where this migration goes. Doesn't matter.",
                "A seagull joins. They don't speak. It's a comfortable silence.",
                "Destination reached. It's where Cheese started. Full circle.",
            ],
            mood_effect=10,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.FLYING,
            title="Above the Clouds",
            scenes=[
                "Cheese breaks through the clouds. There's a whole sky up here.",
                "The sun is closer. Not dangerously. Just more... present.",
                "Other things fly up here. Planes. Balloons. A confused pigeon.",
                "Cheese and the pigeon make eye contact. They don't discuss it.",
                "The clouds below look like a floor. Cheese considers landing on them.",
                "Cheese wakes up with wings still outstretched. Embarrassing.",
            ],
            mood_effect=12,
            xp_bonus=3,
        ),
    ],
    DreamType.FOOD: [
        Dream(
            dream_type=DreamType.FOOD,
            title="Bread Paradise",
            scenes=[
                "Everything is bread. The ground. The sky. Cheese.",
                "Wait, Cheese is not bread. False alarm.",
                "The trees are baguettes. They're just standing there.",
                "Cheese eats a doorknob. It's a croissant. Of course it is.",
                "Wakes up hungry. Dreams don't count as eating.",
            ],
            mood_effect=10,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="The Infinite Feast",
            scenes=[
                "A table stretches to infinity. Standard dream stuff.",
                "Every food exists here. Even the weird ones.",
                "Cheese eats. Then eats more. Then continues eating.",
                "Still not full. Concerning but not unpleasant.",
                "A waiter appears. Asks if everything is okay.",
                "Cheese nods. The waiter vanishes. Cheese keeps eating.",
            ],
            mood_effect=8,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="The Last Crumb",
            scenes=[
                "There is one crumb. Just one. In the whole world.",
                "Cheese approaches. The crumb doesn't move. It's a crumb.",
                "Dramatic music plays from nowhere.",
                "Cheese eats it. It's a crumb. It tastes like crumb.",
                "More crumbs appear. Crisis averted.",
                "Cheese wakes up feeling accomplished.",
            ],
            mood_effect=6,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="The Bread Museum",
            scenes=[
                "A museum. Entirely dedicated to bread. Cheese weeps. Internally.",
                "The exhibits span centuries. Ancient bread. Medieval bread. Space bread.",
                "A tour guide explains sourdough fermentation. Cheese already knows.",
                "The gift shop sells bread-shaped erasers. Cheese buys twelve.",
                "There's a restricted wing. VIP bread. Cheese isn't VIP. Devastating.",
                "Cheese wakes up planning a real bread museum. Abandons plan by breakfast.",
            ],
            mood_effect=10,
            xp_bonus=3,
            special_reward="bread_knowledge",
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="The Food Critic",
            scenes=[
                "Cheese is a food critic now. Has a tiny hat and everything.",
                "A chef presents a single pea on a massive plate. Fine dining.",
                "Cheese tastes it. It's a pea. Cheese writes 'it's a pea' in the notebook.",
                "The chef cries. The review was too honest. Cheese doesn't apologize.",
                "Next course: bread. Cheese gives it eleven stars. Scale only goes to five.",
                "Cheese is fired from food criticism. No regrets.",
            ],
            mood_effect=8,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="Pizza Planet",
            scenes=[
                "An entire planet made of pizza. The geology is questionable.",
                "Cheese explores. The mountains are stuffed crust. The rivers are marinara.",
                "Local inhabitants are pepperoni. They seem content.",
                "Cheese tries to eat the ground. The ground doesn't mind.",
                "A pizza alien offers a slice. Of itself. Cheese declines. Too weird.",
                "Cheese wakes up wanting pizza. Settles for bread. As always.",
            ],
            mood_effect=7,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="The Bread Olympics",
            scenes=[
                "An arena. Bread from every nation competes. Cheese is a judge.",
                "Sourdough does a floor routine. Flawless. Crusty and confident.",
                "A baguette pole-vaults. The height is impressive. The landing is crumbly.",
                "Pumpernickel does something interpretive. Nobody understands. Ten points anyway.",
                "Cheese awards gold to all bread. Every bread wins. No bread left behind.",
                "Cheese wakes up believing in sportsmanship. Specifically bread sportsmanship.",
            ],
            mood_effect=9,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="The Crumb Trail",
            scenes=[
                "Crumbs. Leading somewhere. Cheese follows. Obviously.",
                "The trail winds through a forest of forks. Utensil forest. Unusual.",
                "Each crumb gets slightly larger. Cheese is encouraged.",
                "The trail ends at a door. Behind the door: a kitchen. Warm. Smells like bread.",
                "An oven glows. Inside: the bread of legend. Golden. Perfect.",
                "Cheese wakes up. Mouth watering. The bread was imaginary. The hunger is real.",
            ],
            mood_effect=8,
            xp_bonus=2,
            special_reward="golden_crumb",
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="Cheese's Food Truck",
            scenes=[
                "Cheese owns a food truck. It serves one item: bread. In bread. With bread.",
                "The line wraps around the block. Twice. The menu is very focused.",
                "A food critic arrives. 'What kind of bread?' he asks. 'Yes,' Cheese replies.",
                "Five stars. Obviously. The bread is bread. What more do you want.",
                "Revenue is good. Cheese pays himself in bread. Circular economy.",
                "Cheese wakes up with entrepreneurial energy. It fades. But it was there.",
            ],
            mood_effect=10,
            xp_bonus=3,
        ),
    ],
    DreamType.FRIEND: [
        Dream(
            dream_type=DreamType.FRIEND,
            title="Best Friends Forever",
            scenes=[
                "All of Cheese's friends are here. Even the imaginary ones.",
                "Everyone is talking at once. Cheese hears none of it.",
                "Gerald tells a joke. Nobody laughs. It wasn't funny.",
                "They all agree it wasn't funny. Friendship prevails.",
                "Everyone shares snacks. Cheese takes too many.",
                "No one mentions it. True friendship.",
            ],
            mood_effect=15,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.FRIEND,
            title="Memory Lane",
            scenes=[
                "There's a road. It's made of memories. Somehow.",
                "Cheese steps on a birthday. It squishes.",
                "There's the first friend. They wave. Cheese waves.",
                "This continues for several memories.",
                "At the end: another road. Memory Boulevard, probably.",
                "Cheese turns back. That's enough nostalgia.",
            ],
            mood_effect=12,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FRIEND,
            title="The Reunion",
            scenes=[
                "Everyone Cheese has ever met is in one room.",
                "It's very crowded. Fire hazard, probably.",
                "Nobody knows why they're here. Standard reunion.",
                "Someone brought a casserole. Nobody eats it.",
                "Cheese stands near the snack table. Strategy.",
                "The dream ends. The casserole remains uneaten.",
            ],
            mood_effect=10,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FRIEND,
            title="Pen Pals",
            scenes=[
                "Cheese is writing a letter. To whom is unclear.",
                "The pen is larger than Cheese. Writing is difficult.",
                "The letter says 'hello. I am a duck. This is a letter.'",
                "A reply arrives immediately. It says 'hello. I am also a duck. Small world.'",
                "They exchange sixteen more letters. All say variations of hello.",
                "Cheese wakes up with the urge to write. It passes.",
            ],
            mood_effect=12,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.FRIEND,
            title="The Campfire",
            scenes=[
                "There's a campfire. Friends sit around it. The vibes are adequate.",
                "Someone plays guitar. They know one chord. They play it repeatedly.",
                "Marshmallows exist but nobody can find sticks.",
                "They eat the marshmallows cold. It's the same. Basically.",
                "Someone tells a scary story. It's about taxes. Everyone is scared.",
                "Cheese wakes up warm. The campfire was fake but the warmth was real.",
            ],
            mood_effect=14,
            xp_bonus=3,
        ),
    ],
    DreamType.NIGHTMARE: [
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="The Empty Pond",
            scenes=[
                "The pond is empty. Not of water. Of everyone.",
                "Cheese walks around. Footsteps echo. Dramatic.",
                "A shape appears in the distance. Hope rises.",
                "It's a rock. Hope sits back down.",
                "Cheese wakes up. The pond is fine. Everyone is there.",
                "Cheese checks anyway. Just in case.",
            ],
            mood_effect=-5,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="Bread Shortage",
            scenes=[
                "No bread. Anywhere. This is serious.",
                "Cheese checks everywhere. Under rocks. In clouds.",
                "The bakery is closed. The baker is also missing.",
                "One crumb appears. Cheese guards it with their life.",
                "More bread appears. The shortage is over.",
                "Cheese is relieved. Also hungry.",
            ],
            mood_effect=2,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="The Endless Meeting",
            scenes=[
                "Cheese is in a meeting. It has no agenda.",
                "Someone is talking about synergy. Cheese tunes out.",
                "The clock doesn't move. It never moves.",
                "There's no door. There was one earlier. Gone now.",
                "Coffee appears. It's decaf. The horror.",
                "Cheese wakes up grateful for consciousness.",
            ],
            mood_effect=-3,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="The Gluten-Free Apocalypse",
            scenes=[
                "All bread is gone. Not just some. ALL of it. This is not a drill.",
                "The bakeries are empty shells. Hollow. Like Cheese's soul right now.",
                "Someone offers a rice cake. Cheese stares. This is rock bottom.",
                "A sign reads 'GLUTEN-FREE WORLD. BREAD IS CANCELLED.' Cancelled. CANCELLED.",
                "Cheese screams. No sound comes out. Only the sound of crackers.",
                "Cheese wakes up and immediately checks bread supply. It's fine. It's FINE.",
            ],
            mood_effect=-8,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="Stage Fright",
            scenes=[
                "Cheese is on a stage. There's a spotlight. An audience. Thousands of them.",
                "Cheese is supposed to do something. Nobody said what.",
                "The audience waits. Cheese waits. Everyone is waiting.",
                "Cheese quacks. The audience writes it down. They're taking NOTES.",
                "A judge holds up a card. It says '4.' Out of what. UNKNOWN.",
                "Cheese wakes up and refuses to perform anything for the rest of the day.",
            ],
            mood_effect=-5,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="Lost Feathers",
            scenes=[
                "Cheese's feathers are falling off. One by one. Slowly.",
                "The wind carries them away. Cheese chases but they're faster.",
                "A bald duck stares back from a puddle reflection. Horrifying.",
                "Cheese tries to glue them back. The glue doesn't exist. Dream logic.",
                "All the feathers return at once. They were just on break.",
                "Cheese wakes up and checks feathers immediately. All present. Never speak of this.",
            ],
            mood_effect=-6,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="The Endless Mall",
            scenes=[
                "Cheese is in a mall. It's enormous. There are no exits.",
                "Every store sells things Cheese doesn't need. Candles. Phone cases. More candles.",
                "The escalator goes up. Then up again. There is no down.",
                "A map exists. It shows Cheese's location as 'here.' Unhelpful.",
                "Cheese finds a food court. It's closed. OF COURSE it's closed.",
                "Cheese wakes up and appreciates the pond. No escalators. No candles.",
            ],
            mood_effect=-4,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="The Bread That Wouldn't Be Eaten",
            scenes=[
                "There is bread. Right there. Cheese reaches for it.",
                "The bread moves. Slightly. Just out of reach.",
                "Cheese waddles forward. The bread waddles forward. It shouldn't be able to.",
                "This continues. For what feels like hours. The bread is faster.",
                "The bread turns around. It has a face. It shakes its head.",
                "Cheese wakes up hungry and betrayed. By bread. BREAD.",
            ],
            mood_effect=-7,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="Infinite Rain",
            scenes=[
                "It's raining. Cheese doesn't mind rain. Usually.",
                "It's been raining for three days now. In the dream. Dream days.",
                "The pond is rising. The pond shouldn't rise this much.",
                "Everything is water now. More water than usual. Which is saying something.",
                "A fish swims past. 'Welcome to our world,' it says. Ominous.",
                "Cheese wakes up and checks the sky. Clear. For now. FOR NOW.",
            ],
            mood_effect=-5,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="The Pond Forgot Me",
            scenes=[
                "Cheese returns to the pond. The pond doesn't recognize him.",
                "The water doesn't ripple. The reeds don't sway. Nothing acknowledges.",
                "Another duck is there. In Cheese's spot. Using Cheese's rock.",
                "'Excuse me,' Cheese says. Nobody hears. Nobody can hear.",
                "Cheese quacks. Full volume. The pond remains indifferent.",
                "Cheese wakes up and quacks at the pond immediately. It ripples. THANK GOODNESS.",
            ],
            mood_effect=-7,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="Everything Is Slightly Wrong",
            scenes=[
                "The pond is here. But it's wrong. Slightly to the left.",
                "The sky is blue. But the wrong blue. Too blue. Aggressively blue.",
                "Bread exists. But it tastes like nothing. Not bad. Just nothing.",
                "Everyone smiles. Too wide. Their teeth are too even. Do ducks have teeth? NOT USUALLY.",
                "Everything is fine. Nothing is fine. Both at once.",
                "Cheese wakes up and checks that everything is the right amount of wrong. It is. Normal.",
            ],
            mood_effect=-6,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.NIGHTMARE,
            title="The Presentation",
            scenes=[
                "Cheese is giving a presentation. To a full auditorium. He has no slides.",
                "The topic is 'Why I Am a Good Duck.' He doesn't remember writing this.",
                "The audience takes notes. On what. THERE IS NOTHING TO NOTE.",
                "Someone asks a question. 'What qualifies you as a duck?' Existential. Rude.",
                "Cheese opens his beak. A quack comes out. The audience nods. Apparently sufficient.",
                "Cheese wakes up sweating. Do ducks sweat? He doesn't know. Another crisis.",
            ],
            mood_effect=-5,
            xp_bonus=1,
        ),
    ],
    DreamType.MEMORY: [
        Dream(
            dream_type=DreamType.MEMORY,
            title="First Day Home",
            scenes=[
                "Cheese remembers hatching. It was Tuesday.",
                "The world was big. It still is. That hasn't changed.",
                "Someone offered food. Cheese accepted. Good start.",
                "Everything was new. Now some things are old.",
                "Home was here then. Home is here now. Consistent.",
                "Cheese appreciates the lack of surprises.",
            ],
            mood_effect=10,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.MEMORY,
            title="Yesterday",
            scenes=[
                "Cheese remembers yesterday. It was yesterday.",
                "Things happened. Cheese was there for most of them.",
                "There was food. It was eaten. Standard procedure.",
                "Someone said hello. Cheese said it back.",
                "Then it was night. Now it's this dream.",
                "Tomorrow will probably also happen.",
            ],
            mood_effect=5,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.MEMORY,
            title="The First Bread",
            scenes=[
                "Cheese remembers the first bread. The very first one.",
                "It was small. A crumb, really. But it was everything.",
                "Someone offered it. Cheese accepted. Trust was born.",
                "The taste was unremarkable. The moment was not.",
                "Every bread since has been chasing that first one.",
                "Cheese wakes up with a feeling that can only be called gratitude. Don't tell anyone.",
            ],
            mood_effect=12,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.MEMORY,
            title="The Pond in Summer",
            scenes=[
                "The pond. But warmer. Brighter. A memory of summer.",
                "The water was perfect. Not too cold. Not too warm. Just pond.",
                "Dragonflies hovered. Cheese didn't chase them. For once.",
                "The sun stayed out longer. As if it didn't want to leave either.",
                "Nothing happened. That was the whole point.",
                "Cheese wakes up missing a season that hasn't left yet. Or maybe it has.",
            ],
            mood_effect=10,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.MEMORY,
            title="The Storm That Passed",
            scenes=[
                "There was a storm once. A big one. Cheese remembers.",
                "The wind pushed. The rain shouted. The pond disagreed with itself.",
                "Cheese hunkered down. Small as possible. Which is already small.",
                "Someone was there. Through the noise. A presence.",
                "The storm ended. They were still there. Cheese was still there.",
                "Cheese wakes up feeling braver than usual. Doesn't know why. Doesn't question it.",
            ],
            mood_effect=8,
            xp_bonus=3,
            special_reward="storm_stone",
        ),
    ],
    DreamType.PROPHETIC: [
        Dream(
            dream_type=DreamType.PROPHETIC,
            title="Vision of Tomorrow",
            scenes=[
                "The dream feels different. More... prophetic.",
                "Cheese sees the future. It looks a lot like the present.",
                "A friend will arrive. Or maybe a package. Hard to tell.",
                "Something will be discovered. Could be anything.",
                "The future is bright. There's adequate lighting.",
                "Cheese will remember none of this. Classic prophecy.",
            ],
            mood_effect=8,
            xp_bonus=5,
            special_reward="lucky_charm",
        ),
        Dream(
            dream_type=DreamType.PROPHETIC,
            title="The Warning",
            scenes=[
                "A mysterious voice speaks. It says 'beware.'",
                "Beware of what? The voice doesn't specify.",
                "Cheese waits for more information. None comes.",
                "The voice clears its throat. Still no details.",
                "'Just... beware in general,' it finally says.",
                "Cheese will try. No promises.",
            ],
            mood_effect=6,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.PROPHETIC,
            title="The Third Pond",
            scenes=[
                "There are three ponds. Cheese's pond. A pond made of glass. A pond made of stars.",
                "A voice says: 'One is real. One is memory. One is next.'",
                "Cheese looks into the glass pond. Sees a reflection that's older.",
                "The star pond hums. It sounds like a question.",
                "'Choose,' the voice says. Cheese doesn't. Not yet.",
                "Cheese wakes up certain that something is about to change. What, though. What.",
            ],
            mood_effect=7,
            xp_bonus=5,
            special_reward="star_pebble",
        ),
        Dream(
            dream_type=DreamType.PROPHETIC,
            title="The Counting Dream",
            scenes=[
                "Numbers float past. Cheese doesn't understand numbers. Usually.",
                "But these ones feel important. Seven. Twelve. Three.",
                "A calendar appears. One date glows. Cheese can't read it.",
                "'Pay attention,' something says. To what. PAY ATTENTION TO WHAT.",
                "The numbers dissolve. Left behind: a feeling of anticipation.",
                "Cheese wakes up counting things. Rocks. Ripples. Crumbs. All feel significant.",
            ],
            mood_effect=5,
            xp_bonus=4,
        ),
        Dream(
            dream_type=DreamType.PROPHETIC,
            title="The Door in the Water",
            scenes=[
                "There's a door. In the pond. Standing upright. Underwater.",
                "It's open. Slightly. Light comes through. Warm light.",
                "Cheese swims closer. The door gets no closer. Classic.",
                "Through the crack: the sound of bread being torn. Promising.",
                "'Not yet,' the door says. Doors don't talk. This one does.",
                "Cheese wakes up looking at the pond differently. There might be doors everywhere.",
            ],
            mood_effect=8,
            xp_bonus=5,
            special_reward="pond_key",
        ),
    ],
    DreamType.SILLY: [
        Dream(
            dream_type=DreamType.SILLY,
            title="Upside Down World",
            scenes=[
                "Gravity reversed. Cheese is on the ceiling now.",
                "The furniture doesn't care. It's on the ceiling too.",
                "Walking is the same but in the other direction.",
                "A fish swims by. Through the air. It doesn't explain.",
                "Cheese quacks. It comes out backwards. 'Kcauq.'",
                "Normal enough. Cheese goes back to sleep.",
            ],
            mood_effect=8,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Giant Cheese (the Duck)",
            scenes=[
                "Cheese is growing. This wasn't planned.",
                "Now Cheese is taller than a tree. Inconvenient.",
                "The tiny ducks below look up. They seem concerned.",
                "Cheese tries to reassure them. Voice is too loud.",
                "Everyone just nods and walks away slowly.",
                "Cheese shrinks back. Nobody mentions it again.",
            ],
            mood_effect=6,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="The Talking Hat",
            scenes=[
                "The hat is talking. It hasn't before. Odd.",
                "'I've been watching,' it says. Cheese is uncomfortable.",
                "The hat tells a joke. It's about ducks. It's mediocre.",
                "Cheese laughs politely. The hat seems satisfied.",
                "'Same time tomorrow?' the hat asks.",
                "Cheese pretends not to hear. Wakes up.",
            ],
            mood_effect=10,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Tax Season",
            scenes=[
                "Cheese is filing taxes. In the dream.",
                "This is unprecedented. Ducks don't pay taxes.",
                "The forms are blank. All of them. Every box.",
                "Cheese signs them anyway. Compliance.",
                "A stamp appears. It says 'APPROVED.'",
                "Cheese wakes up feeling oddly responsible.",
            ],
            mood_effect=4,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Cheese the Detective",
            scenes=[
                "Cheese has a magnifying glass. And a hat. Detective Cheese reporting.",
                "The case: someone ate the last crumb. Cheese must find who.",
                "Clue one: beak marks on the plate. Suspicious. Very suspicious.",
                "Cheese interrogates a spoon. The spoon says nothing. Unhelpful.",
                "Plot twist: Cheese ate the crumb. Cheese is the criminal. Case closed.",
                "Cheese arrests itself. Sentence: one nap. Justice served.",
            ],
            mood_effect=8,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="The Dance-Off",
            scenes=[
                "Cheese is in a dance-off. Against a goose. The stakes are unclear.",
                "The goose does a spin. The crowd goes wild. Cheese is unimpressed.",
                "Cheese does the only move it knows: standing still with intensity.",
                "The judges confer. Standing still with intensity is apparently a genre.",
                "Cheese wins. The goose demands a rematch. Cheese waddles away.",
                "Cheese wakes up with one foot slightly raised. Residual dancing.",
            ],
            mood_effect=10,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Mayor Cheese",
            scenes=[
                "Cheese is running for mayor. The campaign slogan is 'bread.'",
                "The opponent is a particularly confident squirrel. It has a platform.",
                "Cheese's platform is also 'bread.' The voters seem into it.",
                "Election day. Cheese wins by three votes. All from ducks. Democracy.",
                "First act as mayor: declare every day bread day. Unanimous approval.",
                "Cheese wakes up and checks for a mayoral sash. There isn't one. Yet.",
            ],
            mood_effect=9,
            xp_bonus=2,
            special_reward="tiny_sash",
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Cheese the Chef",
            scenes=[
                "Cheese is in a kitchen. A tall hat materializes. It's official.",
                "The recipe says: 'one bread, more bread, additional bread.' Cheese approves.",
                "A food critic arrives. It's a pigeon. In a beret. Cheese is unimpressed.",
                "Cheese serves a single crumb on a white plate. Calls it 'deconstructed loaf.'",
                "The pigeon weeps. Five stars. The crumb was transcendent.",
                "Cheese wakes up and attempts to cook. Burns nothing because there's no stove. Victory.",
            ],
            mood_effect=9,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Job Interview",
            scenes=[
                "Cheese is in a job interview. The interviewer is a goat.",
                "'What are your strengths?' the goat asks. 'Bread,' Cheese replies.",
                "'And weaknesses?' 'Also bread. But from a different angle.'",
                "The goat writes something down. Cheese can't read goat handwriting.",
                "'You're hired,' the goat says. For what is never specified.",
                "Cheese wakes up feeling employed. The feeling fades by breakfast.",
            ],
            mood_effect=7,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Duck News Network",
            scenes=[
                "Cheese is behind a news desk. There are cameras. This is happening.",
                "'Breaking news: bread exists,' Cheese reads. The crew nods solemnly.",
                "'In other news: everything else.' Comprehensive reporting.",
                "A weather duck gives the forecast. 'Wet.' That's the whole forecast.",
                "Ratings are through the roof. The roof is very low. But still.",
                "Cheese wakes up with opinions about current events. They pass quickly.",
            ],
            mood_effect=8,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Cheese Goes to Space (Again)",
            scenes=[
                "Cheese is in a rocket. Again. He didn't sign up for this. Again.",
                "The rocket is made of bread. Questionable engineering. Excellent material.",
                "Mission control is a frog. 'You're clear for launch,' it croaks.",
                "Space is cold. And empty. Like a pond with no water. Horrifying.",
                "Cheese plants a flag on the moon. The flag says 'bread.' Representing his values.",
                "Cheese wakes up with crumbs on his face. Suspicious. Connected? Unknown.",
            ],
            mood_effect=7,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="The Court Case",
            scenes=[
                "Cheese is in court. He's the lawyer. Also the defendant. Also the judge.",
                "The crime: eating the last bread crumb. Cheese objects. To himself.",
                "'Sustained,' he says to himself. Efficient legal system.",
                "Evidence is presented: an empty plate. Devastating. Irrefutable.",
                "Cheese finds himself guilty. Sentence: more bread. Justice is delicious.",
                "Cheese wakes up with a strong sense of jurisprudence. It's gone by noon.",
            ],
            mood_effect=9,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.SILLY,
            title="Cheese's Band",
            scenes=[
                "Cheese is in a band. He plays the quack. It's like drums but wetter.",
                "The bassist is a frog. The singer is a crow. The manager is a confused snail.",
                "Their first song is called 'Bread.' The second song is also called 'Bread.' Different tempo.",
                "The crowd goes wild. The crowd is three pigeons and a cat. Wild is relative.",
                "An encore is demanded. Cheese plays 'Bread (Acoustic).' Standing ovation.",
                "Cheese wakes up humming. The melody is just a quack. But it's HIS quack.",
            ],
            mood_effect=10,
            xp_bonus=2,
        ),
    ],
    DreamType.PEACEFUL: [
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Sunset Pond",
            scenes=[
                "The sun is setting. It does that.",
                "The pond is calm. Nothing is happening.",
                "Cheese floats. The water is the correct temperature.",
                "A bird flies overhead. It doesn't stop.",
                "Time passes. Not too fast. Not too slow.",
                "This is fine. This is exactly fine.",
            ],
            mood_effect=12,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Garden Nap",
            scenes=[
                "There are flowers. Cheese is among them.",
                "A butterfly exists nearby. It minds its business.",
                "The breeze is gentle. Not too breezy. Just right.",
                "Nothing urgent is happening. Nothing at all.",
                "Cheese lies there. Could be minutes. Could be hours.",
                "Perfect. Absolutely adequate in every way.",
            ],
            mood_effect=15,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Waiting Room",
            scenes=[
                "Cheese is in a waiting room. There's nothing to wait for.",
                "The chairs are comfortable. The magazines are current.",
                "No one else is here. No one is coming.",
                "The clock ticks. It's not annoying. It's fine.",
                "Cheese waits. For nothing. Contentedly.",
                "This is the whole dream. Cheese wakes up rested.",
            ],
            mood_effect=10,
            xp_bonus=1,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Library Visit",
            scenes=[
                "Cheese is in a library. It smells like old paper. Comforting.",
                "The books have no titles. The pages are warm.",
                "Cheese picks one up. It's heavy. The words rearrange themselves.",
                "A librarian says 'shhh.' Cheese wasn't talking. But fair enough.",
                "Cheese sits by a window. Rain outside. Warm inside. Balance.",
                "The dream ends. Cheese wakes up slightly more literate. Probably.",
            ],
            mood_effect=12,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Stargazing",
            scenes=[
                "Cheese is on a hill. The stars are out. All of them, apparently.",
                "One star is brighter than the rest. Cheese claims it. That one's mine.",
                "The grass is soft. The air is cool. Nothing needs doing.",
                "A shooting star crosses the sky. Cheese makes a wish. It's bread.",
                "More stars appear. The sky is showing off now.",
                "Cheese falls asleep in the dream. Recursive sleeping. Advanced technique.",
            ],
            mood_effect=14,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="The Warm Rock",
            scenes=[
                "There's a rock. It's warm from the sun. Cheese sits on it.",
                "The warmth goes through feathers. Into bones. Into whatever's deeper than bones.",
                "A lizard is on the other end of the rock. They share it. Wordlessly.",
                "The sun moves. The warm spot moves. Cheese moves with it.",
                "Nothing else happens. Nothing else needs to.",
                "Cheese wakes up warm. The warmth is still there. Residual rock magic.",
            ],
            mood_effect=13,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Rain on the Roof",
            scenes=[
                "Cheese is under a roof. Not his roof. Just a roof.",
                "Rain falls around but not on him. A perfect arrangement.",
                "The sound is constant. Tap tap tap. Like the world is typing.",
                "Cheese's eyes get heavy. Sleep within sleep. Advanced.",
                "The rain doesn't stop. Cheese doesn't want it to.",
                "Cheese wakes up to silence. Misses the tapping. Just a little.",
            ],
            mood_effect=14,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="The Old Oak",
            scenes=[
                "An oak tree. Very old. Very large. Cheese sits in its shade.",
                "Leaves move. Slowly. Like they're waving but don't want to commit.",
                "The bark is rough. The ground is soft. Contrasts.",
                "An acorn falls. Lands next to Cheese. A gift from a tree.",
                "Cheese doesn't eat it. It's not bread. But it's a gesture.",
                "Cheese wakes up appreciating trees. For the first time. Probably the last. But still.",
            ],
            mood_effect=12,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="The Quiet Room",
            scenes=[
                "A room. White walls. Warm light. No source for the warmth. Just warmth.",
                "There's a chair. Cheese-sized. Someone built this for a duck. Thoughtful.",
                "A window shows nothing. Not darkness. Not light. Just calm.",
                "Time doesn't pass here. Or it passes but doesn't count.",
                "Cheese sits. For as long as sitting takes. However long that is.",
                "Cheese wakes up feeling lighter. Like something was put down. Something heavy.",
            ],
            mood_effect=15,
            xp_bonus=2,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="Floating",
            scenes=[
                "Cheese is floating. Not on water. On nothing. Just floating.",
                "There is no up or down. There is no direction at all.",
                "The air is warm. The silence is warm. Everything is warm.",
                "No decisions to make. No bread to find. No one to be.",
                "Just floating. Being. A duck-shaped thing in a warm nowhere.",
                "Cheese wakes up and forgets the dream immediately. But the feeling stays.",
            ],
            mood_effect=16,
            xp_bonus=3,
        ),
        Dream(
            dream_type=DreamType.PEACEFUL,
            title="The Slow River",
            scenes=[
                "A river. Moving slowly. Cheese is on it. In it. Part of it.",
                "The banks are green. Not bright green. The quiet kind of green.",
                "Fish swim below. Unhurried. They have no schedule. Neither does Cheese.",
                "The river bends. Then straightens. Then bends again. A gentle argument with the land.",
                "Somewhere ahead the river becomes the sea. But not yet. Not for a long time.",
                "Cheese wakes up feeling carried. By what, he doesn't know. But carried.",
            ],
            mood_effect=14,
            xp_bonus=2,
        ),
    ],

    # ── Round 3: More dreams ──────────────────────────────────────────────
    DreamType.ADVENTURE: [
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="The Clockwork City",
            scenes=[
                "A city made of gears. Everything ticks. Everything turns.",
                "Cheese walks on a gear. It rotates. He walks faster. It rotates faster.",
                "A clock face the size of a building. Both hands point at bread o'clock.",
                "Tiny mechanical birds fly overhead. They don't quack. Amateurs.",
                "A drawbridge made of a giant watch hand. It rises at the hour. Falls at the half.",
                "Cheese wakes to the sound of his own heartbeat. Ticking perfectly.",
            ],
            mood_effect=12,
            xp_bonus=8,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="The Upside-Down Pond",
            scenes=[
                "The pond is above. The sky is below. Cheese is falling upward.",
                "He splashes into the sky-pond. It's warm. The clouds are the bottom.",
                "Fish fly past like birds. Birds swim past like fish. Everything is confused but content.",
                "An upside-down tree grows into the ground-sky. Its roots wave hello.",
                "Cheese finds his reflection. It's right-side up. One of them is wrong.",
                "He falls back down. Or up. Direction has stopped meaning anything. He's home.",
            ],
            mood_effect=14,
            xp_bonus=10,
        ),
        Dream(
            dream_type=DreamType.ADVENTURE,
            title="The Map in the Feather",
            scenes=[
                "One of Cheese's feathers falls out. There's a map printed on it.",
                "The map shows a path through a forest made of bread. Rye trees. Sourdough boulders.",
                "Cheese follows the path. It smells like a bakery. The air is warm and yeasty.",
                "At the center: a clearing. A single crumb the size of a house. Magnificent.",
                "He tries to eat it. It's too big. He sits on it instead. Good enough.",
                "The feather-map dissolves. The memory stays. Somewhere, bread grows wild.",
            ],
            mood_effect=15,
            xp_bonus=12,
        ),
    ],
    DreamType.FOOD: [
        Dream(
            dream_type=DreamType.FOOD,
            title="The Restaurant at the End of the Pond",
            scenes=[
                "A restaurant. Underwater. The menu is seventeen pages long.",
                "Everything is bread. Different breads. Breads Cheese has never heard of.",
                "The waiter is a fish in a bow tie. He recommends the focaccia.",
                "Cheese orders everything. The bill will be someone else's problem.",
                "Course after course arrives. Each one better. Each one warmer.",
                "Cheese wakes up full. This is impossible. But the fullness is real.",
            ],
            mood_effect=18,
            xp_bonus=5,
        ),
        Dream(
            dream_type=DreamType.FOOD,
            title="Bread Museum",
            scenes=[
                "A museum. Every exhibit is bread. Behind glass. Protected. As it should be.",
                "Ancient bread from Egypt. Medieval bread. Space bread. Future bread.",
                "A tour guide explains each one. Cheese takes notes. Mental notes.",
                "The gift shop sells bread-shaped erasers. Cheese buys twelve.",
                "The final exhibit: the world's most perfect crumb. Cheese weeps. Just a little.",
                "He wakes up with new respect for bread. Which is the same as his old respect. Maximum.",
            ],
            mood_effect=12,
            xp_bonus=4,
        ),
    ],
    DreamType.FLYING: [
        Dream(
            dream_type=DreamType.FLYING,
            title="The Wind Festival",
            scenes=[
                "Every bird in the world is here. In the sky. A festival of wings.",
                "Cheese is among them. His wings work. THEY WORK. *flaps with purpose*",
                "An eagle nods at him. Respectfully. Cheese nods back. Casually. As if this is normal.",
                "They form shapes in the sky. A bread shape. An entire aerial bakery.",
                "Cheese leads the formation. He's never led anything. It feels correct.",
                "Dawn breaks. The birds scatter. Cheese hovers. Alone. Finally understanding up.",
            ],
            mood_effect=20,
            xp_bonus=10,
            special_reward="feather_of_flight",
        ),
        Dream(
            dream_type=DreamType.FLYING,
            title="Above the Clouds",
            scenes=[
                "Higher than the clouds. The air is thin but the view is thick with wonder.",
                "Below: the pond. So small. A puddle from up here. But it's HIS puddle.",
                "Stars are closer. He could touch one if he stretched. He doesn't. Boundaries.",
                "A cloud shaped like a duck drifts past. Cheese waves. It waves back. With wind.",
                "The moon looks different from up here. Friendlier. Rounder.",
                "Cheese descends slowly. The pond grows. Home gets bigger the closer you get.",
            ],
            mood_effect=18,
            xp_bonus=8,
        ),
    ],
    DreamType.FRIEND: [
        Dream(
            dream_type=DreamType.FRIEND,
            title="The Friend Who Was Always There",
            scenes=[
                "Someone is sitting by the pond. They've been there forever. Cheese just never noticed.",
                "Not a duck. Not a human. Not a frog. Something in between. Something kind.",
                "They don't speak. They hand Cheese a crumb. The crumb is warm.",
                "They sit together. The sun moves across the sky. Neither of them counts the time.",
                "The friend stands to leave. Cheese panics. The friend sits back down. Just like that.",
                "Cheese wakes up feeling accompanied. Even alone, he doesn't feel alone.",
            ],
            mood_effect=20,
            xp_bonus=6,
        ),
        Dream(
            dream_type=DreamType.FRIEND,
            title="The Gathering",
            scenes=[
                "Everyone Cheese has ever met is here. By the pond. All at once.",
                "The heron. The squirrel. The human. Even the goose. EVEN the goose.",
                "Nobody fights. Nobody leaves. Everyone just... stays.",
                "They share bread. There's enough. For the first time, there's enough for everyone.",
                "Someone tells a joke. Cheese doesn't hear it. But he laughs. Because everyone else does.",
                "Cheese wakes up understanding that he has been collecting people. And they're all still there.",
            ],
            mood_effect=22,
            xp_bonus=8,
            special_reward="bond_token",
        ),
    ],
    DreamType.MEMORY: [
        Dream(
            dream_type=DreamType.MEMORY,
            title="The Egg",
            scenes=[
                "Dark. Warm. Compact. Cheese remembers the egg. Before anything.",
                "No pond. No bread. No concept of either. Just warmth and the sound of a heartbeat.",
                "A crack. Light. The first light. Overwhelming and beautiful and too much.",
                "The world rushing in. Air and sound and cold and someone's voice.",
                "Being small. Being new. Everything enormous and terrifying and wonderful.",
                "Cheese wakes up feeling brand new. As if today is the first day. Again.",
            ],
            mood_effect=15,
            xp_bonus=5,
        ),
    ],
    DreamType.PROPHETIC: [
        Dream(
            dream_type=DreamType.PROPHETIC,
            title="The Calendar",
            scenes=[
                "A calendar. Huge. Each page a day. Cheese flips through them.",
                "Most days look the same. Pond. Bread. Sleep. But some pages glow.",
                "A glowing page: Cheese sitting with someone new. The colors are warm.",
                "Another: Cheese standing somewhere he's never been. Not scared. Just there.",
                "The last page is blank. Not empty. Blank. Waiting to be written.",
                "Cheese wakes knowing that the blank pages are the best ones.",
            ],
            mood_effect=14,
            xp_bonus=8,
            special_reward="glimpse_of_tomorrow",
        ),
    ],
}


@dataclass
class DreamResult:
    """Result of a dream sequence."""
    dream: Dream
    scenes_shown: List[str]
    mood_effect: int
    xp_earned: int
    special_reward: Optional[str]
    message: str


class DreamSystem:
    """Manages duck dreams during sleep."""

    def __init__(self):
        self.dream_history: List[str] = []  # Track recent dream titles
        self.total_dreams: int = 0
        self.dream_type_counts: Dict[str, int] = {}
        self.special_rewards_found: List[str] = []

    def generate_dream(
        self,
        mood_score: int = 50,
        recent_activities: List[str] = None,
        visitor_names: List[str] = None,
    ) -> Dream:
        """Generate a dream based on current state."""
        recent_activities = recent_activities or []
        visitor_names = visitor_names or []

        # Determine dream type probabilities
        weights = {
            DreamType.ADVENTURE: 20,
            DreamType.FLYING: 15,
            DreamType.FOOD: 20,
            DreamType.FRIEND: 15,
            DreamType.NIGHTMARE: 5,
            DreamType.MEMORY: 10,
            DreamType.PROPHETIC: 3,
            DreamType.SILLY: 15,
            DreamType.PEACEFUL: 15,
        }

        # Adjust weights based on mood
        if mood_score < 30:
            weights[DreamType.NIGHTMARE] += 10
            weights[DreamType.PEACEFUL] -= 5
        elif mood_score > 70:
            weights[DreamType.PEACEFUL] += 10
            weights[DreamType.NIGHTMARE] -= 3
            weights[DreamType.FLYING] += 5

        # Adjust based on recent activities
        if "feed" in recent_activities or "eat" in recent_activities:
            weights[DreamType.FOOD] += 15
        if "play" in recent_activities:
            weights[DreamType.ADVENTURE] += 10
            weights[DreamType.SILLY] += 10
        if visitor_names:
            weights[DreamType.FRIEND] += 15

        # Avoid repeating recent dreams
        for title in self.dream_history[-3:]:
            for dream_type, dreams in DREAMS.items():
                for dream in dreams:
                    if dream.title == title:
                        weights[dream_type] = max(1, weights[dream_type] - 10)

        # Select dream type
        dream_types = list(weights.keys())
        probabilities = [weights[dt] for dt in dream_types]
        total = sum(probabilities)
        probabilities = [p / total for p in probabilities]

        selected_type = random.choices(dream_types, weights=probabilities, k=1)[0]

        # Select specific dream
        available_dreams = DREAMS.get(selected_type, [])
        if not available_dreams:
            # Fallback to peaceful dream
            available_dreams = DREAMS[DreamType.PEACEFUL]

        dream = random.choice(available_dreams)
        return dream

    def start_dream(
        self,
        mood_score: int = 50,
        recent_activities: List[str] = None,
        visitor_names: List[str] = None,
    ) -> DreamResult:
        """Start a dream sequence and return the result."""
        dream = self.generate_dream(mood_score, recent_activities, visitor_names)

        # Track this dream
        self.dream_history.append(dream.title)
        if len(self.dream_history) > 10:
            self.dream_history = self.dream_history[-10:]

        self.total_dreams += 1
        type_key = dream.dream_type.value
        self.dream_type_counts[type_key] = self.dream_type_counts.get(type_key, 0) + 1

        # Check for special reward (not guaranteed even if dream has one)
        special_reward = None
        if dream.special_reward and random.random() < 0.3:  # 30% chance
            special_reward = dream.special_reward
            self.special_rewards_found.append(special_reward)

        # Generate result
        result = DreamResult(
            dream=dream,
            scenes_shown=dream.scenes,
            mood_effect=dream.mood_effect,
            xp_earned=dream.xp_bonus,
            special_reward=special_reward,
            message=f"{dream.title}: A {dream.dream_type.value} dream",
        )

        return result

    def get_dream_stats(self) -> Dict:
        """Get statistics about dreams."""
        return {
            "total_dreams": self.total_dreams,
            "dream_types": self.dream_type_counts,
            "special_rewards": self.special_rewards_found,
            "recent_dreams": self.dream_history[-5:],
        }

    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "dream_history": self.dream_history,
            "total_dreams": self.total_dreams,
            "dream_type_counts": self.dream_type_counts,
            "special_rewards_found": self.special_rewards_found,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DreamSystem":
        """Create from dictionary."""
        system = cls()
        system.dream_history = data.get("dream_history", [])
        system.total_dreams = data.get("total_dreams", 0)
        system.dream_type_counts = data.get("dream_type_counts", {})
        system.special_rewards_found = data.get("special_rewards_found", [])
        return system


# Global instance
dreams = DreamSystem()
