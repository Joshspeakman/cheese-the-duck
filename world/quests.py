"""
Mini-Quests System - Multi-step storylines with narrative and rewards.
Features quest chains, branching paths, and memorable adventures.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Callable
from enum import Enum
import random


class QuestType(Enum):
    """Types of quests."""
    MAIN = "main"
    SIDE = "side"
    DAILY = "daily"
    HIDDEN = "hidden"
    SEASONAL = "seasonal"


class QuestDifficulty(Enum):
    """Quest difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    LEGENDARY = "legendary"


class ObjectiveType(Enum):
    """Types of quest objectives."""
    COLLECT = "collect"
    FEED = "feed"
    PLAY = "play"
    EXPLORE = "explore"
    TALK = "talk"
    FISH = "fish"
    GARDEN = "garden"
    CRAFT = "craft"
    FIND = "find"
    WAIT = "wait"
    CHOICE = "choice"


@dataclass
class QuestObjective:
    """A single objective within a quest."""
    id: str
    description: str
    objective_type: ObjectiveType
    target: str  # What to collect/find/etc
    required_amount: int
    current_progress: int = 0
    completed: bool = False
    hint: str = ""
    optional: bool = False


@dataclass
class QuestReward:
    """Rewards for completing a quest."""
    xp: int = 0
    coins: int = 0
    items: List[str] = field(default_factory=list)
    unlocks: List[str] = field(default_factory=list)
    title: Optional[str] = None
    achievement: Optional[str] = None


@dataclass
class QuestStep:
    """A step in a quest with dialogue and objectives."""
    step_id: int
    title: str
    dialogue: List[str]  # NPC/narrator dialogue
    objectives: List[QuestObjective]
    rewards: Optional[QuestReward] = None
    choices: Optional[Dict[str, int]] = None  # choice_text -> next_step_id
    next_step_id: Optional[int] = None


@dataclass
class Quest:
    """A complete quest with multiple steps."""
    id: str
    name: str
    description: str
    quest_type: QuestType
    difficulty: QuestDifficulty
    steps: List[QuestStep]
    final_reward: QuestReward
    prerequisite_quests: List[str] = field(default_factory=list)
    required_level: int = 1
    time_limit_hours: Optional[int] = None
    repeatable: bool = False


@dataclass
class ActiveQuest:
    """An active quest being tracked."""
    quest_id: str
    current_step: int
    started_at: str
    step_progress: Dict[str, int]  # objective_id -> progress
    choices_made: List[str]
    completed: bool = False
    failed: bool = False


