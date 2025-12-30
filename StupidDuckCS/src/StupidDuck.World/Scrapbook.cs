using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

namespace StupidDuck.World;

/// <summary>
/// Categories of scrapbook photos/memories
/// </summary>
public enum PhotoCategory
{
    Milestone,
    Adventure,
    Friendship,
    Discovery,
    Seasonal,
    Achievement,
    Funny,
    Daily
}

/// <summary>
/// A single photo/memory in the scrapbook
/// </summary>
public class ScrapbookPhoto
{
    public string PhotoId { get; set; } = "";
    public PhotoCategory Category { get; set; }
    public string Title { get; set; } = "";
    public string Description { get; set; } = "";
    public DateTime DateTaken { get; set; } = DateTime.Now;
    public List<string> AsciiArt { get; set; } = new();
    public string MoodAtTime { get; set; } = "";
    public int DuckAgeDays { get; set; } = 0;
    public bool IsFavorite { get; set; } = false;
    public List<string> Tags { get; set; } = new();
    public string Location { get; set; } = "home";
    public string Weather { get; set; } = "sunny";
    public List<string> Stickers { get; set; } = new();
}

/// <summary>
/// Photo album/scrapbook system - captures and stores memorable moments
/// </summary>
public class Scrapbook
{
    // Photo ASCII templates for different moments
    private static readonly Dictionary<string, List<string>> _photoArt = new()
    {
        ["duck_happy"] = new List<string> { "   __(o>", "  (  🌟", " _/  \\", "Happy moment!" },
        ["duck_sleeping"] = new List<string> { "   __(-)>", "  (  💤", " _/  \\", "Sweet dreams" },
        ["duck_eating"] = new List<string> { "   __(o>🍞", "  ( nom", " _/  \\", "Yummy time!" },
        ["duck_playing"] = new List<string> { "   __(>o)>", "  ( ⚽", "  _\\ /", "Playtime!" },
        ["duck_friends"] = new List<string> { " __(o> __(o>", "(   )(   )", " \\_/  \\_/", "Friends!" },
        ["duck_adventure"] = new List<string> { "   🗺️__(o>", "  (   🎒", " _/   \\", "Adventure!" },
        ["duck_discovery"] = new List<string> { "   __(O>", "  ( ✨💎", " _/  \\", "Found it!" },
        ["duck_celebration"] = new List<string> { " 🎉__(^o^)>🎉", "  (  🎊", " _/   \\", "Party time!" },
        ["duck_rain"] = new List<string> { "  ☔__(o>", "💧(  💧", " _/  \\", "Rainy day!" },
        ["duck_snow"] = new List<string> { " ❄️ __(o>❄️", "  (  ⛄", " _/  \\", "Snow day!" },
        ["duck_rainbow"] = new List<string> { "  🌈__(^o^)>", "  (   ✨", " _/   \\", "Rainbow!" },
        ["duck_fishing"] = new List<string> { "   __(o>", "  ( 🎣", " _/  \\ ~🐟", "Gone fishing" },
        ["duck_garden"] = new List<string> { "🌸__(o>🌷", "  (  🌻", " _/  \\", "Garden day!" }
    };

    // Decorative stickers
    private static readonly Dictionary<string, string> _stickers = new()
    {
        ["heart"] = "❤️",
        ["star"] = "⭐",
        ["sparkle"] = "✨",
        ["flower"] = "🌸",
        ["rainbow"] = "🌈",
        ["sun"] = "☀️",
        ["moon"] = "🌙",
        ["crown"] = "👑",
        ["trophy"] = "🏆",
        ["bread"] = "🍞",
        ["butterfly"] = "🦋",
        ["music"] = "🎵",
        ["gift"] = "🎁",
        ["camera"] = "📸",
        ["clover"] = "🍀"
    };

