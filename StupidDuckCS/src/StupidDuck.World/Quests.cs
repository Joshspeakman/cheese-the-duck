using System;
using System.Collections.Generic;
using System.Linq;

namespace StupidDuck.World;

/// <summary>
/// Types of quests.
/// </summary>
public enum QuestType
{
    Main,
    Side,
    Daily,
    Hidden,
    Seasonal
}

/// <summary>
/// Quest difficulty levels.
/// </summary>
public enum QuestDifficulty
{
    Easy,
    Medium,
    Hard,
    Legendary
}

/// <summary>
/// Types of quest objectives.
/// </summary>
public enum ObjectiveType
{
    Collect,
    Feed,
    Play,
    Explore,
    Talk,
    Fish,
    Garden,
    Craft,
    Find,
    Wait,
    Choice
}

/// <summary>
/// A single objective within a quest.
/// </summary>
public class QuestObjective
{
    public string Id { get; set; } = "";
    public string Description { get; set; } = "";
    public ObjectiveType Type { get; set; }
    public string Target { get; set; } = "any";
    public int RequiredAmount { get; set; } = 1;
    public int CurrentProgress { get; set; }
    public bool Completed { get; set; }
    public string Hint { get; set; } = "";
    public bool Optional { get; set; }

    public QuestObjective Clone() => new()
    {
        Id = Id,
        Description = Description,
        Type = Type,
        Target = Target,
        RequiredAmount = RequiredAmount,
        CurrentProgress = 0,
        Completed = false,
        Hint = Hint,
        Optional = Optional
    };
}

/// <summary>
/// Rewards for completing a quest.
/// </summary>
public class QuestReward
{
    public int Xp { get; set; }
    public int Coins { get; set; }
    public List<string> Items { get; set; } = new();
    public List<string> Unlocks { get; set; } = new();
    public string? Title { get; set; }
    public string? Achievement { get; set; }
}

/// <summary>
/// A step in a quest with dialogue and objectives.
/// </summary>
public class QuestStep
{
    public int StepId { get; set; }
    public string Title { get; set; } = "";
    public List<string> Dialogue { get; set; } = new();
    public List<QuestObjective> Objectives { get; set; } = new();
    public QuestReward? Rewards { get; set; }
    public Dictionary<string, int>? Choices { get; set; } // choice_text -> next_step_id
    public int? NextStepId { get; set; }
}

/// <summary>
/// A complete quest with multiple steps.
/// </summary>
public class Quest
{
    public string Id { get; set; } = "";
    public string Name { get; set; } = "";
    public string Description { get; set; } = "";
    public QuestType Type { get; set; }
    public QuestDifficulty Difficulty { get; set; }
    public List<QuestStep> Steps { get; set; } = new();
    public QuestReward FinalReward { get; set; } = new();
    public List<string> PrerequisiteQuests { get; set; } = new();
    public int RequiredLevel { get; set; } = 1;
    public int? TimeLimitHours { get; set; }
    public bool Repeatable { get; set; }
}

/// <summary>
/// An active quest being tracked.
/// </summary>
public class ActiveQuest
{
    public string QuestId { get; set; } = "";
    public int CurrentStep { get; set; } = 1;
    public DateTime StartedAt { get; set; } = DateTime.UtcNow;
    public Dictionary<string, int> StepProgress { get; set; } = new();
    public List<string> ChoicesMade { get; set; } = new();
    public bool Completed { get; set; }
    public bool Failed { get; set; }
}

/// <summary>
/// Result of a quest progress update.
/// </summary>
public class QuestUpdate
{
    public string QuestId { get; set; } = "";
    public string Description { get; set; } = "";
    public bool ObjectiveCompleted { get; set; }
}

/// <summary>
/// Status information for an active quest.
/// </summary>
public class QuestStatus
{
    public string QuestName { get; set; } = "";
    public string StepTitle { get; set; } = "";
    public List<ObjectiveStatus> Objectives { get; set; } = new();
    public bool HasChoices { get; set; }
    public List<string> Choices { get; set; } = new();
}

