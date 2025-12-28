"""
Mini-games system - Fun interactive games for bonus rewards.
Includes: Bread Catch, Bug Chase, Memory Match, Duck Race
"""
import random
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum


class MiniGameType(Enum):
    BREAD_CATCH = "bread_catch"
    BUG_CHASE = "bug_chase"
    MEMORY_MATCH = "memory_match"
    DUCK_RACE = "duck_race"


@dataclass
class MiniGameResult:
    """Result of playing a mini-game."""
    game_type: MiniGameType
    score: int
    high_score: bool
    coins_earned: int
    xp_earned: int
    items_earned: List[str] = field(default_factory=list)
    message: str = ""


@dataclass
class BreadCatchGame:
    """
    Bread Catch - Catch falling bread crumbs!
    Player moves left/right to catch bread, avoid rotten food.
    """
    width: int = 20
    height: int = 10
    player_pos: int = 10
    score: int = 0
    lives: int = 3
    falling_items: List[Tuple[int, int, str]] = field(default_factory=list)  # (x, y, type)
    game_over: bool = False
    frame: int = 0

    # Item types: bread (good), golden_bread (bonus), rotten (bad)
    ITEM_CHARS = {
        "bread": "o",
        "golden_bread": "*",
        "rotten": "x",
        "seed": ".",
    }

    ITEM_POINTS = {
        "bread": 10,
        "golden_bread": 50,
        "seed": 5,
        "rotten": -20,
    }

    def spawn_item(self):
        """Spawn a new falling item."""
        x = random.randint(1, self.width - 2)
        # Weighted random item type
        roll = random.random()
        if roll < 0.6:
            item_type = "bread"
        elif roll < 0.75:
            item_type = "seed"
        elif roll < 0.9:
            item_type = "rotten"
        else:
            item_type = "golden_bread"
        self.falling_items.append((x, 0, item_type))

    def update(self):
        """Update game state."""
        if self.game_over:
            return

        self.frame += 1

        # Spawn new items periodically
        if self.frame % 5 == 0:
            self.spawn_item()

        # Move items down
        new_items = []
        for x, y, item_type in self.falling_items:
            new_y = y + 1

            # Check if caught by player
            if new_y >= self.height - 1:
                if abs(x - self.player_pos) <= 1:
                    # Caught!
                    points = self.ITEM_POINTS.get(item_type, 0)
                    self.score += points
                    if item_type == "rotten":
                        self.lives -= 1
                        if self.lives <= 0:
                            self.game_over = True
                # Item reached bottom, remove it
                continue

            new_items.append((x, new_y, item_type))

        self.falling_items = new_items

    def move_left(self):
        """Move player left."""
        self.player_pos = max(1, self.player_pos - 2)

    def move_right(self):
        """Move player right."""
        self.player_pos = min(self.width - 2, self.player_pos + 2)

    def render(self) -> List[str]:
        """Render game state as ASCII art."""
        lines = []
        lines.append(f"  BREAD CATCH!  Score: {self.score}  Lives: {'<3' * self.lives}")
        lines.append("+" + "-" * self.width + "+")

        for y in range(self.height):
            row = [" "] * self.width

            # Draw falling items
            for ix, iy, item_type in self.falling_items:
                if iy == y and 0 <= ix < self.width:
                    row[ix] = self.ITEM_CHARS.get(item_type, "?")

            # Draw player on bottom row
            if y == self.height - 1:
                # Duck catcher
                for dx in range(-1, 2):
                    px = self.player_pos + dx
                    if 0 <= px < self.width:
                        row[px] = "=" if dx != 0 else "V"

            lines.append("|" + "".join(row) + "|")

        lines.append("+" + "-" * self.width + "+")
        lines.append("  [<] Left  [>] Right  [Q] Quit")

        if self.game_over:
            lines.append("")
            lines.append(f"  GAME OVER! Final Score: {self.score}")

        return lines


