namespace StupidDuck.UI;

/// <summary>
/// Animation types for the duck.
/// </summary>
public enum AnimationType
{
    Idle,
    Waddle,
    Bounce,
    Flap,
    Shake,
    Sleep,
    Eat,
    Splash,
    Spin,
    Jump,
    Wiggle,
    Quack
}

/// <summary>
/// Effect overlay types.
/// </summary>
public enum EffectType
{
    Heart,
    Hearts,
    Sparkle,
    Exclaim,
    Question,
    Angry,
    Zzz,
    Music,
    Sweat,
    Happy,
    Sad,
    Splash,
    Crumbs
}

/// <summary>
/// A particle in the world.
/// </summary>
public class Particle
{
    public float X { get; set; }
    public float Y { get; set; }
    public float VelX { get; set; }
    public float VelY { get; set; }
    public char Character { get; set; }
    public string Color { get; set; } = "white";
    public float Life { get; set; }
    public float MaxLife { get; set; }

    public bool IsAlive => Life > 0;

    public void Update(float dt)
    {
        X += VelX * dt;
        Y += VelY * dt;
        VelY += 0.5f * dt; // Gravity
        Life -= dt;
    }
}

/// <summary>
/// Manages animations and visual effects.
/// </summary>
public class AnimationController
{
    private static readonly Random Rng = new();

    private AnimationType _currentAnimation = AnimationType.Idle;
    private EffectType? _currentEffect;
    private int _animationFrame;
    private float _animationTimer;
    private float _effectTimer;
    private readonly List<Particle> _particles = new();

    // Idle movement offsets
    private float _idleOffsetX;
    private float _idleOffsetY;
    private float _idleTimer;

    public AnimationType CurrentAnimation => _currentAnimation;
    public EffectType? CurrentEffect => _currentEffect;
    public IReadOnlyList<Particle> Particles => _particles;

    /// <summary>
    /// Start an animation.
    /// </summary>
    public void PlayAnimation(AnimationType type, float duration = 1f)
    {
        _currentAnimation = type;
        _animationTimer = duration;
        _animationFrame = 0;
    }

    /// <summary>
    /// Show an effect overlay.
    /// </summary>
    public void ShowEffect(EffectType type, float duration = 0.5f)
    {
        _currentEffect = type;
        _effectTimer = duration;
    }

    /// <summary>
    /// Spawn particles.
    /// </summary>
    public void SpawnParticles(float x, float y, char[] chars, string color, int count = 5)
    {
        for (var i = 0; i < count; i++)
        {
            _particles.Add(new Particle
            {
                X = x + (float)(Rng.NextDouble() * 4 - 2),
                Y = y + (float)(Rng.NextDouble() * 2 - 1),
                VelX = (float)(Rng.NextDouble() * 4 - 2),
                VelY = (float)(Rng.NextDouble() * -3 - 1),
                Character = chars[Rng.Next(chars.Length)],
                Color = color,
                Life = (float)(0.5 + Rng.NextDouble() * 1),
                MaxLife = 1.5f
            });
        }
    }

    /// <summary>
    /// Update animations.
    /// </summary>
    public void Update(float dt)
    {
        // Update animation
        if (_animationTimer > 0)
        {
            _animationTimer -= dt;
            _animationFrame++;
            if (_animationTimer <= 0)
            {
                _currentAnimation = AnimationType.Idle;
                _animationFrame = 0;
            }
        }

        // Update effect
        if (_effectTimer > 0)
        {
            _effectTimer -= dt;
            if (_effectTimer <= 0)
                _currentEffect = null;
        }

        // Update particles
        foreach (var p in _particles)
            p.Update(dt);
        _particles.RemoveAll(p => !p.IsAlive);

        // Idle animation
        _idleTimer += dt;
        _idleOffsetX = MathF.Sin(_idleTimer * 2) * 0.3f;
        _idleOffsetY = MathF.Sin(_idleTimer * 3) * 0.2f;
    }

