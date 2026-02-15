"""
Text-to-Speech module for Project Chitti - Cognitive Edge Sentry.

EPIC 2 (Phase 1): Human-Robot Interaction
Handles ephemeral voice synthesis with zero audio persistence.

EB-1A Relevance: Extends zero-retention architecture to audio modality.
TTS audio exists ONLY in kernel pipe buffers, never touches disk.
"""

import logging
import subprocess
from typing import Optional

logger = logging.getLogger(__name__)


class TTSEngine:
    """
    Ephemeral text-to-speech engine.

    Uses espeak with stdout piping to ensure audio never touches SSD.
    Audio exists ONLY in kernel buffers during playback.
    """

    def __init__(self) -> None:
        """Initialize TTS engine."""
        # Verify espeak is available
        try:
            result = subprocess.run(
                ["espeak", "--version"],
                capture_output=True,
                timeout=2
            )
            if result.returncode == 0:
                logger.info("tts_engine_init", extra={"engine": "espeak"})
            else:
                logger.warning("tts_engine_unavailable")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.error("tts_engine_not_found")

    def speak(self, text: str, blocking: bool = True) -> bool:
        """
        Speak text using ephemeral audio pipeline.

        Audio is piped from espeak stdout directly to aplay stdin.
        No intermediate file is created. Zero audio persistence.

        Args:
            text: Text to synthesize and speak
            blocking: If True, wait for speech to complete

        Returns:
            True if speech succeeded, False otherwise
        """
        if not text or not text.strip():
            logger.warning("speak_skipped_empty_text")
            return False

        try:
            # Create espeak process with stdout pipe
            espeak = subprocess.Popen(
                ["espeak", text, "--stdout"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Pipe audio directly to aplay (no disk write)
            aplay = subprocess.run(
                ["aplay", "-q"],  # -q for quiet mode
                stdin=espeak.stdout,
                stderr=subprocess.PIPE,
                timeout=30 if blocking else None
            )

            # Clean up pipe
            if espeak.stdout:
                espeak.stdout.close()

            espeak.wait()

            if espeak.returncode == 0 and aplay.returncode == 0:
                logger.info(
                    "tts_speak_success",
                    extra={
                        "text_length": len(text),
                        "blocking": blocking,
                    }
                )
                return True
            else:
                logger.error(
                    "tts_speak_failed",
                    extra={
                        "espeak_rc": espeak.returncode,
                        "aplay_rc": aplay.returncode,
                    }
                )
                return False

        except subprocess.TimeoutExpired:
            logger.error("tts_timeout")
            return False
        except FileNotFoundError as e:
            logger.error(
                "tts_command_not_found",
                extra={"error": str(e)}
            )
            return False
        except Exception as e:
            logger.error(
                "tts_unexpected_error",
                extra={"error": str(e)}
            )
            return False