public class ObjectiveStatus
{
    public string Description { get; set; } = "";
    public int Progress { get; set; }
    public int Required { get; set; }
    public bool Completed { get; set; }
}

/// <summary>
/// Manages quests, objectives, and story progression.
/// </summary>
public class QuestSystem
{
    // =============================================================================
    // QUEST DEFINITIONS
    // =============================================================================

    public static readonly Dictionary<string, Quest> AllQuests = new()
    {
        // === TUTORIAL QUEST ===
        ["welcome_duckling"] = new()
        {
            Id = "welcome_duckling",
            Name = "Welcome, Little Duckling!",
            Description = "Learn the basics of caring for your new duck friend.",
            Type = QuestType.Main,
            Difficulty = QuestDifficulty.Easy,
            Steps = new()
            {
                new()
                {
                    StepId = 1,
                    Title = "First Steps",
                    Dialogue = new()
                    {
                        "🦆 *quack quack!*",
                        "Your little duckling looks up at you with big curious eyes.",
                        "It seems hungry... maybe you should feed it!"
                    },
                    Objectives = new()
                    {
                        new() { Id = "feed_1", Description = "Feed your duck", Type = ObjectiveType.Feed, Target = "any", RequiredAmount = 1, Hint = "Press 'F' to feed your duck!" }
                    },
                    NextStepId = 2
                },
                new()
                {
                    StepId = 2,
                    Title = "Playtime!",
                    Dialogue = new()
                    {
                        "Your duck happily gobbles up the food!",
                        "*satisfied quack*",
                        "Now it seems energetic and wants to play!"
                    },
                    Objectives = new()
                    {
                        new() { Id = "play_1", Description = "Play with your duck", Type = ObjectiveType.Play, Target = "any", RequiredAmount = 2, Hint = "Press 'P' to play with your duck!" }
                    },
                    NextStepId = 3
                },
                new()
                {
                    StepId = 3,
                    Title = "Getting to Know Each Other",
                    Dialogue = new()
                    {
                        "Your duck is having so much fun!",
                        "It waddles over and nudges your hand affectionately.",
                        "Try talking to your duck to bond with it!"
                    },
                    Objectives = new()
                    {
                        new() { Id = "talk_1", Description = "Talk to your duck", Type = ObjectiveType.Talk, Target = "any", RequiredAmount = 1, Hint = "Press 'T' to chat with your duck!" }
                    },
                    Rewards = new() { Xp = 25, Coins = 10 }
                }
            },
            FinalReward = new()
            {
                Xp = 50,
                Coins = 25,
                Items = new() { "welcome_bread", "duck_toy" },
                Title = "Duckling Caretaker"
            }
        },

        // === THE LOST FEATHER ===
        ["lost_feather"] = new()
        {
            Id = "lost_feather",
            Name = "The Lost Feather",
            Description = "Help your duck find its lost special feather!",
            Type = QuestType.Main,
            Difficulty = QuestDifficulty.Medium,
            PrerequisiteQuests = new() { "welcome_duckling" },
            Steps = new()
            {
                new()
                {
                    StepId = 1,
                    Title = "Something Missing",
                    Dialogue = new()
                    {
                        "Your duck seems distressed! *sad quack*",
                        "It keeps looking at its wing, as if something is missing.",
                        "Oh no! Your duck has lost a special golden feather!",
                        "You should search around the pond area."
                    },
                    Objectives = new()
                    {
                        new() { Id = "explore_pond", Description = "Explore the pond", Type = ObjectiveType.Explore, Target = "pond", RequiredAmount = 1, Hint = "Go to the pond area to look for clues!" }
                    },
                    NextStepId = 2
                },
                new()
                {
                    StepId = 2,
                    Title = "Following Clues",
                    Dialogue = new()
                    {
                        "You found some tiny golden sparkles by the pond!",
                        "The trail leads toward the garden...",
                        "But first, you should ask around."
                    },
                    Objectives = new()
                    {
                        new() { Id = "talk_3", Description = "Ask about the feather", Type = ObjectiveType.Talk, Target = "any", RequiredAmount = 3 },
                        new() { Id = "explore_garden", Description = "Search the garden", Type = ObjectiveType.Explore, Target = "garden", RequiredAmount = 1 }
                    },
                    NextStepId = 3
                },
                new()
                {
                    StepId = 3,
                    Title = "The Magpie's Nest",
                    Dialogue = new()
                    {
                        "You found it! A mischievous magpie took the feather!",
                        "The magpie looks at you curiously...",
                        "It seems like it wants something shiny in exchange."
                    },
                    Objectives = new()
                    {
                        new() { Id = "collect_shiny", Description = "Find something shiny to trade", Type = ObjectiveType.Collect, Target = "shiny_object", RequiredAmount = 1, Hint = "Try fishing or digging for treasures!" }
                    },
                    Rewards = new() { Xp = 50, Coins = 30 }
                }
            },
            FinalReward = new()
            {
                Xp = 100,
                Coins = 75,
                Items = new() { "golden_feather", "magpie_friendship_charm" },
                Title = "Feather Finder",
                Achievement = "first_quest_chain"
            }
        },

        // === THE GREAT FISH TALE ===
        ["great_fish_tale"] = new()
        {
            Id = "great_fish_tale",
            Name = "The Great Fish Tale",
            Description = "Prove yourself as a master fisher!",
            Type = QuestType.Side,
            Difficulty = QuestDifficulty.Medium,
            Steps = new()
            {
                new()
                {
                    StepId = 1,
                    Title = "Fishy Beginnings",
                    Dialogue = new()
                    {
                        "An old duck fisherman waddles by...",
                        "🦆 'Heard you're new to fishing, eh?'",
                        "'Back in my day, we caught fish as big as logs!'",
                        "'Prove yourself by catching some fish!'"
                    },
                    Objectives = new()
                    {
                        new() { Id = "fish_5", Description = "Catch 5 fish", Type = ObjectiveType.Fish, Target = "any", RequiredAmount = 5 }
                    },
                    Rewards = new() { Xp = 30, Coins = 20, Items = new() { "better_bait" } },
                    NextStepId = 2
                },
                new()
                {
                    StepId = 2,
                    Title = "The Hunt for Ol' Whiskers",
                    Dialogue = new()
                    {
                        "🦆 'Not bad, not bad!'",
                        "'But have you heard of Ol' Whiskers?'",
                        "'The legendary catfish that lurks in the deep!'",
                        "'Many have tried to catch it... none have succeeded.'"
                    },
                    Objectives = new()
                    {
                        new() { Id = "fish_rare", Description = "Catch a rare fish", Type = ObjectiveType.Fish, Target = "rare", RequiredAmount = 1 }
                    }
                }
            },
            FinalReward = new()
            {
                Xp = 150,
                Coins = 100,
                Items = new() { "master_fishing_rod", "fish_trophy" },
                Title = "Master Angler"
            }
        },

        // === GARDEN OF DREAMS ===
        ["garden_dreams"] = new()
        {
            Id = "garden_dreams",
            Name = "Garden of Dreams",
            Description = "Grow a magical garden with special flowers!",
            Type = QuestType.Side,
            Difficulty = QuestDifficulty.Medium,
            Steps = new()
            {
                new()
                {
                    StepId = 1,
                    Title = "Seeds of Wonder",
                    Dialogue = new()
                    {
                        "A mysterious packet of seeds blows into your garden...",
                        "The packet reads: 'Dream Seeds - Handle with Care'",
                        "You feel a strange magic emanating from them.",
                        "Plant them and see what grows!"
                    },
                    Objectives = new()
                    {
                        new() { Id = "plant_3", Description = "Plant 3 seeds", Type = ObjectiveType.Garden, Target = "plant", RequiredAmount = 3 }
                    },
                    Rewards = new() { Coins = 15 },
                    NextStepId = 2
                },
                new()
                {
                    StepId = 2,
                    Title = "Nurturing Growth",
                    Dialogue = new()
                    {
                        "The seeds have sprouted! But they need special care.",
                        "Keep them watered and watch them bloom!"
                    },
                    Objectives = new()
                    {
                        new() { Id = "water_10", Description = "Water plants 10 times", Type = ObjectiveType.Garden, Target = "water", RequiredAmount = 10 },
                        new() { Id = "harvest_3", Description = "Harvest 3 plants", Type = ObjectiveType.Garden, Target = "harvest", RequiredAmount = 3 }
                    }
                }
            },
            FinalReward = new()
            {
                Xp = 120,
                Coins = 80,
                Items = new() { "dream_flower", "enchanted_seeds" },
                Title = "Dream Gardener",
                Unlocks = new() { "golden_flower_seed" }
            }
        },

        // === THE MYSTERIOUS STRANGER (Hidden Quest with Choices) ===
        ["mysterious_stranger"] = new()
        {
            Id = "mysterious_stranger",
            Name = "The Mysterious Stranger",
            Description = "A cloaked figure has appeared with an unusual request...",
            Type = QuestType.Hidden,
            Difficulty = QuestDifficulty.Hard,
            Steps = new()
            {
                new()
                {
                    StepId = 1,
                    Title = "An Unusual Visitor",
                    Dialogue = new()
                    {
                        "A cloaked duck appears from the shadows...",
                        "🦆 '...I've been watching you...'",
                        "'You have shown kindness. That is rare.'",
                        "'I have a task... if you're brave enough.'"
                    },
                    Choices = new()
                    {
                        ["Accept the challenge"] = 2,
                        ["Ask for more details first"] = 3,
                        ["Politely decline"] = -1
                    },
                    Objectives = new()
                    {
                        new() { Id = "choice_1", Description = "Make your choice", Type = ObjectiveType.Choice, Target = "any", RequiredAmount = 1 }
                    }
                },
                new()
                {
                    StepId = 2,
                    Title = "The Brave Path",
                    Dialogue = new()
                    {
                        "'Courage! I like that.'",
                        "'Seek the three ancient tokens hidden in this land.'",
                        "'One in the water, one in the earth, one in the sky.'"
                    },
                    Objectives = new()
                    {
                        new() { Id = "find_token_water", Description = "Find the Water Token", Type = ObjectiveType.Find, Target = "water_token", RequiredAmount = 1, Hint = "Try fishing in the deepest waters..." },
                        new() { Id = "find_token_earth", Description = "Find the Earth Token", Type = ObjectiveType.Find, Target = "earth_token", RequiredAmount = 1, Hint = "Dig for buried treasures..." },
                        new() { Id = "find_token_sky", Description = "Find the Sky Token", Type = ObjectiveType.Find, Target = "sky_token", RequiredAmount = 1, Hint = "Sometimes treasures fall from above during special weather..." }
                    },
                    NextStepId = 4
                },
                new()
                {
                    StepId = 3,
                    Title = "The Cautious Path",
                    Dialogue = new()
                    {
                        "'A wise one, you are.'",
                        "'I am a guardian of old secrets.'",
                        "'There is an ancient power scattered across this land.'",
                        "'Help me gather it, and you shall be rewarded greatly.'"
                    },
                    Objectives = new()
                    {
                        new() { Id = "learn_more", Description = "Learn about the tokens", Type = ObjectiveType.Talk, Target = "guardian", RequiredAmount = 3 }
                    },
                    NextStepId = 2
                },
                new()
                {
                    StepId = 4,
                    Title = "The Revelation",
                    Dialogue = new()
                    {
                        "You've gathered all three tokens!",
                        "The mysterious figure's cloak falls away...",
                        "It's a magnificent ancient duck, glowing with ethereal light!",
                        "'You have proven yourself worthy.'",
                        "'These tokens... they are keys to great power.'",
                        "'Use them wisely.'"
                    },
                    Objectives = new()
                }
            },
            FinalReward = new()
            {
                Xp = 500,
                Coins = 300,
                Items = new() { "ancient_amulet", "guardian_blessing" },
                Title = "Token Bearer",
                Achievement = "mysterious_quest_complete",
                Unlocks = new() { "secret_area" }
            }
        },

        // === DAILY QUEST: MORNING ROUTINE ===
        ["daily_morning"] = new()
        {
            Id = "daily_morning",
            Name = "Morning Routine",
            Description = "Start the day right with your duck!",
            Type = QuestType.Daily,
            Difficulty = QuestDifficulty.Easy,
            Repeatable = true,
            TimeLimitHours = 24,
            Steps = new()
            {
                new()
                {
                    StepId = 1,
                    Title = "Rise and Shine",
                    Dialogue = new()
                    {
                        "A new day begins!",
                        "Time to take care of your duck's morning needs."
                    },
                    Objectives = new()
                    {
                        new() { Id = "feed_morning", Description = "Feed your duck breakfast", Type = ObjectiveType.Feed, Target = "any", RequiredAmount = 1 },
                        new() { Id = "play_morning", Description = "Morning playtime", Type = ObjectiveType.Play, Target = "any", RequiredAmount = 1 },
                        new() { Id = "talk_morning", Description = "Morning chat", Type = ObjectiveType.Talk, Target = "any", RequiredAmount = 1 }
                    }
                }
            },
            FinalReward = new()
            {
                Xp = 20,
                Coins = 15
            }
        },

        // === SEASONAL QUEST ===
        ["spring_festival"] = new()
        {
            Id = "spring_festival",
            Name = "Spring Festival",
            Description = "Celebrate the arrival of spring with special activities!",
            Type = QuestType.Seasonal,
            Difficulty = QuestDifficulty.Medium,
            Steps = new()
            {
                new()
                {
                    StepId = 1,
                    Title = "Festival Preparations",
                    Dialogue = new()
                    {
                        "Spring has arrived! The festival is coming!",
                        "Help prepare by gathering flowers and decorations."
                    },
                    Objectives = new()
                    {
                        new() { Id = "collect_flowers", Description = "Collect spring flowers", Type = ObjectiveType.Collect, Target = "wildflower", RequiredAmount = 10 },
                        new() { Id = "plant_flowers", Description = "Plant festival flowers", Type = ObjectiveType.Garden, Target = "plant", RequiredAmount = 5 }
                    },
                    NextStepId = 2
                },
                new()
                {
                    StepId = 2,
                    Title = "Festival Day",
                    Dialogue = new()
                    {
                        "The festival is here! Time to celebrate!",
                        "Enjoy the festivities with your duck!"
                    },
                    Objectives = new()
                    {
                        new() { Id = "play_festival", Description = "Play festival games", Type = ObjectiveType.Play, Target = "any", RequiredAmount = 5 },
                        new() { Id = "explore_festival", Description = "Explore the festival", Type = ObjectiveType.Explore, Target = "festival_area", RequiredAmount = 1 }
                    }
                }
            },
            FinalReward = new()
            {
                Xp = 200,
                Coins = 150,
                Items = new() { "spring_wreath", "festival_hat", "cherry_blossom" },
                Title = "Spring Celebrant"
            }
        }
    };

