# 🦆 Cheese the Duck

A feature-rich terminal-based virtual pet game inspired by Tamagotchi. Raise and care for Cheese, a derpy but adorable duck with unique personality traits, dynamic needs, and AI-powered behavior!

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## ✨ Features

### 🐣 Dynamic Duck Care System
- **Multiple Needs**: Monitor and fulfill hunger, energy, fun, cleanliness, and social needs
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
- Derpy ducks make more unpredictable and silly choices
- AI adapts behavior based on current needs and mood state

### 💬 Interactive Conversations
- **LLM Integration**: Optional Ollama integration for dynamic, AI-powered conversations
- **Memory System**: Duck remembers past conversations and interactions
- **Fallback Responses**: Works without LLM with pre-written personality-based responses
- Supports models: llama3.2, llama3.1, mistral, phi3, gemma2, qwen2

### 🎯 Progression & Rewards
- **Achievement System**: Unlock achievements for interactions, growth milestones, and secret discoveries
- **Daily Rewards**: Login daily to earn rewards and maintain streaks
- **Goal System**: Complete daily and weekly goals for bonus rewards
- **Collectibles**: Discover and collect rare items throughout gameplay
- **Level System**: Gain XP and level up through interactions

### 🏠 Home Customization
- Unlock and customize your duck's home environment
- Purchase decorations and furniture
- Upgrade home features as you progress

### 🎪 Dynamic Events
- Random events occur during gameplay (visitors, weather changes, special occasions)
- Timed events with unique rewards
- Event outcomes affected by duck's personality and stats

### 🎨 Rich Terminal UI
- Colorful ASCII art duck animations
- Real-time status displays for all needs
- Smooth animations and visual feedback
- Sound effects support (optional)

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
git clone https://github.com/yourusername/cheese-the-duck.git
cd cheese-the-duck
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the game**:
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

## 🎮 How to Play

### Controls
- **Arrow Keys**: Navigate menus
- **Enter**: Select option
- **ESC/Q**: Go back / Quit
- **Number Keys**: Quick actions (1-5)

### Basic Actions
1. **Feed**: Satisfy hunger needs with various food items
2. **Play**: Increase fun and social interaction
3. **Clean**: Keep your duck tidy and happy
4. **Pet**: Show affection and boost mood
5. **Sleep**: Restore energy (takes time)
6. **Talk**: Have conversations with your duck

### Tips
- Monitor all needs - low needs lead to unhappy ducks
- Check daily for login rewards and new goals
- Experiment with different items from your inventory
- Complete achievements to unlock special rewards
- Pay attention to your duck's personality - it affects their behavior
- Keep your duck happy for faster XP gain

## 📁 Project Structure

```
cheese_the_duck/
├── audio/              # Sound effects system
├── core/               # Core game systems
│   ├── clock.py        # Game timing
│   ├── game.py         # Main game loop
│   ├── persistence.py  # Save/load system
│   └── progression.py  # XP and leveling
├── dialogue/           # Conversation systems
│   ├── conversation.py # Dialogue management
│   ├── llm_chat.py     # LLM integration
│   └── memory.py       # Duck memory system
├── duck/               # Duck entity logic
│   ├── behavior_ai.py  # Autonomous behavior
│   ├── duck.py         # Duck entity
│   ├── mood.py         # Mood calculations
│   ├── needs.py        # Need tracking
│   └── personality.py  # Personality system
├── ui/                 # User interface
│   ├── animations.py   # Animation controller
│   ├── ascii_art.py    # Duck ASCII art
│   ├── input_handler.py# Input processing
│   └── renderer.py     # Display rendering
├── world/              # Game world systems
│   ├── achievements.py # Achievement tracking
│   ├── events.py       # Random events
│   ├── goals.py        # Daily/weekly goals
│   ├── home.py         # Home customization
│   └── items.py        # Inventory system
├── config.py           # Game configuration
├── main.py             # Entry point
└── requirements.txt    # Python dependencies
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
- Optional LLM support via [Ollama](https://ollama.ai/)

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Have fun raising Cheese! 🦆✨**
