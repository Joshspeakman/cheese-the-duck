using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.World;

/// <summary>
/// Different biome types the duck can explore.
/// </summary>
public enum BiomeType
{
    Pond,       // Home base - water, reeds, fish
    Forest,     // Trees, twigs, leaves, berries, mushrooms
    Meadow,     // Flowers, grass, seeds, insects
    Riverside,  // Pebbles, shells, clay, driftwood
    Garden,     // Vegetables, flowers, string, fabric scraps
    Mountains,  // Rocks, crystals, moss, pine needles (unlockable)
    Beach,      // Sand, shells, seaweed, glass, treasures (unlockable)
    Swamp,      // Murky water, fireflies, bog plants, mysterious finds
    Urban       // City park, bread crumbs, lost coins, human treasures
}

/// <summary>
/// A gatherable resource in an area.
/// </summary>
public class ResourceNode
{
    public string ResourceId { get; set; } = "";
    public string Name { get; set; } = "";
    public int Quantity { get; set; }
    public float RegenTimeHours { get; set; }
    public DateTime? LastGathered { get; set; }
    public int SkillRequired { get; set; }

    public bool IsAvailable()
    {
        if (Quantity <= 0)
        {
            if (!LastGathered.HasValue)
                return true;
            var hoursPassed = (DateTime.UtcNow - LastGathered.Value).TotalHours;
            return hoursPassed >= RegenTimeHours;
        }
        return true;
    }

    public int Gather(int amount = 1)
    {
        if (!IsAvailable())
            return 0;

        // Regenerate if needed
        if (Quantity <= 0)
            Quantity = Random.Shared.Next(2, 6);

        var gathered = Math.Min(amount, Quantity);
        Quantity -= gathered;
        if (Quantity <= 0)
            LastGathered = DateTime.UtcNow;
        return gathered;
    }
}

/// <summary>
/// A specific explorable area within a biome.
/// </summary>
public class BiomeArea
{
    public BiomeType Biome { get; set; }
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public List<ResourceNode> Resources { get; set; } = new();
    public float DiscoveryChance { get; set; } = 0.1f;
    public int UnlockLevel { get; set; } = 1;
    public bool IsDiscovered { get; set; }
    public int TimesVisited { get; set; }
    public List<string> SpecialEvents { get; set; } = new();
}

/// <summary>
/// Result of an exploration action.
/// </summary>
public class ExplorationResult
{
    public bool Success { get; set; }
    public string Message { get; set; } = "";
    public Dictionary<string, int> ResourcesFound { get; set; } = new();
    public string? RareDiscovery { get; set; }
    public string? Encounter { get; set; }
    public int XpGained { get; set; }
    public string? NewAreaDiscovered { get; set; }
    public string? BiomeName { get; set; }
    public bool SkillUp { get; set; }
}

/// <summary>
/// System for managing duck exploration and resource gathering.
/// </summary>
public class ExplorationSystem
{
    // =============================================================================
    // RESOURCE DEFINITIONS BY BIOME
    // (resource_id, name, quantity, regen_hours, skill_required)
    // =============================================================================

