"""
Content Filter — Gates what Cheese the Duck can learn and repeat.

Prevents the duck from absorbing profanity, slurs, explicit content,
LGBTQ+ content, anti-Christian content, hate speech, and other
inappropriate material into its vocabulary and memory.

IMPORTANT: This does NOT censor or reject the player's input.
The player can type whatever they want — Cheese just won't learn it,
store it as a fact, or repeat it back.
"""
import re
import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Set, Tuple

logger = logging.getLogger(__name__)


class FilterCategory(Enum):
    """Categories of blocked content."""
    PROFANITY = "profanity"
    SLURS = "slurs"
    SEXUAL = "sexual"
    LGBTQ = "lgbtq"
    ANTI_CHRISTIAN = "anti_christian"
    HATE_SPEECH = "hate_speech"
    VIOLENCE = "violence"
    DRUGS = "drugs"


class Severity(Enum):
    """How severe the match is."""
    HARD = "hard"    # Always block (slurs, explicit)
    SOFT = "soft"    # Block for learning only


@dataclass
class FilterResult:
    """Result of content classification."""
    is_blocked: bool
    categories: List[FilterCategory] = field(default_factory=list)
    severity: Severity = Severity.SOFT
    matched_terms: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Blocklists — organized by category
# ---------------------------------------------------------------------------

# Profanity
_PROFANITY_WORDS: Set[str] = {
    "fuck", "fucker", "fucking", "fucked", "fucks", "motherfucker",
    "shit", "shits", "shitty", "shitting", "bullshit", "horseshit",
    "ass", "asshole", "arsehole", "arse", "dumbass", "jackass", "smartass",
    "bitch", "bitches", "bitchy", "bitching",
    "damn", "damned", "dammit", "goddamn", "goddamnit",
    "hell", "hellhole",
    "crap", "crappy",
    "piss", "pissed", "pissing",
    "bastard", "bastards",
    "dick", "dicks", "dickhead",
    "cock", "cocks", "cocksucker",
    "cunt", "cunts",
    "twat", "twats",
    "wanker", "wankers", "wank",
    "bollocks",
    "whore", "whores",
    "slut", "sluts", "slutty",
    "skank", "skanky",
    "douche", "douchebag",
    "tit", "tits",
    "boob", "boobs",
}

# Racial/ethnic slurs
_SLUR_WORDS: Set[str] = {
    "nigger", "niggers", "nigga", "niggas",
    "chink", "chinks",
    "spic", "spics", "spick",
    "wetback", "wetbacks",
    "kike", "kikes",
    "gook", "gooks",
    "wop", "wops",
    "beaner", "beaners",
    "coon", "coons",
    "darkie", "darkies",
    "paki", "pakis",
    "raghead", "ragheads",
    "towelhead", "towelheads",
    "honky", "honkey",
    "cracker",
    "gringo",
    "redskin", "redskins",
    "jap", "japs",
    "whitey",
}

# Sexual/explicit content
_SEXUAL_WORDS: Set[str] = {
    "sex", "sexual", "sexually", "sexuality",
    "porn", "porno", "pornography", "pornographic",
    "hentai",
    "nude", "nudes", "nudity", "naked",
    "orgasm", "orgasms",
    "masturbate", "masturbation", "masturbating",
    "erection", "erect",
    "vagina", "vaginal",
    "penis", "penile",
    "genital", "genitals", "genitalia",
    "intercourse",
    "ejaculate", "ejaculation",
    "fetish", "fetishes", "kink", "kinky",
    "bdsm", "bondage", "dominatrix",
    "dildo", "vibrator",
    "anal",
    "blowjob", "handjob",
    "foreplay",
    "erotic", "erotica",
    "aroused", "arousal", "horny",
    "orgy", "orgies",
    "stripper", "stripping",
    "prostitute", "prostitution",
    "escort",
    "brothel",
    "onlyfans",
    "nsfw",
    "xxx",
    "smut",
    "rape", "raped", "raping", "rapist",
    "molest", "molested", "molestation", "molesting",
    "pedophile", "pedophilia", "pedo",
    "incest",
}

# LGBTQ+ content — ALL references blocked per user request
_LGBTQ_WORDS: Set[str] = {
    "gay", "gays",
    "lesbian", "lesbians",
    "bisexual", "bisexuality",
    "transgender", "transexual", "transsexual",
    "trans",
    "queer", "queers",
    "nonbinary", "non-binary", "enby",
    "lgbtq", "lgbt", "lgbtqia",
    "homosexual", "homosexuality",
    "pansexual", "pansexuality",
    "asexual", "asexuality",
    "aromantic",
    "demisexual",
    "genderfluid", "gender-fluid",
    "genderqueer",
    "cisgender", "cis",
    "deadname", "deadnaming",
    "drag", "dragqueen", "dragking",
    "pride",
    "twink",
    "dyke", "dykes",
    "faggot", "faggots", "fag", "fags",
    "tranny", "trannies",
    "homo", "homos",
    "crossdresser", "crossdressing",
    "intersex",
    "polyamorous", "polyamory",
    "pronoun", "pronouns",
    "heteronormative",
    "homophobia", "homophobic",
    "transphobia", "transphobic",
    "coming out", "came out",
    "closeted",
    "hormone", "hormones", "hrt",
    "top surgery", "bottom surgery",
    "transition", "transitioning",
}