# Quest definitions
QUESTS: Dict[str, Quest] = {
    # Tutorial Quest
    "welcome_duckling": Quest(
        id="welcome_duckling",
        name="Welcome, Little Duckling!",
        description="Learn the basics of caring for your new duck friend.",
        quest_type=QuestType.MAIN,
        difficulty=QuestDifficulty.EASY,
        steps=[
            QuestStep(
                step_id=1,
                title="First Steps",
                dialogue=[
                    "d *quack quack!*",
                    "Your little duckling looks up at you with big curious eyes.",
                    "It seems hungry... maybe you should feed it!",
                ],
                objectives=[
                    QuestObjective(
                        id="feed_1",
                        description="Feed your duck",
                        objective_type=ObjectiveType.FEED,
                        target="any",
                        required_amount=1,
                        hint="Press 'F' to feed your duck!",
                    ),
                ],
                next_step_id=2,
            ),
            QuestStep(
                step_id=2,
                title="Playtime!",
                dialogue=[
                    "Your duck happily gobbles up the food!",
                    "*satisfied quack*",
                    "Now it seems energetic and wants to play!",
                ],
                objectives=[
                    QuestObjective(
                        id="play_1",
                        description="Play with your duck",
                        objective_type=ObjectiveType.PLAY,
                        target="any",
                        required_amount=2,
                        hint="Press 'P' to play with your duck!",
                    ),
                ],
                next_step_id=3,
            ),
            QuestStep(
                step_id=3,
                title="Getting to Know Each Other",
                dialogue=[
                    "Your duck is having so much fun!",
                    "It waddles over and nudges your hand affectionately.",
                    "Try talking to your duck to bond with it!",
                ],
                objectives=[
                    QuestObjective(
                        id="talk_1",
                        description="Talk to your duck",
                        objective_type=ObjectiveType.TALK,
                        target="any",
                        required_amount=1,
                        hint="Press 'T' to chat with your duck!",
                    ),
                ],
                rewards=QuestReward(xp=25, coins=10),
            ),
        ],
        final_reward=QuestReward(
            xp=50,
            coins=25,
            items=["welcome_bread", "duck_toy"],
            title="Duckling Caretaker",
        ),
    ),
    
    # The Lost Feather
    "lost_feather": Quest(
        id="lost_feather",
        name="The Lost Feather",
        description="Help your duck find its lost special feather!",
        quest_type=QuestType.MAIN,
        difficulty=QuestDifficulty.MEDIUM,
        prerequisite_quests=["welcome_duckling"],
        steps=[
            QuestStep(
                step_id=1,
                title="Something Missing",
                dialogue=[
                    "Your duck seems distressed! *sad quack*",
                    "It keeps looking at its wing, as if something is missing.",
                    "Oh no! Your duck has lost a special golden feather!",
                    "You should search around the pond area.",
                ],
                objectives=[
                    QuestObjective(
                        id="explore_pond",
                        description="Explore the pond",
                        objective_type=ObjectiveType.EXPLORE,
                        target="pond",
                        required_amount=1,
                        hint="Go to the pond area to look for clues!",
                    ),
                ],
                next_step_id=2,
            ),
            QuestStep(
                step_id=2,
                title="Following Clues",
                dialogue=[
                    "You found some tiny golden sparkles by the pond!",
                    "The trail leads toward the garden...",
                    "But first, you should ask around.",
                ],
                objectives=[
                    QuestObjective(
                        id="talk_3",
                        description="Ask about the feather",
                        objective_type=ObjectiveType.TALK,
                        target="any",
                        required_amount=3,
                    ),
                    QuestObjective(
                        id="explore_garden",
                        description="Search the garden",
                        objective_type=ObjectiveType.EXPLORE,
                        target="garden",
                        required_amount=1,
                    ),
                ],
                next_step_id=3,
            ),
            QuestStep(
                step_id=3,
                title="The Magpie's Nest",
                dialogue=[
                    "You found it! A mischievous magpie took the feather!",
                    "The magpie looks at you curiously...",
                    "It seems like it wants something shiny in exchange.",
                ],
                objectives=[
                    QuestObjective(
                        id="collect_shiny",
                        description="Find something shiny to trade",
                        objective_type=ObjectiveType.COLLECT,
                        target="shiny_object",
                        required_amount=1,
                        hint="Try fishing or digging for treasures!",
                    ),
                ],
                rewards=QuestReward(xp=50, coins=30),
            ),
        ],
        final_reward=QuestReward(
            xp=100,
            coins=75,
            items=["golden_feather", "magpie_friendship_charm"],
            title="Feather Finder",
            achievement="first_quest_chain",
        ),
    ),
    
    # The Great Fish Tale
    "great_fish_tale": Quest(
        id="great_fish_tale",
        name="The Great Fish Tale",
        description="Prove yourself as a master fisher!",
        quest_type=QuestType.SIDE,
        difficulty=QuestDifficulty.MEDIUM,
        steps=[
            QuestStep(
                step_id=1,
                title="Fishy Beginnings",
                dialogue=[
                    "An old duck fisherman waddles by...",
                    "d 'Heard you're new to fishing, eh?'",
                    "'Back in my day, we caught fish as big as logs!'",
                    "'Prove yourself by catching some fish!'",
                ],
                objectives=[
                    QuestObjective(
                        id="fish_5",
                        description="Catch 5 fish",
                        objective_type=ObjectiveType.FISH,
                        target="any",
                        required_amount=5,
                    ),
                ],
                rewards=QuestReward(xp=30, coins=20, items=["better_bait"]),
                next_step_id=2,
            ),
            QuestStep(
                step_id=2,
                title="The Hunt for Ol' Whiskers",
                dialogue=[
                    "d 'Not bad, not bad!'",
                    "'But have you heard of Ol' Whiskers?'",
                    "'The legendary catfish that lurks in the deep!'",
                    "'Many have tried to catch it... none have succeeded.'",
                ],
                objectives=[
                    QuestObjective(
                        id="fish_rare",
                        description="Catch a rare fish",
                        objective_type=ObjectiveType.FISH,
                        target="rare",
                        required_amount=1,
                    ),
                ],
            ),
        ],
        final_reward=QuestReward(
            xp=150,
            coins=100,
            items=["master_fishing_rod", "fish_trophy"],
            title="Master Angler",
        ),
    ),
    
    # Garden of Dreams
    "garden_dreams": Quest(
        id="garden_dreams",
        name="Garden of Dreams",
        description="Grow a magical garden with special flowers!",
        quest_type=QuestType.SIDE,
        difficulty=QuestDifficulty.MEDIUM,
        steps=[
            QuestStep(
                step_id=1,
                title="Seeds of Wonder",
                dialogue=[
                    "A mysterious packet of seeds blows into your garden...",
                    "The packet reads: 'Dream Seeds - Handle with Care'",
                    "You feel a strange magic emanating from them.",
                    "Plant them and see what grows!",
                ],
                objectives=[
                    QuestObjective(
                        id="plant_3",
                        description="Plant 3 seeds",
                        objective_type=ObjectiveType.GARDEN,
                        target="plant",
                        required_amount=3,
                    ),
                ],
                rewards=QuestReward(coins=15),
                next_step_id=2,
            ),
            QuestStep(
                step_id=2,
                title="Nurturing Growth",
                dialogue=[
                    "The seeds have sprouted! But they need special care.",
                    "Keep them watered and watch them bloom!",
                ],
                objectives=[
                    QuestObjective(
                        id="water_10",
                        description="Water plants 10 times",
                        objective_type=ObjectiveType.GARDEN,
                        target="water",
                        required_amount=10,
                    ),
                    QuestObjective(
                        id="harvest_3",
                        description="Harvest 3 plants",
                        objective_type=ObjectiveType.GARDEN,
                        target="harvest",
                        required_amount=3,
                    ),
                ],
            ),
        ],
        final_reward=QuestReward(
            xp=120,
            coins=80,
            items=["dream_flower", "enchanted_seeds"],
            title="Dream Gardener",
            unlocks=["golden_flower_seed"],
        ),
    ),
    
    # The Mysterious Stranger
    "mysterious_stranger": Quest(
        id="mysterious_stranger",
        name="The Mysterious Stranger",
        description="A cloaked figure has appeared with an unusual request...",
        quest_type=QuestType.HIDDEN,
        difficulty=QuestDifficulty.HARD,
        steps=[
            QuestStep(
                step_id=1,
                title="An Unusual Visitor",
                dialogue=[
                    "A cloaked duck appears from the shadows...",
                    "d '...I've been watching you...'",
                    "'You have shown kindness. That is rare.'",
                    "'I have a task... if you're brave enough.'",
                ],
                choices={
                    "Accept the challenge": 2,
                    "Ask for more details first": 3,
                    "Politely decline": -1,  # Ends quest
                },
                objectives=[
                    QuestObjective(
                        id="choice_1",
                        description="Make your choice",
                        objective_type=ObjectiveType.CHOICE,
                        target="any",
                        required_amount=1,
                    ),
                ],
            ),
            QuestStep(
                step_id=2,
                title="The Brave Path",
                dialogue=[
                    "'Courage! I like that.'",
                    "'Seek the three ancient tokens hidden in this land.'",
                    "'One in the water, one in the earth, one in the sky.'",
                ],
                objectives=[
                    QuestObjective(
                        id="find_token_water",
                        description="Find the Water Token",
                        objective_type=ObjectiveType.FIND,
                        target="water_token",
                        required_amount=1,
                        hint="Try fishing in the deepest waters...",
                    ),
                    QuestObjective(
                        id="find_token_earth",
                        description="Find the Earth Token",
                        objective_type=ObjectiveType.FIND,
                        target="earth_token",
                        required_amount=1,
                        hint="Dig for buried treasures...",
                    ),
                    QuestObjective(
                        id="find_token_sky",
                        description="Find the Sky Token",
                        objective_type=ObjectiveType.FIND,
                        target="sky_token",
                        required_amount=1,
                        hint="Sometimes treasures fall from above during special weather...",
                    ),
                ],
                next_step_id=4,
            ),
            QuestStep(
                step_id=3,
                title="The Cautious Path",
                dialogue=[
                    "'A wise one, you are.'",
                    "'I am a guardian of old secrets.'",
                    "'There is an ancient power scattered across this land.'",
                    "'Help me gather it, and you shall be rewarded greatly.'",
                ],
                objectives=[
                    QuestObjective(
                        id="learn_more",
                        description="Learn about the tokens",
                        objective_type=ObjectiveType.TALK,
                        target="guardian",
                        required_amount=3,
                    ),
                ],
                next_step_id=2,
            ),
            QuestStep(
                step_id=4,
                title="The Revelation",
                dialogue=[
                    "You've gathered all three tokens!",
                    "The mysterious figure's cloak falls away...",
                    "It's a magnificent ancient duck, glowing with ethereal light!",
                    "'You have proven yourself worthy.'",
                    "'These tokens... they are keys to great power.'",
                    "'Use them wisely.'",
                ],
                objectives=[],
            ),
        ],
        final_reward=QuestReward(
            xp=500,
            coins=300,
            items=["ancient_amulet", "guardian_blessing"],
            title="Token Bearer",
            achievement="mysterious_quest_complete",
            unlocks=["secret_area"],
        ),
    ),
}


