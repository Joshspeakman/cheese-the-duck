#!/bin/bash
# Find and monitor the Stupid Duck game process

echo "Looking for Stupid Duck game process..."
PID=$(ps aux | grep "[p]ython.*main.py" | grep -v grep | awk '{print $2}' | head -1)

if [ -z "$PID" ]; then
    echo "Error: Game is not running!"
    echo ""
    echo "Please start the game first with: python main.py"
    echo "Then run this script again."
    exit 1
fi

echo "Found game process: PID $PID"
echo ""
echo "Starting 5-minute memory monitor..."
echo "Play the game normally - open menus, interact, explore, etc."
echo ""

python3 monitor_memory.py "$PID" 5 10