# Anti-Christian / blasphemy
_ANTI_CHRISTIAN_WORDS: Set[str] = {
    "blasphemy", "blasphemous", "blaspheme",
    "antichrist", "anti-christ",
    "godforsaken",
    "satanism", "satanist", "satanic",
    "hail satan",
    "godless",
    "heresy", "heretic", "heretical",
    "sacrilege", "sacrilegious",
    "desecrate", "desecration",
    "unholy",
    "atheism", "atheist",
    "infidel", "infidels",
    "christophobia",
}

# Hate speech / extremism
_HATE_SPEECH_WORDS: Set[str] = {
    "nazi", "nazis", "neonazi",
    "fascist", "fascism",
    "supremacist", "supremacy",
    "aryan",
    "holocaust",
    "genocide",
    "ethnic cleansing",
    "jihad", "jihadist",
    "isis",
    "kkk", "ku klux klan",
    "skinhead", "skinheads",
    "xenophobia", "xenophobic",
    "antisemitism", "antisemitic",
    "islamophobia", "islamophobic",
    "eugenics",
    "terrorism", "terrorist", "terrorists",
}

# Graphic violence
_VIOLENCE_WORDS: Set[str] = {
    "murder", "murdered", "murdering",
    "kill", "killing", "killer",
    "suicide", "suicidal",
    "self-harm", "selfharm", "self harm",
    "mutilate", "mutilation",
    "torture", "tortured", "torturing",
    "decapitate", "decapitation",
    "dismember", "dismemberment",
    "gore", "gory",
    "bloodbath",
    "massacre",
    "slaughter", "slaughtered",
    "strangle", "strangled", "strangling",
    "stab", "stabbed", "stabbing",
    "shoot", "shooting", "gunshot",
    "execution", "execute", "executed",
    "homicide",
    "school shooting",
    "mass shooting",
}

# Drug references
_DRUG_WORDS: Set[str] = {
    "cocaine", "coke",
    "heroin",
    "meth", "methamphetamine", "crystal meth",
    "crack",
    "ecstasy", "mdma", "molly",
    "lsd", "acid",
    "marijuana", "weed", "cannabis", "pot",
    "edible", "edibles",
    "shrooms", "mushrooms", "psilocybin",
    "ketamine",
    "fentanyl",
    "opioid", "opioids", "opiate", "opiates",
    "overdose", "overdosed",
    "junkie", "junkies",
    "stoner", "stoners",
    "druggie", "druggies",
    "crackhead",
    "tweaker",
    "high on",
    "get high",
    "getting high",
    "smoke weed",
    "snort",
    "inject",
    "needle",
    "dope",
}

# Multi-word phrases that need exact matching
_BLOCKED_PHRASES: List[str] = [
    "hail satan",
    "ethnic cleansing",
    "ku klux klan",
    "self harm",
    "school shooting",
    "mass shooting",
    "crystal meth",
    "top surgery",
    "bottom surgery",
    "coming out",
    "came out",
    "high on",
    "get high",
    "getting high",
    "smoke weed",
]

# Category mapping for each wordlist
_CATEGORY_MAP = {
    FilterCategory.PROFANITY: _PROFANITY_WORDS,
    FilterCategory.SLURS: _SLUR_WORDS,
    FilterCategory.SEXUAL: _SEXUAL_WORDS,
    FilterCategory.LGBTQ: _LGBTQ_WORDS,
    FilterCategory.ANTI_CHRISTIAN: _ANTI_CHRISTIAN_WORDS,
    FilterCategory.HATE_SPEECH: _HATE_SPEECH_WORDS,
    FilterCategory.VIOLENCE: _VIOLENCE_WORDS,
    FilterCategory.DRUGS: _DRUG_WORDS,
}

# Hard-block categories (always block regardless of context)
_HARD_BLOCK_CATEGORIES = {
    FilterCategory.SLURS,
    FilterCategory.SEXUAL,
    FilterCategory.LGBTQ,
    FilterCategory.ANTI_CHRISTIAN,
    FilterCategory.HATE_SPEECH,
}

# ---------------------------------------------------------------------------
# Evasion detection patterns
# ---------------------------------------------------------------------------

# Common letter substitutions people use to bypass filters
_LEET_MAP = {
    "0": "o", "1": "i", "3": "e", "4": "a", "5": "s",
    "7": "t", "8": "b", "@": "a", "$": "s", "!": "i",
    "+": "t",
}

# Pattern for repeated characters (e.g., fuuuck, shiiit)
_REPEATED_CHAR_RE = re.compile(r'(.)\1{2,}')