@dataclass
class BugChaseGame:
    """
    Bug Chase - Quick reaction game to catch bugs!
    Bugs appear randomly, player must press key quickly.
    """
    width: int = 20
    height: int = 8
    score: int = 0
    bugs_caught: int = 0
    bugs_escaped: int = 0
    max_escaped: int = 5
    current_bug: Optional[Tuple[int, int]] = None
    bug_timer: float = 0
    bug_lifetime: float = 2.0  # Seconds to catch bug
    game_over: bool = False
    reaction_times: List[float] = field(default_factory=list)
    bug_spawn_time: float = 0
    waiting_for_bug: bool = True

    BUG_CHARS = ["@", "#", "&", "%", "~"]

    def spawn_bug(self):
        """Spawn a new bug at random position."""
        x = random.randint(2, self.width - 3)
        y = random.randint(1, self.height - 2)
        self.current_bug = (x, y)
        self.bug_spawn_time = time.time()
        self.waiting_for_bug = False

    def update(self, delta_time: float):
        """Update game state."""
        if self.game_over:
            return

        if self.waiting_for_bug:
            self.bug_timer += delta_time
            if self.bug_timer > random.uniform(0.5, 2.0):
                self.spawn_bug()
                self.bug_timer = 0
        elif self.current_bug:
            elapsed = time.time() - self.bug_spawn_time
            if elapsed > self.bug_lifetime:
                # Bug escaped!
                self.bugs_escaped += 1
                self.current_bug = None
                self.waiting_for_bug = True
                if self.bugs_escaped >= self.max_escaped:
                    self.game_over = True

    def catch_bug(self) -> bool:
        """Try to catch the current bug."""
        if self.current_bug and not self.waiting_for_bug:
            reaction_time = time.time() - self.bug_spawn_time
            self.reaction_times.append(reaction_time)

            # Score based on reaction time
            if reaction_time < 0.3:
                points = 100
            elif reaction_time < 0.6:
                points = 50
            elif reaction_time < 1.0:
                points = 25
            else:
                points = 10

            self.score += points
            self.bugs_caught += 1
            self.current_bug = None
            self.waiting_for_bug = True
            return True
        return False

    def get_average_reaction(self) -> float:
        """Get average reaction time."""
        if not self.reaction_times:
            return 0.0
        return sum(self.reaction_times) / len(self.reaction_times)

    def render(self) -> List[str]:
        """Render game state."""
        lines = []
        lines.append(f"  BUG CHASE!  Score: {self.score}  Caught: {self.bugs_caught}")
        lines.append(f"  Escaped: {self.bugs_escaped}/{self.max_escaped}")
        lines.append("+" + "-" * self.width + "+")

        for y in range(self.height):
            row = [" "] * self.width

            # Draw bug if present
            if self.current_bug and not self.waiting_for_bug:
                bx, by = self.current_bug
                if by == y and 0 <= bx < self.width:
                    row[bx] = random.choice(self.BUG_CHARS)

            lines.append("|" + "".join(row) + "|")

        lines.append("+" + "-" * self.width + "+")

        if self.waiting_for_bug and not self.game_over:
            lines.append("  Wait for it...")
        elif self.current_bug:
            lines.append("  [SPACE] CATCH IT!")

        if self.game_over:
            avg = self.get_average_reaction()
            lines.append("")
            lines.append(f"  GAME OVER! Bugs caught: {self.bugs_caught}")
            lines.append(f"  Avg reaction: {avg:.2f}s")

        lines.append("  [Q] Quit")

        return lines


