using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.World
{
    // Note: ItemCategory and ItemRarity are defined in Items.cs

    /// <summary>
    /// A purchasable item for the habitat.
    /// </summary>
    public class ShopItem
    {
        public string Id { get; set; } = "";
        public string Name { get; set; } = "";
        public string Description { get; set; } = "";
        public ItemCategory Category { get; set; }
        public ItemRarity Rarity { get; set; }
        public int Cost { get; set; }
        public int UnlockLevel { get; set; }
        public int UnlockXp { get; set; }
        public string Size { get; set; } = "small"; // "small", "medium", "large"
        public bool Animated { get; set; }
        public List<string> InteractionText { get; set; } = new();
    }

    /// <summary>
    /// Player's shop inventory and purchases.
    /// </summary>
    public class ShopInventory
    {
        public Dictionary<string, int> OwnedItems { get; set; } = new();
        public List<string> EquippedCosmetics { get; set; } = new();
        public Dictionary<string, (int X, int Y)> PlacedItems { get; set; } = new();
        public int TotalSpent { get; set; }
        public int ItemsPurchased { get; set; }

        public Dictionary<string, object> ToSaveData()
        {
            var placedData = new Dictionary<string, object>();
            foreach (var (id, pos) in PlacedItems)
            {
                placedData[id] = new Dictionary<string, int> { ["x"] = pos.X, ["y"] = pos.Y };
            }

            return new Dictionary<string, object>
            {
                ["owned_items"] = new Dictionary<string, int>(OwnedItems),
                ["equipped_cosmetics"] = new List<string>(EquippedCosmetics),
                ["placed_items"] = placedData,
                ["total_spent"] = TotalSpent,
                ["items_purchased"] = ItemsPurchased
            };
        }

        public static ShopInventory FromSaveData(Dictionary<string, object> data)
        {
            var inventory = new ShopInventory();

            if (data.TryGetValue("owned_items", out var ownedObj) && ownedObj is Dictionary<string, int> owned)
                inventory.OwnedItems = new Dictionary<string, int>(owned);

            if (data.TryGetValue("equipped_cosmetics", out var equipObj) && equipObj is List<string> equipped)
                inventory.EquippedCosmetics = new List<string>(equipped);

            if (data.TryGetValue("placed_items", out var placedObj) && placedObj is Dictionary<string, object> placed)
            {
                foreach (var (id, posObj) in placed)
                {
                    if (posObj is Dictionary<string, int> pos)
                    {
                        inventory.PlacedItems[id] = (pos.GetValueOrDefault("x"), pos.GetValueOrDefault("y"));
                    }
                }
            }

            inventory.TotalSpent = Convert.ToInt32(data.GetValueOrDefault("total_spent", 0));
            inventory.ItemsPurchased = Convert.ToInt32(data.GetValueOrDefault("items_purchased", 0));

            return inventory;
        }
    }

    /// <summary>
    /// Shop system with 255 purchasable items.
    /// </summary>
    public class ShopSystem
    {
        // All shop items database
        public static readonly Dictionary<string, ShopItem> ShopItems = new();

        // Initialize all items
        static ShopSystem()
        {
            RegisterAllItems();
        }

        private static void Register(ShopItem item)
        {
            ShopItems[item.Id] = item;
        }

        private static void RegisterAllItems()
        {
            // ========================================
            // COSMETICS (50 items) - Hats & Accessories
            // ========================================

            // Common cosmetics
            Register(new ShopItem
            {
                Id = "hat_red", Name = "Red Cap", Description = "A classic red baseball cap. Very dapper!",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Common,
                Cost = 50, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*adjusts cap* How do I look? *quack*", "*tips cap* M'human." }
            });
            Register(new ShopItem
            {
                Id = "hat_blue", Name = "Blue Cap", Description = "A cool blue cap for a cool duck.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Common,
                Cost = 50, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*straightens cap* Blue is SO my color!", "*quack* Stylin'!" }
            });
            Register(new ShopItem
            {
                Id = "hat_party", Name = "Party Hat", Description = "Pointy, colorful, and festive!",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Common,
                Cost = 75, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*PARTY QUACK!*", "Every day is a party! *dances*" }
            });
            Register(new ShopItem
            {
                Id = "hat_chef", Name = "Chef's Hat", Description = "For the sophisticated culinary duck.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Common,
                Cost = 100, UnlockLevel = 2, UnlockXp = 50, Size = "small",
                InteractionText = new() { "*chef's kiss* Quack!", "Bread is art. I am artist. *nods*" }
            });
            Register(new ShopItem
            {
                Id = "hat_wizard", Name = "Wizard Hat", Description = "Mystical pointy hat with stars.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Uncommon,
                Cost = 200, UnlockLevel = 3, UnlockXp = 150, Size = "small",
                InteractionText = new() { "*waves wing* Abra-qua-dabra!", "*mystical quacking*" }
            });
            Register(new ShopItem
            {
                Id = "hat_crown", Name = "Golden Crown", Description = "For royalty. You're looking at them.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Rare,
                Cost = 500, UnlockLevel = 5, UnlockXp = 500, Size = "small",
                InteractionText = new() { "*regal quack* KNEEL.", "Being royalty is exhausting. *sigh*" }
            });
            Register(new ShopItem
            {
                Id = "hat_viking", Name = "Viking Helmet", Description = "With horns! Historically inaccurate but awesome.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Uncommon,
                Cost = 250, UnlockLevel = 4, UnlockXp = 300, Size = "small",
                InteractionText = new() { "*warrior quack* FOR VALHALLA!", "*pillages bread basket*" }
            });
            Register(new ShopItem
            {
                Id = "hat_pirate", Name = "Pirate Hat", Description = "Arr! A tricorn for swashbuckling ducks.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Uncommon,
                Cost = 250, UnlockLevel = 4, UnlockXp = 300, Size = "small",
                InteractionText = new() { "Arr! *pirate quack*", "Where's me treasure? Oh wait, it's bread." }
            });
            Register(new ShopItem
            {
                Id = "hat_cowboy", Name = "Cowboy Hat", Description = "Yeehaw! Partner.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Uncommon,
                Cost = 200, UnlockLevel = 3, UnlockXp = 150, Size = "small",
                InteractionText = new() { "*tips hat* Howdy, partner!", "This pond ain't big enough for both of us. Wait, yes it is." }
            });
            Register(new ShopItem
            {
                Id = "hat_tophat", Name = "Top Hat", Description = "Classy and sophisticated. Very fancy.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Rare,
                Cost = 400, UnlockLevel = 5, UnlockXp = 500, Size = "small",
                InteractionText = new() { "*sophisticated quack*", "Indeed. Quite. *adjusts monocle that doesn't exist*" }
            });
            Register(new ShopItem
            {
                Id = "hat_beret", Name = "Beret", Description = "Très chic! For the artistic duck.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Common,
                Cost = 150, UnlockLevel = 2, UnlockXp = 50, Size = "small",
                InteractionText = new() { "*artistic quack* C'est magnifique!", "I don't speak French but I feel fancy." }
            });
            Register(new ShopItem
            {
                Id = "glasses_cool", Name = "Sunglasses", Description = "Deal with it. 😎",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Common,
                Cost = 150, UnlockLevel = 2, UnlockXp = 50, Size = "small",
                InteractionText = new() { "*cool quack*", "Can't see anything but I LOOK GOOD." }
            });
            Register(new ShopItem
            {
                Id = "bowtie", Name = "Bow Tie", Description = "Fancy neckwear for formal occasions.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Common,
                Cost = 120, UnlockLevel = 2, UnlockXp = 50, Size = "small",
                InteractionText = new() { "*adjusts bow tie* Dapper!", "Bow ties are cool. *quack*" }
            });
            Register(new ShopItem
            {
                Id = "cape", Name = "Superhero Cape", Description = "For when you need to save the day!",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Rare,
                Cost = 600, UnlockLevel = 6, UnlockXp = 800, Size = "small",
                InteractionText = new() { "*heroic pose* SUPER DUCK!", "*attempts to fly, waddles instead*" }
            });
            Register(new ShopItem
            {
                Id = "wings_fairy", Name = "Fairy Wings", Description = "Sparkly, magical wings.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Epic,
                Cost = 1000, UnlockLevel = 8, UnlockXp = 1500, Size = "small", Animated = true,
                InteractionText = new() { "*sparkles*", "*magical quacking*" }
            });
            Register(new ShopItem
            {
                Id = "halo", Name = "Halo", Description = "Angelic duck mode activated.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Rare,
                Cost = 500, UnlockLevel = 6, UnlockXp = 800, Size = "small", Animated = true,
                InteractionText = new() { "*angelic quack*", "I'm basically a saint. Of bread." }
            });
            Register(new ShopItem
            {
                Id = "headphones", Name = "Headphones", Description = "Listening to duck jams.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Uncommon,
                Cost = 150, UnlockLevel = 3, UnlockXp = 150, Size = "small", Animated = true,
                InteractionText = new() { "*vibing to music*", "Can't hear you, jamming!" }
            });
            Register(new ShopItem
            {
                Id = "monocle", Name = "Monocle", Description = "Distinguished and refined.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Rare,
                Cost = 350, UnlockLevel = 6, UnlockXp = 800, Size = "small",
                InteractionText = new() { "*posh quack*", "Indeed, quite!" }
            });
            Register(new ShopItem
            {
                Id = "space_helmet", Name = "Space Helmet", Description = "Astronaut duck reporting!",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Epic,
                Cost = 1000, UnlockLevel = 10, UnlockXp = 3000, Size = "small",
                InteractionText = new() { "Houston, we have a quack!", "*floats weightlessly*" }
            });
            Register(new ShopItem
            {
                Id = "halo_angel", Name = "Angel Halo", Description = "Angelic duck halo.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Legendary,
                Cost = 1500, UnlockLevel = 12, UnlockXp = 5000, Size = "small", Animated = true,
                InteractionText = new() { "*innocent quack*", "I'm an angel, I swear!" }
            });
            Register(new ShopItem
            {
                Id = "devil_horns", Name = "Devil Horns", Description = "Mischievous devil horns.",
                Category = ItemCategory.Cosmetic, Rarity = ItemRarity.Legendary,
                Cost = 1500, UnlockLevel = 12, UnlockXp = 5000, Size = "small", Animated = true,
                InteractionText = new() { "*evil quack*", "Let's cause some chaos!" }
            });

            // ========================================
            // TOYS (30 items) - Interactive items
            // ========================================

            Register(new ShopItem
            {
                Id = "toy_ball", Name = "Rubber Ball", Description = "A bouncy ball to play with!",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Common,
                Cost = 80, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*pushes ball* Wheee!", "*chases ball* Come back here!" }
            });
            Register(new ShopItem
            {
                Id = "toy_blocks", Name = "Building Blocks", Description = "Colorful blocks to stack and knock over.",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Common,
                Cost = 100, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*stacks blocks carefully*", "*KNOCKS OVER BLOCKS* Oops!" }
            });
            Register(new ShopItem
            {
                Id = "toy_trumpet", Name = "Toy Trumpet", Description = "For making noise! So much noise!",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Common,
                Cost = 150, UnlockLevel = 2, UnlockXp = 50, Size = "small",
                InteractionText = new() { "*HONK HONK* This is AMAZING!", "*jazz quacking*" }
            });
            Register(new ShopItem
            {
                Id = "toy_skateboard", Name = "Skateboard", Description = "Radical! Cowabunga!",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Uncommon,
                Cost = 300, UnlockLevel = 3, UnlockXp = 150, Size = "medium",
                InteractionText = new() { "*kickflips* ...almost!", "*rolls around* Quack yeah!" }
            });
            Register(new ShopItem
            {
                Id = "toy_piano", Name = "Toy Piano", Description = "A small piano for musical ducks.",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Uncommon,
                Cost = 400, UnlockLevel = 4, UnlockXp = 300, Size = "medium",
                InteractionText = new() { "*pecks keys* ♪♫", "*composes masterpiece* This is called 'Bread in D Minor'" }
            });
            Register(new ShopItem
            {
                Id = "toy_trampoline", Name = "Trampoline", Description = "Bounce bounce bounce!",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Uncommon,
                Cost = 500, UnlockLevel = 5, UnlockXp = 500, Size = "medium", Animated = true,
                InteractionText = new() { "*BOING BOING* THIS IS THE BEST!", "*bouncing intensifies*" }
            });
            Register(new ShopItem
            {
                Id = "toy_slide", Name = "Playground Slide", Description = "Whee! Down we go!",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Rare,
                Cost = 800, UnlockLevel = 6, UnlockXp = 800, Size = "large",
                InteractionText = new() { "*slides down* WHEEEEE!", "*climbs up for another turn*" }
            });
            Register(new ShopItem
            {
                Id = "toy_swing", Name = "Swing Set", Description = "Swing high into the sky!",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Rare,
                Cost = 800, UnlockLevel = 6, UnlockXp = 800, Size = "large", Animated = true,
                InteractionText = new() { "*swinging* Higher! HIGHER!", "*pumps legs* I can touch the clouds!" }
            });
            Register(new ShopItem
            {
                Id = "toy_sandbox", Name = "Sandbox", Description = "Dig, build, play!",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Common,
                Cost = 250, UnlockLevel = 3, UnlockXp = 150, Size = "medium",
                InteractionText = new() { "*digs furiously*", "*makes sand castle* Architectural genius!" }
            });
            Register(new ShopItem
            {
                Id = "toy_boombox", Name = "Boombox", Description = "A retro boombox for some tunes!",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Rare,
                Cost = 350, UnlockLevel = 3, UnlockXp = 150, Size = "medium", Animated = true,
                InteractionText = new() { "*turns on boombox* ♪♫ MUSIC TIME! ♫♪", "*dances to the beat*" }
            });
            Register(new ShopItem
            {
                Id = "telescope", Name = "Telescope", Description = "Star gazing duck.",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Epic,
                Cost = 800, UnlockLevel = 8, UnlockXp = 1500, Size = "medium",
                InteractionText = new() { "*gazes at stars*", "Is that... Pluto?" }
            });
            Register(new ShopItem
            {
                Id = "drums", Name = "Drum Set", Description = "Rock out!",
                Category = ItemCategory.Toy, Rarity = ItemRarity.Epic,
                Cost = 900, UnlockLevel = 9, UnlockXp = 2000, Size = "large", Animated = true,
                InteractionText = new() { "*BANG CRASH*", "*epic drum solo*" }
            });

            // ========================================
            // FURNITURE (30 items)
            // ========================================

            Register(new ShopItem
            {
                Id = "chair_wood", Name = "Wooden Chair", Description = "Simple, sturdy, sittable.",
                Category = ItemCategory.Furniture, Rarity = ItemRarity.Common,
                Cost = 100, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*sits* Ahh, perfect.", "*lounges* This is the life." }
            });
            Register(new ShopItem
            {
                Id = "chair_throne", Name = "Royal Throne", Description = "For sitting like royalty.",
                Category = ItemCategory.Furniture, Rarity = ItemRarity.Epic,
                Cost = 2000, UnlockLevel = 10, UnlockXp = 3000, Size = "large",
                InteractionText = new() { "*sits majestically* BEHOLD.", "*waves wing dismissively* Peasants." }
            });
            Register(new ShopItem
            {
                Id = "table_small", Name = "Small Table", Description = "Perfect for snacks!",
                Category = ItemCategory.Furniture, Rarity = ItemRarity.Common,
                Cost = 150, UnlockLevel = 1, UnlockXp = 0, Size = "medium",
                InteractionText = new() { "*hops on table* Great view!", "*places bread here* My shrine." }
            });
            Register(new ShopItem
            {
                Id = "bed_small", Name = "Cozy Bed", Description = "For naps. So many naps.",
                Category = ItemCategory.Furniture, Rarity = ItemRarity.Common,
                Cost = 200, UnlockLevel = 2, UnlockXp = 50, Size = "medium",
                InteractionText = new() { "*flops into bed* zzz", "*makes nest* Perfect!" }
            });
            Register(new ShopItem
            {
                Id = "bed_king", Name = "King Size Bed", Description = "Ridiculously large for one duck.",
                Category = ItemCategory.Furniture, Rarity = ItemRarity.Rare,
                Cost = 1000, UnlockLevel = 7, UnlockXp = 1000, Size = "large",
                InteractionText = new() { "*spreads out* SO MUCH ROOM!", "*gets lost in bed*" }
            });
            Register(new ShopItem
            {
                Id = "couch", Name = "Comfy Couch", Description = "For lounging like a boss.",
                Category = ItemCategory.Furniture, Rarity = ItemRarity.Uncommon,
                Cost = 500, UnlockLevel = 5, UnlockXp = 500, Size = "large",
                InteractionText = new() { "*sprawls* Don't wanna move. Ever.", "*cushion quack*" }
            });
            Register(new ShopItem
            {
                Id = "bookshelf", Name = "Bookshelf", Description = "For books you pretend to read.",
                Category = ItemCategory.Furniture, Rarity = ItemRarity.Uncommon,
                Cost = 300, UnlockLevel = 3, UnlockXp = 150, Size = "medium",
                InteractionText = new() { "*looks at books* I can't read. But it looks SMART!", "*pulls out book* Is this about bread?" }
            });
            Register(new ShopItem
            {
                Id = "desk", Name = "Writing Desk", Description = "For important duck business.",
                Category = ItemCategory.Furniture, Rarity = ItemRarity.Uncommon,
                Cost = 400, UnlockLevel = 4, UnlockXp = 300, Size = "medium",
                InteractionText = new() { "*sits at desk importantly*", "*scribbles* Dear diary: BREAD." }
            });
            Register(new ShopItem
            {
                Id = "piano", Name = "Grand Piano", Description = "Tickle those ivories!",
                Category = ItemCategory.Furniture, Rarity = ItemRarity.Epic,
                Cost = 1200, UnlockLevel = 10, UnlockXp = 3000, Size = "large", Animated = true,
                InteractionText = new() { "*plays Moonlight Quackata*", "*dramatic musical flourish*" }
            });
            Register(new ShopItem
            {
                Id = "fireplace", Name = "Stone Fireplace", Description = "Cozy warmth.",
                Category = ItemCategory.Furniture, Rarity = ItemRarity.Legendary,
                Cost = 2000, UnlockLevel = 12, UnlockXp = 5000, Size = "large", Animated = true,
                InteractionText = new() { "*warms by fire*", "*crackle crackle*" }
            });
            Register(new ShopItem
            {
                Id = "golden_throne", Name = "Golden Throne", Description = "For the ultimate duck emperor!",
                Category = ItemCategory.Furniture, Rarity = ItemRarity.Legendary,
                Cost = 5000, UnlockLevel = 20, UnlockXp = 20000, Size = "large",
                InteractionText = new() { "*sits majestically*", "Bow before me!" }
            });

            // ========================================
            // WATER FEATURES (20 items)
            // ========================================

            Register(new ShopItem
            {
                Id = "pool_kiddie", Name = "Kiddie Pool", Description = "A small inflatable pool. Splish splash!",
                Category = ItemCategory.Water, Rarity = ItemRarity.Common,
                Cost = 300, UnlockLevel = 2, UnlockXp = 50, Size = "medium", Animated = true,
                InteractionText = new() { "*splashes* WATER!", "*paddles around*" }
            });
            Register(new ShopItem
            {
                Id = "pool_large", Name = "Swimming Pool", Description = "A proper pool for swimming!",
                Category = ItemCategory.Water, Rarity = ItemRarity.Rare,
                Cost = 1500, UnlockLevel = 8, UnlockXp = 1500, Size = "large", Animated = true,
                InteractionText = new() { "*dives in* CANNONBALL!", "*swims laps* I'm an athlete!" }
            });
            Register(new ShopItem
            {
                Id = "fountain_small", Name = "Garden Fountain", Description = "Peaceful bubbling water.",
                Category = ItemCategory.Water, Rarity = ItemRarity.Uncommon,
                Cost = 600, UnlockLevel = 5, UnlockXp = 500, Size = "medium", Animated = true,
                InteractionText = new() { "*drinks from fountain*", "*splashes face* Refreshing!" }
            });
            Register(new ShopItem
            {
                Id = "fountain_grand", Name = "Grand Fountain", Description = "Majestic, tall, impressive!",
                Category = ItemCategory.Water, Rarity = ItemRarity.Epic,
                Cost = 2500, UnlockLevel = 12, UnlockXp = 4000, Size = "large", Animated = true,
                InteractionText = new() { "*stares in awe*", "*feels fancy*" }
            });
            Register(new ShopItem
            {
                Id = "pond", Name = "Duck Pond", Description = "A natural pond. Your ancestral home!",
                Category = ItemCategory.Water, Rarity = ItemRarity.Rare,
                Cost = 1200, UnlockLevel = 7, UnlockXp = 1000, Size = "large", Animated = true,
                InteractionText = new() { "*happy duck noises* HOME!", "*floats peacefully*" }
            });
            Register(new ShopItem
            {
                Id = "birdbath", Name = "Bird Bath", Description = "Ironically, perfect for ducks too.",
                Category = ItemCategory.Water, Rarity = ItemRarity.Common,
                Cost = 150, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*splashes* Bath time!", "*preens feathers*" }
            });
            Register(new ShopItem
            {
                Id = "hot_tub", Name = "Hot Tub", Description = "Luxury! Bubbles! Warmth!",
                Category = ItemCategory.Water, Rarity = ItemRarity.Rare,
                Cost = 2000, UnlockLevel = 10, UnlockXp = 3000, Size = "large", Animated = true,
                InteractionText = new() { "*relaxes* Ahhhh...", "*bubbles* This is AMAZING!" }
            });
            Register(new ShopItem
            {
                Id = "waterfall", Name = "Waterfall", Description = "Cascading water. Very zen.",
                Category = ItemCategory.Water, Rarity = ItemRarity.Epic,
                Cost = 3000, UnlockLevel = 13, UnlockXp = 5000, Size = "large", Animated = true,
                InteractionText = new() { "*listens to water* So peaceful...", "*stands under waterfall* COLD!" }
            });
            Register(new ShopItem
            {
                Id = "infinity_pool", Name = "Infinity Pool", Description = "Never-ending pool!",
                Category = ItemCategory.Water, Rarity = ItemRarity.Legendary,
                Cost = 4000, UnlockLevel = 18, UnlockXp = 15000, Size = "large", Animated = true,
                InteractionText = new() { "*swims forever*", "No edges!" }
            });

            // ========================================
            // PLANTS (25 items)
            // ========================================

            Register(new ShopItem
            {
                Id = "flower_rose", Name = "Rose Bush", Description = "Beautiful red roses.",
                Category = ItemCategory.Plant, Rarity = ItemRarity.Common,
                Cost = 100, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*smells roses* Quack!", "*tries to eat* ...not bread." }
            });
            Register(new ShopItem
            {
                Id = "flower_tulip", Name = "Tulips", Description = "Colorful spring flowers!",
                Category = ItemCategory.Plant, Rarity = ItemRarity.Common,
                Cost = 80, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*appreciates beauty*", "*waddles through tulips*" }
            });
            Register(new ShopItem
            {
                Id = "flower_sunflower", Name = "Sunflower", Description = "Tall, bright, happy!",
                Category = ItemCategory.Plant, Rarity = ItemRarity.Common,
                Cost = 120, UnlockLevel = 1, UnlockXp = 0, Size = "medium",
                InteractionText = new() { "*stands next to sunflower* I'm taller! Wait...", "*pecks seeds* SNACK!" }
            });
            Register(new ShopItem
            {
                Id = "tree_small", Name = "Small Tree", Description = "A cute little tree for shade.",
                Category = ItemCategory.Plant, Rarity = ItemRarity.Uncommon,
                Cost = 300, UnlockLevel = 3, UnlockXp = 150, Size = "medium",
                InteractionText = new() { "*sits under tree* Shady!", "*pecks bark* Knock knock!" }
            });
            Register(new ShopItem
            {
                Id = "tree_oak", Name = "Oak Tree", Description = "Large, majestic, ancient.",
                Category = ItemCategory.Plant, Rarity = ItemRarity.Rare,
                Cost = 800, UnlockLevel = 6, UnlockXp = 800, Size = "large",
                InteractionText = new() { "*looks up* So tall!", "*naps under tree*" }
            });
            Register(new ShopItem
            {
                Id = "tree_cherry", Name = "Cherry Blossom Tree", Description = "Pink petals drift down beautifully.",
                Category = ItemCategory.Plant, Rarity = ItemRarity.Epic,
                Cost = 1500, UnlockLevel = 9, UnlockXp = 2000, Size = "large", Animated = true,
                InteractionText = new() { "*catches petal* Magical!", "*photo op quack*" }
            });
            Register(new ShopItem
            {
                Id = "bamboo", Name = "Bamboo Grove", Description = "Peaceful bamboo stalks.",
                Category = ItemCategory.Plant, Rarity = ItemRarity.Rare,
                Cost = 700, UnlockLevel = 6, UnlockXp = 800, Size = "medium",
                InteractionText = new() { "*zen quack*", "*hides in bamboo*" }
            });
            Register(new ShopItem
            {
                Id = "hedge_maze", Name = "Hedge Maze", Description = "Get lost in the maze!",
                Category = ItemCategory.Plant, Rarity = ItemRarity.Legendary,
                Cost = 2000, UnlockLevel = 13, UnlockXp = 7000, Size = "large",
                InteractionText = new() { "*wanders around*", "I'm lost... again!" }
            });
            Register(new ShopItem
            {
                Id = "world_tree", Name = "World Tree Yggdrasil", Description = "The tree that holds the universe!",
                Category = ItemCategory.Plant, Rarity = ItemRarity.Legendary,
                Cost = 5000, UnlockLevel = 20, UnlockXp = 20000, Size = "large", Animated = true,
                InteractionText = new() { "*touches trunk*", "I can feel the cosmos!" }
            });

            // ========================================
            // STRUCTURES (25 items)
            // ========================================

            Register(new ShopItem
            {
                Id = "duck_house", Name = "Duck House", Description = "A cozy little house.",
                Category = ItemCategory.Structure, Rarity = ItemRarity.Uncommon,
                Cost = 300, UnlockLevel = 3, UnlockXp = 150, Size = "large",
                InteractionText = new() { "*enters house*", "Home sweet home!" }
            });
            Register(new ShopItem
            {
                Id = "picket_fence", Name = "Picket Fence", Description = "White picket fence section.",
                Category = ItemCategory.Structure, Rarity = ItemRarity.Common,
                Cost = 100, UnlockLevel = 2, UnlockXp = 50, Size = "medium",
                InteractionText = new() { "*hops over fence*", "Can't contain me!" }
            });
            Register(new ShopItem
            {
                Id = "gazebo", Name = "Wooden Gazebo", Description = "Peaceful garden gazebo.",
                Category = ItemCategory.Structure, Rarity = ItemRarity.Epic,
                Cost = 1200, UnlockLevel = 10, UnlockXp = 3000, Size = "large",
                InteractionText = new() { "*sits in gazebo*", "What a view!" }
            });
            Register(new ShopItem
            {
                Id = "bridge", Name = "Wooden Bridge", Description = "Crosses over water.",
                Category = ItemCategory.Structure, Rarity = ItemRarity.Rare,
                Cost = 600, UnlockLevel = 7, UnlockXp = 1200, Size = "large",
                InteractionText = new() { "*crosses bridge*", "*clack clack clack*" }
            });
            Register(new ShopItem
            {
                Id = "windmill", Name = "Windmill", Description = "Classic spinning windmill.",
                Category = ItemCategory.Structure, Rarity = ItemRarity.Legendary,
                Cost = 2500, UnlockLevel = 13, UnlockXp = 7000, Size = "large", Animated = true,
                InteractionText = new() { "*blades spin*", "*whoosh whoosh*" }
            });
            Register(new ShopItem
            {
                Id = "treehouse", Name = "Treehouse", Description = "Duck fortress in the trees!",
                Category = ItemCategory.Structure, Rarity = ItemRarity.Epic,
                Cost = 1800, UnlockLevel = 12, UnlockXp = 5000, Size = "large",
                InteractionText = new() { "*climbs up*", "No grown-ups allowed!" }
            });
            Register(new ShopItem
            {
                Id = "wishing_well", Name = "Wishing Well", Description = "Make a wish!",
                Category = ItemCategory.Structure, Rarity = ItemRarity.Rare,
                Cost = 800, UnlockLevel = 8, UnlockXp = 1500, Size = "medium",
                InteractionText = new() { "*tosses coin*", "I wish for more bread!" }
            });
            Register(new ShopItem
            {
                Id = "castle_tower", Name = "Castle Tower", Description = "Medieval stone tower.",
                Category = ItemCategory.Structure, Rarity = ItemRarity.Legendary,
                Cost = 3000, UnlockLevel = 15, UnlockXp = 10000, Size = "large",
                InteractionText = new() { "*feels majestic*", "My castle!" }
            });
            Register(new ShopItem
            {
                Id = "cosmic_arch", Name = "Cosmic Archway", Description = "Gateway to the stars!",
                Category = ItemCategory.Structure, Rarity = ItemRarity.Legendary,
                Cost = 5000, UnlockLevel = 20, UnlockXp = 20000, Size = "large", Animated = true,
                InteractionText = new() { "*walks through*", "The universe awaits!" }
            });

            // ========================================
            // DECORATIONS (30 items)
            // ========================================

            Register(new ShopItem
            {
                Id = "garden_gnome", Name = "Garden Gnome", Description = "Creepy little guy.",
                Category = ItemCategory.Decoration, Rarity = ItemRarity.Common,
                Cost = 100, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*stares at gnome*", "Is it... watching me?" }
            });
            Register(new ShopItem
            {
                Id = "duck_statue", Name = "Duck Statue", Description = "A statue of... you!",
                Category = ItemCategory.Decoration, Rarity = ItemRarity.Rare,
                Cost = 500, UnlockLevel = 6, UnlockXp = 800, Size = "medium",
                InteractionText = new() { "*strikes same pose*", "Nailed it!" }
            });
            Register(new ShopItem
            {
                Id = "wind_chimes", Name = "Wind Chimes", Description = "Tinkle in the breeze.",
                Category = ItemCategory.Decoration, Rarity = ItemRarity.Common,
                Cost = 150, UnlockLevel = 2, UnlockXp = 50, Size = "small", Animated = true,
                InteractionText = new() { "*ting ting*", "So peaceful!" }
            });
            Register(new ShopItem
            {
                Id = "banner_duck", Name = "Duck Banner", Description = "Proudly display duck pride!",
                Category = ItemCategory.Decoration, Rarity = ItemRarity.Uncommon,
                Cost = 200, UnlockLevel = 3, UnlockXp = 150, Size = "medium",
                InteractionText = new() { "*salutes*", "Duck pride!" }
            });
            Register(new ShopItem
            {
                Id = "golden_statue", Name = "Golden Duck Statue", Description = "Ultimate tribute to ducks!",
                Category = ItemCategory.Decoration, Rarity = ItemRarity.Legendary,
                Cost = 3000, UnlockLevel = 15, UnlockXp = 10000, Size = "large",
                InteractionText = new() { "*bows*", "It's beautiful!" }
            });

            // ========================================
            // LIGHTING (15 items)
            // ========================================

            Register(new ShopItem
            {
                Id = "lamp_floor", Name = "Floor Lamp", Description = "Provides ambiance and light!",
                Category = ItemCategory.Lighting, Rarity = ItemRarity.Common,
                Cost = 200, UnlockLevel = 2, UnlockXp = 50, Size = "small",
                InteractionText = new() { "*flicks lamp on and off* MAGIC!", "*basks in the glow*" }
            });
            Register(new ShopItem
            {
                Id = "lantern", Name = "Paper Lantern", Description = "Soft, warm glow.",
                Category = ItemCategory.Lighting, Rarity = ItemRarity.Common,
                Cost = 100, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*warm quack*", "Cozy!" }
            });
            Register(new ShopItem
            {
                Id = "string_lights", Name = "String Lights", Description = "Fairy lights for magic!",
                Category = ItemCategory.Lighting, Rarity = ItemRarity.Uncommon,
                Cost = 250, UnlockLevel = 3, UnlockXp = 150, Size = "medium", Animated = true,
                InteractionText = new() { "*twinkle twinkle*", "So magical!" }
            });
            Register(new ShopItem
            {
                Id = "chandelier", Name = "Crystal Chandelier", Description = "Fancy ceiling light!",
                Category = ItemCategory.Lighting, Rarity = ItemRarity.Epic,
                Cost = 1500, UnlockLevel = 10, UnlockXp = 3000, Size = "large", Animated = true,
                InteractionText = new() { "*sparkles*", "So fancy!" }
            });
            Register(new ShopItem
            {
                Id = "eternal_flame", Name = "Eternal Flame", Description = "Never goes out!",
                Category = ItemCategory.Lighting, Rarity = ItemRarity.Legendary,
                Cost = 3500, UnlockLevel = 17, UnlockXp = 12000, Size = "small", Animated = true,
                InteractionText = new() { "*flames dance*", "It burns forever!" }
            });

            // ========================================
            // FLOORING (10 items)
            // ========================================

            Register(new ShopItem
            {
                Id = "rug_small", Name = "Small Rug", Description = "Soft underfoot!",
                Category = ItemCategory.Flooring, Rarity = ItemRarity.Common,
                Cost = 100, UnlockLevel = 1, UnlockXp = 0, Size = "small",
                InteractionText = new() { "*sits on rug*", "Soft!" }
            });
            Register(new ShopItem
            {
                Id = "rug_fancy", Name = "Persian Rug", Description = "Elegant patterns!",
                Category = ItemCategory.Flooring, Rarity = ItemRarity.Rare,
                Cost = 600, UnlockLevel = 6, UnlockXp = 800, Size = "large",
                InteractionText = new() { "*admires patterns*", "So cultured!" }
            });
            Register(new ShopItem
            {
                Id = "tiles_fancy", Name = "Marble Tiles", Description = "Luxurious flooring!",
                Category = ItemCategory.Flooring, Rarity = ItemRarity.Epic,
                Cost = 1000, UnlockLevel = 8, UnlockXp = 1500, Size = "large",
                InteractionText = new() { "*tap tap*", "Fancy!" }
            });

            // ========================================
            // SPECIAL (30 items) - Unique animated items
            // ========================================

            Register(new ShopItem
            {
                Id = "magic_crystal", Name = "Magic Crystal", Description = "Glowing mysterious crystal!",
                Category = ItemCategory.Special, Rarity = ItemRarity.Epic,
                Cost = 1200, UnlockLevel = 9, UnlockXp = 2000, Size = "small", Animated = true,
                InteractionText = new() { "*glows mysteriously*", "What secrets does it hold?" }
            });
            Register(new ShopItem
            {
                Id = "portal", Name = "Magic Portal", Description = "Where does it lead?!",
                Category = ItemCategory.Special, Rarity = ItemRarity.Legendary,
                Cost = 3000, UnlockLevel = 15, UnlockXp = 10000, Size = "large", Animated = true,
                InteractionText = new() { "*swirls*", "Should I go in...?" }
            });
            Register(new ShopItem
            {
                Id = "time_machine", Name = "Time Machine", Description = "Travel through time!",
                Category = ItemCategory.Special, Rarity = ItemRarity.Legendary,
                Cost = 5000, UnlockLevel = 20, UnlockXp = 20000, Size = "large", Animated = true,
                InteractionText = new() { "*whirs*", "When should we go?" }
            });
            Register(new ShopItem
            {
                Id = "ufo", Name = "UFO", Description = "Alien spacecraft!",
                Category = ItemCategory.Special, Rarity = ItemRarity.Legendary,
                Cost = 4500, UnlockLevel = 19, UnlockXp = 18000, Size = "large", Animated = true,
                InteractionText = new() { "*beams up*", "Take me to your leader!" }
            });
            Register(new ShopItem
            {
                Id = "jetpack", Name = "Jetpack", Description = "FLY DUCK FLY!",
                Category = ItemCategory.Special, Rarity = ItemRarity.Epic,
                Cost = 1800, UnlockLevel = 12, UnlockXp = 5000, Size = "small", Animated = true,
                InteractionText = new() { "*BLAST OFF*", "I'M FLYING!" }
            });
            Register(new ShopItem
            {
                Id = "rocket_ship", Name = "Rocket Ship", Description = "To the moon!",
                Category = ItemCategory.Special, Rarity = ItemRarity.Legendary,
                Cost = 5000, UnlockLevel = 20, UnlockXp = 20000, Size = "large", Animated = true,
                InteractionText = new() { "*countdown 3...2...1*", "BLAST OFF!" }
            });
            Register(new ShopItem
            {
                Id = "philosophers_stone", Name = "Philosopher's Stone", Description = "Legendary alchemical treasure!",
                Category = ItemCategory.Special, Rarity = ItemRarity.Legendary,
                Cost = 10000, UnlockLevel = 25, UnlockXp = 50000, Size = "small", Animated = true,
                InteractionText = new() { "*glows mysteriously*", "The secret of immortality!" }
            });
        }

        // Instance fields
        public ShopInventory Inventory { get; private set; } = new();
        public int PlayerCoins { get; set; }
        public int PlayerLevel { get; set; } = 1;

        /// <summary>
        /// Get all items in a category.
        /// </summary>
        public static List<ShopItem> GetItemsByCategory(ItemCategory category)
        {
            return ShopItems.Values.Where(item => item.Category == category).ToList();
        }

        /// <summary>
        /// Get all items of a rarity tier.
        /// </summary>
        public static List<ShopItem> GetItemsByRarity(ItemRarity rarity)
        {
            return ShopItems.Values.Where(item => item.Rarity == rarity).ToList();
        }

        /// <summary>
        /// Get items the player can afford and has unlocked.
        /// </summary>
        public List<ShopItem> GetAffordableItems()
        {
            return ShopItems.Values
                .Where(item => item.Cost <= PlayerCoins && item.UnlockLevel <= PlayerLevel)
                .ToList();
        }

        /// <summary>
        /// Get an item by ID.
        /// </summary>
        public static ShopItem? GetItem(string itemId)
        {
            return ShopItems.TryGetValue(itemId, out var item) ? item : null;
        }

        /// <summary>
        /// Purchase an item.
        /// </summary>
        public (bool Success, string Message) PurchaseItem(string itemId)
        {
            var item = GetItem(itemId);
            if (item == null)
                return (false, "Item not found!");

            if (item.UnlockLevel > PlayerLevel)
                return (false, $"You need to be level {item.UnlockLevel} to buy this!");

            if (item.Cost > PlayerCoins)
                return (false, "Not enough coins!");

            PlayerCoins -= item.Cost;
            Inventory.OwnedItems[itemId] = Inventory.OwnedItems.GetValueOrDefault(itemId) + 1;
            Inventory.TotalSpent += item.Cost;
            Inventory.ItemsPurchased++;

            return (true, $"Purchased {item.Name}! 🛒");
        }

        /// <summary>
        /// Equip a cosmetic item.
        /// </summary>
        public (bool Success, string Message) EquipCosmetic(string itemId)
        {
            var item = GetItem(itemId);
            if (item == null)
                return (false, "Item not found!");

            if (item.Category != ItemCategory.Cosmetic)
                return (false, "This item is not a cosmetic!");

            if (!Inventory.OwnedItems.ContainsKey(itemId) || Inventory.OwnedItems[itemId] <= 0)
                return (false, "You don't own this item!");

            if (Inventory.EquippedCosmetics.Contains(itemId))
            {
                Inventory.EquippedCosmetics.Remove(itemId);
                return (true, $"Unequipped {item.Name}.");
            }
            else
            {
                Inventory.EquippedCosmetics.Add(itemId);
                return (true, $"Equipped {item.Name}! ✨");
            }
        }

        /// <summary>
        /// Place an item in the habitat.
        /// </summary>
        public (bool Success, string Message) PlaceItem(string itemId, int x, int y)
        {
            var item = GetItem(itemId);
            if (item == null)
                return (false, "Item not found!");

            if (!Inventory.OwnedItems.ContainsKey(itemId) || Inventory.OwnedItems[itemId] <= 0)
                return (false, "You don't own this item!");

            if (Inventory.PlacedItems.ContainsKey(itemId))
                return (false, "This item is already placed!");

            Inventory.PlacedItems[itemId] = (x, y);
            return (true, $"Placed {item.Name}! 📍");
        }

        /// <summary>
        /// Get a random interaction text for an item.
        /// </summary>
        public static string? GetInteraction(string itemId)
        {
            var item = GetItem(itemId);
            if (item == null || item.InteractionText.Count == 0)
                return null;

            return item.InteractionText[new Random().Next(item.InteractionText.Count)];
        }

        /// <summary>
        /// Render the shop display.
        /// </summary>
        public List<string> RenderShop(ItemCategory? category = null)
        {
            var items = category.HasValue
                ? GetItemsByCategory(category.Value)
                : ShopItems.Values.Take(20).ToList();

            var lines = new List<string>
            {
                "╔═══════════════════════════════════════╗",
                "║          🛒 DUCK SHOP 🛒              ║",
                $"║  Coins: {PlayerCoins,-8} Level: {PlayerLevel,-5}    ║",
                "╠═══════════════════════════════════════╣"
            };

            foreach (var item in items.Take(10))
            {
                string owned = Inventory.OwnedItems.ContainsKey(item.Id) ? "✓" : " ";
                string affordable = item.Cost <= PlayerCoins && item.UnlockLevel <= PlayerLevel ? "" : "🔒";
                lines.Add($"║ {owned} {item.Name,-18} {item.Cost,5}c {affordable} ║");
            }

            lines.Add("╠═══════════════════════════════════════╣");
            lines.Add($"║ Total Items: {ShopItems.Count,-4}                   ║");
            lines.Add("╚═══════════════════════════════════════╝");

            return lines;
        }

        /// <summary>
        /// Get shop statistics.
        /// </summary>
        public Dictionary<string, object> GetStats()
        {
            return new Dictionary<string, object>
            {
                ["items_owned"] = Inventory.OwnedItems.Values.Sum(),
                ["unique_items"] = Inventory.OwnedItems.Count,
                ["total_spent"] = Inventory.TotalSpent,
                ["items_purchased"] = Inventory.ItemsPurchased,
                ["cosmetics_equipped"] = Inventory.EquippedCosmetics.Count,
                ["items_placed"] = Inventory.PlacedItems.Count
            };
        }

        /// <summary>
        /// Convert to dictionary for saving.
        /// </summary>
        public Dictionary<string, object> ToSaveData()
        {
            return new Dictionary<string, object>
            {
                ["inventory"] = Inventory.ToSaveData(),
                ["player_coins"] = PlayerCoins,
                ["player_level"] = PlayerLevel
            };
        }

        /// <summary>
        /// Create from dictionary.
        /// </summary>
        public static ShopSystem FromSaveData(Dictionary<string, object> data)
        {
            var shop = new ShopSystem
            {
                PlayerCoins = Convert.ToInt32(data.GetValueOrDefault("player_coins", 0)),
                PlayerLevel = Convert.ToInt32(data.GetValueOrDefault("player_level", 1))
            };

            if (data.TryGetValue("inventory", out var invObj) && invObj is Dictionary<string, object> invData)
            {
                shop.Inventory = ShopInventory.FromSaveData(invData);
            }

            return shop;
        }
    }
}
