# Cheese the Duck
### A Terminal Virtual Pet Game

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Version](https://img.shields.io/badge/version-2.0.0-green.svg)

---

## About

**Cheese the Duck** is a sprawling terminal-based virtual pet game where you raise a duck who has *opinions*. Inspired by classic Tamagotchi pets and the unsettling candor of Seaman, this game combines nostalgic pet-raising gameplay with AI-powered conversations, a deep personality system, and a world that's far bigger than it has any right to be.

Cheese isn't just a collection of stats — he has moods, personality traits, trust issues, a diary, and a complicated relationship with bread. He notices your habits, remembers your conversations, and will absolutely comment if you're late for his morning feed.

---

## 🚀 Quick Install

### 🪟 Windows

Open **PowerShell as Administrator** and run:

```powershell
cd $env:TEMP; Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Joshspeakman/cheese-the-duck/main/install_windows.ps1" -OutFile "install.ps1"; powershell -ExecutionPolicy Bypass -File install.ps1
```

**Alternative:** Download from [Releases](https://github.com/Joshspeakman/cheese-the-duck/releases) and run `install_windows.ps1` → Right-click → "Run with PowerShell"

This will:
- ✅ Download and install Python if needed
- ✅ Install all dependencies automatically
- ✅ Create Desktop and Start Menu shortcuts
- ✅ Download the AI model

After install, double-click **"Cheese the Duck"** on your Desktop!

---

### 🐧 Debian / Ubuntu (One Command)

```bash
curl -fsSL https://raw.githubusercontent.com/Joshspeakman/cheese-the-duck/main/install_linux.sh | bash
```

Or build and install a .deb package:

```bash
curl -fsSL https://raw.githubusercontent.com/Joshspeakman/cheese-the-duck/main/build_deb.sh | bash
sudo dpkg -i cheese-the-duck_*.deb
```

After install, run: `cheese-the-duck`

---

### 🏗️ Arch Linux (Full Commands)

```bash
# Install dependencies
sudo pacman -S python python-pip python-virtualenv sdl2 sdl2_mixer sdl2_image imagemagick

# Clone repository
git clone https://github.com/Joshspeakman/cheese-the-duck.git
cd cheese-the-duck

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Run the game
python main.py
```

**Create a launcher script:**

```bash
# Create launcher
mkdir -p ~/.local/bin
cat > ~/.local/bin/cheese-the-duck << 'EOF'
#!/bin/bash
cd ~/cheese-the-duck
source .venv/bin/activate
python main.py
EOF
chmod +x ~/.local/bin/cheese-the-duck

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

Now run: `cheese-the-duck`

---

### 🍎 macOS

```bash
# Install Python via Homebrew
brew install python

# Clone and install
git clone https://github.com/Joshspeakman/cheese-the-duck.git
cd cheese-the-duck
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run
python3 main.py
```

---

## 📦 Portable Windows Package (No Install)

Download the pre-built portable package from [Releases](https://github.com/Joshspeakman/cheese-the-duck/releases):

1. Download `CheeseTheDuck-Windows-Portable.zip`
2. Extract anywhere
3. Run `CheeseTheDuck.bat`

No Python installation required!

---

## 🎮 Features

### Care & Consequences
Monitor your duck's needs — hunger, energy, fun, cleanliness, and social. Neglect has real consequences: Cheese will complain, get sick, give you the cold shoulder, or eventually hide entirely. Trust takes time to rebuild.

### Growth, Personality & Mood
Your duck grows through life stages from egg to elder. Each duck develops unique personality traits across multiple dimensions that shift over time based on how you treat them. Mood isn't just a number — it changes how Cheese talks, what he's willing to do, and whether he'll even acknowledge your existence.

### Ritual Detection
Play at the same time every day? Cheese notices. Feed him at 8am like clockwork? He'll comment on your punctuality. Show up late? He'll comment on that too. Not that he was waiting.

### Autonomous AI Behavior
Your duck has agency — he wanders, explores, interacts with items, and makes decisions based on his needs, personality, and current grudges. A background LLM generates unique commentary when available, with extensive handcrafted fallbacks when it's not.

### Deep Conversation System
Talk to Cheese and he'll remember what you said. The game tracks conversation topics, extracts facts about you, builds a player model from your behavior, and lets Cheese bring things up later. He keeps a diary. He has opinions about your visit patterns. He will reference things you said weeks ago.

### Visiting Friends
Duck friends with distinct personalities visit regularly. Each has their own dialogue style, weather opinions, and multi-turn conversations with Cheese. Friendships develop over time through shared experiences.

### World Exploration
Multiple biomes to explore, each with unique events, discoveries, and seasonal content. The world has its own weather, day/night cycle, and atmosphere that changes how everything feels.

### Crafting, Building & Collecting
Gather materials, craft tools and structures, and build out your duck's habitat. A substantial collection system with achievements, collectibles, and discoveries to track.

### Tricks & Training
Teach Cheese tricks across multiple categories — movement, sound, social, and special performances. Training takes time, failure is frequent, and mastery is hard-earned. Cheese's commentary on the process is... characteristically unenthusiastic.

### Mini-Games
Several mini-games including Bread Catch, Bug Chase, Memory Match, Duck Race, and Fishing — each with their own scoring and rewards.

### Streaming Radio
Listen to internet radio stations while you play:
- **Quack FM** — Lofi beats for staring at walls
- **The Pond** — Ambient nature sounds
- **Bread Crumbs** — 8-bit chiptune nostalgia
- **Feather & Bone** — Smooth jazz
- **HONK Radio** — Chaotic upbeat energy
- **Nook Radio** — Hourly music that changes with the time of day
- **DJ Duck Live** — Saturday nights 8pm–midnight with deadpan commentary

### Weather, Dreams & Events
Weather changes naturally and affects activities, moods, and visitor conversations. When Cheese sleeps, he dreams — adventures, nightmares, prophecies, and occasionally something about bread. Random and seasonal events keep things unpredictable.

### The Writing
Thousands of handcrafted dialogue lines across dozens of systems. Cheese has a specific voice — deadpan, sardonic, bread-obsessed, and occasionally vulnerable when he thinks you're not looking. Visitors each have their own personality and speech patterns. The game has more dialogue than most people will ever see.

---

## 🎹 Controls

| Key | Action |
|-----|--------|
| **TAB** | Open Main Menu |
| **F / 1** | Feed |
| **P / 2** | Play |
| **L / 3** | Clean |
| **D / 4** | Pet |
| **Z / 5** | Sleep |
| **T** | Talk to duck |
| **E** | Explore |
| **C** | Crafting |
| **B** | Shop |
| **M / N** | Toggle music/sound |
| **H** | Help |
| **Q** | Save & Quit |

---

## 🤖 AI Conversations

The game includes a bundled **Llama 3.2** AI model for dynamic conversations. Installers download this automatically.

### Alternative: Use Ollama (Larger Models)

For better performance with larger models:

```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.2
ollama serve
```

The game uses Ollama if available, otherwise falls back to the bundled model.

---

## 🔧 Manual Installation (All Platforms)

```bash
# Clone
git clone https://github.com/Joshspeakman/cheese-the-duck.git
cd cheese-the-duck

# Create virtual environment
python3 -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip python3-venv python3-dev libsdl2-dev libsdl2-mixer-dev
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip python3-devel SDL2-devel SDL2_mixer-devel
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip sdl2 sdl2_mixer
```

---

## 💾 Save System

Progress auto-saves to `~/.cheese_the_duck/save.json`

Your duck continues living while you're away—offline time is calculated when you return.

---

## 🔄 Updates

The game includes a built-in update system:
1. A notification appears when updates are available
2. Access **Settings** from the main menu
3. Select **Check for Updates**

Or run the installer again to update.

---

## 📁 Project Structure

```
cheese-the-duck/
├── audio/      # Sound engine, streaming radio, ambient system
├── core/       # Game loop, saves, progression, consequences, prestige
├── dialogue/   # Conversations, memory, personality dialogue, diary, questions
├── duck/       # Entity logic, mood, personality, tricks, cosmetics
├── ui/         # Terminal rendering, ASCII art, animations, menus
├── world/      # Exploration, crafting, events, dreams, weather, achievements
├── config.py   # Settings & tuning
└── main.py     # Entry point
```

---

## 🤝 Contributing

Pull requests welcome! Fork → Branch → Commit → PR

---

## 📄 License

MIT License - see LICENSE file.

---

## 🙏 Acknowledgments

- Inspired by Tamagotchi, Animal Crossing, and [Seaman](https://en.wikipedia.org/wiki/Seaman_(video_game))
- Built with [blessed](https://github.com/jquast/blessed) for terminal UI
- Audio powered by [pygame](https://www.pygame.org/)
- LLM support via [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) and [Ollama](https://ollama.ai/)

### Radio Streaming

The in-game radio streams music from these services:

- **[SomaFM](https://somafm.com/)** - Listener-supported, commercial-free internet radio
- **[laut.fm](https://laut.fm/)** - German internet radio platform
- **[I Love Radio](https://www.iloveradio.de/)** - German radio network
- **[nook.camp](https://nook.camp/)** - Animal Crossing hourly music (via [nook-desktop](https://github.com/OpenSauce04/nook-desktop))

All streams are used in accordance with their respective terms of service for non-commercial, personal use. This game is not affiliated with these services.

---

```
         __|   |__
        /   \ /   \
       (___) (___)

    Have fun raising Cheese!
```
