#!/bin/bash
# ============================================================
# Cheese the Duck - Linux Installer
# ============================================================
# This script installs Cheese the Duck on Linux systems.
# 
# Usage:
#   chmod +x install_linux.sh
#   ./install_linux.sh
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$HOME/.local/share/CheeseTheDuck"
BIN_LINK="$HOME/.local/bin/cheese-the-duck"
DESKTOP_FILE="$HOME/.local/share/applications/cheese-the-duck.desktop"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║           🦆 Cheese the Duck - Linux Installer              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    echo "  ✓ Python $PYTHON_VERSION found"
    
    # Check if version is 3.8+
    MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
        echo "  ✗ Error: Python 3.8+ required (found $PYTHON_VERSION)"
        exit 1
    fi
else
    echo "  ✗ Error: Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Create directories
echo ""
echo "Creating installation directory..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$HOME/.local/bin"
mkdir -p "$HOME/.local/share/applications"

# Copy files
echo "Copying game files..."
cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/"

# Remove installer scripts from installed location
rm -f "$INSTALL_DIR/install_linux.sh"
rm -f "$INSTALL_DIR/install_windows.bat"
rm -f "$INSTALL_DIR/build_installer.py"

# Create virtual environment
echo ""
echo "Setting up Python environment..."
cd "$INSTALL_DIR"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo "  ✓ Dependencies installed"

# Download AI model (optional)
echo ""
read -p "Download AI model for conversations? (~700MB) [y/N]: " download_model
if [[ "$download_model" =~ ^[Yy]$ ]]; then
    echo "Downloading AI model..."
    python download_model.py
fi

# Create launcher script
echo ""
echo "Creating launcher..."
cat > "$BIN_LINK" << 'EOF'
#!/bin/bash
cd "$HOME/.local/share/CheeseTheDuck"
if [ -f ".venv/bin/python" ]; then
    .venv/bin/python main.py "$@"
else
    python3 main.py "$@"
fi
EOF
chmod +x "$BIN_LINK"
echo "  ✓ Launcher created at $BIN_LINK"

# Create desktop entry
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=Cheese the Duck
Comment=A terminal-based virtual pet game
Exec=$BIN_LINK
Terminal=true
Type=Application
Categories=Game;
Icon=$INSTALL_DIR/assets/gameplay.png
EOF
echo "  ✓ Desktop entry created"

# Done
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                   ✅ Installation Complete!                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "To play Cheese the Duck:"
echo ""
echo "  Option 1: Run from terminal:"
echo "            cheese-the-duck"
echo ""
echo "  Option 2: Find 'Cheese the Duck' in your applications menu"
echo ""
echo "  Option 3: Run directly:"
echo "            cd $INSTALL_DIR && ./run_game.sh"
echo ""
echo "Installed to: $INSTALL_DIR"
echo ""
echo "To uninstall, run:"
echo "  rm -rf $INSTALL_DIR $BIN_LINK $DESKTOP_FILE"
echo ""