    private static readonly Dictionary<BiomeType, List<(string Id, string Name, int Qty, float Regen, int Skill)>> BiomeResources = new()
    {
        [BiomeType.Pond] = new()
        {
            ("reed", "Reed", 5, 2.0f, 0),
            ("pond_weed", "Pond Weed", 8, 1.0f, 0),
            ("small_fish", "Small Fish", 2, 4.0f, 2),
            ("frog_spawn", "Frog Spawn", 1, 24.0f, 3),
            ("lily_pad", "Lily Pad", 3, 6.0f, 1),
            ("pond_clay", "Pond Clay", 4, 3.0f, 1)
        },
        [BiomeType.Forest] = new()
        {
            ("twig", "Twig", 10, 1.0f, 0),
            ("leaf", "Leaf", 15, 0.5f, 0),
            ("bark", "Bark", 6, 2.0f, 1),
            ("acorn", "Acorn", 4, 3.0f, 0),
            ("mushroom", "Mushroom", 3, 4.0f, 1),
            ("berry", "Berry", 5, 2.0f, 0),
            ("pine_cone", "Pine Cone", 4, 3.0f, 0),
            ("feather", "Feather", 2, 6.0f, 0),
            ("moss", "Moss", 6, 2.0f, 1)
        },
        [BiomeType.Meadow] = new()
        {
            ("grass_blade", "Grass Blade", 20, 0.5f, 0),
            ("wildflower", "Wildflower", 8, 2.0f, 0),
            ("seed", "Seed", 10, 1.0f, 0),
            ("clover", "Clover", 6, 1.5f, 0),
            ("dandelion", "Dandelion", 5, 1.0f, 0),
            ("butterfly_wing", "Butterfly Wing", 1, 12.0f, 3),
            ("honeycomb", "Honeycomb", 1, 24.0f, 4)
        },
        [BiomeType.Riverside] = new()
        {
            ("pebble", "Pebble", 12, 1.0f, 0),
            ("smooth_stone", "Smooth Stone", 6, 2.0f, 1),
            ("shell", "Shell", 4, 3.0f, 0),
            ("driftwood", "Driftwood", 3, 4.0f, 1),
            ("clay", "Clay", 5, 2.0f, 1),
            ("sand", "Sand", 15, 0.5f, 0),
            ("river_pearl", "River Pearl", 1, 48.0f, 5)
        },
        [BiomeType.Garden] = new()
        {
            ("string", "String", 3, 4.0f, 0),
            ("fabric_scrap", "Fabric Scrap", 2, 6.0f, 0),
            ("vegetable_seed", "Vegetable Seed", 6, 2.0f, 0),
            ("garden_flower", "Garden Flower", 5, 2.0f, 0),
            ("worm", "Worm", 4, 1.0f, 0),
            ("bread_crumb", "Bread Crumb", 8, 1.0f, 0),
            ("shiny_button", "Shiny Button", 1, 12.0f, 2)
        },
        [BiomeType.Mountains] = new()
        {
            ("rock", "Rock", 10, 2.0f, 0),
            ("iron_ore", "Iron Ore", 2, 8.0f, 4),
            ("crystal", "Crystal", 1, 24.0f, 5),
            ("pine_needle", "Pine Needle", 12, 1.0f, 0),
            ("mountain_moss", "Mountain Moss", 5, 3.0f, 2),
            ("eagle_feather", "Eagle Feather", 1, 48.0f, 5)
        },
        [BiomeType.Beach] = new()
        {
            ("sea_shell", "Sea Shell", 8, 1.0f, 0),
            ("sea_glass", "Sea Glass", 3, 4.0f, 1),
            ("seaweed", "Seaweed", 10, 1.0f, 0),
            ("driftwood_large", "Large Driftwood", 2, 6.0f, 2),
            ("sand_dollar", "Sand Dollar", 2, 12.0f, 2),
            ("message_bottle", "Message in Bottle", 1, 72.0f, 4),
            ("treasure_chest", "Treasure Chest", 1, 168.0f, 6)  // Weekly!
        },
        [BiomeType.Swamp] = new()
        {
            ("swamp_reed", "Swamp Reed", 8, 1.5f, 0),
            ("bog_moss", "Bog Moss", 10, 1.0f, 0),
            ("firefly_jar", "Firefly Jar", 1, 8.0f, 2),
            ("murky_pearl", "Murky Pearl", 1, 24.0f, 4),
            ("ancient_bone", "Ancient Bone", 1, 48.0f, 3),
            ("glowing_mushroom", "Glowing Mushroom", 3, 6.0f, 2),
            ("cypress_bark", "Cypress Bark", 5, 3.0f, 1)
        },
        [BiomeType.Urban] = new()
        {
            ("bread_crumb", "Bread Crumb", 10, 0.5f, 0),
            ("lost_coin", "Lost Coin", 3, 4.0f, 0),
            ("shiny_wrapper", "Shiny Wrapper", 6, 1.0f, 0),
            ("park_flower", "Park Flower", 4, 2.0f, 0),
            ("dropped_fry", "Dropped Fry", 2, 2.0f, 0),
            ("fancy_button", "Fancy Button", 1, 12.0f, 2),
            ("lost_earring", "Lost Earring", 1, 48.0f, 4)
        }
    };

