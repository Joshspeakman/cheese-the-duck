#!/bin/bash
# ============================================================
# Cheese the Duck - Debian Package Builder
# ============================================================
# Builds a .deb package from the latest GitHub release.
#
# Usage: ./build_deb.sh
# Output: cheese-the-duck_VERSION_all.deb
# ============================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_NAME="cheese-the-duck"
GITHUB_REPO="Joshspeakman/cheese-the-duck"

echo -e "${CYAN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║           🦆 Cheese the Duck - DEB Package Builder          ║${NC}"
echo -e "${CYAN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check for required tools
echo -e "${YELLOW}→${NC} Checking build dependencies..."

DEPS_NEEDED=()
if ! command -v dpkg-deb &> /dev/null; then
    DEPS_NEEDED+=("dpkg-dev")
fi
if ! command -v fakeroot &> /dev/null; then
    DEPS_NEEDED+=("fakeroot")
fi
if ! command -v convert &> /dev/null; then
    DEPS_NEEDED+=("imagemagick")
fi
if ! command -v curl &> /dev/null; then
    DEPS_NEEDED+=("curl")
fi
if ! command -v jq &> /dev/null; then
    DEPS_NEEDED+=("jq")
fi

if [ ${#DEPS_NEEDED[@]} -gt 0 ]; then
    echo -e "${YELLOW}→${NC} Installing build dependencies: ${DEPS_NEEDED[*]}"
    sudo apt-get update -qq
    sudo apt-get install -y -qq "${DEPS_NEEDED[@]}"
fi
echo -e "${GREEN}✓${NC} Build dependencies ready"

# Fetch latest release info from GitHub
echo -e "${YELLOW}→${NC} Fetching latest release from GitHub..."
RELEASE_INFO=$(curl -s "https://api.github.com/repos/${GITHUB_REPO}/releases/latest" 2>/dev/null || echo "")

if [ -z "$RELEASE_INFO" ] || echo "$RELEASE_INFO" | grep -q "Not Found"; then
    # No releases, use latest tag or main branch
    echo -e "${YELLOW}→${NC} No releases found, checking for tags..."
    TAG_INFO=$(curl -s "https://api.github.com/repos/${GITHUB_REPO}/tags" 2>/dev/null || echo "[]")
    
    if [ "$TAG_INFO" != "[]" ] && echo "$TAG_INFO" | jq -e '.[0].name' > /dev/null 2>&1; then
        VERSION=$(echo "$TAG_INFO" | jq -r '.[0].name' | sed 's/^v//')
        DOWNLOAD_URL="https://github.com/${GITHUB_REPO}/archive/refs/tags/$(echo "$TAG_INFO" | jq -r '.[0].name').tar.gz"
        echo -e "${GREEN}✓${NC} Found tag: v${VERSION}"
    else
        # No tags, use main branch
        VERSION="1.2.0"
        DOWNLOAD_URL="https://github.com/${GITHUB_REPO}/archive/refs/heads/main.tar.gz"
        echo -e "${YELLOW}→${NC} No tags found, using main branch (v${VERSION})"
    fi
else
    VERSION=$(echo "$RELEASE_INFO" | jq -r '.tag_name' | sed 's/^v//')
    DOWNLOAD_URL=$(echo "$RELEASE_INFO" | jq -r '.tarball_url')
    echo -e "${GREEN}✓${NC} Found release: v${VERSION}"
fi

# Create build directory in /tmp for proper permissions
BUILD_DIR="/tmp/cheese-deb-build-$$"
PACKAGE_DIR="$BUILD_DIR/${PACKAGE_NAME}_${VERSION}-1_all"
SOURCE_DIR="$BUILD_DIR/source"

echo -e "${YELLOW}→${NC} Creating package structure..."
rm -rf "$BUILD_DIR"
mkdir -p "$PACKAGE_DIR/DEBIAN"
mkdir -p "$PACKAGE_DIR/opt/cheese-the-duck"
mkdir -p "$PACKAGE_DIR/usr/bin"
mkdir -p "$PACKAGE_DIR/usr/share/applications"
mkdir -p "$PACKAGE_DIR/usr/share/icons/hicolor/256x256/apps"
mkdir -p "$PACKAGE_DIR/usr/share/icons/hicolor/128x128/apps"
mkdir -p "$PACKAGE_DIR/usr/share/icons/hicolor/64x64/apps"
mkdir -p "$PACKAGE_DIR/usr/share/icons/hicolor/48x48/apps"
mkdir -p "$PACKAGE_DIR/usr/share/icons/hicolor/32x32/apps"
mkdir -p "$PACKAGE_DIR/usr/share/icons/hicolor/16x16/apps"
mkdir -p "$SOURCE_DIR"

# Fix permissions for DEBIAN directory
chmod 755 "$PACKAGE_DIR/DEBIAN"

# Download source from GitHub
echo -e "${YELLOW}→${NC} Downloading source code..."
curl -sL "$DOWNLOAD_URL" | tar -xz -C "$SOURCE_DIR" --strip-components=1
echo -e "${GREEN}✓${NC} Source downloaded"

# Copy game files from downloaded source
echo -e "${YELLOW}→${NC} Copying game files..."
cp -r "$SOURCE_DIR/audio" "$PACKAGE_DIR/opt/cheese-the-duck/"
cp -r "$SOURCE_DIR/core" "$PACKAGE_DIR/opt/cheese-the-duck/"
cp -r "$SOURCE_DIR/dialogue" "$PACKAGE_DIR/opt/cheese-the-duck/"
cp -r "$SOURCE_DIR/duck" "$PACKAGE_DIR/opt/cheese-the-duck/"
cp -r "$SOURCE_DIR/ui" "$PACKAGE_DIR/opt/cheese-the-duck/"
cp -r "$SOURCE_DIR/world" "$PACKAGE_DIR/opt/cheese-the-duck/"

# Copy optional directories
[ -d "$SOURCE_DIR/assets" ] && cp -r "$SOURCE_DIR/assets" "$PACKAGE_DIR/opt/cheese-the-duck/"
[ -d "$SOURCE_DIR/data" ] && cp -r "$SOURCE_DIR/data" "$PACKAGE_DIR/opt/cheese-the-duck/"
[ -d "$SOURCE_DIR/models" ] && mkdir -p "$PACKAGE_DIR/opt/cheese-the-duck/models"

# Copy main files
cp "$SOURCE_DIR/main.py" "$PACKAGE_DIR/opt/cheese-the-duck/"
cp "$SOURCE_DIR/config.py" "$PACKAGE_DIR/opt/cheese-the-duck/"
cp "$SOURCE_DIR/game_logger.py" "$PACKAGE_DIR/opt/cheese-the-duck/"
cp "$SOURCE_DIR/requirements.txt" "$PACKAGE_DIR/opt/cheese-the-duck/"
[ -f "$SOURCE_DIR/download_model.py" ] && cp "$SOURCE_DIR/download_model.py" "$PACKAGE_DIR/opt/cheese-the-duck/"
[ -f "$SOURCE_DIR/cheese.ico" ] && cp "$SOURCE_DIR/cheese.ico" "$PACKAGE_DIR/opt/cheese-the-duck/"

# Remove __pycache__ directories
find "$PACKAGE_DIR" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$PACKAGE_DIR" -name "*.pyc" -delete 2>/dev/null || true

echo -e "${GREEN}✓${NC} Game files copied"

# Convert icon
if [ -f "$SOURCE_DIR/cheese.ico" ] && command -v convert &> /dev/null; then
    echo -e "${YELLOW}→${NC} Creating icons..."
    convert "$SOURCE_DIR/cheese.ico[0]" -resize 256x256 "$PACKAGE_DIR/usr/share/icons/hicolor/256x256/apps/cheese-the-duck.png" 2>/dev/null || true
    convert "$SOURCE_DIR/cheese.ico[0]" -resize 128x128 "$PACKAGE_DIR/usr/share/icons/hicolor/128x128/apps/cheese-the-duck.png" 2>/dev/null || true
    convert "$SOURCE_DIR/cheese.ico[0]" -resize 64x64 "$PACKAGE_DIR/usr/share/icons/hicolor/64x64/apps/cheese-the-duck.png" 2>/dev/null || true
    convert "$SOURCE_DIR/cheese.ico[0]" -resize 48x48 "$PACKAGE_DIR/usr/share/icons/hicolor/48x48/apps/cheese-the-duck.png" 2>/dev/null || true
    convert "$SOURCE_DIR/cheese.ico[0]" -resize 32x32 "$PACKAGE_DIR/usr/share/icons/hicolor/32x32/apps/cheese-the-duck.png" 2>/dev/null || true
    convert "$SOURCE_DIR/cheese.ico[0]" -resize 16x16 "$PACKAGE_DIR/usr/share/icons/hicolor/16x16/apps/cheese-the-duck.png" 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Icons created"
fi

# Create launcher script
echo -e "${YELLOW}→${NC} Creating launcher..."
cat > "$PACKAGE_DIR/usr/bin/cheese-the-duck" << 'EOF'
#!/bin/bash
# Cheese the Duck Launcher
cd /opt/cheese-the-duck

# Create venv on first run if needed
if [ ! -d ".venv" ]; then
    echo "Setting up Cheese the Duck (first run)..."
    python3 -m venv .venv
    .venv/bin/pip install -q --upgrade pip
    .venv/bin/pip install -q -r requirements.txt
    echo "Setup complete! Starting game..."
fi

exec .venv/bin/python main.py "$@"
EOF
chmod 755 "$PACKAGE_DIR/usr/bin/cheese-the-duck"
echo -e "${GREEN}✓${NC} Launcher created"

# Create desktop entry
echo -e "${YELLOW}→${NC} Creating desktop entry..."
cat > "$PACKAGE_DIR/usr/share/applications/cheese-the-duck.desktop" << EOF
[Desktop Entry]
Version=${VERSION}
Type=Application
Name=Cheese the Duck
Comment=A terminal-based virtual pet game
Exec=cheese-the-duck
Icon=cheese-the-duck
Terminal=true
Categories=Game;Simulation;
Keywords=duck;pet;virtual;game;terminal;
StartupNotify=false
EOF
echo -e "${GREEN}✓${NC} Desktop entry created"

# Create DEBIAN control file
echo -e "${YELLOW}→${NC} Creating package metadata..."
cat > "$PACKAGE_DIR/DEBIAN/control" << EOF
Package: cheese-the-duck
Version: ${VERSION}-1
Section: games
Priority: optional
Architecture: all
Depends: python3 (>= 3.8), python3-venv, python3-pip, libsdl2-2.0-0, libsdl2-mixer-2.0-0
Recommends: imagemagick
Maintainer: Cheese the Duck Team <cheese@example.com>
Description: A terminal-based virtual pet duck game
 Cheese the Duck is an interactive terminal game where you care for
 your virtual pet duck named Cheese. Features include AI-powered
 conversations, day/night cycles, weather systems, exploration,
 crafting, mini-games, and much more.
Homepage: https://github.com/${GITHUB_REPO}
EOF

# Create postinst script
cat > "$PACKAGE_DIR/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# Set permissions
chmod -R a+rX /opt/cheese-the-duck
mkdir -p /opt/cheese-the-duck/data /opt/cheese-the-duck/logs
chmod 777 /opt/cheese-the-duck/data /opt/cheese-the-duck/logs

# Update caches
gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
update-desktop-database /usr/share/applications 2>/dev/null || true

echo ""
echo "🦆 Cheese the Duck installed!"
echo "   Run: cheese-the-duck"
echo ""

exit 0
EOF
chmod 755 "$PACKAGE_DIR/DEBIAN/postinst"

# Create postrm script  
cat > "$PACKAGE_DIR/DEBIAN/postrm" << 'EOF'
#!/bin/bash
set -e

case "$1" in
    purge|remove)
        rm -rf /opt/cheese-the-duck/.venv 2>/dev/null || true
        rm -rf /opt/cheese-the-duck/__pycache__ 2>/dev/null || true
        rm -rf /opt/cheese-the-duck/logs 2>/dev/null || true
        [ "$1" = "purge" ] && rm -rf /opt/cheese-the-duck 2>/dev/null || true
        gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
        update-desktop-database /usr/share/applications 2>/dev/null || true
        ;;
esac

exit 0
EOF
chmod 755 "$PACKAGE_DIR/DEBIAN/postrm"

echo -e "${GREEN}✓${NC} Package metadata created"

# Build the package
echo -e "${YELLOW}→${NC} Building .deb package..."
cd "$BUILD_DIR"
fakeroot dpkg-deb --build "${PACKAGE_NAME}_${VERSION}-1_all"

# Move to original script directory
mv "${PACKAGE_NAME}_${VERSION}-1_all.deb" "$SCRIPT_DIR/"

# Clean up
rm -rf "$BUILD_DIR"

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Package Built Successfully! 🦆                 ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Source:${NC} GitHub ${GITHUB_REPO} (v${VERSION})"
echo -e "${CYAN}Output:${NC} ${PACKAGE_NAME}_${VERSION}-1_all.deb"
echo ""
echo -e "${YELLOW}To install:${NC}"
echo "  sudo apt install ./${PACKAGE_NAME}_${VERSION}-1_all.deb"
echo ""
echo -e "${YELLOW}To uninstall:${NC}"
echo "  sudo apt remove cheese-the-duck"
echo ""
