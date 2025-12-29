using NAudio.Wave;
using NAudio.Wave.SampleProviders;

namespace StupidDuck.Audio;

/// <summary>
/// Cross-platform audio engine using NAudio.
/// </summary>
public class SoundEngine : IDisposable
{
    private IWavePlayer? _waveOut;
    private MixingSampleProvider? _mixer;
    private bool _enabled = true;
    private float _volume = 0.5f;
    private readonly Dictionary<string, string> _soundPaths = new();
    private bool _disposed;

    public bool IsEnabled => _enabled;

    public SoundEngine()
    {
        try
        {
            InitializeAudio();
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Audio initialization failed: {ex.Message}");
            _enabled = false;
        }
    }

    private void InitializeAudio()
    {
        // Try to use platform-appropriate output
        try
        {
            _waveOut = new WaveOutEvent();
            _mixer = new MixingSampleProvider(WaveFormat.CreateIeeeFloatWaveFormat(44100, 2))
            {
                ReadFully = true
            };
            _waveOut.Init(_mixer);
            _waveOut.Play();
        }
        catch
        {
            _enabled = false;
        }
    }

    public void SetEnabled(bool enabled) => _enabled = enabled;

    public void SetVolume(float volume)
    {
        _volume = Math.Clamp(volume, 0f, 1f);
        if (_waveOut != null)
            _waveOut.Volume = _volume;
    }

    /// <summary>
    /// Register a sound file path.
    /// </summary>
    public void RegisterSound(string name, string path)
    {
        if (File.Exists(path))
            _soundPaths[name] = path;
    }

    /// <summary>
    /// Play a registered sound effect.
    /// </summary>
    public void PlaySound(string name)
    {
        if (!_enabled || _mixer == null)
            return;

        if (!_soundPaths.TryGetValue(name, out var path))
            return;

        try
        {
            var audioFile = new AudioFileReader(path);
            _mixer.AddMixerInput((ISampleProvider)audioFile);
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Failed to play sound {name}: {ex.Message}");
        }
    }

    /// <summary>
    /// Play a WAV file.
    /// </summary>
    public void PlayWav(string path, bool loop = false)
    {
        if (!_enabled || !File.Exists(path))
            return;

        try
        {
            var audioFile = new AudioFileReader(path);
            if (loop && _mixer != null)
            {
                var looped = new LoopStream(new WaveFileReader(path));
                var loopedSample = looped.ToSampleProvider();
                _mixer.AddMixerInput((ISampleProvider)loopedSample);
            }
            else if (_mixer != null)
            {
                _mixer.AddMixerInput((ISampleProvider)audioFile);
            }
        }
        catch (Exception ex)
        {
            Console.Error.WriteLine($"Failed to play WAV: {ex.Message}");
        }
    }

    /// <summary>
    /// Stop all currently playing sounds.
    /// </summary>
    public void StopAll()
    {
        if (_mixer != null)
        {
            _mixer.RemoveAllMixerInputs();
        }
    }

    public void Dispose()
    {
        if (_disposed)
            return;

        _disposed = true;
        StopAll();
        _waveOut?.Stop();
        _waveOut?.Dispose();
    }
}

/// <summary>
/// Helper class for looping audio.
/// </summary>
internal class LoopStream : WaveStream
{
    private readonly WaveStream _sourceStream;
    private bool _enableLooping = true;

    public LoopStream(WaveStream sourceStream)
    {
        _sourceStream = sourceStream;
    }

    public override WaveFormat WaveFormat => _sourceStream.WaveFormat;
    public override long Length => _sourceStream.Length;
    public override long Position
    {
        get => _sourceStream.Position;
        set => _sourceStream.Position = value;
    }

    public override int Read(byte[] buffer, int offset, int count)
    {
        var totalBytesRead = 0;
        while (totalBytesRead < count)
        {
            var bytesRead = _sourceStream.Read(buffer, offset + totalBytesRead, count - totalBytesRead);
            if (bytesRead == 0)
            {
                if (_sourceStream.Position == 0 || !_enableLooping)
                    break;
                _sourceStream.Position = 0;
            }
            totalBytesRead += bytesRead;
        }
        return totalBytesRead;
    }

    protected override void Dispose(bool disposing)
    {
        _sourceStream.Dispose();
        base.Dispose(disposing);
    }
}

/// <summary>
/// Text-based sound effects for when audio is not available.
/// </summary>
public static class DuckSounds
{
    public static readonly Dictionary<string, string> TextSounds = new()
    {
        ["quack"] = "~QUACK!~",
        ["happy_quack"] = "~Quack quack!~",
        ["sad_quack"] = "~quack...~",
        ["splash"] = "*SPLASH*",
        ["munch"] = "*munch munch*",
        ["sleep"] = "*zzz...*",
        ["waddle"] = "*waddle waddle*",
        ["flap"] = "*flap flap*",
        ["preen"] = "*preen preen*",
        ["play"] = "*wheee!*"
    };

    public static string GetTextSound(string sound) =>
        TextSounds.TryGetValue(sound, out var text) ? text : "*....*";
}
