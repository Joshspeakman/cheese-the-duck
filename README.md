# 🦆 Cheese the Duck

A feature-rich terminal-based virtual pet game inspired by Tamagotchi. Raise and care for Cheese, a derpy but adorable duck with unique personality traits, dynamic needs, and AI-powered behavior!

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)

## ✨ Features

### 🐣 Dynamic Duck Care System
- **Five Core Needs**: Monitor and fulfill hunger, energy, fun, cleanliness, and social needs
- **Color-Coded Stats**: Visual progress bars with percentages - green (70%+), yellow (40-69%), red (below 40%)
- **Mood System**: Duck's mood changes based on how well their needs are met (ecstatic, happy, content, grumpy, sad, miserable)
- **Growth Stages**: Watch your duck grow from egg → duckling → teen → adult → elder
- **Unique Personality**: Each duck has personality traits that affect their behavior:
  - Clever ↔ Derpy
  - Brave ↔ Timid
  - Active ↔ Lazy
  - Social ↔ Shy
  - Neat ↔ Messy

### 🤖 Autonomous AI Behavior
- Ducks perform autonomous actions based on their needs and personality
- **Structure-Aware AI**: Duck interacts with built structures (naps in nests, hides in shelters, uses bird baths)
- Derpy ducks make more unpredictable and silly choices
- AI adapts behavior based on current needs, mood, and environment

### 💬 Interactive Conversations
- **LLM Integration**: Optional Ollama integration for dynamic, AI-powered conversations
- **Memory System**: Duck remembers past conversations and interactions
- **Fallback Responses**: Works without LLM with pre-written personality-based responses
- **Duck Diary**: Automatic storytelling that creates a narrative of your duck's life
- Supports models: llama3.2, llama3.1, mistral, phi3, gemma2, qwen2

### 🗺️ Exploration System
- **Multiple Biomes**: Explore Pond, Forest, Meadow, Riverside, Garden, Mountains, and Beach
- **Resource Gathering**: Collect materials like twigs, leaves, pebbles, shells, and more
- **Travel Animations**: Watch your duck waddle to new locations
- **Discovery System**: Find rare resources and unlock new areas
- **Gathering Skill**: Level up your exploration abilities

### ⚒️ Crafting & Building
- **Material Collection**: Gather 40+ unique materials from different biomes
- **Crafting Recipes**: Combine materials to create tools, decorations, and special items
- **Building System**: Construct nests, houses, workshops, and other structures
- **Structure Benefits**: Built structures provide bonuses and shelter
- **Multi-Stage Construction**: Watch buildings progress through construction phases

### 🎮 Item Interactions
- **45+ Interactive Items**: Play with balls, swim in pools, bounce on trampolines, and more
- **Custom Animations**: ASCII art animations show your duck interacting with objects
- **Edge Cases**: Different responses based on duck's state (tired, hungry, happy)
- **Natural Commands**: Type "play with ball" or "swim in pool" in Talk mode
- **Use Menu**: Press [U] to see all interactable items you own

### 🎯 Progression & Rewards
- **Achievement System**: 50+ achievements including secret discoveries
- **Daily Rewards**: Login daily to earn rewards and maintain streaks
- **Goal System**: Complete daily and weekly goals for bonus rewards
- **Collectibles**: Discover and collect rare items throughout gameplay
- **Level System**: Gain XP and level up through interactions
- **Interaction Cooldowns**: Prevents spam-clicking with themed cooldown messages

### 🏠 Habitat System
- **255+ Shop Items**: Decorations, toys, furniture, water features, plants, and cosmetics
- **Decoratable Playfield**: Place items around your duck's habitat
- **Cosmetic System**: Dress up your duck with hats, glasses, bow ties, and more
- **Dynamic Atmosphere**: Weather effects (rain, snow, storms, fog, rainbows)
- **Duck-Item Reactions**: Duck autonomously interacts with nearby items

### 🎪 Dynamic Events
- Random events occur during gameplay (visitors, weather changes, special occasions)
- **Visitor System**: Meet other ducks and characters
- Timed events with unique rewards
- Event outcomes affected by duck's personality and stats

### 🎮 Mini-Games
- **Bread Catch**: Catch falling bread with your duck
- **Bug Chase**: Chase and catch bugs for rewards
- **Memory Match**: Test your memory with card matching
- **Duck Race**: Race against other ducks

### 💤 Dream System
- Ducks dream while sleeping with unique dream sequences
- Dreams influenced by recent activities and mood
- Types: Adventure, Flying, Food, Friends, Memories, Silly, and more
- Prophetic dreams may hint at future events

### 🎨 Rich Terminal UI
- Colorful ASCII art duck animations
- **Animated Sprites**: Duck animates during interactions (sleeping, eating, playing, cleaning, petting)
- **Traveling Animations**: Duck waddles between areas
- **Building Animations**: Watch structures being constructed
- **Kaomoji-style Close-ups**: Expressive emotion displays
- **Animated Celebrations**: Level-up and achievement animations
- Real-time status displays with color-coded progress bars