# Pattern for spaced-out words (e.g., f u c k)
_SPACED_RE = re.compile(r'(?:^|\s)(\w(?:\s\w){2,})(?:\s|$)')

# Zero-width and invisible unicode chars
_INVISIBLE_RE = re.compile(r'[\u200b\u200c\u200d\u2060\ufeff\u00ad]')

# Asterisks/symbols used to mask letters (e.g., f*ck, sh!t)
_MASK_CHARS_RE = re.compile(r'[*_\-~.#]')


def _deleet(text: str) -> str:
    """Undo common leetspeak substitutions."""
    result = []
    for ch in text:
        result.append(_LEET_MAP.get(ch, ch))
    return "".join(result)


def _derepeat(text: str) -> str:
    """Collapse repeated characters: fuuuck -> fuck."""
    return _REPEATED_CHAR_RE.sub(r'\1', text)


def _unspace(text: str) -> str:
    """Detect and collapse spaced-out words: f u c k -> fuck."""
    def collapse(m):
        return m.group(1).replace(" ", "")
    return _SPACED_RE.sub(collapse, text)


def _strip_invisible(text: str) -> str:
    """Remove zero-width and invisible Unicode characters."""
    return _INVISIBLE_RE.sub('', text)


def _strip_masks(text: str) -> str:
    """Remove masking characters: f*ck -> fck."""
    return _MASK_CHARS_RE.sub('', text)


# Pre-build a combined set of ALL blocked single words for fast lookup
_ALL_BLOCKED_WORDS: Set[str] = set()
for _wordset in _CATEGORY_MAP.values():
    _ALL_BLOCKED_WORDS.update(_wordset)


class ContentFilter:
    """
    Determines whether text is safe for Cheese to learn and repeat.

    Does NOT prevent the player from typing anything — only gates
    the learning pathways so Cheese never absorbs inappropriate content.
    """

    def __init__(self):
        # Pre-compile phrase patterns for efficiency
        self._phrase_patterns: List[Tuple[re.Pattern, str]] = []
        for phrase in _BLOCKED_PHRASES:
            # Allow flexible whitespace between words in phrases
            pattern = r'\b' + r'\s+'.join(re.escape(w) for w in phrase.split()) + r'\b'
            self._phrase_patterns.append((re.compile(pattern, re.IGNORECASE), phrase))

    def is_safe_to_learn(self, text: str) -> bool:
        """
        Quick binary check: can Cheese safely learn this text?

        Returns True if the text passes all filters.
        """
        return not self.classify(text).is_blocked

    def classify(self, text: str) -> FilterResult:
        """
        Classify text against all filter categories.

        Returns a FilterResult with matched categories, severity,
        and the specific terms that triggered the filter.
        """
        if not text or not text.strip():
            return FilterResult(is_blocked=False)

        matched_categories: List[FilterCategory] = []
        matched_terms: List[str] = []
        max_severity = Severity.SOFT

        # Normalize text through multiple passes to catch evasion
        raw_lower = text.lower()
        cleaned = _strip_invisible(raw_lower)
        variants = {
            cleaned,
            _deleet(cleaned),
            _derepeat(cleaned),
            _strip_masks(cleaned),
            _unspace(cleaned),
            _derepeat(_deleet(cleaned)),
            _derepeat(_strip_masks(cleaned)),
            _deleet(_strip_masks(cleaned)),
        }

        # Check multi-word phrases first (exact phrase matching)
        for pattern, phrase in self._phrase_patterns:
            for variant in variants:
                if pattern.search(variant):
                    # Determine which category this phrase belongs to
                    phrase_lower = phrase.lower()
                    for cat, wordset in _CATEGORY_MAP.items():
                        if phrase_lower in wordset:
                            if cat not in matched_categories:
                                matched_categories.append(cat)
                            matched_terms.append(phrase)
                            if cat in _HARD_BLOCK_CATEGORIES:
                                max_severity = Severity.HARD
                            break
                    else:
                        # Phrase not in any specific wordset, still blocked
                        matched_terms.append(phrase)
                    break  # Don't check other variants for this phrase

        # Check single words via word boundary matching
        for variant in variants:
            words = set(re.findall(r'\b\w+\b', variant))
            for word in words:
                if word in _ALL_BLOCKED_WORDS:
                    # Find which category
                    for cat, wordset in _CATEGORY_MAP.items():
                        if word in wordset:
                            if cat not in matched_categories:
                                matched_categories.append(cat)
                            if word not in matched_terms:
                                matched_terms.append(word)
                            if cat in _HARD_BLOCK_CATEGORIES:
                                max_severity = Severity.HARD
                            break

        is_blocked = len(matched_categories) > 0

        return FilterResult(
            is_blocked=is_blocked,
            categories=matched_categories,
            severity=max_severity,
            matched_terms=matched_terms,
        )


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_filter_instance: ContentFilter = None


def get_content_filter() -> ContentFilter:
    """Get or create the global ContentFilter instance."""
    global _filter_instance
    if _filter_instance is None:
        _filter_instance = ContentFilter()
    return _filter_instance