    // =============================================================================
    // STATE
    // =============================================================================

    public Dictionary<string, ActiveQuest> ActiveQuests { get; set; } = new();
    public Dictionary<string, int> CompletedQuests { get; set; } = new();
    public List<string> FailedQuests { get; set; } = new();
    public List<string> UnlockedQuests { get; set; } = new() { "welcome_duckling" };
    public int TotalQuestsCompleted { get; set; }
    public Dictionary<string, List<string>> ChoicesHistory { get; set; } = new();
    public List<string> EarnedTitles { get; set; } = new();
    public Dictionary<string, int> QuestChainProgress { get; set; } = new();

    // =============================================================================
    // QUEST ACCESS
    // =============================================================================

    public List<Quest> GetAvailableQuests(int playerLevel = 1)
    {
        var available = new List<Quest>();

        foreach (var questId in UnlockedQuests)
        {
            if (ActiveQuests.ContainsKey(questId))
                continue;

            if (CompletedQuests.ContainsKey(questId))
            {
                if (!AllQuests.TryGetValue(questId, out var q) || !q.Repeatable)
                    continue;
            }

            if (!AllQuests.TryGetValue(questId, out var quest))
                continue;

            var prereqsMet = quest.PrerequisiteQuests.All(pq => CompletedQuests.ContainsKey(pq));
            if (prereqsMet && playerLevel >= quest.RequiredLevel)
                available.Add(quest);
        }

        return available;
    }