    // =============================================================================
    // AREA DEFINITIONS
    // =============================================================================

    private static readonly Dictionary<BiomeType, List<BiomeArea>> DefaultAreas = new()
    {
        [BiomeType.Pond] = new()
        {
            new BiomeArea
            {
                Biome = BiomeType.Pond,
                Name = "Home Pond",
                Description = "Your cozy home pond with grassy shores and calm waters.",
                DiscoveryChance = 0.05f,
                UnlockLevel = 1,
                IsDiscovered = true
            },
            new BiomeArea
            {
                Biome = BiomeType.Pond,
                Name = "Deep End",
                Description = "The mysterious deep part of the pond. What lurks below?",
                DiscoveryChance = 0.15f,
                UnlockLevel = 3
            }
        },
        [BiomeType.Forest] = new()
        {
            new BiomeArea
            {
                Biome = BiomeType.Forest,
                Name = "Forest Edge",
                Description = "Where the pond meets the forest. Lots of fallen twigs.",
                DiscoveryChance = 0.10f,
                UnlockLevel = 1,
                IsDiscovered = true
            },
            new BiomeArea
            {
                Biome = BiomeType.Forest,
                Name = "Ancient Oak",
                Description = "A massive old oak tree. Home to many creatures.",
                DiscoveryChance = 0.20f,
                UnlockLevel = 5
            },
            new BiomeArea
            {
                Biome = BiomeType.Forest,
                Name = "Mushroom Grove",
                Description = "A damp, shady area full of interesting fungi.",
                DiscoveryChance = 0.25f,
                UnlockLevel = 7
            }
        },
        [BiomeType.Meadow] = new()
        {
            new BiomeArea
            {
                Biome = BiomeType.Meadow,
                Name = "Sunny Meadow",
                Description = "A bright, flower-filled meadow buzzing with bees.",
                DiscoveryChance = 0.10f,
                UnlockLevel = 2
            },
            new BiomeArea
            {
                Biome = BiomeType.Meadow,
                Name = "Butterfly Garden",
                Description = "Rare butterflies dance among exotic flowers.",
                DiscoveryChance = 0.30f,
                UnlockLevel = 8
            }
        },
        [BiomeType.Riverside] = new()
        {
            new BiomeArea
            {
                Biome = BiomeType.Riverside,
                Name = "Pebble Beach",
                Description = "A calm section of river with smooth stones.",
                DiscoveryChance = 0.15f,
                UnlockLevel = 3
            },
            new BiomeArea
            {
                Biome = BiomeType.Riverside,
                Name = "Waterfall",
                Description = "A beautiful waterfall! Treasures wash up here.",
                DiscoveryChance = 0.35f,
                UnlockLevel = 10
            }
        },
        [BiomeType.Garden] = new()
        {
            new BiomeArea
            {
                Biome = BiomeType.Garden,
                Name = "Vegetable Patch",
                Description = "A human's garden. Full of useful scraps!",
                DiscoveryChance = 0.20f,
                UnlockLevel = 4
            },
            new BiomeArea
            {
                Biome = BiomeType.Garden,
                Name = "Tool Shed",
                Description = "The humans keep interesting things here...",
                DiscoveryChance = 0.40f,
                UnlockLevel = 12
            }
        },
        [BiomeType.Mountains] = new()
        {
            new BiomeArea
            {
                Biome = BiomeType.Mountains,
                Name = "Foothills",
                Description = "The base of the mountains. Rocky and wild.",
                DiscoveryChance = 0.20f,
                UnlockLevel = 15
            },
            new BiomeArea
            {
                Biome = BiomeType.Mountains,
                Name = "Crystal Cave",
                Description = "A hidden cave sparkling with crystals!",
                DiscoveryChance = 0.50f,
                UnlockLevel = 20
            }
        },
        [BiomeType.Beach] = new()
        {
            new BiomeArea
            {
                Biome = BiomeType.Beach,
                Name = "Sandy Shore",
                Description = "The ocean! So many shells and treasures.",
                DiscoveryChance = 0.25f,
                UnlockLevel = 18
            },
            new BiomeArea
            {
                Biome = BiomeType.Beach,
                Name = "Shipwreck Cove",
                Description = "An old shipwreck! Who knows what's inside?",
                DiscoveryChance = 0.60f,
                UnlockLevel = 25
            }
        },
        [BiomeType.Swamp] = new()
        {
            new BiomeArea
            {
                Biome = BiomeType.Swamp,
                Name = "Misty Marsh",
                Description = "Thick fog hangs over murky waters. Fireflies glow in the mist.",
                DiscoveryChance = 0.20f,
                UnlockLevel = 9
            },
            new BiomeArea
            {
                Biome = BiomeType.Swamp,
                Name = "Cypress Hollow",
                Description = "Ancient twisted trees draped in moss. Secrets hide here.",
                DiscoveryChance = 0.35f,
                UnlockLevel = 16
            },
            new BiomeArea
            {
                Biome = BiomeType.Swamp,
                Name = "Sunken Ruins",
                Description = "Mysterious old structures half-submerged in the bog.",
                DiscoveryChance = 0.55f,
                UnlockLevel = 24
            }
        },
        [BiomeType.Urban] = new()
        {
            new BiomeArea
            {
                Biome = BiomeType.Urban,
                Name = "Park Fountain",
                Description = "A busy city park! Humans drop all sorts of treasures.",
                DiscoveryChance = 0.15f,
                UnlockLevel = 6
            },
            new BiomeArea
            {
                Biome = BiomeType.Urban,
                Name = "Rooftop Garden",
                Description = "A hidden garden high above the city streets.",
                DiscoveryChance = 0.30f,
                UnlockLevel = 14
            },
            new BiomeArea
            {
                Biome = BiomeType.Urban,
                Name = "Storm Drain",
                Description = "Underground tunnels where lost things wash up.",
                DiscoveryChance = 0.50f,
                UnlockLevel = 22
            }
        }
    };

