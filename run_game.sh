#!/bin/bash
cd "/home/joshspeakman/System_NVMe/Claude Code/Projects/Stupid Duck/stupid_duck"

# Use venv if it exists (for AI support)
if [ -f ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
else
    PYTHON="python3"
    
    # Check if model exists for AI chat
    if ! ls models/*.gguf 1>/dev/null 2>&1; then
        echo "╔═══════════════════════════════════════════════════════════════╗"
        echo "║  🦆 TIP: Run 'python3 download_model.py' for AI conversations ║"
        echo "╚═══════════════════════════════════════════════════════════════╝"
        echo ""
        sleep 2
    fi
fi

$PYTHON main.py
read -p "Press Enter to close..."