### 🔊 Audio System
- **Background Music**: Looping ambient music (pygame-based)
- **Duck Quacks**: Realistic WAV sound effects
- **Level-Up Sounds**: Special sound effects for achievements
- **Syllable-Based Speech**: Duck quacks once per syllable when responding!
- Volume controls for music and sound effects independently

### 💾 Save System
- Automatic save functionality
- Offline progression - your duck continues living while you're away
- Data saved to `~/.cheese_the_duck/save.json`

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Terminal with color support

### Quick Start

1. **Clone the repository**:
```bash
git clone https://github.com/Joshspeakman/cheese-the-duck.git
cd cheese-the-duck
```

2. **Create virtual environment** (recommended):
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or: .venv\Scripts\activate  # Windows
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the game**:
```bash
python main.py
```

Or use the provided shell script:
```bash
chmod +x run_game.sh
./run_game.sh
```

### Optional: LLM Integration

For enhanced conversations, install [Ollama](https://ollama.ai/) and pull a supported model:

```bash
# Install Ollama (see https://ollama.ai for installation instructions)

# Pull a model (recommended: llama3.2)
ollama pull llama3.2

# Start Ollama server
ollama serve
```

The game will automatically detect and use Ollama if available.

## 🎮 Controls

### Duck Care
| Key | Action |
|-----|--------|
| F / 1 | Feed the duck |
| P / 2 | Play with duck |
| L / 3 | Clean the duck |
| D / 4 | Pet the duck |
| Z / 5 | Let duck sleep |

### Social & Info
| Key | Action |
|-----|--------|
| T | Talk to duck |
| S | View detailed stats |
| I | Open inventory |
| G | View goals |

### World & Building
| Key | Action |
|-----|--------|
| E | Explore current area |
| A | Travel to other areas |
| C | Open crafting menu |
| R | Open building menu |
| B | Open shop |
| U | Use/interact with items |

### Fun
| Key | Action |
|-----|--------|
| J | Mini-games menu |
| K | Random duck fact |

### Audio
| Key | Action |
|-----|--------|
| M | Toggle sound on/off |
| N | Toggle music on/off |
| + | Volume up |
| - | Volume down |

### Game
| Key | Action |
|-----|--------|
| H | Show help |
| Q | Save & quit |
| X | Reset game |

### Pro Tip
Type commands like "play with ball", "swim in pool", or "sit on throne" in Talk mode [T]!

## 📁 Project Structure

```
cheese_the_duck/
├── audio/                  # Sound effects system
├── core/                   # Core game systems
│   ├── clock.py           # Game timing
│   ├── game.py            # Main game loop
│   ├── persistence.py     # Save/load system
│   └── progression.py     # XP and leveling
├── dialogue/               # Conversation systems
│   ├── conversation.py    # Dialogue management
│   ├── diary.py           # Duck diary/journal
│   ├── llm_chat.py        # LLM integration
│   └── memory.py          # Duck memory system
├── duck/                   # Duck entity logic
│   ├── behavior_ai.py     # Autonomous behavior
│   ├── cosmetics.py       # Cosmetic rendering
│   ├── duck.py            # Duck entity
│   ├── mood.py            # Mood calculations
│   ├── needs.py           # Need tracking
│   └── personality.py     # Personality system
├── ui/                     # User interface
│   ├── animations.py      # Animation controller
│   ├── ascii_art.py       # Duck ASCII art & sprites
│   ├── habitat_art.py     # Habitat/structure art
│   ├── habitat_icons.py   # Item icons
│   ├── input_handler.py   # Input processing
│   └── renderer.py        # Display rendering
├── world/                  # Game world systems
│   ├── achievements.py    # Achievement tracking
│   ├── atmosphere.py      # Weather & time effects
│   ├── building.py        # Structure building
│   ├── crafting.py        # Item crafting
│   ├── dreams.py          # Dream sequences
│   ├── events.py          # Random events
│   ├── exploration.py     # Biome exploration
│   ├── facts.py           # Duck facts/trivia
│   ├── goals.py           # Daily/weekly goals
│   ├── habitat.py         # Habitat item placement
│   ├── home.py            # Home customization
│   ├── item_interactions.py # Item interaction system
│   ├── items.py           # Inventory system
│   ├── materials.py       # Crafting materials
│   ├── minigames.py       # Mini-game system
│   └── shop.py            # In-game shop (255+ items)
├── config.py              # Game configuration
├── main.py                # Entry point
└── requirements.txt       # Python dependencies
```

## 🔧 Configuration

Edit `config.py` to customize:
- Need decay rates
- Time multipliers (for testing)
- Personality defaults
- Growth stage durations
- AI behavior parameters
- UI colors

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add feature-name"`
6. Push: `git push origin feature-name`
7. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by classic Tamagotchi virtual pets
- Built with [blessed](https://github.com/jquast/blessed) for terminal UI
- Audio powered by [pygame](https://www.pygame.org/)
- Optional LLM support via [Ollama](https://ollama.ai/)

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Have fun raising Cheese! 🦆✨**