    public List<Quest> GetActiveQuestsList() =>
        ActiveQuests.Keys
            .Where(qid => AllQuests.ContainsKey(qid))
            .Select(qid => AllQuests[qid])
            .ToList();

    // =============================================================================
    // QUEST ACTIONS
    // =============================================================================

    public (bool Success, string Message, List<string>? Dialogue) StartQuest(string questId)
    {
        if (ActiveQuests.ContainsKey(questId))
            return (false, "Quest already in progress!", null);

        if (!AllQuests.TryGetValue(questId, out var quest))
            return (false, "Quest not found!", null);

        var active = new ActiveQuest
        {
            QuestId = questId,
            CurrentStep = 1,
            StartedAt = DateTime.UtcNow
        };

        ActiveQuests[questId] = active;

        var firstStep = quest.Steps.FirstOrDefault(s => s.StepId == 1);
        var dialogue = firstStep?.Dialogue;

        return (true, $"📜 Quest Started: {quest.Name}", dialogue);
    }

    public List<QuestUpdate> UpdateProgress(string objectiveType, string target, int amount = 1)
    {
        var updates = new List<QuestUpdate>();

        foreach (var (questId, active) in ActiveQuests.ToList())
        {
            if (active.Completed)
                continue;

            if (!AllQuests.TryGetValue(questId, out var quest))
                continue;

            var currentStep = quest.Steps.FirstOrDefault(s => s.StepId == active.CurrentStep);
            if (currentStep == null)
                continue;

            foreach (var objective in currentStep.Objectives)
            {
                if (objective.Completed)
                    continue;

                if (!objective.Type.ToString().Equals(objectiveType, StringComparison.OrdinalIgnoreCase))
                    continue;

                if (objective.Target != "any" && !objective.Target.Equals(target, StringComparison.OrdinalIgnoreCase))
                    continue;

                var objKey = $"{questId}_{objective.Id}";
                var current = active.StepProgress.GetValueOrDefault(objKey);
                var newProgress = Math.Min(current + amount, objective.RequiredAmount);
                active.StepProgress[objKey] = newProgress;

                var completed = newProgress >= objective.RequiredAmount;
                updates.Add(new QuestUpdate
                {
                    QuestId = questId,
                    Description = objective.Description,
                    ObjectiveCompleted = completed
                });
            }
        }

        // Check for step completions
        foreach (var questId in ActiveQuests.Keys.ToList())
            CheckStepCompletion(questId);

        return updates;
    }

