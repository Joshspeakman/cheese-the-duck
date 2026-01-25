# Installation

```text
    +-----------------------------------------+
    |         INSTALLATION GUIDE              |
    +-----------------------------------------+
```

## Requirements

- Python 3.8 or higher
- Terminal with color support
- Linux, macOS, or Windows

---

## 🪟 Windows

### PowerShell Install (Run as Administrator)

```powershell
cd $env:TEMP; Invoke-WebRequest -Uri "https://raw.githubusercontent.com/Joshspeakman/cheese-the-duck/main/install_windows.ps1" -OutFile "install.ps1"; powershell -ExecutionPolicy Bypass -File install.ps1
```

**Alternative:** Download `install_windows.ps1` from the repo, right-click → "Run with PowerShell"

### Portable Package (No Install)

1. Download `CheeseTheDuck-Windows-Portable.zip` from [Releases](https://github.com/Joshspeakman/cheese-the-duck/releases)
2. Extract anywhere
3. Run `CheeseTheDuck.bat`

---

## 🐧 Debian / Ubuntu

### One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/Joshspeakman/cheese-the-duck/main/install_linux.sh | bash
```

### Build .deb Package

```bash
curl -fsSL https://raw.githubusercontent.com/Joshspeakman/cheese-the-duck/main/build_deb.sh | bash
sudo dpkg -i cheese-the-duck_*.deb
```

After install: `cheese-the-duck`

---

## 🏗️ Arch Linux

```bash
# Install dependencies
sudo pacman -S python python-pip python-virtualenv sdl2 sdl2_mixer sdl2_image imagemagick

# Clone and setup
git clone https://github.com/Joshspeakman/cheese-the-duck.git
cd cheese-the-duck
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run
python main.py
```

### Create Launcher

```bash
mkdir -p ~/.local/bin
cat > ~/.local/bin/cheese-the-duck << 'EOF'
#!/bin/bash
cd ~/cheese-the-duck
source .venv/bin/activate
python main.py
EOF
chmod +x ~/.local/bin/cheese-the-duck
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

---

## 🍎 macOS

```bash
brew install python
git clone https://github.com/Joshspeakman/cheese-the-duck.git
cd cheese-the-duck
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

---

## 🔧 Manual Installation

```bash
git clone https://github.com/Joshspeakman/cheese-the-duck.git
cd cheese-the-duck
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .\.venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
python main.py
```

---

## 🤖 Optional: AI Dialogue

The game includes a bundled AI model. Installers download this automatically.

### Manual Download

```bash
python download_model.py
```

### Use Ollama (Alternative)

```bash
ollama pull llama3.2
ollama serve
```

---

## Troubleshooting

### Game looks weird
- Terminal must be at least 80x24 characters
- Use a monospace font
- Enable color support

### No sound
Sound is optional. Install pygame:
```bash
pip install pygame
```

---

```text
            .---.       
           / ^   \   Ready to play!
          |   __  |     
           \____/      
```
