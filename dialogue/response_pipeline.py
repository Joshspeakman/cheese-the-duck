"""
Response Pipeline - Pluggable response source chain.

Each ResponseSource wraps an existing dialogue subsystem (LLM, keywords,
learning engine, voice generator, SeamanDialogue).  The ResponsePipeline
tries them in priority order and returns the first successful response.

This replaces the hard-coded ``if/elif`` chain in
``ConversationSystem.process_player_input`` with an extensible, testable
architecture while reusing ALL existing generation code.
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import logging
import re

from dialogue.dialogue_core import (
    DialogueContext,
    DialogueResponse,
    DialogueState,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# ResponseSource ABC
# ---------------------------------------------------------------------------

class ResponseSource(ABC):
    """
    Abstract base for a dialogue response source.

    Subclasses wrap existing generation code (LLM, keywords, etc.)
    and present a uniform interface to the pipeline.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable identifier for this source."""
        ...

    @abstractmethod
    def can_handle(
        self, context: DialogueContext, state: DialogueState
    ) -> bool:
        """
        Return True if this source *could* produce a response
        for the given context.  Lightweight check (no generation).
        """
        ...

    @abstractmethod
    def generate(
        self, context: DialogueContext, state: DialogueState
    ) -> Optional[DialogueResponse]:
        """
        Try to produce a response.  Return None on failure.
        """
        ...

    def is_enabled(self) -> bool:
        """
        Return True if this source is switched on.  Default: True.
        Subclasses may check config flags.
        """
        return True


# ---------------------------------------------------------------------------
# LLMResponseSource
# ---------------------------------------------------------------------------

class LLMResponseSource(ResponseSource):
    """
    Wraps ``dialogue.llm_chat.LLMChat`` for local-LLM responses.
    """

    _ACTION_TAG_RE = re.compile(r"\[ACTION:(\w+)\]")

    def __init__(self) -> None:
        # Lazy-import to avoid import-time model loading
        self._llm = None
        self._import_failed = False

    @property
    def name(self) -> str:
        return "llm"

    def is_enabled(self) -> bool:
        try:
            from config import LLM_ENABLED
            return LLM_ENABLED
        except ImportError:
            return True

    def _get_llm(self):
        """Lazy-load the LLMChat singleton."""
        if self._llm is None and not self._import_failed:
            try:
                from dialogue.llm_chat import get_llm_chat
                self._llm = get_llm_chat()
            except Exception as exc:
                logger.debug("LLM import failed: %s", exc)
                self._import_failed = True
        return self._llm

    def can_handle(
        self, context: DialogueContext, state: DialogueState
    ) -> bool:
        if not self.is_enabled():
            return False
        if context.player_message is None:
            return False
        llm = self._get_llm()
        if llm is None:
            return False
        return llm.is_available()

    def generate(
        self, context: DialogueContext, state: DialogueState
    ) -> Optional[DialogueResponse]:
        llm = self._get_llm()
        if llm is None:
            return None

        # We need a Duck object for the existing LLM API.
        # The pipeline caller is responsible for providing it via
        # state.player_model or a duck reference on state.
        duck = getattr(state, "_duck_ref", None)
        if duck is None:
            logger.debug("LLMResponseSource: no duck reference on state")
            return None

        try:
            # Build memory context string from state if available
            memory_context = getattr(state, "_memory_context", "")
            raw = llm.generate_response(
                duck, context.player_message, memory_context=memory_context
            )
        except Exception as exc:
            logger.debug("LLM generation failed: %s", exc)
            return None

        if not raw:
            return None

        # Parse action tags out of the response text
        actions = self._ACTION_TAG_RE.findall(raw)
        clean_text = self._ACTION_TAG_RE.sub("", raw).strip()

        return DialogueResponse(
            text=clean_text or raw,
            source="llm",
            confidence=0.85,
            actions=actions,
            should_record=True,
        )


# ---------------------------------------------------------------------------
# AmbientChatSource — pre-generated LLM responses from background enrichment
# ---------------------------------------------------------------------------

class AmbientChatSource(ResponseSource):
    """
    Serves pre-generated ``chat_response`` ambient lines that were
    created in the background by the LLM after previous conversations.
    """

    @property
    def name(self) -> str:
        return "ambient_chat"

    def is_enabled(self) -> bool:
        try:
            from config import LLM_ENABLED, LLM_AMBIENT_ENABLED
            return LLM_ENABLED and LLM_AMBIENT_ENABLED
        except ImportError:
            return True

    def can_handle(
        self, context: DialogueContext, state: DialogueState
    ) -> bool:
        if context.player_message is None:
            return False
        # Only serve ambient lines if the generator has stock
        duck = getattr(state, "_duck_ref", None)
        if duck is None:
            return False
        brain = getattr(duck, "_duck_brain", None)
        if brain is None:
            return False
        gen = getattr(brain, "_ambient_generator", None)
        if gen is None:
            return False
        return gen.count_unused("chat_response") > 0

    def generate(
        self, context: DialogueContext, state: DialogueState
    ) -> Optional[DialogueResponse]:
        duck = getattr(state, "_duck_ref", None)
        if duck is None:
            return None
        brain = getattr(duck, "_duck_brain", None)
        if brain is None:
            return None
        gen = getattr(brain, "_ambient_generator", None)
        if gen is None:
            return None

        line = gen.consume_chat_response(context.player_message or "")
        if not line:
            return None

        return DialogueResponse(
            text=line,
            source="ambient_chat",
            confidence=0.80,
            should_record=True,
        )


# ---------------------------------------------------------------------------
# KeywordResponseSource
# ---------------------------------------------------------------------------

class KeywordResponseSource(ResponseSource):
    """
    Wraps ``dialogue.keyword_responses.KeywordEngine``.
    """

    def __init__(self) -> None:
        self._engine = None

    @property
    def name(self) -> str:
        return "keyword"

    def _get_engine(self):
        if self._engine is None:
            try:
                from dialogue.keyword_responses import get_keyword_engine
                self._engine = get_keyword_engine()
            except Exception as exc:
                logger.debug("Keyword engine import failed: %s", exc)
        return self._engine

    def can_handle(
        self, context: DialogueContext, state: DialogueState
    ) -> bool:
        if context.player_message is None:
            return False
        return self._get_engine() is not None

    def generate(
        self, context: DialogueContext, state: DialogueState
    ) -> Optional[DialogueResponse]:
        engine = self._get_engine()
        if engine is None:
            return None

        # KeywordEngine.process() needs a Duck object for mood lookup
        duck = getattr(state, "_duck_ref", None)
        if duck is None:
            logger.debug("KeywordResponseSource: no duck reference on state")
            return None

        try:
            result = engine.process(context.player_message, duck)
        except Exception as exc:
            logger.debug("Keyword engine failed: %s", exc)
            return None

        if not result:
            return None

        return DialogueResponse(
            text=result,
            source="keyword",
            confidence=0.70,
            should_record=True,
        )


# ---------------------------------------------------------------------------
# LearningResponseSource
# ---------------------------------------------------------------------------

class LearningResponseSource(ResponseSource):
    """
    Wraps ``dialogue.learning_engine.LearningEngine``.
    """

    def __init__(self) -> None:
        self._engine = None
        self._import_failed = False

    @property
    def name(self) -> str:
        return "learning"

    def is_enabled(self) -> bool:
        try:
            from config import LEARNING_ENGINE_ENABLED
            return LEARNING_ENGINE_ENABLED
        except ImportError:
            return True

    def _get_engine(self):
        if self._engine is None and not self._import_failed:
            try:
                from dialogue.learning_engine import get_learning_engine
                self._engine = get_learning_engine()
            except Exception as exc:
                logger.debug("Learning engine import failed: %s", exc)
                self._import_failed = True
        return self._engine

    def can_handle(
        self, context: DialogueContext, state: DialogueState
    ) -> bool:
        if not self.is_enabled():
            return False
        if context.player_message is None:
            return False
        engine = self._get_engine()
        return engine is not None and engine.is_seeded

    def generate(
        self, context: DialogueContext, state: DialogueState
    ) -> Optional[DialogueResponse]:
        engine = self._get_engine()
        if engine is None:
            return None

        try:
            result = engine.get_response(
                context.player_message, confidence_threshold=0.55
            )
        except Exception as exc:
            logger.debug("Learning engine failed: %s", exc)
            return None

        if not result:
            return None

        text, score = result
        return DialogueResponse(
            text=text,
            source="learning",
            confidence=score,
            should_record=True,
        )


# ---------------------------------------------------------------------------
# SeamanResponseSource
# ---------------------------------------------------------------------------

class SeamanResponseSource(ResponseSource):
    """
    Wraps ``dialogue.seaman_style.SeamanDialogue`` for template-based
    deadpan responses.  Acts as a reliable fallback that always works.
    """

    def __init__(self) -> None:
        self._generator = None

    @property
    def name(self) -> str:
        return "seaman"

    def _get_generator(self):
        if self._generator is None:
            try:
                from dialogue.seaman_style import SeamanDialogue
                self._generator = SeamanDialogue()
            except Exception as exc:
                logger.debug("SeamanDialogue import failed: %s", exc)
        return self._generator

    def can_handle(
        self, context: DialogueContext, state: DialogueState
    ) -> bool:
        # Always available as a fallback
        return self._get_generator() is not None

    def generate(
        self, context: DialogueContext, state: DialogueState
    ) -> Optional[DialogueResponse]:
        gen = self._get_generator()
        if gen is None:
            return None

        try:
            # Sync trust / cold-shoulder to the generator so golden rules apply
            gen._duck_trust = context.duck_trust
            cold_shoulder = getattr(state, "_cold_shoulder_active", False)
            gen._cold_shoulder_active = cold_shoulder

            if context.player_message:
                # Try question-style response for player input
                line = gen.generate_question_response(
                    context.player_message,
                    state.player_model,
                    None,  # duck_memory
                )
            elif context.conversation_state == "idle":
                line = gen.generate_idle(
                    duck_mood=context.duck_mood,
                    weather=context.weather,
                    time_of_day=context.time_of_day,
                    player_model=state.player_model,
                )
            else:
                line = gen.get_random_thought()
        except Exception as exc:
            logger.debug("SeamanDialogue generation failed: %s", exc)
            return None

        if not line:
            return None

        return DialogueResponse(
            text=line.text,
            source="seaman",
            confidence=0.50,
            mood_hint=line.tone.value if hasattr(line, "tone") else None,
            should_record=True,
        )


# ---------------------------------------------------------------------------
# VoiceResponseSource
# ---------------------------------------------------------------------------

class VoiceResponseSource(ResponseSource):
    """
    Wraps ``dialogue.voice_generator.VoiceGenerator`` for Markov-chain
    novel lines.  Output is flagged ``should_record=False`` because
    Markov gibberish should not pollute persistent memory.
    """

    def __init__(self) -> None:
        self._generator = None
        self._import_failed = False

    @property
    def name(self) -> str:
        return "voice"

    def is_enabled(self) -> bool:
        try:
            from config import VOICE_GENERATOR_ENABLED
            return VOICE_GENERATOR_ENABLED
        except ImportError:
            return True

    def _get_generator(self):
        if self._generator is None and not self._import_failed:
            try:
                from dialogue.voice_generator import get_voice_generator
                self._generator = get_voice_generator()
            except Exception as exc:
                logger.debug("Voice generator import failed: %s", exc)
                self._import_failed = True
        return self._generator

    def can_handle(
        self, context: DialogueContext, state: DialogueState
    ) -> bool:
        if not self.is_enabled():
            return False
        gen = self._get_generator()
        return gen is not None and gen.is_trained

    def generate(
        self, context: DialogueContext, state: DialogueState
    ) -> Optional[DialogueResponse]:
        gen = self._get_generator()
        if gen is None:
            return None

        try:
            # If we have a player message, try to seed with a keyword
            hint = None
            if context.player_message:
                words = context.player_message.lower().split()
                # Pick a content word (>3 chars) as a seed hint
                hints = [w for w in words if len(w) > 3]
                if hints:
                    hint = hints[0]
            raw = gen.generate(hint=hint)
        except Exception as exc:
            logger.debug("Voice generator failed: %s", exc)
            return None

        if not raw:
            return None

        return DialogueResponse(
            text=raw,
            source="voice",
            confidence=0.30,
            should_record=False,  # Markov output should not pollute memory
        )


# ---------------------------------------------------------------------------
# ResponsePipeline
# ---------------------------------------------------------------------------

class ResponsePipeline:
    """
    Tries registered ResponseSources in priority order (lower number
    = tried first) and returns the first successful response.

    If every source fails, returns a minimal ``"..."`` fallback.
    """

    def __init__(self) -> None:
        # List of (priority, source) tuples, kept sorted
        self._sources: List[Tuple[int, ResponseSource]] = []

    def register_source(
        self, source: ResponseSource, priority: int
    ) -> None:
        """
        Register a response source at the given priority.
        Lower priority numbers are tried first.

        Args:
            source: A ResponseSource implementation.
            priority: Integer priority (10 = first, 50 = last).
        """
        self._sources.append((priority, source))
        self._sources.sort(key=lambda pair: pair[0])

    def remove_source(self, name: str) -> None:
        """
        Remove a source by name.

        Args:
            name: The ``name`` property of the source to remove.
        """
        self._sources = [
            (p, s) for p, s in self._sources if s.name != name
        ]

    def generate_response(
        self,
        context: DialogueContext,
        state: DialogueState,
    ) -> DialogueResponse:
        """
        Run through sources in priority order and return the first
        successful response.

        Args:
            context: The current DialogueContext.
            state: The current DialogueState.

        Returns:
            A DialogueResponse.  Guaranteed non-None; falls back to
            ``"..."`` if every source fails.
        """
        for _priority, source in self._sources:
            if not source.is_enabled():
                continue
            try:
                if not source.can_handle(context, state):
                    continue
            except Exception as exc:
                logger.debug(
                    "Source '%s' can_handle raised: %s", source.name, exc
                )
                continue

            try:
                response = source.generate(context, state)
            except Exception as exc:
                logger.debug(
                    "Source '%s' generate raised: %s", source.name, exc
                )
                continue

            if response is not None:
                return response

        # Ultimate fallback
        return DialogueResponse(
            text="...",
            source="fallback",
            confidence=0.0,
            should_record=False,
        )

    def get_sources(self) -> List[Tuple[int, str, bool]]:
        """
        Return a snapshot of registered sources for debugging.

        Returns:
            List of ``(priority, name, enabled)`` tuples.
        """
        return [
            (priority, source.name, source.is_enabled())
            for priority, source in self._sources
        ]


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def create_default_pipeline() -> ResponsePipeline:
    """
    Create the standard response pipeline with all available sources.

    Sources that fail to initialise are silently skipped so the game
    can always start, even without an LLM model.

    The LLM is NOT a direct response source — it enriches future
    responses via the ambient line system in the background.

    Default priority order:
        5  - AmbientChat  (pre-generated LLM responses from background)
        10 - Keywords  (hand-crafted topic-specific)
        20 - Learning engine  (fuzzy-match learned pairs)
        30 - Seaman  (template deadpan fallback)
        40 - Voice  (Markov chain novel lines)
    """
    pipeline = ResponsePipeline()

    try:
        pipeline.register_source(AmbientChatSource(), priority=5)
    except Exception:
        logger.debug("Source init failed: AmbientChatSource", exc_info=True)

    pipeline.register_source(KeywordResponseSource(), priority=10)

    try:
        pipeline.register_source(LearningResponseSource(), priority=20)
    except Exception:
        logger.debug("Source init failed: LearningResponseSource", exc_info=True)

    pipeline.register_source(SeamanResponseSource(), priority=30)

    try:
        pipeline.register_source(VoiceResponseSource(), priority=40)
    except Exception:
        logger.debug("Source init failed: VoiceResponseSource", exc_info=True)

    return pipeline