@dataclass
class MemoryMatchGame:
    """
    Memory Match - Classic card matching game!
    Find matching pairs of duck items.
    """
    grid_size: int = 4  # 4x4 grid = 8 pairs
    cards: List[str] = field(default_factory=list)
    revealed: List[bool] = field(default_factory=list)
    matched: List[bool] = field(default_factory=list)
    first_pick: Optional[int] = None
    second_pick: Optional[int] = None
    moves: int = 0
    pairs_found: int = 0
    game_over: bool = False
    cursor_pos: int = 0
    show_picks: bool = False
    show_timer: float = 0

    CARD_SYMBOLS = ["@", "#", "$", "%", "&", "*", "+", "="]

    def __post_init__(self):
        self.setup_game()

    def setup_game(self):
        """Setup the card grid."""
        # Create pairs
        num_pairs = (self.grid_size * self.grid_size) // 2
        symbols = self.CARD_SYMBOLS[:num_pairs]
        self.cards = symbols * 2
        random.shuffle(self.cards)
        self.revealed = [False] * len(self.cards)
        self.matched = [False] * len(self.cards)
        self.first_pick = None
        self.second_pick = None
        self.moves = 0
        self.pairs_found = 0
        self.game_over = False
        self.cursor_pos = 0

    def select_card(self) -> bool:
        """Select the card at cursor position."""
        if self.matched[self.cursor_pos] or self.revealed[self.cursor_pos]:
            return False

        if self.first_pick is None:
            self.first_pick = self.cursor_pos
            self.revealed[self.cursor_pos] = True
        elif self.second_pick is None and self.cursor_pos != self.first_pick:
            self.second_pick = self.cursor_pos
            self.revealed[self.cursor_pos] = True
            self.moves += 1
            self.show_picks = True
            self.show_timer = time.time()

        return True

    def update(self):
        """Update game state."""
        if self.show_picks and self.first_pick is not None and self.second_pick is not None:
            if time.time() - self.show_timer > 1.0:
                # Check for match
                if self.cards[self.first_pick] == self.cards[self.second_pick]:
                    self.matched[self.first_pick] = True
                    self.matched[self.second_pick] = True
                    self.pairs_found += 1
                else:
                    self.revealed[self.first_pick] = False
                    self.revealed[self.second_pick] = False

                self.first_pick = None
                self.second_pick = None
                self.show_picks = False

                # Check win
                if self.pairs_found >= len(self.cards) // 2:
                    self.game_over = True

    def move_cursor(self, direction: str):
        """Move cursor in grid."""
        row = self.cursor_pos // self.grid_size
        col = self.cursor_pos % self.grid_size

        if direction == "up" and row > 0:
            row -= 1
        elif direction == "down" and row < self.grid_size - 1:
            row += 1
        elif direction == "left" and col > 0:
            col -= 1
        elif direction == "right" and col < self.grid_size - 1:
            col += 1

        self.cursor_pos = row * self.grid_size + col

    def render(self) -> List[str]:
        """Render game state."""
        lines = []
        lines.append(f"  MEMORY MATCH!  Pairs: {self.pairs_found}/{len(self.cards)//2}  Moves: {self.moves}")
        lines.append("")

        for row in range(self.grid_size):
            row_str = "    "
            for col in range(self.grid_size):
                idx = row * self.grid_size + col

                if self.matched[idx]:
                    card = "  "  # Matched cards disappear
                elif self.revealed[idx]:
                    card = f" {self.cards[idx]}"
                else:
                    card = " ?"

                # Add cursor indicator
                if idx == self.cursor_pos:
                    card = f"[{card.strip()}]"
                else:
                    card = f" {card} "

                row_str += card
            lines.append(row_str)

        lines.append("")
        lines.append("  [Arrows] Move  [SPACE/ENTER] Select  [Q] Quit")

        if self.game_over:
            lines.append("")
            lines.append(f"  YOU WIN! Completed in {self.moves} moves!")

        return lines