class QuestSystem:
    """
    Manages quests, objectives, and story progression.
    """
    
    def __init__(self):
        self.active_quests: Dict[str, ActiveQuest] = {}
        self.completed_quests: Dict[str, int] = {}  # quest_id -> times completed
        self.failed_quests: List[str] = []
        self.unlocked_quests: List[str] = ["welcome_duckling"]  # Start with tutorial
        self.total_quests_completed: int = 0
        self.choices_history: Dict[str, List[str]] = {}
        self.earned_titles: List[str] = []
        self.quest_chain_progress: Dict[str, int] = {}
    
    def get_available_quests(self, player_level: int = 1) -> List[Quest]:
        """Get list of quests available to start."""
        available = []
        
        for quest_id in self.unlocked_quests:
            if quest_id in self.active_quests:
                continue  # Already active
            
            if quest_id in self.completed_quests:
                quest = QUESTS.get(quest_id)
                if not quest or not quest.repeatable:
                    continue  # Already completed and not repeatable
            
            quest = QUESTS.get(quest_id)
            if not quest:
                continue
            
            # Check prerequisites
            prereqs_met = all(
                pq in self.completed_quests
                for pq in quest.prerequisite_quests
            )
            
            if prereqs_met and player_level >= quest.required_level:
                available.append(quest)
        
        return available
    
    def start_quest(self, quest_id: str) -> Tuple[bool, str, Optional[List[str]]]:
        """Start a new quest."""
        if quest_id in self.active_quests:
            return False, "Quest already in progress!", None
        
        quest = QUESTS.get(quest_id)
        if not quest:
            return False, "Quest not found!", None
        
        active = ActiveQuest(
            quest_id=quest_id,
            current_step=1,
            started_at=datetime.now().isoformat(),
            step_progress={},
            choices_made=[],
        )
        
        self.active_quests[quest_id] = active
        
        # Get first step dialogue
        first_step = next((s for s in quest.steps if s.step_id == 1), None)
        dialogue = first_step.dialogue if first_step else []
        
        return True, f"[=] Quest Started: {quest.name}", dialogue
    
    def update_progress(self, objective_type: str, target: str, amount: int = 1) -> Tuple[List[Tuple[str, str, bool]], List[Tuple[str, QuestReward]]]:
        """Update progress on quest objectives.
        Returns: (objective_updates, completed_quests_with_rewards)
        - objective_updates: List of (quest_id, objective_description, completed)
        - completed_quests_with_rewards: List of (quest_id, QuestReward)
        """
        updates = []
        completed_quests = []
        
        for quest_id, active in list(self.active_quests.items()):
            if active.completed:
                continue
            
            quest = QUESTS.get(quest_id)
            if not quest:
                continue
            
            current_step = next(
                (s for s in quest.steps if s.step_id == active.current_step),
                None
            )
            
            if not current_step:
                continue
            
            for objective in current_step.objectives:
                if objective.completed:
                    continue
                
                if objective.objective_type.value != objective_type:
                    continue
                
                # Check target match
                if objective.target != "any" and objective.target != target:
                    continue
                
                # Update progress
                obj_key = f"{quest_id}_{objective.id}"
                current = active.step_progress.get(obj_key, 0)
                new_progress = min(current + amount, objective.required_amount)
                active.step_progress[obj_key] = new_progress
                objective.current_progress = new_progress
                
                # Check completion
                completed = new_progress >= objective.required_amount
                if completed:
                    objective.completed = True
                
                updates.append((quest_id, objective.description, completed))
        
        # Check for step completions and collect completed quest rewards
        for quest_id in list(self.active_quests.keys()):
            result = self._check_step_completion(quest_id)
            if result:
                completed_quests.append(result)
        
        return updates, completed_quests
    
    def make_choice(self, quest_id: str, choice: str) -> Tuple[bool, str, Optional[int]]:
        """Make a choice in a quest with branching paths."""
        active = self.active_quests.get(quest_id)
        if not active:
            return False, "Quest not active!", None
        
        quest = QUESTS.get(quest_id)
        if not quest:
            return False, "Quest not found!", None
        
        current_step = next(
            (s for s in quest.steps if s.step_id == active.current_step),
            None
        )
        
        if not current_step or not current_step.choices:
            return False, "No choices available!", None
        
        if choice not in current_step.choices:
            return False, "Invalid choice!", None
        
        next_step = current_step.choices[choice]
        active.choices_made.append(choice)
        
        # Track in history
        if quest_id not in self.choices_history:
            self.choices_history[quest_id] = []
        self.choices_history[quest_id].append(choice)

        # Keep history manageable to prevent memory leak
        if len(self.choices_history[quest_id]) > 50:
            self.choices_history[quest_id] = self.choices_history[quest_id][-50:]
        
        # Handle quest end (-1 means end/fail)
        if next_step == -1:
            active.failed = True
            self.failed_quests.append(quest_id)
            del self.active_quests[quest_id]
            return True, "Quest ended based on your choice.", None
        
        # Complete choice objective
        for obj in current_step.objectives:
            if obj.objective_type == ObjectiveType.CHOICE:
                obj.completed = True
        
        # Move to next step
        active.current_step = next_step
        
        # Get next step dialogue
        next_step_obj = next((s for s in quest.steps if s.step_id == next_step), None)
        if next_step_obj:
            return True, f"You chose: {choice}", next_step
        
        return True, f"You chose: {choice}", next_step
    
    def _check_step_completion(self, quest_id: str) -> Optional[Tuple[str, QuestReward]]:
        """Check if current step is complete and advance if so.
        Returns (quest_id, reward) if quest was completed, else None.
        """
        active = self.active_quests.get(quest_id)
        if not active or active.completed:
            return None
        
        quest = QUESTS.get(quest_id)
        if not quest:
            return None
        
        current_step = next(
            (s for s in quest.steps if s.step_id == active.current_step),
            None
        )
        
        if not current_step:
            return None
        
        # Check if all required objectives are complete
        required_objectives = [o for o in current_step.objectives if not o.optional]
        all_complete = all(
            active.step_progress.get(f"{quest_id}_{o.id}", 0) >= o.required_amount
            for o in required_objectives
        )
        
        if not all_complete:
            return None
        
        # Step complete!
        if current_step.next_step_id:
            active.current_step = current_step.next_step_id
            return None
        else:
            # Quest complete!
            reward = self._complete_quest(quest_id)
            if reward:
                return (quest_id, reward)
            return None
    
    def _complete_quest(self, quest_id: str) -> Optional[QuestReward]:
        """Complete a quest and return rewards."""
        active = self.active_quests.get(quest_id)
        if not active:
            return None
        
        active.completed = True
        
        quest = QUESTS.get(quest_id)
        if not quest:
            return None
        
        # Track completion
        self.completed_quests[quest_id] = self.completed_quests.get(quest_id, 0) + 1
        self.total_quests_completed += 1
        
        # Track title
        if quest.final_reward.title:
            self.earned_titles.append(quest.final_reward.title)
        
        # Unlock follow-up quests
        for q_id, q in QUESTS.items():
            if quest_id in q.prerequisite_quests:
                if q_id not in self.unlocked_quests:
                    self.unlocked_quests.append(q_id)
        
        # Clean up active quest
        del self.active_quests[quest_id]
        
        # Return the reward for the caller to apply
        return quest.final_reward
    
    def get_active_quest_status(self, quest_id: str) -> Optional[Dict]:
        """Get status of an active quest."""
        active = self.active_quests.get(quest_id)
        if not active:
            return None
        
        quest = QUESTS.get(quest_id)
        if not quest:
            return None
        
        current_step = next(
            (s for s in quest.steps if s.step_id == active.current_step),
            None
        )
        
        objectives_status = []
        if current_step:
            for obj in current_step.objectives:
                progress = active.step_progress.get(f"{quest_id}_{obj.id}", 0)
                objectives_status.append({
                    "description": obj.description,
                    "progress": progress,
                    "required": obj.required_amount,
                    "completed": progress >= obj.required_amount,
                })
        
        return {
            "quest_name": quest.name,
            "step_title": current_step.title if current_step else "",
            "objectives": objectives_status,
            "has_choices": bool(current_step and current_step.choices),
            "choices": list(current_step.choices.keys()) if current_step and current_step.choices else [],
        }
    
    def render_quest_log(self) -> List[str]:
        """Render the quest log display."""
        lines = [
            "+===============================================+",
            "|            [=] QUEST LOG [=]                    |",
            "+===============================================+",
        ]
        
        if self.active_quests:
            lines.append("|  ACTIVE QUESTS:                               |")
            for quest_id, active in self.active_quests.items():
                quest = QUESTS.get(quest_id)
                if quest:
                    lines.append(f"|  > {quest.name[:35]:35}      |")
                    status = self.get_active_quest_status(quest_id)
                    if status:
                        for obj in status["objectives"][:3]:  # Show up to 3 objectives
                            mark = "x" if obj["completed"] else "o"
                            lines.append(f"|    {mark} {obj['description'][:33]:33}  |")
            lines.append("+===============================================+")
        
        # Available quests - show more with scroll hint
        available = self.get_available_quests()
        if available:
            lines.append("|  AVAILABLE QUESTS:                            |")
            show_count = min(5, len(available))  # Show up to 5 available
            for quest in available[:show_count]:
                diff_icon = {"easy": "*", "medium": "**", "hard": "***", "legendary": "[D]"}
                icon = diff_icon.get(quest.difficulty.value, "*")
                lines.append(f"|  {icon} {quest.name[:33]:33}    |")
            if len(available) > show_count:
                lines.append(f"|  ... and {len(available) - show_count} more available        |")
        
        lines.extend([
            "+===============================================+",
            f"|  Completed: {self.total_quests_completed:3}  |  Titles: {len(self.earned_titles):3}          |",
            "+===============================================+",
        ])
        
        return lines
    
    def render_quest_detail(self, quest_id: str) -> List[str]:
        """Render detailed view of a quest."""
        quest = QUESTS.get(quest_id)
        if not quest:
            return ["Quest not found!"]
        
        active = self.active_quests.get(quest_id)
        
        diff_colors = {"easy": "+", "medium": "#", "hard": "O", "legendary": "!"}
        diff = diff_colors.get(quest.difficulty.value, "o")
        
        lines = [
            "+===============================================+",
            f"|  {quest.name:^41}  |",
            f"|  {diff} {quest.difficulty.value.title():^37}  |",
            "+===============================================+",
        ]
        
        # Description
        desc_lines = [quest.description[i:i+40] for i in range(0, len(quest.description), 40)]
        for line in desc_lines:
            lines.append(f"|  {line:40}     |")
        
        lines.append("+===============================================+")
        
        if active:
            status = self.get_active_quest_status(quest_id)
            if status:
                lines.append(f"|  Step: {status['step_title'][:34]:34}    |")
                lines.append("|  Objectives:                                  |")
                for obj in status["objectives"]:
                    mark = "x" if obj["completed"] else "o"
                    prog = f"{obj['progress']}/{obj['required']}"
                    lines.append(f"|   {mark} {obj['description'][:28]:28} {prog:6} |")
        else:
            lines.append("|  Status: Not Started                          |")
        
        lines.append("+===============================================+")
        lines.append("|  Rewards:                                      |")
        
        reward = quest.final_reward
        lines.append(f"|    XP: {reward.xp}  Coins: {reward.coins:^25}    |")
        if reward.title:
            lines.append(f"|    Title: {reward.title:^31}    |")
        
        lines.append("+===============================================+")
        
        return lines
    
    def to_dict(self) -> dict:
        """Convert to dictionary for saving."""
        return {
            "active_quests": {
                qid: {
                    "quest_id": aq.quest_id,
                    "current_step": aq.current_step,
                    "started_at": aq.started_at,
                    "step_progress": aq.step_progress,
                    "choices_made": aq.choices_made,
                    "completed": aq.completed,
                    "failed": aq.failed,
                }
                for qid, aq in self.active_quests.items()
            },
            "completed_quests": self.completed_quests,
            "failed_quests": self.failed_quests,
            "unlocked_quests": self.unlocked_quests,
            "total_quests_completed": self.total_quests_completed,
            "choices_history": self.choices_history,
            "earned_titles": self.earned_titles,
            "quest_chain_progress": self.quest_chain_progress,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "QuestSystem":
        """Create from dictionary."""
        system = cls()
        
        for qid, aq_data in data.get("active_quests", {}).items():
            system.active_quests[qid] = ActiveQuest(
                quest_id=aq_data["quest_id"],
                current_step=aq_data["current_step"],
                started_at=aq_data["started_at"],
                step_progress=aq_data.get("step_progress", {}),
                choices_made=aq_data.get("choices_made", []),
                completed=aq_data.get("completed", False),
                failed=aq_data.get("failed", False),
            )
        
        system.completed_quests = data.get("completed_quests", {})
        system.failed_quests = data.get("failed_quests", [])
        system.unlocked_quests = data.get("unlocked_quests", ["welcome_duckling"])
        system.total_quests_completed = data.get("total_quests_completed", 0)
        system.choices_history = data.get("choices_history", {})
        system.earned_titles = data.get("earned_titles", [])
        system.quest_chain_progress = data.get("quest_chain_progress", {})
        
        return system


# Global quest system instance
quest_system = QuestSystem()