    // Photo frame templates
    private static readonly Dictionary<string, List<string>> _photoFrames = new()
    {
        ["simple"] = new List<string>
        {
            "╔════════════════════════╗",
            "║  {title}  ║",
            "╠════════════════════════╣",
            "║                        ║",
            "║   {art1}   ║",
            "║   {art2}   ║",
            "║   {art3}   ║",
            "║   {art4}   ║",
            "║                        ║",
            "╠════════════════════════╣",
            "║  {date}  ║",
            "╚════════════════════════╝"
        },
        ["fancy"] = new List<string>
        {
            "╭─────────✦ ✧ ✦─────────╮",
            "│  {title}  │",
            "├───────────────────────┤",
            "│                       │",
            "│  {art1}  │",
            "│  {art2}  │",
            "│  {art3}  │",
            "│  {art4}  │",
            "│                       │",
            "├───────────────────────┤",
            "│  ✿ {date} ✿  │",
            "╰─────────✧ ✦ ✧─────────╯"
        },
        ["polaroid"] = new List<string>
        {
            "┌─────────────────────────┐",
            "│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │",
            "│ ▓                     ▓ │",
            "│ ▓  {art1}  ▓ │",
            "│ ▓  {art2}  ▓ │",
            "│ ▓  {art3}  ▓ │",
            "│ ▓  {art4}  ▓ │",
            "│ ▓                     ▓ │",
            "│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ │",
            "│                         │",
            "│  {title}  │",
            "│  {date}  │",
            "└─────────────────────────┘"
        }
    };

    // Instance state
    public Dictionary<string, ScrapbookPhoto> Photos { get; private set; } = new();
    public List<List<string>> Pages { get; private set; } = new();
    public int CurrentPage { get; set; } = 0;
    public int PhotosPerPage { get; } = 4;
    public int TotalPhotosTaken { get; private set; } = 0;
    public int FavoriteCount { get; private set; } = 0;
    public bool AutoCaptureEnabled { get; set; } = true;
    public List<string> UnlockedFrames { get; private set; } = new() { "simple" };
    public List<string> UnlockedStickers { get; private set; } = new() { "heart", "star", "sparkle" };

    public Scrapbook()
    {
    }

    /// <summary>
    /// Take a new photo and add it to the scrapbook
    /// </summary>
    public ScrapbookPhoto TakePhoto(
        string title,
        string description,
        PhotoCategory category,
        string artKey = "duck_happy",
        string mood = "happy",
        int duckAge = 1,
        string location = "home",
        string weather = "sunny",
        List<string>? tags = null)
    {
        TotalPhotosTaken++;
        string photoId = $"photo_{TotalPhotosTaken}_{DateTime.Now:yyyyMMdd_HHmmss}";

        var asciiArt = _photoArt.GetValueOrDefault(artKey, _photoArt["duck_happy"]).ToList();

        var photo = new ScrapbookPhoto
        {
            PhotoId = photoId,
            Category = category,
            Title = title,
            Description = description,
            DateTaken = DateTime.Now,
            AsciiArt = asciiArt,
            MoodAtTime = mood,
            DuckAgeDays = duckAge,
            Tags = tags ?? new List<string>(),
            Location = location,
            Weather = weather
        };

        Photos[photoId] = photo;
        AddToPage(photoId);

        return photo;
    }

    /// <summary>
    /// Add a photo to album pages
    /// </summary>
    private void AddToPage(string photoId)
    {
        if (!Pages.Any() || Pages.Last().Count >= PhotosPerPage)
        {
            Pages.Add(new List<string>());
        }
        Pages.Last().Add(photoId);
    }

    /// <summary>
    /// Toggle favorite status of a photo
    /// </summary>
    public bool ToggleFavorite(string photoId)
    {
        if (Photos.TryGetValue(photoId, out var photo))
        {
            photo.IsFavorite = !photo.IsFavorite;
            FavoriteCount += photo.IsFavorite ? 1 : -1;
            return photo.IsFavorite;
        }
        return false;
    }