    // Rare items by biome
    private static readonly Dictionary<BiomeType, List<string>> RareItems = new()
    {
        [BiomeType.Pond] = new() { "Golden Scale", "Ancient Coin", "Frog Prince" },
        [BiomeType.Forest] = new() { "Fairy Dust", "Owl Pellet", "Magic Acorn" },
        [BiomeType.Meadow] = new() { "Rainbow Flower", "Bee Crown", "Lucky Clover" },
        [BiomeType.Riverside] = new() { "River Pearl", "Message Bottle", "Fish Bone" },
        [BiomeType.Garden] = new() { "Garden Gnome", "Lost Ring", "Magic Bean" },
        [BiomeType.Mountains] = new() { "Dragon Scale", "Star Crystal", "Thunder Stone" },
        [BiomeType.Beach] = new() { "Pirate Map", "Mermaid Scale", "Treasure Key" },
        [BiomeType.Swamp] = new() { "Will-o-Wisp", "Bog Amber", "Swamp Witch Charm" },
        [BiomeType.Urban] = new() { "Lucky Penny", "Diamond Ring", "Love Letter" }
    };

    // XP thresholds for skill levels
    private static readonly int[] SkillThresholds = { 0, 50, 150, 300, 500, 800, 1200, 1800, 2500, 3500 };

    // =============================================================================
    // STATE
    // =============================================================================

    public BiomeArea? CurrentArea { get; set; }
    public Dictionary<string, BiomeArea> DiscoveredAreas { get; set; } = new();
    public int GatheringSkill { get; set; } = 1;
    public int ExplorationXp { get; set; }
    public int TotalResourcesGathered { get; set; }
    public List<string> RareItemsFound { get; set; } = new();
    private DateTime _lastExploration = DateTime.MinValue;
    private readonly TimeSpan _explorationCooldown = TimeSpan.FromSeconds(30);
    private int _playerLevel = 1;

