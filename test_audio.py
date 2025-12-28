#!/usr/bin/env python3
"""
Test audio system - checks if audio files can be played.
"""
from pathlib import Path
import subprocess

# Check audio files
audio_dir = Path(__file__).parent
title_file = audio_dir / 'Title.wav'
quack_file = audio_dir / 'single-quack-from-a-duck.wav'

print("=== Audio System Test ===\n")

# Check files exist
print("1. Checking audio files:")
print(f"   Title.wav: {'✓ Found' if title_file.exists() else '✗ NOT FOUND'} at {title_file}")
print(f"   Quack.wav: {'✓ Found' if quack_file.exists() else '✗ NOT FOUND'} at {quack_file}")
print()

# Check audio players
print("2. Checking audio players:")
players = {
    'paplay': 'PulseAudio (recommended)',
    'aplay': 'ALSA',
    'ffplay': 'FFmpeg'
}

available_player = None
for player, desc in players.items():
    try:
        result = subprocess.run(
            ['which', player],
            capture_output=True,
            timeout=1
        )
        if result.returncode == 0:
            print(f"   {player}: ✓ Available ({desc})")
            if not available_player:
                available_player = player
        else:
            print(f"   {player}: ✗ Not found")
    except:
        print(f"   {player}: ✗ Error checking")

print()

# Test playback
if available_player and title_file.exists():
    print(f"3. Testing playback with {available_player}:")
    print(f"   Playing Title.wav for 3 seconds...")
    try:
        if available_player == 'paplay':
            process = subprocess.Popen(
                ['paplay', str(title_file)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            import time
            time.sleep(3)
            process.terminate()
            print("   ✓ Playback successful!")
        elif available_player == 'aplay':
            subprocess.run(
                ['aplay', '-q', '-d', '3', str(title_file)],
                timeout=5
            )
            print("   ✓ Playback successful!")
    except Exception as e:
        print(f"   ✗ Playback failed: {e}")
else:
    if not available_player:
        print("3. ✗ No audio player available!")
        print("\n   Install one with:")
        print("   sudo apt install pulseaudio-utils")
    if not title_file.exists():
        print("3. ✗ Audio file not found!")

print("\n=== Test Complete ===")