    /// <summary>
    /// Add a sticker to a photo
    /// </summary>
    public bool AddSticker(string photoId, string sticker)
    {
        if (Photos.TryGetValue(photoId, out var photo) && UnlockedStickers.Contains(sticker))
        {
            photo.Stickers.Add(sticker);
            return true;
        }
        return false;
    }

    /// <summary>
    /// Unlock a new photo frame style
    /// </summary>
    public void UnlockFrame(string frameName)
    {
        if (_photoFrames.ContainsKey(frameName) && !UnlockedFrames.Contains(frameName))
        {
            UnlockedFrames.Add(frameName);
        }
    }

    /// <summary>
    /// Unlock a new sticker
    /// </summary>
    public void UnlockSticker(string stickerName)
    {
        if (_stickers.ContainsKey(stickerName) && !UnlockedStickers.Contains(stickerName))
        {
            UnlockedStickers.Add(stickerName);
        }
    }

    /// <summary>
    /// Get photos for a specific page
    /// </summary>
    public List<ScrapbookPhoto> GetPage(int pageNum)
    {
        if (pageNum >= 0 && pageNum < Pages.Count)
        {
            return Pages[pageNum]
                .Where(pid => Photos.ContainsKey(pid))
                .Select(pid => Photos[pid])
                .ToList();
        }
        return new List<ScrapbookPhoto>();
    }

    /// <summary>
    /// Get all photos in a category
    /// </summary>
    public List<ScrapbookPhoto> GetPhotosByCategory(PhotoCategory category)
    {
        return Photos.Values.Where(p => p.Category == category).ToList();
    }

    /// <summary>
    /// Get all favorite photos
    /// </summary>
    public List<ScrapbookPhoto> GetFavorites()
    {
        return Photos.Values.Where(p => p.IsFavorite).ToList();
    }

    /// <summary>
    /// Render a photo with its frame
    /// </summary>
    public List<string> RenderPhoto(ScrapbookPhoto photo, string frameStyle = "simple")
    {
        var frame = _photoFrames.GetValueOrDefault(frameStyle, _photoFrames["simple"]);

        // Pad art to 4 lines
        var art = photo.AsciiArt.Take(4).ToList();
        while (art.Count < 4)
        {
            art.Add("");
        }

        var rendered = new List<string>();
        foreach (var line in frame)
        {
            string renderedLine = line
                .Replace("{title}", photo.Title.PadLeft(10).PadRight(20))
                .Replace("{date}", photo.DateTaken.ToString("yyyy-MM-dd").PadLeft(10).PadRight(20))
                .Replace("{art1}", art[0].PadRight(20))
                .Replace("{art2}", art[1].PadRight(20))
                .Replace("{art3}", art[2].PadRight(20))
                .Replace("{art4}", art[3].PadRight(20));
            rendered.Add(renderedLine);
        }

        // Add stickers if any
        if (photo.Stickers.Any())
        {
            string stickerLine = string.Join(" ", photo.Stickers.Take(5).Select(s => _stickers.GetValueOrDefault(s, s)));
            rendered.Add($"  {stickerLine}");
        }

        return rendered;
    }

    /// <summary>
    /// Render a full album page
    /// </summary>
    public List<string> RenderAlbumPage(int? pageNum = null)
    {
        int page = pageNum ?? CurrentPage;
        var photos = GetPage(page);

        if (!photos.Any())
        {
            return new List<string>
            {
                "╔═══════════════════════════════════════╗",
                "║        📷 SCRAPBOOK - Empty Page 📷    ║",
                "║                                       ║",
                "║       No photos on this page yet!     ║",
                "║                                       ║",
                "║   Make memories with your duck to     ║",
                "║   fill your scrapbook!                ║",
                "║                                       ║",
                "╚═══════════════════════════════════════╝"
            };
        }

        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════════╗",
            $"║     📷 SCRAPBOOK - Page {page + 1}/{Pages.Count} 📷     ║",
            "╠═══════════════════════════════════════════════════╣"
        };