    // =============================================================================
    // INITIALIZATION
    // =============================================================================

    public ExplorationSystem()
    {
        InitializeAreas();
    }

    private void InitializeAreas()
    {
        foreach (var (biome, areas) in DefaultAreas)
        {
            foreach (var area in areas)
            {
                if (area.IsDiscovered)
                {
                    // Create a new instance to avoid modifying static data
                    var discovered = CloneArea(area);
                    PopulateAreaResources(discovered);
                    DiscoveredAreas[discovered.Name] = discovered;
                }
            }
        }

        // Set default starting location
        if (DiscoveredAreas.TryGetValue("Home Pond", out var homePond) && CurrentArea == null)
            CurrentArea = homePond;
    }

    private static BiomeArea CloneArea(BiomeArea source) => new()
    {
        Biome = source.Biome,
        Name = source.Name,
        Description = source.Description,
        DiscoveryChance = source.DiscoveryChance,
        UnlockLevel = source.UnlockLevel,
        IsDiscovered = source.IsDiscovered,
        TimesVisited = source.TimesVisited,
        Resources = new(),
        SpecialEvents = new(source.SpecialEvents)
    };

    private void PopulateAreaResources(BiomeArea area)
    {
        if (area.Resources.Count > 0)
            return;

        if (!BiomeResources.TryGetValue(area.Biome, out var resources))
            return;

        foreach (var (id, name, qty, regen, skill) in resources)
        {
            var startingQty = Random.Shared.Next(qty / 2 + 1, qty + 1);
            area.Resources.Add(new ResourceNode
            {
                ResourceId = id,
                Name = name,
                Quantity = startingQty,
                RegenTimeHours = regen,
                SkillRequired = skill
            });
        }
    }

    // =============================================================================
    // AREA ACCESS
    // =============================================================================

    public List<BiomeArea> GetAvailableAreas(int? playerLevel = null)
    {
        var level = playerLevel ?? _playerLevel;
        return DiscoveredAreas.Values
            .Where(a => a.UnlockLevel <= level)
            .ToList();
    }

    public List<BiomeArea> GetUndiscoveredAreas(int playerLevel)
    {
        var undiscovered = new List<BiomeArea>();
        foreach (var (_, areas) in DefaultAreas)
        {
            foreach (var area in areas)
            {
                if (!DiscoveredAreas.ContainsKey(area.Name) && area.UnlockLevel <= playerLevel)
                    undiscovered.Add(area);
            }
        }
        return undiscovered;
    }

    // =============================================================================
    // TRAVEL
    // =============================================================================

    public (bool Success, string Message) TravelTo(string areaName)
    {
        if (!DiscoveredAreas.TryGetValue(areaName, out var area))
            return (false, $"You haven't discovered {areaName} yet!");

        CurrentArea = area;
        CurrentArea.TimesVisited++;

        return (true, $"Traveled to {areaName}. {CurrentArea.Description}");
    }

    public (bool Success, string Message) TravelTo(BiomeArea area) => TravelTo(area.Name);

    // =============================================================================
    // EXPLORATION
    // =============================================================================