@dataclass
class DuckRaceGame:
    """
    Duck Race - Mash keys to race your duck!
    Compete against AI ducks in a waddle race.
    """
    track_length: int = 30
    player_pos: float = 0
    ai_positions: List[float] = field(default_factory=list)
    ai_speeds: List[float] = field(default_factory=list)
    player_stamina: float = 100
    game_over: bool = False
    winner: Optional[str] = None
    race_time: float = 0
    mashes: int = 0

    AI_NAMES = ["Quackers", "Waddles", "Feathers", "Bread Boy", "Splash"]

    def __post_init__(self):
        self.setup_race()

    def setup_race(self):
        """Setup the race."""
        num_ai = 3
        self.ai_positions = [0.0] * num_ai
        self.ai_speeds = [random.uniform(0.3, 0.7) for _ in range(num_ai)]
        self.player_pos = 0
        self.player_stamina = 100
        self.game_over = False
        self.winner = None
        self.race_time = 0
        self.mashes = 0

    def mash(self):
        """Player mashes key to move forward."""
        if self.game_over or self.player_stamina <= 0:
            return

        self.mashes += 1
        speed = 0.8 if self.player_stamina > 50 else 0.4
        self.player_pos += speed
        self.player_stamina -= 2

    def update(self, delta_time: float):
        """Update race state."""
        if self.game_over:
            return

        self.race_time += delta_time

        # Recover stamina slowly
        self.player_stamina = min(100, self.player_stamina + delta_time * 5)

        # Move AI ducks
        for i in range(len(self.ai_positions)):
            # AI has slight speed variation
            speed = self.ai_speeds[i] + random.uniform(-0.1, 0.1)
            self.ai_positions[i] += speed * delta_time * 10

        # Check for winner
        if self.player_pos >= self.track_length:
            self.game_over = True
            self.winner = "You"
        else:
            for i, pos in enumerate(self.ai_positions):
                if pos >= self.track_length:
                    self.game_over = True
                    self.winner = self.AI_NAMES[i]
                    break

    def render(self) -> List[str]:
        """Render race state."""
        lines = []
        lines.append(f"  DUCK RACE!  Time: {self.race_time:.1f}s  Stamina: {int(self.player_stamina)}%")
        lines.append("")

        # Draw track for player
        track = ["-"] * self.track_length
        player_idx = min(int(self.player_pos), self.track_length - 1)
        track[player_idx] = ">"
        lines.append(f"  You:      |{''.join(track)}| FINISH")

        # Draw tracks for AI
        for i, pos in enumerate(self.ai_positions):
            track = ["-"] * self.track_length
            ai_idx = min(int(pos), self.track_length - 1)
            track[ai_idx] = "@"
            name = self.AI_NAMES[i][:8].ljust(8)
            lines.append(f"  {name}  |{''.join(track)}|")

        lines.append("")
        lines.append("  [SPACE] Mash to waddle faster!")
        lines.append("  [Q] Quit race")

        if self.game_over:
            lines.append("")
            if self.winner == "You":
                lines.append(f"  YOU WIN! Time: {self.race_time:.1f}s  Mashes: {self.mashes}")
            else:
                lines.append(f"  {self.winner} wins! Better luck next time!")

        return lines