    public (bool Success, string Message, int? NextStep) MakeChoice(string questId, string choice)
    {
        if (!ActiveQuests.TryGetValue(questId, out var active))
            return (false, "Quest not active!", null);

        if (!AllQuests.TryGetValue(questId, out var quest))
            return (false, "Quest not found!", null);

        var currentStep = quest.Steps.FirstOrDefault(s => s.StepId == active.CurrentStep);
        if (currentStep?.Choices == null || !currentStep.Choices.Any())
            return (false, "No choices available!", null);

        if (!currentStep.Choices.TryGetValue(choice, out var nextStep))
            return (false, "Invalid choice!", null);

        active.ChoicesMade.Add(choice);

        if (!ChoicesHistory.ContainsKey(questId))
            ChoicesHistory[questId] = new();
        ChoicesHistory[questId].Add(choice);

        // Keep history manageable
        if (ChoicesHistory[questId].Count > 50)
            ChoicesHistory[questId] = ChoicesHistory[questId].TakeLast(50).ToList();

        // Handle quest end (-1 means fail)
        if (nextStep == -1)
        {
            active.Failed = true;
            FailedQuests.Add(questId);
            ActiveQuests.Remove(questId);
            return (true, "Quest ended based on your choice.", null);
        }

        // Complete choice objective
        foreach (var obj in currentStep.Objectives.Where(o => o.Type == ObjectiveType.Choice))
        {
            var objKey = $"{questId}_{obj.Id}";
            active.StepProgress[objKey] = obj.RequiredAmount;
        }

        active.CurrentStep = nextStep;
        return (true, $"You chose: {choice}", nextStep);
    }