        foreach (var photo in photos)
        {
            string fav = photo.IsFavorite ? "★" : "☆";
            string title = photo.Title.Length > 25 ? photo.Title[..25] : photo.Title;
            lines.Add($"║ {fav} {title,-25} - {photo.DateTaken:yyyy-MM-dd} ║");
            string desc = photo.Description.Length > 40 ? photo.Description[..40] : photo.Description;
            lines.Add($"║   {desc,-40} ║");
            lines.Add("╟───────────────────────────────────────────────────╢");
        }

        lines.Add("║  [<] Prev  [>] Next  [F] Toggle Favorite  [Q] Back ║");
        lines.Add("╚═══════════════════════════════════════════════════╝");

        return lines;
    }

    /// <summary>
    /// Automatically capture a milestone photo
    /// </summary>
    public void AutoCaptureMilestone(string milestoneType, string duckName, int duckAge, string mood = "happy")
    {
        var milestones = new Dictionary<string, (string title, string desc, string art)>
        {
            ["first_feed"] = ("First Meal!", $"{duckName}'s very first feeding!", "duck_eating"),
            ["first_play"] = ("First Playtime!", $"{duckName} played for the first time!", "duck_playing"),
            ["growth_teen"] = ("Growing Up!", $"{duckName} became a teenager!", "duck_celebration"),
            ["growth_adult"] = ("All Grown Up!", $"{duckName} is now an adult!", "duck_celebration"),
            ["growth_elder"] = ("Wise Duck", $"{duckName} has become an elder!", "duck_celebration"),
            ["best_friends"] = ("Best Friends!", $"You and {duckName} are now best friends!", "duck_friends"),
            ["first_visitor"] = ("First Visitor!", $"{duckName} met their first visitor!", "duck_friends"),
            ["first_adventure"] = ("Adventure Time!", $"{duckName}'s first adventure!", "duck_adventure"),
            ["rainbow_seen"] = ("Rainbow Spotted!", $"{duckName} saw a beautiful rainbow!", "duck_rainbow"),
            ["treasure_found"] = ("Treasure Hunter!", $"{duckName} found treasure!", "duck_discovery"),
            ["fishing_catch"] = ("Big Catch!", $"{duckName} caught a fish!", "duck_fishing"),
            ["garden_harvest"] = ("Harvest Time!", $"{duckName} harvested from the garden!", "duck_garden")
        };

        if (milestones.TryGetValue(milestoneType, out var milestone) && AutoCaptureEnabled)
        {
            TakePhoto(
                title: milestone.title,
                description: milestone.desc,
                category: PhotoCategory.Milestone,
                artKey: milestone.art,
                mood: mood,
                duckAge: duckAge,
                tags: new List<string> { milestoneType, "auto" }
            );
        }
    }

    /// <summary>
    /// Convert to save data
    /// </summary>
    public Dictionary<string, object> ToSaveData()
    {
        var photosData = new Dictionary<string, object>();
        foreach (var kvp in Photos)
        {
            photosData[kvp.Key] = new Dictionary<string, object>
            {
                ["photo_id"] = kvp.Value.PhotoId,
                ["category"] = kvp.Value.Category.ToString().ToLower(),
                ["title"] = kvp.Value.Title,
                ["description"] = kvp.Value.Description,
                ["date_taken"] = kvp.Value.DateTaken.ToString("o"),
                ["ascii_art"] = kvp.Value.AsciiArt,
                ["mood_at_time"] = kvp.Value.MoodAtTime,
                ["duck_age_days"] = kvp.Value.DuckAgeDays,
                ["is_favorite"] = kvp.Value.IsFavorite,
                ["tags"] = kvp.Value.Tags,
                ["location"] = kvp.Value.Location,
                ["weather"] = kvp.Value.Weather,
                ["stickers"] = kvp.Value.Stickers
            };
        }

        return new Dictionary<string, object>
        {
            ["photos"] = photosData,
            ["pages"] = Pages,
            ["current_page"] = CurrentPage,
            ["total_photos_taken"] = TotalPhotosTaken,
            ["favorite_count"] = FavoriteCount,
            ["auto_capture_enabled"] = AutoCaptureEnabled,
            ["unlocked_frames"] = UnlockedFrames,
            ["unlocked_stickers"] = UnlockedStickers
        };
    }

    /// <summary>
    /// Load from save data
    /// </summary>
    public static Scrapbook FromSaveData(Dictionary<string, object> data)
    {
        var scrapbook = new Scrapbook();

        if (data.TryGetValue("photos", out var photosObj) && photosObj is JsonElement photosElem)
        {
            foreach (var prop in photosElem.EnumerateObject())
            {
                var pdata = prop.Value;
                var photo = new ScrapbookPhoto
                {
                    PhotoId = pdata.GetProperty("photo_id").GetString() ?? "",
                    Category = Enum.TryParse<PhotoCategory>(pdata.GetProperty("category").GetString(), true, out var cat) ? cat : PhotoCategory.Daily,
                    Title = pdata.GetProperty("title").GetString() ?? "",
                    Description = pdata.GetProperty("description").GetString() ?? "",
                    DateTaken = DateTime.Parse(pdata.GetProperty("date_taken").GetString() ?? DateTime.Now.ToString()),
                    MoodAtTime = pdata.GetProperty("mood_at_time").GetString() ?? "",
                    DuckAgeDays = pdata.GetProperty("duck_age_days").GetInt32(),
                    IsFavorite = pdata.TryGetProperty("is_favorite", out var fav) && fav.GetBoolean(),
                    Location = pdata.TryGetProperty("location", out var loc) ? loc.GetString() ?? "home" : "home",
                    Weather = pdata.TryGetProperty("weather", out var wea) ? wea.GetString() ?? "sunny" : "sunny"
                };

                if (pdata.TryGetProperty("ascii_art", out var artElem))
                {
                    photo.AsciiArt = artElem.EnumerateArray().Select(a => a.GetString() ?? "").ToList();
                }

                if (pdata.TryGetProperty("tags", out var tagsElem))
                {
                    photo.Tags = tagsElem.EnumerateArray().Select(t => t.GetString() ?? "").ToList();
                }

                if (pdata.TryGetProperty("stickers", out var stickersElem))
                {
                    photo.Stickers = stickersElem.EnumerateArray().Select(s => s.GetString() ?? "").ToList();
                }

                scrapbook.Photos[prop.Name] = photo;
            }
        }

        if (data.TryGetValue("pages", out var pagesObj) && pagesObj is JsonElement pagesElem)
        {
            scrapbook.Pages = pagesElem.EnumerateArray()
                .Select(p => p.EnumerateArray().Select(pid => pid.GetString() ?? "").ToList())
                .ToList();
        }

        scrapbook.CurrentPage = Convert.ToInt32(data.GetValueOrDefault("current_page", 0));
        scrapbook.TotalPhotosTaken = Convert.ToInt32(data.GetValueOrDefault("total_photos_taken", scrapbook.Photos.Count));
        scrapbook.FavoriteCount = Convert.ToInt32(data.GetValueOrDefault("favorite_count", 0));
        scrapbook.AutoCaptureEnabled = data.TryGetValue("auto_capture_enabled", out var auto) && auto is bool b ? b : true;

        if (data.TryGetValue("unlocked_frames", out var framesObj) && framesObj is JsonElement framesElem)
        {
            scrapbook.UnlockedFrames = framesElem.EnumerateArray().Select(f => f.GetString() ?? "").ToList();
        }

        if (data.TryGetValue("unlocked_stickers", out var stickObj) && stickObj is JsonElement stickElem)
        {
            scrapbook.UnlockedStickers = stickElem.EnumerateArray().Select(s => s.GetString() ?? "").ToList();
        }

        return scrapbook;
    }
}