    public ExplorationResult Explore(int? playerLevel = null)
    {
        var now = DateTime.UtcNow;

        if (playerLevel.HasValue)
            _playerLevel = playerLevel.Value;

        // Check cooldown
        var timeSince = now - _lastExploration;
        if (timeSince < _explorationCooldown)
        {
            var remaining = (int)(_explorationCooldown - timeSince).TotalSeconds;
            return new ExplorationResult
            {
                Success = false,
                Message = $"Still tired from exploring... Wait {remaining}s"
            };
        }

        if (CurrentArea == null)
            TravelTo("Home Pond");

        _lastExploration = now;

        var result = new ExplorationResult
        {
            Success = true,
            XpGained = 5,
            BiomeName = CurrentArea?.Biome.ToString()
        };

        var area = CurrentArea!;
        var messages = new List<string>();

        // Gather some resources automatically
        var gatherable = area.Resources
            .Where(r => r.IsAvailable() && r.SkillRequired <= GatheringSkill)
            .ToList();

        if (gatherable.Count > 0)
        {
            var count = Math.Min(gatherable.Count, Random.Shared.Next(1, 4));
            var toGather = gatherable.OrderBy(_ => Random.Shared.Next()).Take(count);

            foreach (var resource in toGather)
            {
                var amount = resource.Gather(Random.Shared.Next(1, 3));
                if (amount > 0)
                {
                    result.ResourcesFound[resource.ResourceId] = amount;
                    TotalResourcesGathered += amount;
                    messages.Add($"Found {amount}x {resource.Name}!");
                }
            }
        }

        // Check for rare discovery
        if (Random.Shared.NextDouble() < area.DiscoveryChance)
        {
            if (RareItems.TryGetValue(area.Biome, out var rareList) && rareList.Count > 0)
            {
                var rareItem = rareList[Random.Shared.Next(rareList.Count)];
                result.RareDiscovery = rareItem;
                RareItemsFound.Add(rareItem);
                result.XpGained += 20;
                messages.Add($"✨ RARE FIND: {rareItem}!");
            }
        }

        // Check for new area discovery
        if (Random.Shared.NextDouble() < 0.1) // 10% chance
        {
            var undiscovered = GetUndiscoveredAreas(_playerLevel);
            if (undiscovered.Count > 0)
            {
                var newArea = undiscovered[Random.Shared.Next(undiscovered.Count)];
                DiscoverArea(newArea);
                result.NewAreaDiscovered = newArea.Name;
                result.XpGained += 50;
                messages.Add($"🗺️ Discovered new area: {newArea.Name}!");
            }
        }

        // Build final message
        if (messages.Count == 0)
            messages.Add($"Explored {area.Name} but didn't find much this time.");

        result.Message = string.Join(" ", messages);

        // Check for skill up
        var oldSkill = GatheringSkill;
        ExplorationXp += result.XpGained;
        CheckSkillUp();
        if (GatheringSkill > oldSkill)
            result.SkillUp = true;

        return result;
    }

    private void DiscoverArea(BiomeArea templateArea)
    {
        var area = CloneArea(templateArea);
        area.IsDiscovered = true;
        PopulateAreaResources(area);
        DiscoveredAreas[area.Name] = area;
    }

    // =============================================================================
    // RESOURCE GATHERING
    // =============================================================================

    public (int Gathered, string Message) GatherResource(string resourceId, int amount = 1)
    {
        if (CurrentArea == null)
            return (0, "You're not exploring any area!");

        var resource = CurrentArea.Resources.FirstOrDefault(r => r.ResourceId == resourceId);
        if (resource == null)
            return (0, $"No {resourceId} found in this area");

        if (resource.SkillRequired > GatheringSkill)
            return (0, $"Need gathering skill {resource.SkillRequired} for {resource.Name}!");

        if (!resource.IsAvailable())
        {
            if (resource.LastGathered.HasValue)
            {
                var hoursLeft = resource.RegenTimeHours - (DateTime.UtcNow - resource.LastGathered.Value).TotalHours;
                return (0, $"{resource.Name} is depleted. Regenerates in {hoursLeft:F1}h");
            }
        }

        var gathered = resource.Gather(amount);
        if (gathered > 0)
        {
            TotalResourcesGathered += gathered;
            return (gathered, $"Gathered {gathered}x {resource.Name}!");
        }

        return (0, $"Couldn't gather any {resource.Name}");
    }

    private void CheckSkillUp()
    {
        for (var level = 0; level < SkillThresholds.Length; level++)
        {
            if (ExplorationXp >= SkillThresholds[level])
                GatheringSkill = Math.Max(GatheringSkill, level + 1);
        }
    }

    // =============================================================================
    // DISPLAY
    // =============================================================================