    private void CheckStepCompletion(string questId)
    {
        if (!ActiveQuests.TryGetValue(questId, out var active) || active.Completed)
            return;

        if (!AllQuests.TryGetValue(questId, out var quest))
            return;

        var currentStep = quest.Steps.FirstOrDefault(s => s.StepId == active.CurrentStep);
        if (currentStep == null)
            return;

        var requiredObjectives = currentStep.Objectives.Where(o => !o.Optional);
        var allComplete = requiredObjectives.All(o =>
            active.StepProgress.GetValueOrDefault($"{questId}_{o.Id}") >= o.RequiredAmount);

        if (!allComplete)
            return;

        if (currentStep.NextStepId.HasValue)
            active.CurrentStep = currentStep.NextStepId.Value;
        else
            CompleteQuest(questId);
    }

    private void CompleteQuest(string questId)
    {
        if (!ActiveQuests.TryGetValue(questId, out var active))
            return;

        active.Completed = true;

        if (!AllQuests.TryGetValue(questId, out var quest))
            return;

        CompletedQuests[questId] = CompletedQuests.GetValueOrDefault(questId) + 1;
        TotalQuestsCompleted++;

        if (!string.IsNullOrEmpty(quest.FinalReward.Title))
            EarnedTitles.Add(quest.FinalReward.Title);

        // Unlock follow-up quests
        foreach (var (qId, q) in AllQuests)
        {
            if (q.PrerequisiteQuests.Contains(questId) && !UnlockedQuests.Contains(qId))
                UnlockedQuests.Add(qId);
        }

        ActiveQuests.Remove(questId);
    }

