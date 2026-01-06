# Installation

```text
    +-----------------------------------------+
    |         INSTALLATION GUIDE              |
    +-----------------------------------------+
```

## Requirements

- Python 3.8 or higher
- Terminal with color support
- Linux, macOS, or Windows (WSL recommended)

## Quick Install

### 1. Clone the Repository

```bash
git clone https://github.com/Joshspeakman/cheese-the-duck.git
cd cheese-the-duck
```

### 2. Install Dependencies

**Linux/macOS:**
```bash
chmod +x install_linux.sh
./install_linux.sh
```

**Windows:**
```batch
install_windows.bat
```

**Manual:**
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

Or use the run script:

```bash
./run_game.sh
```

## Optional: AI Dialogue

The game includes optional AI-powered dialogue using a local LLM. To enable:

### Download the Model

```bash
python download_model.py
```

This downloads a small (~2GB) language model that runs locally on your computer. No internet required during gameplay!

```text
+--------------------------------------------------+
|  NOTE: The game works perfectly without the      |
|  AI model! It will use pre-written dialogue      |
|  if no model is detected.                        |
+--------------------------------------------------+
```

## Troubleshooting

### Game looks weird

Make sure your terminal:
- Supports at least 80x24 characters
- Has color support enabled
- Uses a monospace font

### No sound

Sound is optional. Install audio dependencies:

```bash
# Linux
sudo apt install mpg123 aplay

# macOS  
brew install mpg123
```

---

```text
            .---.       
           / ^   \   Ready to play!
          |   __  |     
           \  \_) |>    
            `---|--'    
              _|  \     
             (_)  (_)   
```

[[Home]] | [[Getting Started]] | [[Controls]]
