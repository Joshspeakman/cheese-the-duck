using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.World
{
    /// <summary>
    /// Types of dreams the duck can have.
    /// </summary>
    public enum DreamType
    {
        Adventure,
        Flying,
        Food,
        Friend,
        Nightmare,
        Memory,
        Prophetic,
        Silly,
        Peaceful
    }

    /// <summary>
    /// A single dream sequence.
    /// </summary>
    public class Dream
    {
        public DreamType DreamType { get; set; }
        public string Title { get; set; } = "";
        public List<string> Scenes { get; set; } = new();
        public int MoodEffect { get; set; }
        public string? SpecialReward { get; set; }
        public int XpBonus { get; set; }
        public bool IsRecurring { get; set; }
    }

    /// <summary>
    /// Result of a dream sequence.
    /// </summary>
    public class DreamResult
    {
        public Dream Dream { get; set; } = new();
        public List<string> ScenesShown { get; set; } = new();
        public int MoodEffect { get; set; }
        public int XpEarned { get; set; }
        public string? SpecialReward { get; set; }
        public string Message { get; set; } = "";
    }

    /// <summary>
    /// Manages duck dreams during sleep.
    /// </summary>
    public class DreamSystem
    {
        private static readonly Random _random = new();

        // All dreams database
        public static readonly Dictionary<DreamType, List<Dream>> Dreams = new()
        {
            [DreamType.Adventure] = new List<Dream>
            {
                new Dream
                {
                    DreamType = DreamType.Adventure,
                    Title = "The Great Bread Quest",
                    Scenes = new()
                    {
                        "Cheese is in a desert. It's made of bread. Sure.",
                        "A mountain of sourdough loaves blocks the path.",
                        "Cheese climbs it anyway. Takes about three hours.",
                        "At the summit: more bread. Cheese is not surprised.",
                        "Eats some. It's fine. Tastes like bread.",
                        "Quest complete. Nothing has fundamentally changed."
                    },
                    MoodEffect = 10, XpBonus = 5
                },
                new Dream
                {
                    DreamType = DreamType.Adventure,
                    Title = "Pirate Duck",
                    Scenes = new()
                    {
                        "Cheese is on a boat. Cheese did not ask for this.",
                        "The ocean is suspiciously calm. Too calm.",
                        "A treasure map appears. The X is where Cheese is standing.",
                        "Cheese digs. Finds a smaller boat. Okay.",
                        "The smaller boat also has a treasure map.",
                        "This is going to take a while."
                    },
                    MoodEffect = 8, XpBonus = 3, SpecialReward = "treasure_map"
                },
                new Dream
                {
                    DreamType = DreamType.Adventure,
                    Title = "Space Duck",
                    Scenes = new()
                    {
                        "Cheese is in space now. Nobody explained how.",
                        "There are stars. They're just... there.",
                        "An alien duck waves. Cheese waves back. Professional courtesy.",
                        "The moon is closer than expected. Smells like cheese.",
                        "Not the duck. The other cheese. Dairy cheese.",
                        "Cheese wakes up confused about identity."
                    },
                    MoodEffect = 12, XpBonus = 5
                },
                new Dream
                {
                    DreamType = DreamType.Adventure,
                    Title = "The Cave",
                    Scenes = new()
                    {
                        "There's a cave. Cheese enters. Standard procedure.",
                        "It's dark. Cheese can still see somehow. Dream logic.",
                        "A dragon appears. It's the size of a potato.",
                        "The dragon asks for directions. Cheese doesn't know any.",
                        "They sit in awkward silence for a while.",
                        "Cheese leaves. The dragon stays. Life goes on."
                    },
                    MoodEffect = 7, XpBonus = 3
                }
            },
            [DreamType.Flying] = new List<Dream>
            {
                new Dream
                {
                    DreamType = DreamType.Flying,
                    Title = "Cloud Surfing",
                    Scenes = new()
                    {
                        "Cheese's wings work now. They usually don't. Suspicious.",
                        "Flying is exactly as advertised. You go up.",
                        "A cloud passes by. Cheese sits on it. It holds.",
                        "Other birds fly past. They seem busy.",
                        "Cheese is not busy. Cheese is sitting on a cloud.",
                        "This is fine."
                    },
                    MoodEffect = 15, XpBonus = 3
                },
                new Dream
                {
                    DreamType = DreamType.Flying,
                    Title = "Rainbow Rider",
                    Scenes = new()
                    {
                        "A rainbow appears. Cheese gets on it. As one does.",
                        "It's a slide now. Cheese didn't consent to this.",
                        "The colors blur together. Everything is briefly purple.",
                        "At the bottom: a pot of corn. Not gold. Corn.",
                        "Cheese eats some. It's fine."
                    },
                    MoodEffect = 20, XpBonus = 5, SpecialReward = "rainbow_feather"
                },
                new Dream
                {
                    DreamType = DreamType.Flying,
                    Title = "Just Falling",
                    Scenes = new()
                    {
                        "Cheese is falling. Not flying. Just falling.",
                        "The ground approaches. Then recedes. Then approaches again.",
                        "This has been happening for some time now.",
                        "A passing bird asks if Cheese needs help.",
                        "Cheese says no. Pride is important.",
                        "Still falling. Might be falling forever. It's fine."
                    },
                    MoodEffect = 5, XpBonus = 2
                }
            },
            [DreamType.Food] = new List<Dream>
            {
                new Dream
                {
                    DreamType = DreamType.Food,
                    Title = "Bread Paradise",
                    Scenes = new()
                    {
                        "Everything is bread. The ground. The sky. Cheese.",
                        "Wait, Cheese is not bread. False alarm.",
                        "The trees are baguettes. They're just standing there.",
                        "Cheese eats a doorknob. It's a croissant. Of course it is.",
                        "Wakes up hungry. Dreams don't count as eating."
                    },
                    MoodEffect = 10, XpBonus = 2
                },
                new Dream
                {
                    DreamType = DreamType.Food,
                    Title = "The Infinite Feast",
                    Scenes = new()
                    {
                        "A table stretches to infinity. Standard dream stuff.",
                        "Every food exists here. Even the weird ones.",
                        "Cheese eats. Then eats more. Then continues eating.",
                        "Still not full. Concerning but not unpleasant.",
                        "A waiter appears. Asks if everything is okay.",
                        "Cheese nods. The waiter vanishes. Cheese keeps eating."
                    },
                    MoodEffect = 8, XpBonus = 2
                },
                new Dream
                {
                    DreamType = DreamType.Food,
                    Title = "The Last Crumb",
                    Scenes = new()
                    {
                        "There is one crumb. Just one. In the whole world.",
                        "Cheese approaches. The crumb doesn't move. It's a crumb.",
                        "Dramatic music plays from nowhere.",
                        "Cheese eats it. It's a crumb. It tastes like crumb.",
                        "More crumbs appear. Crisis averted.",
                        "Cheese wakes up feeling accomplished."
                    },
                    MoodEffect = 6, XpBonus = 1
                }
            },
            [DreamType.Friend] = new List<Dream>
            {
                new Dream
                {
                    DreamType = DreamType.Friend,
                    Title = "Best Friends Forever",
                    Scenes = new()
                    {
                        "All of Cheese's friends are here. Even the imaginary ones.",
                        "Everyone is talking at once. Cheese hears none of it.",
                        "Gerald tells a joke. Nobody laughs. It wasn't funny.",
                        "They all agree it wasn't funny. Friendship prevails.",
                        "Everyone shares snacks. Cheese takes too many.",
                        "No one mentions it. True friendship."
                    },
                    MoodEffect = 15, XpBonus = 3
                },
                new Dream
                {
                    DreamType = DreamType.Friend,
                    Title = "Memory Lane",
                    Scenes = new()
                    {
                        "There's a road. It's made of memories. Somehow.",
                        "Cheese steps on a birthday. It squishes.",
                        "There's the first friend. They wave. Cheese waves.",
                        "This continues for several memories.",
                        "At the end: another road. Memory Boulevard, probably.",
                        "Cheese turns back. That's enough nostalgia."
                    },
                    MoodEffect = 12, XpBonus = 2
                },
                new Dream
                {
                    DreamType = DreamType.Friend,
                    Title = "The Reunion",
                    Scenes = new()
                    {
                        "Everyone Cheese has ever met is in one room.",
                        "It's very crowded. Fire hazard, probably.",
                        "Nobody knows why they're here. Standard reunion.",
                        "Someone brought a casserole. Nobody eats it.",
                        "Cheese stands near the snack table. Strategy.",
                        "The dream ends. The casserole remains uneaten."
                    },
                    MoodEffect = 10, XpBonus = 2
                }
            },
            [DreamType.Nightmare] = new List<Dream>
            {
                new Dream
                {
                    DreamType = DreamType.Nightmare,
                    Title = "The Empty Pond",
                    Scenes = new()
                    {
                        "The pond is empty. Not of water. Of everyone.",
                        "Cheese walks around. Footsteps echo. Dramatic.",
                        "A shape appears in the distance. Hope rises.",
                        "It's a rock. Hope sits back down.",
                        "Cheese wakes up. The pond is fine. Everyone is there.",
                        "Cheese checks anyway. Just in case."
                    },
                    MoodEffect = -5, XpBonus = 1
                },
                new Dream
                {
                    DreamType = DreamType.Nightmare,
                    Title = "Bread Shortage",
                    Scenes = new()
                    {
                        "No bread. Anywhere. This is serious.",
                        "Cheese checks everywhere. Under rocks. In clouds.",
                        "The bakery is closed. The baker is also missing.",
                        "One crumb appears. Cheese guards it with their life.",
                        "More bread appears. The shortage is over.",
                        "Cheese is relieved. Also hungry."
                    },
                    MoodEffect = 2, XpBonus = 2
                },
                new Dream
                {
                    DreamType = DreamType.Nightmare,
                    Title = "The Endless Meeting",
                    Scenes = new()
                    {
                        "Cheese is in a meeting. It has no agenda.",
                        "Someone is talking about synergy. Cheese tunes out.",
                        "The clock doesn't move. It never moves.",
                        "There's no door. There was one earlier. Gone now.",
                        "Coffee appears. It's decaf. The horror.",
                        "Cheese wakes up grateful for consciousness."
                    },
                    MoodEffect = -3, XpBonus = 1
                }
            },
            [DreamType.Memory] = new List<Dream>
            {
                new Dream
                {
                    DreamType = DreamType.Memory,
                    Title = "First Day Home",
                    Scenes = new()
                    {
                        "Cheese remembers hatching. It was Tuesday.",
                        "The world was big. It still is. That hasn't changed.",
                        "Someone offered food. Cheese accepted. Good start.",
                        "Everything was new. Now some things are old.",
                        "Home was here then. Home is here now. Consistent.",
                        "Cheese appreciates the lack of surprises."
                    },
                    MoodEffect = 10, XpBonus = 3
                },
                new Dream
                {
                    DreamType = DreamType.Memory,
                    Title = "Yesterday",
                    Scenes = new()
                    {
                        "Cheese remembers yesterday. It was yesterday.",
                        "Things happened. Cheese was there for most of them.",
                        "There was food. It was eaten. Standard procedure.",
                        "Someone said hello. Cheese said it back.",
                        "Then it was night. Now it's this dream.",
                        "Tomorrow will probably also happen."
                    },
                    MoodEffect = 5, XpBonus = 1
                }
            },
            [DreamType.Prophetic] = new List<Dream>
            {
                new Dream
                {
                    DreamType = DreamType.Prophetic,
                    Title = "Vision of Tomorrow",
                    Scenes = new()
                    {
                        "The dream feels different. More... prophetic.",
                        "Cheese sees the future. It looks a lot like the present.",
                        "A friend will arrive. Or maybe a package. Hard to tell.",
                        "Something will be discovered. Could be anything.",
                        "The future is bright. There's adequate lighting.",
                        "Cheese will remember none of this. Classic prophecy."
                    },
                    MoodEffect = 8, XpBonus = 5, SpecialReward = "lucky_charm"
                },
                new Dream
                {
                    DreamType = DreamType.Prophetic,
                    Title = "The Warning",
                    Scenes = new()
                    {
                        "A mysterious voice speaks. It says 'beware.'",
                        "Beware of what? The voice doesn't specify.",
                        "Cheese waits for more information. None comes.",
                        "The voice clears its throat. Still no details.",
                        "'Just... beware in general,' it finally says.",
                        "Cheese will try. No promises."
                    },
                    MoodEffect = 6, XpBonus = 3
                }
            },
            [DreamType.Silly] = new List<Dream>
            {
                new Dream
                {
                    DreamType = DreamType.Silly,
                    Title = "Upside Down World",
                    Scenes = new()
                    {
                        "Gravity reversed. Cheese is on the ceiling now.",
                        "The furniture doesn't care. It's on the ceiling too.",
                        "Walking is the same but in the other direction.",
                        "A fish swims by. Through the air. It doesn't explain.",
                        "Cheese quacks. It comes out backwards. 'Kcauq.'",
                        "Normal enough. Cheese goes back to sleep."
                    },
                    MoodEffect = 8, XpBonus = 1
                },
                new Dream
                {
                    DreamType = DreamType.Silly,
                    Title = "Giant Cheese (the Duck)",
                    Scenes = new()
                    {
                        "Cheese is growing. This wasn't planned.",
                        "Now Cheese is taller than a tree. Inconvenient.",
                        "The tiny ducks below look up. They seem concerned.",
                        "Cheese tries to reassure them. Voice is too loud.",
                        "Everyone just nods and walks away slowly.",
                        "Cheese shrinks back. Nobody mentions it again."
                    },
                    MoodEffect = 6, XpBonus = 1
                },
                new Dream
                {
                    DreamType = DreamType.Silly,
                    Title = "The Talking Hat",
                    Scenes = new()
                    {
                        "The hat is talking. It hasn't before. Odd.",
                        "'I've been watching,' it says. Cheese is uncomfortable.",
                        "The hat tells a joke. It's about ducks. It's mediocre.",
                        "Cheese laughs politely. The hat seems satisfied.",
                        "'Same time tomorrow?' the hat asks.",
                        "Cheese pretends not to hear. Wakes up."
                    },
                    MoodEffect = 10, XpBonus = 2
                },
                new Dream
                {
                    DreamType = DreamType.Silly,
                    Title = "Tax Season",
                    Scenes = new()
                    {
                        "Cheese is filing taxes. In the dream.",
                        "This is unprecedented. Ducks don't pay taxes.",
                        "The forms are blank. All of them. Every box.",
                        "Cheese signs them anyway. Compliance.",
                        "A stamp appears. It says 'APPROVED.'",
                        "Cheese wakes up feeling oddly responsible."
                    },
                    MoodEffect = 4, XpBonus = 1
                }
            },
            [DreamType.Peaceful] = new List<Dream>
            {
                new Dream
                {
                    DreamType = DreamType.Peaceful,
                    Title = "Sunset Pond",
                    Scenes = new()
                    {
                        "The sun is setting. It does that.",
                        "The pond is calm. Nothing is happening.",
                        "Cheese floats. The water is the correct temperature.",
                        "A bird flies overhead. It doesn't stop.",
                        "Time passes. Not too fast. Not too slow.",
                        "This is fine. This is exactly fine."
                    },
                    MoodEffect = 12, XpBonus = 2
                },
                new Dream
                {
                    DreamType = DreamType.Peaceful,
                    Title = "Garden Nap",
                    Scenes = new()
                    {
                        "There are flowers. Cheese is among them.",
                        "A butterfly exists nearby. It minds its business.",
                        "The breeze is gentle. Not too breezy. Just right.",
                        "Nothing urgent is happening. Nothing at all.",
                        "Cheese lies there. Could be minutes. Could be hours.",
                        "Perfect. Absolutely adequate in every way."
                    },
                    MoodEffect = 15, XpBonus = 2
                },
                new Dream
                {
                    DreamType = DreamType.Peaceful,
                    Title = "Waiting Room",
                    Scenes = new()
                    {
                        "Cheese is in a waiting room. There's nothing to wait for.",
                        "The chairs are comfortable. The magazines are current.",
                        "No one else is here. No one is coming.",
                        "The clock ticks. It's not annoying. It's fine.",
                        "Cheese waits. For nothing. Contentedly.",
                        "This is the whole dream. Cheese wakes up rested."
                    },
                    MoodEffect = 10, XpBonus = 1
                }
            }
        };

        // Instance fields
        public List<string> DreamHistory { get; private set; } = new();
        public int TotalDreams { get; private set; }
        public Dictionary<string, int> DreamTypeCounts { get; private set; } = new();
        public List<string> SpecialRewardsFound { get; private set; } = new();

        /// <summary>
        /// Generate a dream based on current state.
        /// </summary>
        public Dream GenerateDream(int moodScore = 50, List<string>? recentActivities = null, List<string>? visitorNames = null)
        {
            recentActivities ??= new List<string>();
            visitorNames ??= new List<string>();

            // Determine dream type probabilities
            var weights = new Dictionary<DreamType, int>
            {
                [DreamType.Adventure] = 20,
                [DreamType.Flying] = 15,
                [DreamType.Food] = 20,
                [DreamType.Friend] = 15,
                [DreamType.Nightmare] = 5,
                [DreamType.Memory] = 10,
                [DreamType.Prophetic] = 3,
                [DreamType.Silly] = 15,
                [DreamType.Peaceful] = 15
            };

            // Adjust weights based on mood
            if (moodScore < 30)
            {
                weights[DreamType.Nightmare] += 10;
                weights[DreamType.Peaceful] -= 5;
            }
            else if (moodScore > 70)
            {
                weights[DreamType.Peaceful] += 10;
                weights[DreamType.Nightmare] -= 3;
                weights[DreamType.Flying] += 5;
            }

            // Adjust based on recent activities
            if (recentActivities.Contains("feed") || recentActivities.Contains("eat"))
                weights[DreamType.Food] += 15;
            if (recentActivities.Contains("play"))
            {
                weights[DreamType.Adventure] += 10;
                weights[DreamType.Silly] += 10;
            }
            if (visitorNames.Count > 0)
                weights[DreamType.Friend] += 15;

            // Avoid repeating recent dreams
            var recentTitles = DreamHistory.TakeLast(3).ToList();
            foreach (var title in recentTitles)
            {
                foreach (var (dreamType, dreams) in Dreams)
                {
                    foreach (var dream in dreams)
                    {
                        if (dream.Title == title)
                        {
                            weights[dreamType] = Math.Max(1, weights[dreamType] - 10);
                        }
                    }
                }
            }

            // Select dream type
            var total = weights.Values.Sum();
            var roll = _random.Next(total);
            DreamType selectedType = DreamType.Peaceful;
            int cumulative = 0;

            foreach (var (dreamType, weight) in weights)
            {
                cumulative += weight;
                if (roll < cumulative)
                {
                    selectedType = dreamType;
                    break;
                }
            }

            // Select specific dream
            var availableDreams = Dreams.TryGetValue(selectedType, out var dreamList)
                ? dreamList : Dreams[DreamType.Peaceful];

            return availableDreams[_random.Next(availableDreams.Count)];
        }

        /// <summary>
        /// Start a dream sequence and return the result.
        /// </summary>
        public DreamResult StartDream(int moodScore = 50, List<string>? recentActivities = null, List<string>? visitorNames = null)
        {
            var dream = GenerateDream(moodScore, recentActivities, visitorNames);

            // Track this dream
            DreamHistory.Add(dream.Title);
            if (DreamHistory.Count > 10)
                DreamHistory = DreamHistory.TakeLast(10).ToList();

            TotalDreams++;
            var typeKey = dream.DreamType.ToString().ToLower();
            DreamTypeCounts[typeKey] = DreamTypeCounts.GetValueOrDefault(typeKey) + 1;

            // Check for special reward (30% chance)
            string? specialReward = null;
            if (!string.IsNullOrEmpty(dream.SpecialReward) && _random.NextDouble() < 0.3)
            {
                specialReward = dream.SpecialReward;
                SpecialRewardsFound.Add(specialReward);
            }

            return new DreamResult
            {
                Dream = dream,
                ScenesShown = new List<string>(dream.Scenes),
                MoodEffect = dream.MoodEffect,
                XpEarned = dream.XpBonus,
                SpecialReward = specialReward,
                Message = $"{dream.Title}: A {dream.DreamType.ToString().ToLower()} dream"
            };
        }

        /// <summary>
        /// Get statistics about dreams.
        /// </summary>
        public Dictionary<string, object> GetDreamStats()
        {
            return new Dictionary<string, object>
            {
                ["total_dreams"] = TotalDreams,
                ["dream_types"] = new Dictionary<string, int>(DreamTypeCounts),
                ["special_rewards"] = new List<string>(SpecialRewardsFound),
                ["recent_dreams"] = DreamHistory.TakeLast(5).ToList()
            };
        }

        /// <summary>
        /// Convert to dictionary for saving.
        /// </summary>
        public Dictionary<string, object> ToSaveData()
        {
            return new Dictionary<string, object>
            {
                ["dream_history"] = new List<string>(DreamHistory),
                ["total_dreams"] = TotalDreams,
                ["dream_type_counts"] = new Dictionary<string, int>(DreamTypeCounts),
                ["special_rewards_found"] = new List<string>(SpecialRewardsFound)
            };
        }

        /// <summary>
        /// Create from dictionary.
        /// </summary>
        public static DreamSystem FromSaveData(Dictionary<string, object> data)
        {
            var system = new DreamSystem();

            if (data.TryGetValue("dream_history", out var historyObj) && historyObj is List<string> history)
                system.DreamHistory = new List<string>(history);

            system.TotalDreams = Convert.ToInt32(data.GetValueOrDefault("total_dreams", 0));

            if (data.TryGetValue("dream_type_counts", out var countsObj) && countsObj is Dictionary<string, int> counts)
                system.DreamTypeCounts = new Dictionary<string, int>(counts);

            if (data.TryGetValue("special_rewards_found", out var rewardsObj) && rewardsObj is List<string> rewards)
                system.SpecialRewardsFound = new List<string>(rewards);

            return system;
        }
    }
}