    // =============================================================================
    // STATUS
    // =============================================================================

    public QuestStatus? GetActiveQuestStatus(string questId)
    {
        if (!ActiveQuests.TryGetValue(questId, out var active))
            return null;

        if (!AllQuests.TryGetValue(questId, out var quest))
            return null;

        var currentStep = quest.Steps.FirstOrDefault(s => s.StepId == active.CurrentStep);

        var objectives = currentStep?.Objectives.Select(obj =>
        {
            var progress = active.StepProgress.GetValueOrDefault($"{questId}_{obj.Id}");
            return new ObjectiveStatus
            {
                Description = obj.Description,
                Progress = progress,
                Required = obj.RequiredAmount,
                Completed = progress >= obj.RequiredAmount
            };
        }).ToList() ?? new();

        return new QuestStatus
        {
            QuestName = quest.Name,
            StepTitle = currentStep?.Title ?? "",
            Objectives = objectives,
            HasChoices = currentStep?.Choices?.Any() == true,
            Choices = currentStep?.Choices?.Keys.ToList() ?? new()
        };
    }

    public List<string> RenderQuestLog()
    {
        var lines = new List<string>
        {
            "╔═══════════════════════════════════════════════╗",
            "║            📜 QUEST LOG 📜                    ║",
            "╠═══════════════════════════════════════════════╣"
        };

        if (ActiveQuests.Any())
        {
            lines.Add("║  ACTIVE QUESTS:                               ║");
            foreach (var (questId, active) in ActiveQuests)
            {
                if (!AllQuests.TryGetValue(questId, out var quest))
                    continue;

                lines.Add($"║  ► {quest.Name.PadRight(35).Substring(0, 35)}      ║");
                var status = GetActiveQuestStatus(questId);
                if (status != null)
                {
                    foreach (var obj in status.Objectives.Take(2))
                    {
                        var mark = obj.Completed ? "✓" : "○";
                        lines.Add($"║    {mark} {obj.Description.PadRight(33).Substring(0, 33)}  ║");
                    }
                }
            }
            lines.Add("╠═══════════════════════════════════════════════╣");
        }

        var available = GetAvailableQuests();
        if (available.Any())
        {
            lines.Add("║  AVAILABLE QUESTS:                            ║");
            foreach (var quest in available.Take(3))
            {
                var icon = quest.Difficulty switch
                {
                    QuestDifficulty.Easy => "⭐",
                    QuestDifficulty.Medium => "⭐⭐",
                    QuestDifficulty.Hard => "⭐⭐⭐",
                    QuestDifficulty.Legendary => "💎",
                    _ => "⭐"
                };
                lines.Add($"║  {icon} {quest.Name.PadRight(33).Substring(0, 33)}    ║");
            }
        }

        lines.Add("╠═══════════════════════════════════════════════╣");
        lines.Add($"║  Completed: {TotalQuestsCompleted,3}  |  Titles: {EarnedTitles.Count,3}          ║");
        lines.Add("╚═══════════════════════════════════════════════╝");

        return lines;
    }

