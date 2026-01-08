#!/bin/bash
# ============================================================
# Cheese the Duck - Linux Installer
# ============================================================
# Installs all dependencies via apt, creates virtual environment,
# desktop shortcuts with icons, and proper launcher.
#
# Usage: chmod +x install_linux.sh && ./install_linux.sh
# Uninstall: ./install_linux.sh --uninstall
# ============================================================

set -e

# Configuration
APP_NAME="Cheese the Duck"
APP_ID="cheese-the-duck"
DEFAULT_INSTALL_DIR="$HOME/.local/share/CheeseTheDuck"
LAUNCHER_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_header() {
    echo ""
    echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║           🦆 Cheese the Duck - Linux Installer              ║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_step() {
    echo -e "  ${YELLOW}→${NC} $1"
}

print_success() {
    echo -e "  ${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "  ${RED}✗${NC} $1"
}

print_info() {
    echo -e "  ${BLUE}ℹ${NC} $1"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check and install system dependencies via apt
install_apt_dependencies() {
    print_step "Checking system dependencies..."
    
    local deps_needed=()
    
    # Check for Python 3.8+
    if ! command_exists python3; then
        deps_needed+=("python3")
    else
        local py_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        local py_major=$(echo "$py_version" | cut -d. -f1)
        local py_minor=$(echo "$py_version" | cut -d. -f2)
        if [ "$py_major" -lt 3 ] || { [ "$py_major" -eq 3 ] && [ "$py_minor" -lt 8 ]; }; then
            print_error "Python 3.8+ required, found $py_version"
            deps_needed+=("python3")
        fi
    fi
    
    # Check for pip
    if ! command_exists pip3 && ! python3 -m pip --version >/dev/null 2>&1; then
        deps_needed+=("python3-pip")
    fi
    
    # Check for venv
    if ! python3 -c "import venv" 2>/dev/null; then
        deps_needed+=("python3-venv")
    fi
    
    # Check for ImageMagick (for icon conversion)
    if ! command_exists convert; then
        deps_needed+=("imagemagick")
    fi
    
    # Check for SDL2 (for pygame)
    if ! ldconfig -p 2>/dev/null | grep -q libSDL2; then
        deps_needed+=("libsdl2-dev" "libsdl2-mixer-dev" "libsdl2-image-dev")
    fi
    
    # Install if needed
    if [ ${#deps_needed[@]} -gt 0 ]; then
        print_step "Installing required packages: ${deps_needed[*]}"
        
        if command_exists apt-get; then
            sudo apt-get update -qq
            sudo apt-get install -y -qq "${deps_needed[@]}"
            print_success "System dependencies installed"
        elif command_exists dnf; then
            # Fedora/RHEL equivalent packages
            local fedora_deps=()
            for dep in "${deps_needed[@]}"; do
                case "$dep" in
                    python3) fedora_deps+=("python3") ;;
                    python3-pip) fedora_deps+=("python3-pip") ;;
                    python3-venv) ;;  # Included with python3 on Fedora
                    imagemagick) fedora_deps+=("ImageMagick") ;;
                    libsdl2*) fedora_deps+=("SDL2-devel" "SDL2_mixer-devel" "SDL2_image-devel") ;;
                esac
            done
            if [ ${#fedora_deps[@]} -gt 0 ]; then
                sudo dnf install -y "${fedora_deps[@]}"
            fi
            print_success "System dependencies installed"
        elif command_exists pacman; then
            # Arch equivalent packages
            local arch_deps=()
            for dep in "${deps_needed[@]}"; do
                case "$dep" in
                    python3) arch_deps+=("python") ;;
                    python3-pip) arch_deps+=("python-pip") ;;
                    python3-venv) ;;  # Included with python on Arch
                    imagemagick) arch_deps+=("imagemagick") ;;
                    libsdl2*) arch_deps+=("sdl2" "sdl2_mixer" "sdl2_image") ;;
                esac
            done
            if [ ${#arch_deps[@]} -gt 0 ]; then
                sudo pacman -S --noconfirm "${arch_deps[@]}"
            fi
            print_success "System dependencies installed"
        else
            print_error "No supported package manager found. Please install manually:"
            for dep in "${deps_needed[@]}"; do
                echo "    - $dep"
            done
            exit 1
        fi
    else
        print_success "All system dependencies satisfied"
    fi
}

# Convert ICO to PNG for Linux icons
create_linux_icons() {
    print_step "Creating application icons..."
    
    local ico_file="$1/cheese.ico"
    
    if [ ! -f "$ico_file" ]; then
        print_info "Icon file not found, using default icon"
        return
    fi
    
    # Create icon directories
    mkdir -p "$ICON_DIR/16x16/apps"
    mkdir -p "$ICON_DIR/24x24/apps"
    mkdir -p "$ICON_DIR/32x32/apps"
    mkdir -p "$ICON_DIR/48x48/apps"
    mkdir -p "$ICON_DIR/64x64/apps"
    mkdir -p "$ICON_DIR/128x128/apps"
    mkdir -p "$ICON_DIR/256x256/apps"
    
    # Convert ICO to different sizes using ImageMagick
    # Use [8] which is the 512x512 PNG (highest quality) and scale DOWN for best results
    if command_exists convert; then
        convert "$ico_file[8]" -resize 16x16 "$ICON_DIR/16x16/apps/$APP_ID.png" 2>/dev/null || true
        convert "$ico_file[8]" -resize 24x24 "$ICON_DIR/24x24/apps/$APP_ID.png" 2>/dev/null || true
        convert "$ico_file[8]" -resize 32x32 "$ICON_DIR/32x32/apps/$APP_ID.png" 2>/dev/null || true
        convert "$ico_file[8]" -resize 48x48 "$ICON_DIR/48x48/apps/$APP_ID.png" 2>/dev/null || true
        convert "$ico_file[8]" -resize 64x64 "$ICON_DIR/64x64/apps/$APP_ID.png" 2>/dev/null || true
        convert "$ico_file[8]" -resize 128x128 "$ICON_DIR/128x128/apps/$APP_ID.png" 2>/dev/null || true
        convert "$ico_file[8]" -resize 256x256 "$ICON_DIR/256x256/apps/$APP_ID.png" 2>/dev/null || true
        
        # Update icon cache
        if command_exists gtk-update-icon-cache; then
            gtk-update-icon-cache -f -t "$ICON_DIR" 2>/dev/null || true
        fi
        
        print_success "Application icons created"
    else
        print_info "ImageMagick not available, using fallback icon"
    fi
}

# Select installation directory
select_install_location() {
    echo ""
    echo -e "${YELLOW}Select installation location:${NC}"
    echo "  [1] Default: $DEFAULT_INSTALL_DIR"
    echo "  [2] Custom location"
    echo ""
    read -p "Enter choice (1 or 2): " choice
    
    if [ "$choice" = "2" ]; then
        read -p "Enter installation path: " custom_path
        if [ -n "$custom_path" ]; then
            # Expand ~ if present
            INSTALL_DIR="${custom_path/#\~/$HOME}"
        else
            INSTALL_DIR="$DEFAULT_INSTALL_DIR"
        fi
    else
        INSTALL_DIR="$DEFAULT_INSTALL_DIR"
    fi
    
    print_info "Installing to: $INSTALL_DIR"
}

# Main uninstall function
uninstall() {
    print_header
    echo -e "${YELLOW}Uninstalling $APP_NAME...${NC}"
    echo ""
    
    # Remove launcher
    print_step "Removing launcher..."
    rm -f "$LAUNCHER_DIR/$APP_ID"
    print_success "Launcher removed"
    
    # Remove desktop file
    print_step "Removing desktop entry..."
    rm -f "$DESKTOP_DIR/$APP_ID.desktop"
    print_success "Desktop entry removed"
    
    # Remove icons
    print_step "Removing icons..."
    rm -f "$ICON_DIR"/*/apps/$APP_ID.png 2>/dev/null || true
    print_success "Icons removed"
    
    # Remove installation directory
    print_step "Removing program files..."
    if [ -d "$DEFAULT_INSTALL_DIR" ]; then
        rm -rf "$DEFAULT_INSTALL_DIR"
        print_success "Program files removed"
    fi
    
    # Update desktop database
    if command_exists update-desktop-database; then
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
    fi
    
    echo ""
    print_success "$APP_NAME has been uninstalled successfully!"
    echo ""
}

# Main install function
install_game() {
    print_header
    
    # Select install location
    if [ -z "$INSTALL_DIR" ]; then
        select_install_location
    fi
    
    # Install system dependencies
    install_apt_dependencies
    
    # Create installation directory
    print_step "Creating installation directory..."
    if [ -d "$INSTALL_DIR" ]; then
        rm -rf "$INSTALL_DIR"
    fi
    mkdir -p "$INSTALL_DIR"
    print_success "Directory created"
    
    # Copy files
    print_step "Copying game files..."
    cp -r "$SCRIPT_DIR"/* "$INSTALL_DIR/" 2>/dev/null || true
    
    # Remove installer scripts from destination
    rm -f "$INSTALL_DIR/install_linux.sh" "$INSTALL_DIR/install_windows.ps1" "$INSTALL_DIR/install_windows.bat" 2>/dev/null || true
    rm -rf "$INSTALL_DIR/.venv" "$INSTALL_DIR/.git" "$INSTALL_DIR/__pycache__" 2>/dev/null || true
    find "$INSTALL_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find "$INSTALL_DIR" -name "*.pyc" -delete 2>/dev/null || true
    print_success "Files copied"
    
    # Create virtual environment
    print_step "Setting up Python environment..."
    cd "$INSTALL_DIR"
    python3 -m venv .venv
    
    # Activate and install requirements
    source .venv/bin/activate
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    deactivate
    print_success "Dependencies installed"
    
    # Ask about AI model
    echo ""
    read -p "Download AI model for conversations? (~700MB) (y/N): " download_model
    if [ "$download_model" = "y" ] || [ "$download_model" = "Y" ]; then
        print_step "Downloading AI model (this may take a while)..."
        cd "$INSTALL_DIR"
        .venv/bin/python download_model.py
    fi
    
    # Create icons from ICO
    create_linux_icons "$INSTALL_DIR"
    
    # Create launcher script
    print_step "Creating launcher..."
    mkdir -p "$LAUNCHER_DIR"
    
    cat > "$LAUNCHER_DIR/$APP_ID" << EOF
#!/bin/bash
# Cheese the Duck Launcher
cd "$INSTALL_DIR"
exec .venv/bin/python main.py "\$@"
EOF
    chmod +x "$LAUNCHER_DIR/$APP_ID"
    print_success "Launcher created at $LAUNCHER_DIR/$APP_ID"
    
    # Create desktop file
    print_step "Creating desktop entry..."
    mkdir -p "$DESKTOP_DIR"
    
    cat > "$DESKTOP_DIR/$APP_ID.desktop" << EOF
[Desktop Entry]
Version=1.2.0
Type=Application
Name=Cheese the Duck
Comment=A terminal-based virtual pet game
Exec=$LAUNCHER_DIR/$APP_ID
Icon=$APP_ID
Terminal=true
Categories=Game;Simulation;
Keywords=duck;pet;virtual;game;terminal;
StartupNotify=false
EOF
    chmod +x "$DESKTOP_DIR/$APP_ID.desktop"
    
    # Update desktop database
    if command_exists update-desktop-database; then
        update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
    fi
    print_success "Desktop entry created"
    
    # Add to PATH if needed
    if [[ ":$PATH:" != *":$LAUNCHER_DIR:"* ]]; then
        print_info "Adding $LAUNCHER_DIR to PATH..."
        
        # Add to appropriate shell config
        if [ -f "$HOME/.bashrc" ]; then
            if ! grep -q "$LAUNCHER_DIR" "$HOME/.bashrc" 2>/dev/null; then
                echo "" >> "$HOME/.bashrc"
                echo "# Cheese the Duck" >> "$HOME/.bashrc"
                echo "export PATH=\"\$PATH:$LAUNCHER_DIR\"" >> "$HOME/.bashrc"
            fi
        fi
        
        if [ -f "$HOME/.zshrc" ]; then
            if ! grep -q "$LAUNCHER_DIR" "$HOME/.zshrc" 2>/dev/null; then
                echo "" >> "$HOME/.zshrc"
                echo "# Cheese the Duck" >> "$HOME/.zshrc"
                echo "export PATH=\"\$PATH:$LAUNCHER_DIR\"" >> "$HOME/.zshrc"
            fi
        fi
        
        export PATH="$PATH:$LAUNCHER_DIR"
    fi
    
    # Keep a copy of the installer for uninstall
    cp "$SCRIPT_DIR/install_linux.sh" "$INSTALL_DIR/uninstall.sh" 2>/dev/null || true
    
    # Done!
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              Installation Complete! 🦆                      ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    print_info "Installed to: $INSTALL_DIR"
    print_info "Launcher: $LAUNCHER_DIR/$APP_ID"
    print_info "Desktop entry: Find 'Cheese the Duck' in your applications menu"
    echo ""
    echo -e "${YELLOW}To play:${NC}"
    echo "  • From terminal: $APP_ID"
    echo "  • From apps menu: Search for 'Cheese the Duck'"
    echo ""
    echo -e "${YELLOW}To uninstall:${NC}"
    echo "  $INSTALL_DIR/uninstall.sh --uninstall"
    echo ""
    
    read -p "Launch the game now? (Y/n): " play_now
    if [ "$play_now" != "n" ] && [ "$play_now" != "N" ]; then
        exec "$LAUNCHER_DIR/$APP_ID"
    fi
}

# Entry point - handle arguments
case "${1:-}" in
    --uninstall|-u)
        uninstall
        ;;
    --help|-h)
        echo "Usage: $0 [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --uninstall, -u   Uninstall Cheese the Duck"
        echo "  --help, -h        Show this help message"
        echo ""
        ;;
    *)
        install_game "$@"
        ;;
esac
