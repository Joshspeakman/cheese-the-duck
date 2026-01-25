# Cheese the Duck
### A Terminal Virtual Pet Game

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Version](https://img.shields.io/badge/version-1.6.0-green.svg)

---

## About

**Cheese the Duck** is a feature-rich terminal-based virtual pet game where you raise and care for a duck with a personality all its own. Inspired by classic Tamagotchi pets, this game combines nostalgic pet-raising gameplay with modern features like AI-powered behavior, dynamic conversations, and a surprisingly deep world to explore.

Your duck isn't just a collection of stats—it has moods, personality traits, and autonomous behaviors that make each playthrough unique.

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

### Care & Survival
Monitor five essential needs: **Hunger**, **Energy**, **Fun**, **Cleanliness**, and **Social**. Each affects your duck's mood.

### Growth & Personality
Your duck grows through life stages: Egg → Duckling → Teen → Adult → Elder. Each duck has unique personality traits that affect behavior.

### Autonomous AI Behavior
Your duck has agency—it wanders, explores, interacts with items, and makes decisions based on its needs and personality.

### Dynamic Conversations
Talk to your duck! With **LLM integration**, conversations are truly dynamic—your duck remembers what you've talked about.

### World Exploration
Seven distinct biomes to explore: Pond, Forest, Meadow, Riverside, Garden, Mountains, Beach.

### Crafting & Building
Gather 40+ materials. Craft tools and structures. Build your duck's perfect home.

### Mini-Games
- Bread Catch
- Bug Chase
- Memory Match
- Duck Race
- Fishing

### Streaming Radio
Listen to duck-themed internet radio stations while you play:
- **Quack FM** - Lofi beats for staring at walls
- **The Pond** - Ambient nature sounds
- **Bread Crumbs** - 8-bit chiptune nostalgia
- **Feather & Bone** - Smooth jazz
- **HONK Radio** - Chaotic upbeat energy
- **Nook Radio** - Hourly music that changes with the time of day
- **DJ Duck Live** - Saturday nights 8pm-midnight with deadpan commentary

### Dynamic Weather & Dreams
Weather changes naturally. When your duck sleeps, it dreams based on recent activities.

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
├── audio/      # Sound engine
├── core/       # Game loop, saves
├── dialogue/   # Conversations, memory
├── duck/       # Entity logic, AI
├── ui/         # Rendering, ASCII art
├── world/      # Exploration, crafting, events
├── config.py   # Settings
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

- Inspired by classic Tamagotchi virtual pets
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