    /// <summary>
    /// Get duck position offset from current animation.
    /// </summary>
    public (float x, float y) GetAnimationOffset()
    {
        return _currentAnimation switch
        {
            AnimationType.Idle => (_idleOffsetX, _idleOffsetY),
            AnimationType.Waddle => (MathF.Sin(_animationFrame * 0.5f) * 0.5f, 0),
            AnimationType.Bounce => (0, MathF.Abs(MathF.Sin(_animationFrame * 0.8f)) * -1),
            AnimationType.Flap => (0, MathF.Sin(_animationFrame * 1.2f) * 0.5f),
            AnimationType.Shake => ((Rng.Next(3) - 1) * 0.3f, 0),
            AnimationType.Jump => (0, _animationFrame < 5 ? -_animationFrame * 0.3f : (_animationFrame - 10) * 0.3f),
            AnimationType.Spin => (MathF.Cos(_animationFrame * 0.5f) * 0.5f, MathF.Sin(_animationFrame * 0.5f) * 0.3f),
            _ => (0, 0)
        };
    }

    /// <summary>
    /// Get effect overlay text.
    /// </summary>
    public string? GetEffectOverlay()
    {
        return _currentEffect switch
        {
            EffectType.Heart => "♥",
            EffectType.Hearts => "♥♥♥",
            EffectType.Sparkle => "✨",
            EffectType.Exclaim => "!",
            EffectType.Question => "?",
            EffectType.Angry => "💢",
            EffectType.Zzz => "Zzz",
            EffectType.Music => "♪♫",
            EffectType.Sweat => "💧",
            EffectType.Happy => "^-^",
            EffectType.Sad => ";-;",
            EffectType.Splash => "💦",
            EffectType.Crumbs => "•••",
            _ => null
        };
    }

    /// <summary>
    /// Get duck sprite based on animation.
    /// </summary>
    public string GetDuckSprite(bool facingRight)
    {
        var baseSprite = facingRight ? "(^)>" : "<(^)";
        
        return _currentAnimation switch
        {
            AnimationType.Sleep => facingRight ? "(-)>" : "<(-)".Replace("-", "z"[0].ToString()),
            AnimationType.Eat => facingRight ? "(o)v" : "v(o)",
            AnimationType.Splash => facingRight ? "(O)≈" : "≈(O)",
            AnimationType.Quack => facingRight ? "(O)>" : "<(O)",
            AnimationType.Flap when _animationFrame % 4 < 2 => facingRight ? "(^)^" : "^(^)",
            _ => baseSprite
        };
    }
}

/// <summary>
/// Static effect definitions.
/// </summary>
public static class Effects
{
    public static readonly Dictionary<EffectType, string[]> Overlays = new()
    {
        [EffectType.Heart] = new[] { "   ♥   ", "  ♥♥♥  ", "   ♥   " },
        [EffectType.Hearts] = new[] { " ♥   ♥ ", "  ♥ ♥  ", "   ♥   " },
        [EffectType.Sparkle] = new[] { "  ✧ ✧  ", " ✧ ✧ ✧ ", "  ✧ ✧  " },
        [EffectType.Zzz] = new[] { "    z  ", "   z   ", "  Z    " },
        [EffectType.Music] = new[] { " ♪  ♫  ", "  ♫  ♪ ", " ♪  ♫  " }
    };

    public static readonly Dictionary<string, char[]> ParticleChars = new()
    {
        ["dust"] = new[] { '.', '·', '°' },
        ["water"] = new[] { '~', '≈', '∿' },
        ["sparkle"] = new[] { '*', '✧', '✦' },
        ["leaves"] = new[] { '~', '^', '-' },
        ["crumbs"] = new[] { '.', '·', ',' },
        ["hearts"] = new[] { '♥', '♡', '♥' },
        ["snow"] = new[] { '*', '·', '°', '❄' }
    };
}
