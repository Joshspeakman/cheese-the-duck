# Audio Setup for Cheese the Duck

## Current Audio Files

The game now includes real audio files:

1. **single-quack-from-a-duck.wav** - Duck quack sound effect
2. **Title.wav** - Title screen background music

## How Audio Works

### Sound Playback Methods

The game automatically detects the best available audio player on your system:

1. **paplay** (PulseAudio) - Preferred on most Linux systems
2. **aplay** (ALSA) - Fallback for systems without PulseAudio
3. **ffplay** (FFmpeg) - Alternative playback method

If none are available, the game falls back to synthesized beep sounds.

### When Sounds Play

**Duck Quacks:**
- When you talk to the duck
- When petting the duck
- When playing with the duck
- When feeding the duck
- When cleaning the duck
- Based on duck's mood (different emotions)

**Title Music:**
- Plays automatically on the title screen
- Loops continuously until you start a new game
- Stops when game begins

### Enabling/Disabling Sound

By default, sound is **disabled**. To enable it:

1. Start the game
2. Press `M` to toggle sound on/off
3. The setting is remembered during the session

## Adding More Sounds

To add additional sound effects:

1. Place WAV files in the project root directory
2. Update the `_wav_files` dictionary in `audio/sound.py`:

```python
self._wav_files = {
    'quack': self._audio_dir / 'single-quack-from-a-duck.wav',
    'title': self._audio_dir / 'Title.wav',
    'your_sound': self._audio_dir / 'your-sound-file.wav',  # Add here
}
```

3. Call the sound in code:
```python
sound_engine.play_wav('your_sound')
```

## Troubleshooting

**No sound playing?**
- Check if `paplay` or `aplay` is installed: `which paplay`
- Make sure sound is enabled in-game (press `M`)
- Check that audio files exist in the project root

**Installing audio players:**
```bash
# Ubuntu/Debian
sudo apt install pulseaudio-utils alsa-utils

# Fedora
sudo dnf install pulseaudio-utils alsa-utils
```

## Technical Details

- Audio format: WAV (recommended)
- Volume control: Adjustable via `sound_engine.volume` (0.0 to 1.0)
- Threading: All audio plays in background threads to avoid blocking gameplay
- Memory efficient: Files are streamed, not loaded into memory
