"""Core perception modules for Project Chitti."""

from core.camera import CameraCapture
from core.inference import VLMClient
from core.privacy import PrivacyGate

# PerceptionPipeline is NOT imported eagerly because it pulls in
# hri.tts.TTSEngine which spawns an espeak subprocess at import time.
# Import directly: from core.pipeline import PerceptionPipeline

__all__ = [
    "CameraCapture",
    "VLMClient",
    "PrivacyGate",
]