    // =============================================================================
    // SERIALIZATION
    // =============================================================================

    public QuestSaveData ToSaveData() => new()
    {
        ActiveQuests = ActiveQuests.ToDictionary(
            kvp => kvp.Key,
            kvp => new ActiveQuestSaveData
            {
                QuestId = kvp.Value.QuestId,
                CurrentStep = kvp.Value.CurrentStep,
                StartedAt = kvp.Value.StartedAt.ToString("o"),
                StepProgress = kvp.Value.StepProgress,
                ChoicesMade = kvp.Value.ChoicesMade,
                Completed = kvp.Value.Completed,
                Failed = kvp.Value.Failed
            }),
        CompletedQuests = CompletedQuests,
        FailedQuests = FailedQuests,
        UnlockedQuests = UnlockedQuests,
        TotalQuestsCompleted = TotalQuestsCompleted,
        ChoicesHistory = ChoicesHistory,
        EarnedTitles = EarnedTitles,
        QuestChainProgress = QuestChainProgress
    };

    public static QuestSystem FromSaveData(QuestSaveData data)
    {
        var system = new QuestSystem
        {
            CompletedQuests = data.CompletedQuests ?? new(),
            FailedQuests = data.FailedQuests ?? new(),
            UnlockedQuests = data.UnlockedQuests ?? new() { "welcome_duckling" },
            TotalQuestsCompleted = data.TotalQuestsCompleted,
            ChoicesHistory = data.ChoicesHistory ?? new(),
            EarnedTitles = data.EarnedTitles ?? new(),
            QuestChainProgress = data.QuestChainProgress ?? new()
        };

        if (data.ActiveQuests != null)
        {
            foreach (var (questId, aqData) in data.ActiveQuests)
            {
                DateTime.TryParse(aqData.StartedAt, out var started);
                system.ActiveQuests[questId] = new ActiveQuest
                {
                    QuestId = aqData.QuestId ?? questId,
                    CurrentStep = aqData.CurrentStep,
                    StartedAt = started,
                    StepProgress = aqData.StepProgress ?? new(),
                    ChoicesMade = aqData.ChoicesMade ?? new(),
                    Completed = aqData.Completed,
                    Failed = aqData.Failed
                };
            }
        }

        return system;
    }
}

public class ActiveQuestSaveData
{
    public string? QuestId { get; set; }
    public int CurrentStep { get; set; }
    public string? StartedAt { get; set; }
    public Dictionary<string, int>? StepProgress { get; set; }
    public List<string>? ChoicesMade { get; set; }
    public bool Completed { get; set; }
    public bool Failed { get; set; }
}

public class QuestSaveData
{
    public Dictionary<string, ActiveQuestSaveData>? ActiveQuests { get; set; }
    public Dictionary<string, int>? CompletedQuests { get; set; }
    public List<string>? FailedQuests { get; set; }
    public List<string>? UnlockedQuests { get; set; }
    public int TotalQuestsCompleted { get; set; }
    public Dictionary<string, List<string>>? ChoicesHistory { get; set; }
    public List<string>? EarnedTitles { get; set; }
    public Dictionary<string, int>? QuestChainProgress { get; set; }
}
