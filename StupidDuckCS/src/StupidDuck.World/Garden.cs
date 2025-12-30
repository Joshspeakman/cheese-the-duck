using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.World
{
    /// <summary>
    /// Types of plants.
    /// </summary>
    public enum PlantType
    {
        Flower,
        Vegetable,
        Fruit,
        Herb,
        Special
    }

    /// <summary>
    /// Growth stages of plants.
    /// </summary>
    public enum PlantGrowthStage
    {
        Seed,
        Sprout,
        Growing,
        Mature,
        Flowering,
        Harvestable,
        Withered
    }

    /// <summary>
    /// Definition of a plant type.
    /// </summary>
    public class PlantDefinition
    {
        public string Id { get; set; } = "";
        public string Name { get; set; } = "";
        public string Description { get; set; } = "";
        public PlantType PlantType { get; set; }
        public double GrowthTimeHours { get; set; }
        public int WaterNeeds { get; set; } // 1-5
        public List<string> Seasons { get; set; } = new();
        public (int Min, int Max) HarvestAmount { get; set; }
        public string HarvestItem { get; set; } = "";
        public int XpValue { get; set; }
        public int CoinValue { get; set; }
        public string Rarity { get; set; } = "common";
        public Dictionary<PlantGrowthStage, List<string>> AsciiStages { get; set; } = new();
        public string FunFact { get; set; } = "";
    }

    /// <summary>
    /// A plant that has been planted.
    /// </summary>
    public class PlantedPlant
    {
        public string PlantId { get; set; } = "";
        public int PlotId { get; set; }
        public string PlantedAt { get; set; } = "";
        public string LastWatered { get; set; } = "";
        public PlantGrowthStage GrowthStage { get; set; } = PlantGrowthStage.Seed;
        public int WaterLevel { get; set; } = 100;
        public int Health { get; set; } = 100;
        public int TimesWatered { get; set; }
        public bool IsWithered { get; set; }

        public Dictionary<string, object> ToSaveData()
        {
            return new Dictionary<string, object>
            {
                ["plant_id"] = PlantId,
                ["plot_id"] = PlotId,
                ["planted_at"] = PlantedAt,
                ["last_watered"] = LastWatered,
                ["growth_stage"] = GrowthStage.ToString().ToLower(),
                ["water_level"] = WaterLevel,
                ["health"] = Health,
                ["times_watered"] = TimesWatered,
                ["is_withered"] = IsWithered
            };
        }

        public static PlantedPlant FromSaveData(Dictionary<string, object> data)
        {
            var plant = new PlantedPlant
            {
                PlantId = data.GetValueOrDefault("plant_id", "").ToString() ?? "",
                PlotId = Convert.ToInt32(data.GetValueOrDefault("plot_id", 0)),
                PlantedAt = data.GetValueOrDefault("planted_at", "").ToString() ?? "",
                LastWatered = data.GetValueOrDefault("last_watered", "").ToString() ?? "",
                WaterLevel = Convert.ToInt32(data.GetValueOrDefault("water_level", 100)),
                Health = Convert.ToInt32(data.GetValueOrDefault("health", 100)),
                TimesWatered = Convert.ToInt32(data.GetValueOrDefault("times_watered", 0)),
                IsWithered = Convert.ToBoolean(data.GetValueOrDefault("is_withered", false))
            };

            var stageStr = data.GetValueOrDefault("growth_stage", "seed").ToString() ?? "seed";
            plant.GrowthStage = Enum.TryParse<PlantGrowthStage>(stageStr, true, out var stage)
                ? stage : PlantGrowthStage.Seed;

            return plant;
        }
    }

    /// <summary>
    /// A single plot in the garden.
    /// </summary>
    public class GardenPlot
    {
        public int PlotId { get; set; }
        public PlantedPlant? Plant { get; set; }
        public bool IsUnlocked { get; set; } = true;
        public int SoilQuality { get; set; } = 100;
        public List<string> Decorations { get; set; } = new();
    }

    /// <summary>
    /// Seed information for purchasing.
    /// </summary>
    public class SeedInfo
    {
        public string PlantId { get; set; } = "";
        public int Cost { get; set; }
    }

    /// <summary>
    /// Result of a harvest operation.
    /// </summary>
    public class HarvestResult
    {
        public string Item { get; set; } = "";
        public int Amount { get; set; }
        public int Xp { get; set; }
        public int Coins { get; set; }
    }

    /// <summary>
    /// Garden statistics.
    /// </summary>
    public class GardenStats
    {
        public int TotalHarvests { get; set; }
        public Dictionary<string, int> PlantsGrown { get; set; } = new();
        public int UnlockedPlots { get; set; }
        public int ActivePlants { get; set; }
    }

    /// <summary>
    /// Garden system for planting and growing.
    /// </summary>
    public class GardenSystem
    {
        private static readonly Random _random = new();

        // Plant database
        public static readonly Dictionary<string, PlantDefinition> Plants = new()
        {
            // Flowers
            ["sunflower"] = new PlantDefinition
            {
                Id = "sunflower",
                Name = "Sunflower",
                Description = "A tall, cheerful flower that follows the sun!",
                PlantType = PlantType.Flower,
                GrowthTimeHours = 24.0,
                WaterNeeds = 2,
                Seasons = new List<string> { "spring", "summer" },
                HarvestAmount = (1, 3),
                HarvestItem = "sunflower_seeds",
                XpValue = 15,
                CoinValue = 10,
                Rarity = "common",
                AsciiStages = new Dictionary<PlantGrowthStage, List<string>>
                {
                    [PlantGrowthStage.Seed] = new() { "." },
                    [PlantGrowthStage.Sprout] = new() { "v" },
                    [PlantGrowthStage.Growing] = new() { "│", "v" },
                    [PlantGrowthStage.Mature] = new() { "│", "Y" },
                    [PlantGrowthStage.Flowering] = new() { "│", "🌻" },
                    [PlantGrowthStage.Harvestable] = new() { "│", "🌻✨" }
                },
                FunFact = "Sunflowers can grow up to 12 feet tall!"
            },
            ["tulip"] = new PlantDefinition
            {
                Id = "tulip",
                Name = "Tulip",
                Description = "A beautiful spring flower in many colors!",
                PlantType = PlantType.Flower,
                GrowthTimeHours = 18.0,
                WaterNeeds = 2,
                Seasons = new List<string> { "spring" },
                HarvestAmount = (1, 2),
                HarvestItem = "tulip_bulb",
                XpValue = 12,
                CoinValue = 8,
                Rarity = "common",
                AsciiStages = new Dictionary<PlantGrowthStage, List<string>>
                {
                    [PlantGrowthStage.Seed] = new() { "." },
                    [PlantGrowthStage.Sprout] = new() { "│" },
                    [PlantGrowthStage.Growing] = new() { "│", "│" },
                    [PlantGrowthStage.Mature] = new() { "│", "Y" },
                    [PlantGrowthStage.Flowering] = new() { "│", "🌷" },
                    [PlantGrowthStage.Harvestable] = new() { "│", "🌷✨" }
                },
                FunFact = "Tulip bulbs were once more valuable than gold!"
            },
            ["rose"] = new PlantDefinition
            {
                Id = "rose",
                Name = "Rose",
                Description = "The classic flower of love and beauty.",
                PlantType = PlantType.Flower,
                GrowthTimeHours = 36.0,
                WaterNeeds = 3,
                Seasons = new List<string> { "spring", "summer" },
                HarvestAmount = (1, 2),
                HarvestItem = "rose_petal",
                XpValue = 25,
                CoinValue = 20,
                Rarity = "uncommon",
                AsciiStages = new Dictionary<PlantGrowthStage, List<string>>
                {
                    [PlantGrowthStage.Seed] = new() { "." },
                    [PlantGrowthStage.Sprout] = new() { "┌" },
                    [PlantGrowthStage.Growing] = new() { "│", "┌" },
                    [PlantGrowthStage.Mature] = new() { "│", "Y" },
                    [PlantGrowthStage.Flowering] = new() { "│", "🌹" },
                    [PlantGrowthStage.Harvestable] = new() { "│", "🌹✨" }
                },
                FunFact = "Roses are related to apples, cherries, and almonds!"
            },

            // Vegetables
            ["carrot"] = new PlantDefinition
            {
                Id = "carrot",
                Name = "Carrot",
                Description = "A crunchy orange root vegetable!",
                PlantType = PlantType.Vegetable,
                GrowthTimeHours = 20.0,
                WaterNeeds = 2,
                Seasons = new List<string> { "spring", "fall" },
                HarvestAmount = (2, 5),
                HarvestItem = "carrot",
                XpValue = 10,
                CoinValue = 6,
                Rarity = "common",
                AsciiStages = new Dictionary<PlantGrowthStage, List<string>>
                {
                    [PlantGrowthStage.Seed] = new() { "." },
                    [PlantGrowthStage.Sprout] = new() { "~" },
                    [PlantGrowthStage.Growing] = new() { "~", "~~" },
                    [PlantGrowthStage.Mature] = new() { "~~~" },
                    [PlantGrowthStage.Harvestable] = new() { "🥕~~" }
                },
                FunFact = "Carrots were originally purple, not orange!"
            },
            ["tomato"] = new PlantDefinition
            {
                Id = "tomato",
                Name = "Tomato",
                Description = "A juicy red fruit (yes, fruit!) for salads!",
                PlantType = PlantType.Vegetable,
                GrowthTimeHours = 30.0,
                WaterNeeds = 3,
                Seasons = new List<string> { "summer" },
                HarvestAmount = (3, 8),
                HarvestItem = "tomato",
                XpValue = 15,
                CoinValue = 10,
                Rarity = "common",
                AsciiStages = new Dictionary<PlantGrowthStage, List<string>>
                {
                    [PlantGrowthStage.Seed] = new() { "." },
                    [PlantGrowthStage.Sprout] = new() { "v" },
                    [PlantGrowthStage.Growing] = new() { "│", "v" },
                    [PlantGrowthStage.Mature] = new() { "│", "Y" },
                    [PlantGrowthStage.Flowering] = new() { "│", "⚘" },
                    [PlantGrowthStage.Harvestable] = new() { "│", "🍅" }
                },
                FunFact = "Tomatoes were once thought to be poisonous!"
            },
            ["pumpkin"] = new PlantDefinition
            {
                Id = "pumpkin",
                Name = "Pumpkin",
                Description = "A big orange squash, perfect for fall!",
                PlantType = PlantType.Vegetable,
                GrowthTimeHours = 48.0,
                WaterNeeds = 3,
                Seasons = new List<string> { "fall" },
                HarvestAmount = (1, 3),
                HarvestItem = "pumpkin",
                XpValue = 30,
                CoinValue = 25,
                Rarity = "uncommon",
                AsciiStages = new Dictionary<PlantGrowthStage, List<string>>
                {
                    [PlantGrowthStage.Seed] = new() { "." },
                    [PlantGrowthStage.Sprout] = new() { "v" },
                    [PlantGrowthStage.Growing] = new() { "~~" },
                    [PlantGrowthStage.Mature] = new() { "~~o" },
                    [PlantGrowthStage.Harvestable] = new() { "~🎃" }
                },
                FunFact = "The largest pumpkin ever weighed over 2,700 pounds!"
            },

            // Fruits
            ["strawberry"] = new PlantDefinition
            {
                Id = "strawberry",
                Name = "Strawberry",
                Description = "Sweet, red, heart-shaped berries!",
                PlantType = PlantType.Fruit,
                GrowthTimeHours = 24.0,
                WaterNeeds = 3,
                Seasons = new List<string> { "spring", "summer" },
                HarvestAmount = (3, 8),
                HarvestItem = "strawberry",
                XpValue = 12,
                CoinValue = 8,
                Rarity = "common",
                AsciiStages = new Dictionary<PlantGrowthStage, List<string>>
                {
                    [PlantGrowthStage.Seed] = new() { "." },
                    [PlantGrowthStage.Sprout] = new() { "v" },
                    [PlantGrowthStage.Growing] = new() { "vv" },
                    [PlantGrowthStage.Flowering] = new() { "⚘" },
                    [PlantGrowthStage.Harvestable] = new() { "🍓🍓" }
                },
                FunFact = "Strawberries are the only fruit with seeds on the outside!"
            },
            ["watermelon"] = new PlantDefinition
            {
                Id = "watermelon",
                Name = "Watermelon",
                Description = "Big, refreshing summer fruit!",
                PlantType = PlantType.Fruit,
                GrowthTimeHours = 72.0,
                WaterNeeds = 4,
                Seasons = new List<string> { "summer" },
                HarvestAmount = (1, 2),
                HarvestItem = "watermelon",
                XpValue = 40,
                CoinValue = 35,
                Rarity = "uncommon",
                AsciiStages = new Dictionary<PlantGrowthStage, List<string>>
                {
                    [PlantGrowthStage.Seed] = new() { "." },
                    [PlantGrowthStage.Sprout] = new() { "v" },
                    [PlantGrowthStage.Growing] = new() { "~~" },
                    [PlantGrowthStage.Mature] = new() { "~~O" },
                    [PlantGrowthStage.Harvestable] = new() { "~🍉" }
                },
                FunFact = "Watermelon is 92% water!"
            },

            // Herbs
            ["mint"] = new PlantDefinition
            {
                Id = "mint",
                Name = "Mint",
                Description = "Fresh, aromatic herb that spreads quickly!",
                PlantType = PlantType.Herb,
                GrowthTimeHours = 16.0,
                WaterNeeds = 2,
                Seasons = new List<string> { "spring", "summer", "fall" },
                HarvestAmount = (5, 10),
                HarvestItem = "mint_leaves",
                XpValue = 8,
                CoinValue = 5,
                Rarity = "common",
                AsciiStages = new Dictionary<PlantGrowthStage, List<string>>
                {
                    [PlantGrowthStage.Seed] = new() { "." },
                    [PlantGrowthStage.Sprout] = new() { "v" },
                    [PlantGrowthStage.Growing] = new() { "vv" },
                    [PlantGrowthStage.Harvestable] = new() { "🌿🌿" }
                },
                FunFact = "Mint can help soothe an upset stomach!"
            },

            // Special plants
            ["golden_flower"] = new PlantDefinition
            {
                Id = "golden_flower",
                Name = "Golden Flower",
                Description = "A rare, magical flower that glows at night!",
                PlantType = PlantType.Special,
                GrowthTimeHours = 96.0,
                WaterNeeds = 4,
                Seasons = new List<string> { "any" },
                HarvestAmount = (1, 1),
                HarvestItem = "golden_petal",
                XpValue = 100,
                CoinValue = 100,
                Rarity = "legendary",
                AsciiStages = new Dictionary<PlantGrowthStage, List<string>>
                {
                    [PlantGrowthStage.Seed] = new() { "✧" },
                    [PlantGrowthStage.Sprout] = new() { "│", "✧" },
                    [PlantGrowthStage.Growing] = new() { "│", "❀" },
                    [PlantGrowthStage.Mature] = new() { "│", "❁" },
                    [PlantGrowthStage.Flowering] = new() { "│", "✿" },
                    [PlantGrowthStage.Harvestable] = new() { "│", "🌟" }
                },
                FunFact = "Legend says this flower only blooms once every century!"
            },
            ["crystal_plant"] = new PlantDefinition
            {
                Id = "crystal_plant",
                Name = "Crystal Plant",
                Description = "A mysterious plant made of pure crystal!",
                PlantType = PlantType.Special,
                GrowthTimeHours = 120.0,
                WaterNeeds = 5,
                Seasons = new List<string> { "winter" },
                HarvestAmount = (1, 2),
                HarvestItem = "crystal_shard",
                XpValue = 150,
                CoinValue = 150,
                Rarity = "legendary",
                AsciiStages = new Dictionary<PlantGrowthStage, List<string>>
                {
                    [PlantGrowthStage.Seed] = new() { "◇" },
                    [PlantGrowthStage.Sprout] = new() { "◇", "◇" },
                    [PlantGrowthStage.Growing] = new() { "◇", "◆" },
                    [PlantGrowthStage.Mature] = new() { "◆", "◆" },
                    [PlantGrowthStage.Harvestable] = new() { "💎", "✨" }
                },
                FunFact = "Crystal plants only grow in the coldest conditions!"
            }
        };

        // Seeds available in shop
        public static readonly Dictionary<string, SeedInfo> Seeds = new()
        {
            ["sunflower_seeds"] = new SeedInfo { PlantId = "sunflower", Cost = 5 },
            ["tulip_seeds"] = new SeedInfo { PlantId = "tulip", Cost = 5 },
            ["rose_seeds"] = new SeedInfo { PlantId = "rose", Cost = 15 },
            ["carrot_seeds"] = new SeedInfo { PlantId = "carrot", Cost = 3 },
            ["tomato_seeds"] = new SeedInfo { PlantId = "tomato", Cost = 5 },
            ["pumpkin_seeds"] = new SeedInfo { PlantId = "pumpkin", Cost = 10 },
            ["strawberry_seeds"] = new SeedInfo { PlantId = "strawberry", Cost = 8 },
            ["watermelon_seeds"] = new SeedInfo { PlantId = "watermelon", Cost = 15 },
            ["mint_seeds"] = new SeedInfo { PlantId = "mint", Cost = 4 },
            ["golden_seeds"] = new SeedInfo { PlantId = "golden_flower", Cost = 200 },
            ["crystal_seeds"] = new SeedInfo { PlantId = "crystal_plant", Cost = 250 }
        };

        // Instance fields
        public Dictionary<int, GardenPlot> Plots { get; private set; } = new();
        public int MaxPlots { get; } = 4;
        public int UnlockedPlots { get; private set; } = 2;
        public Dictionary<string, int> SeedInventory { get; private set; } = new();
        public Dictionary<string, int> HarvestInventory { get; private set; } = new();
        public int TotalHarvests { get; private set; }
        public Dictionary<string, int> PlantsGrown { get; private set; } = new();

        public GardenSystem()
        {
            // Initialize plots
            for (int i = 0; i < MaxPlots; i++)
            {
                Plots[i] = new GardenPlot
                {
                    PlotId = i,
                    IsUnlocked = i < UnlockedPlots
                };
            }

            // Starting seeds
            SeedInventory["sunflower_seeds"] = 3;
            SeedInventory["carrot_seeds"] = 3;
        }

        /// <summary>
        /// Get current season based on date.
        /// </summary>
        public string GetCurrentSeason()
        {
            int month = DateTime.Now.Month;
            return month switch
            {
                >= 3 and <= 5 => "spring",
                >= 6 and <= 8 => "summer",
                >= 9 and <= 11 => "fall",
                _ => "winter"
            };
        }

        /// <summary>
        /// Plant a seed in a plot.
        /// </summary>
        public (bool Success, string Message) PlantSeed(int plotId, string seedId)
        {
            if (!Plots.TryGetValue(plotId, out var plot))
                return (false, "Invalid plot!");

            if (!plot.IsUnlocked)
                return (false, "This plot is locked!");

            if (plot.Plant != null)
                return (false, "This plot already has a plant!");

            if (!SeedInventory.TryGetValue(seedId, out var count) || count <= 0)
                return (false, $"You don't have any {seedId}!");

            if (!Seeds.TryGetValue(seedId, out var seedInfo))
                return (false, "Invalid seed!");

            if (!Plants.TryGetValue(seedInfo.PlantId, out var plantDef))
                return (false, "Unknown plant!");

            // Check season
            string season = GetCurrentSeason();
            if (!plantDef.Seasons.Contains("any") && !plantDef.Seasons.Contains(season))
                return (false, $"{plantDef.Name} doesn't grow in {season}!");

            // Plant the seed
            SeedInventory[seedId]--;
            string now = DateTime.Now.ToString("o");

            plot.Plant = new PlantedPlant
            {
                PlantId = plantDef.Id,
                PlotId = plotId,
                PlantedAt = now,
                LastWatered = now,
                GrowthStage = PlantGrowthStage.Seed
            };

            return (true, $"Planted {plantDef.Name}! 🌱");
        }

        /// <summary>
        /// Water a plant.
        /// </summary>
        public (bool Success, string Message) WaterPlant(int plotId)
        {
            if (!Plots.TryGetValue(plotId, out var plot))
                return (false, "Invalid plot!");

            if (plot.Plant == null)
                return (false, "No plant to water!");

            var plant = plot.Plant;
            if (plant.IsWithered)
                return (false, "This plant has withered... 😢");

            plant.WaterLevel = Math.Min(100, plant.WaterLevel + 50);
            plant.LastWatered = DateTime.Now.ToString("o");
            plant.TimesWatered++;

            return (true, "Watered the plant! 💧");
        }

        /// <summary>
        /// Update all plants based on time passed.
        /// </summary>
        public void UpdatePlants(double deltaHours)
        {
            foreach (var plot in Plots.Values)
            {
                if (plot.Plant == null)
                    continue;

                var plant = plot.Plant;
                if (!Plants.TryGetValue(plant.PlantId, out var plantDef))
                    continue;

                // Decrease water level
                double waterDecrease = plantDef.WaterNeeds * deltaHours * 5;
                plant.WaterLevel = Math.Max(0, plant.WaterLevel - (int)waterDecrease);

                // Check for withering
                if (plant.WaterLevel <= 0)
                {
                    plant.Health -= (int)(deltaHours * 10);
                    if (plant.Health <= 0)
                    {
                        plant.IsWithered = true;
                        plant.GrowthStage = PlantGrowthStage.Withered;
                    }
                }
                else
                {
                    plant.Health = Math.Min(100, plant.Health + (int)(deltaHours * 2));
                }

                // Growth progress
                if (!plant.IsWithered && plant.WaterLevel > 20)
                {
                    if (DateTime.TryParse(plant.PlantedAt, out var plantedTime))
                    {
                        double hoursSincePlanting = (DateTime.Now - plantedTime).TotalHours;
                        double growthPercent = hoursSincePlanting / plantDef.GrowthTimeHours;

                        // Determine growth stage
                        if (growthPercent >= 1.0)
                            plant.GrowthStage = PlantGrowthStage.Harvestable;
                        else if (growthPercent >= 0.8)
                            plant.GrowthStage = plantDef.PlantType == PlantType.Flower
                                ? PlantGrowthStage.Flowering : PlantGrowthStage.Mature;
                        else if (growthPercent >= 0.5)
                            plant.GrowthStage = PlantGrowthStage.Mature;
                        else if (growthPercent >= 0.3)
                            plant.GrowthStage = PlantGrowthStage.Growing;
                        else if (growthPercent >= 0.1)
                            plant.GrowthStage = PlantGrowthStage.Sprout;
                    }
                }
            }
        }

        /// <summary>
        /// Harvest a mature plant.
        /// </summary>
        public (bool Success, string Message, HarvestResult? Result) HarvestPlant(int plotId)
        {
            if (!Plots.TryGetValue(plotId, out var plot))
                return (false, "Invalid plot!", null);

            if (plot.Plant == null)
                return (false, "No plant to harvest!", null);

            var plant = plot.Plant;
            if (plant.GrowthStage != PlantGrowthStage.Harvestable)
                return (false, "Plant is not ready to harvest!", null);

            if (!Plants.TryGetValue(plant.PlantId, out var plantDef))
                return (false, "Unknown plant!", null);

            // Calculate harvest amount
            int amount = _random.Next(plantDef.HarvestAmount.Min, plantDef.HarvestAmount.Max + 1);

            // Bonus for well-watered plants
            if (plant.TimesWatered >= plantDef.WaterNeeds * 2)
                amount++;

            string harvestItem = plantDef.HarvestItem;
            HarvestInventory[harvestItem] = HarvestInventory.GetValueOrDefault(harvestItem) + amount;
            TotalHarvests++;
            PlantsGrown[plant.PlantId] = PlantsGrown.GetValueOrDefault(plant.PlantId) + 1;

            // Clear the plot
            plot.Plant = null;

            var result = new HarvestResult
            {
                Item = harvestItem,
                Amount = amount,
                Xp = plantDef.XpValue,
                Coins = plantDef.CoinValue * amount
            };

            return (true, $"Harvested {amount} {plantDef.Name}! 🌾", result);
        }

        /// <summary>
        /// Remove a plant (including withered ones).
        /// </summary>
        public (bool Success, string Message) RemovePlant(int plotId)
        {
            if (!Plots.TryGetValue(plotId, out var plot))
                return (false, "Invalid plot!");

            if (plot.Plant == null)
                return (false, "No plant to remove!");

            plot.Plant = null;
            return (true, "Removed the plant.");
        }

        /// <summary>
        /// Unlock a new garden plot.
        /// </summary>
        public (bool Success, string Message) UnlockPlot(int plotId)
        {
            if (!Plots.TryGetValue(plotId, out var plot))
                return (false, "Invalid plot!");

            if (plot.IsUnlocked)
                return (false, "Plot already unlocked!");

            plot.IsUnlocked = true;
            UnlockedPlots++;
            return (true, "Unlocked new garden plot! 🌱");
        }

        /// <summary>
        /// Add seeds to inventory.
        /// </summary>
        public void AddSeeds(string seedId, int amount)
        {
            SeedInventory[seedId] = SeedInventory.GetValueOrDefault(seedId) + amount;
        }

        /// <summary>
        /// Render the garden display.
        /// </summary>
        public List<string> RenderGarden()
        {
            var lines = new List<string>
            {
                "╔═══════════════════════════════════════╗",
                "║         🌻 YOUR GARDEN 🌻              ║",
                $"║  Season: {char.ToUpper(GetCurrentSeason()[0]) + GetCurrentSeason()[1..],-12}              ║",
                "╠═══════════════════════════════════════╣"
            };

            foreach (var (plotId, plot) in Plots)
            {
                if (!plot.IsUnlocked)
                {
                    lines.Add($"║ Plot {plotId + 1}: [LOCKED] 🔒              ║");
                    continue;
                }

                if (plot.Plant == null)
                {
                    lines.Add($"║ Plot {plotId + 1}: [Empty] - Ready to plant  ║");
                }
                else
                {
                    var plant = plot.Plant;
                    if (Plants.TryGetValue(plant.PlantId, out var plantDef))
                    {
                        string stage = plant.GrowthStage.ToString().ToLower();
                        string water = plant.WaterLevel > 0
                            ? string.Concat(Enumerable.Repeat("~", plant.WaterLevel / 25))
                            : "dry";
                        string art = plantDef.AsciiStages.TryGetValue(plant.GrowthStage, out var stages)
                            ? stages.Last() : "?";

                        string name = plantDef.Name.Length > 10
                            ? plantDef.Name[..10] : plantDef.Name;
                        lines.Add($"| Plot {plotId + 1}: {art} {name,-10} {water,-4} |");
                        lines.Add($"|         Stage: {stage,-15}       |");
                    }
                }
            }

            lines.Add("╠═══════════════════════════════════════╣");
            lines.Add("║ [P]lant [W]ater [H]arvest [R]emove    ║");
            lines.Add("╚═══════════════════════════════════════╝");

            return lines;
        }

        /// <summary>
        /// Get garden statistics.
        /// </summary>
        public GardenStats GetStats()
        {
            return new GardenStats
            {
                TotalHarvests = TotalHarvests,
                PlantsGrown = new Dictionary<string, int>(PlantsGrown),
                UnlockedPlots = UnlockedPlots,
                ActivePlants = Plots.Values.Count(p => p.Plant != null)
            };
        }

        /// <summary>
        /// Convert to dictionary for saving.
        /// </summary>
        public Dictionary<string, object> ToSaveData()
        {
            var plotsData = new Dictionary<string, object>();
            foreach (var (pid, plot) in Plots)
            {
                plotsData[pid.ToString()] = new Dictionary<string, object>
                {
                    ["plot_id"] = plot.PlotId,
                    ["is_unlocked"] = plot.IsUnlocked,
                    ["soil_quality"] = plot.SoilQuality,
                    ["plant"] = plot.Plant?.ToSaveData()!
                };
            }

            return new Dictionary<string, object>
            {
                ["plots"] = plotsData,
                ["seed_inventory"] = new Dictionary<string, int>(SeedInventory),
                ["harvest_inventory"] = new Dictionary<string, int>(HarvestInventory),
                ["total_harvests"] = TotalHarvests,
                ["plants_grown"] = new Dictionary<string, int>(PlantsGrown),
                ["unlocked_plots"] = UnlockedPlots
            };
        }

        /// <summary>
        /// Create from dictionary.
        /// </summary>
        public static GardenSystem FromSaveData(Dictionary<string, object> data)
        {
            var garden = new GardenSystem();

            if (data.TryGetValue("plots", out var plotsObj) && plotsObj is Dictionary<string, object> plotsData)
            {
                foreach (var (pidStr, plotDataObj) in plotsData)
                {
                    if (int.TryParse(pidStr, out int pid) && garden.Plots.ContainsKey(pid) &&
                        plotDataObj is Dictionary<string, object> plotData)
                    {
                        var plot = garden.Plots[pid];
                        plot.IsUnlocked = Convert.ToBoolean(plotData.GetValueOrDefault("is_unlocked", false));
                        plot.SoilQuality = Convert.ToInt32(plotData.GetValueOrDefault("soil_quality", 100));

                        if (plotData.TryGetValue("plant", out var plantObj) &&
                            plantObj is Dictionary<string, object> plantData)
                        {
                            plot.Plant = PlantedPlant.FromSaveData(plantData);
                        }
                    }
                }
            }

            if (data.TryGetValue("seed_inventory", out var seedObj) && seedObj is Dictionary<string, int> seeds)
                garden.SeedInventory = new Dictionary<string, int>(seeds);

            if (data.TryGetValue("harvest_inventory", out var harvestObj) && harvestObj is Dictionary<string, int> harvests)
                garden.HarvestInventory = new Dictionary<string, int>(harvests);

            garden.TotalHarvests = Convert.ToInt32(data.GetValueOrDefault("total_harvests", 0));

            if (data.TryGetValue("plants_grown", out var grownObj) && grownObj is Dictionary<string, int> grown)
                garden.PlantsGrown = new Dictionary<string, int>(grown);

            garden.UnlockedPlots = Convert.ToInt32(data.GetValueOrDefault("unlocked_plots", 2));

            return garden;
        }
    }
}