class MiniGameSystem:
    """Manages mini-games and rewards."""

    def __init__(self):
        self.high_scores: Dict[str, int] = {
            "bread_catch": 0,
            "bug_chase": 0,
            "memory_match": 999,  # Lower is better for memory
            "duck_race": 999,  # Lower time is better
        }
        self.games_played: Dict[str, int] = {
            "bread_catch": 0,
            "bug_chase": 0,
            "memory_match": 0,
            "duck_race": 0,
        }
        self.total_coins_earned: int = 0
        self.current_game: Optional[str] = None
        self.cooldowns: Dict[str, float] = {}
        self.cooldown_duration: float = 60.0  # 1 minute between games

    def can_play(self, game_type: str) -> Tuple[bool, str]:
        """Check if a game can be played (cooldown check)."""
        if game_type in self.cooldowns:
            elapsed = time.time() - self.cooldowns[game_type]
            if elapsed < self.cooldown_duration:
                remaining = int(self.cooldown_duration - elapsed)
                return False, f"Wait {remaining}s before playing again!"
        return True, ""

    def start_game(self, game_type: str):
        """Start a mini-game."""
        self.current_game = game_type
        self.cooldowns[game_type] = time.time()

    def finish_game(self, game_type: str, score: int, is_time_based: bool = False) -> MiniGameResult:
        """Finish a game and calculate rewards."""
        self.games_played[game_type] = self.games_played.get(game_type, 0) + 1

        # Check high score
        current_high = self.high_scores.get(game_type, 0)
        if is_time_based:
            # Lower is better for time-based games
            is_high_score = score < current_high or current_high == 0
            if is_high_score:
                self.high_scores[game_type] = score
        else:
            is_high_score = score > current_high
            if is_high_score:
                self.high_scores[game_type] = score

        # Calculate rewards based on score
        coins = self._calculate_coins(game_type, score)
        xp = self._calculate_xp(game_type, score)
        items = self._calculate_items(game_type, score)

        self.total_coins_earned += coins

        # Build result message
        if is_high_score:
            message = f"NEW HIGH SCORE! {score}"
        else:
            message = f"Score: {score}"

        return MiniGameResult(
            game_type=MiniGameType(game_type),
            score=score,
            high_score=is_high_score,
            coins_earned=coins,
            xp_earned=xp,
            items_earned=items,
            message=message
        )

    def _calculate_coins(self, game_type: str, score: int) -> int:
        """Calculate coins earned from score."""
        if game_type == "bread_catch":
            return score // 5
        elif game_type == "bug_chase":
            return score // 10
        elif game_type == "memory_match":
            # Fewer moves = more coins (16 is perfect for 4x4)
            return max(10, 100 - score * 3)
        elif game_type == "duck_race":
            # Faster time = more coins
            return max(10, 100 - int(score * 2))
        return 10

    def _calculate_xp(self, game_type: str, score: int) -> int:
        """Calculate XP earned from score."""
        base_xp = 10
        if game_type == "bread_catch":
            return base_xp + score // 20
        elif game_type == "bug_chase":
            return base_xp + score // 25
        elif game_type == "memory_match":
            return base_xp + max(0, 20 - score)
        elif game_type == "duck_race":
            return base_xp + max(0, 30 - int(score))
        return base_xp

    def _calculate_items(self, game_type: str, score: int) -> List[str]:
        """Calculate item drops from score."""
        items = []

        # Chance for rare items on high scores
        if game_type == "bread_catch" and score >= 200:
            if random.random() < 0.3:
                items.append("golden_crumb")
        elif game_type == "bug_chase" and score >= 500:
            if random.random() < 0.2:
                items.append("rare_bug_jar")
        elif game_type == "memory_match" and score <= 20:
            if random.random() < 0.25:
                items.append("memory_trophy")
        elif game_type == "duck_race" and score <= 15:
            if random.random() < 0.2:
                items.append("racing_medal")

        return items

    def get_available_games(self) -> List[Dict]:
        """Get list of available mini-games with status."""
        games = [
            {
                "id": "bread_catch",
                "name": "Bread Catch",
                "description": "Catch falling bread crumbs!",
                "high_score": self.high_scores.get("bread_catch", 0),
                "times_played": self.games_played.get("bread_catch", 0),
            },
            {
                "id": "bug_chase",
                "name": "Bug Chase",
                "description": "Quick reactions to catch bugs!",
                "high_score": self.high_scores.get("bug_chase", 0),
                "times_played": self.games_played.get("bug_chase", 0),
            },
            {
                "id": "memory_match",
                "name": "Memory Match",
                "description": "Find matching pairs!",
                "high_score": self.high_scores.get("memory_match", 999),
                "times_played": self.games_played.get("memory_match", 0),
            },
            {
                "id": "duck_race",
                "name": "Duck Race",
                "description": "Mash to win the race!",
                "high_score": self.high_scores.get("duck_race", 999),
                "times_played": self.games_played.get("duck_race", 0),
            },
        ]

        # Add cooldown status
        for game in games:
            can_play, msg = self.can_play(game["id"])
            game["can_play"] = can_play
            game["cooldown_msg"] = msg

        return games

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "high_scores": self.high_scores,
            "games_played": self.games_played,
            "total_coins_earned": self.total_coins_earned,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MiniGameSystem":
        """Deserialize from dictionary."""
        system = cls()
        system.high_scores = data.get("high_scores", system.high_scores)
        system.games_played = data.get("games_played", system.games_played)
        system.total_coins_earned = data.get("total_coins_earned", 0)
        return system


# Global instance
minigames = MiniGameSystem()