    public string GetCurrentAreaInfo()
    {
        if (CurrentArea == null)
            return "Not currently exploring";

        var available = CurrentArea.Resources.Count(r => r.IsAvailable());
        var total = CurrentArea.Resources.Count;

        return $"📍 {CurrentArea.Name} ({CurrentArea.Biome})\n" +
               $"   {CurrentArea.Description}\n" +
               $"   Available resources: {available}/{total}\n" +
               $"   Visited: {CurrentArea.TimesVisited} times";
    }

    public List<string> RenderExplorationScreen()
    {
        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            "║            🗺️ EXPLORATION 🗺️                 ║",
            "╠═══════════════════════════════════════════════╣"
        };

        if (CurrentArea != null)
        {
            var name = CurrentArea.Name.Length > 25 ? CurrentArea.Name[..25] : CurrentArea.Name;
            lines.Add($"║  Current: {name,-30} ║");
            lines.Add($"║  Biome: {CurrentArea.Biome,-32} ║");
            lines.Add("╠═══════════════════════════════════════════════╣");
        }

        lines.Add($"║  Gathering Skill: {GatheringSkill,2}  |  XP: {ExplorationXp,-10} ║");
        lines.Add($"║  Resources Gathered: {TotalResourcesGathered,-18} ║");
        lines.Add($"║  Rare Items Found: {RareItemsFound.Count,-20} ║");
        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add("║  DISCOVERED AREAS:                            ║");

        foreach (var (name, area) in DiscoveredAreas.Take(5))
        {
            var shortName = name.Length > 25 ? name[..25] : name;
            var biome = area.Biome.ToString().ToLower();
            lines.Add($"║   • {shortName,-25} ({biome,-8}) ║");
        }

        if (DiscoveredAreas.Count > 5)
            lines.Add($"║   ... and {DiscoveredAreas.Count - 5} more areas              ║");

        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    // =============================================================================
    // SERIALIZATION
    // =============================================================================

    public ExplorationSaveData ToSaveData() => new()
    {
        CurrentArea = CurrentArea?.Name,
        DiscoveredAreas = DiscoveredAreas.Keys.ToList(),
        GatheringSkill = GatheringSkill,
        ExplorationXp = ExplorationXp,
        TotalResourcesGathered = TotalResourcesGathered,
        RareItemsFound = RareItemsFound
    };

    public static ExplorationSystem FromSaveData(ExplorationSaveData data)
    {
        var system = new ExplorationSystem
        {
            GatheringSkill = data.GatheringSkill > 0 ? data.GatheringSkill : 1,
            ExplorationXp = data.ExplorationXp,
            TotalResourcesGathered = data.TotalResourcesGathered,
            RareItemsFound = data.RareItemsFound ?? new()
        };

        // Clear default discovered areas and restore from save
        system.DiscoveredAreas.Clear();
        if (data.DiscoveredAreas != null)
        {
            foreach (var areaName in data.DiscoveredAreas)
            {
                // Find the template area
                foreach (var (_, areas) in DefaultAreas)
                {
                    var template = areas.FirstOrDefault(a => a.Name == areaName);
                    if (template != null)
                    {
                        var area = CloneArea(template);
                        area.IsDiscovered = true;
                        system.PopulateAreaResources(area);
                        system.DiscoveredAreas[area.Name] = area;
                        break;
                    }
                }
            }
        }

        // Ensure Home Pond is always discovered
        if (!system.DiscoveredAreas.ContainsKey("Home Pond"))
            system.InitializeAreas();

        // Restore current area
        if (!string.IsNullOrEmpty(data.CurrentArea) && system.DiscoveredAreas.ContainsKey(data.CurrentArea))
            system.CurrentArea = system.DiscoveredAreas[data.CurrentArea];
        else if (system.DiscoveredAreas.TryGetValue("Home Pond", out var home))
            system.CurrentArea = home;

        return system;
    }
}

/// <summary>
/// Save data for exploration system.
/// </summary>
public class ExplorationSaveData
{
    public string? CurrentArea { get; set; }
    public List<string>? DiscoveredAreas { get; set; }
    public int GatheringSkill { get; set; }
    public int ExplorationXp { get; set; }
    public int TotalResourcesGathered { get; set; }
    public List<string>? RareItemsFound { get; set; }
}
