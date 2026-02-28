"""
Configuration settings for Project Chitti - Cognitive Edge Sentry.

EPIC 1 (Phase 1): Perception & Privacy
All hardware pins, paths, URLs, and safety thresholds centralized here.

EB-1A Relevance: Demonstrates systematic engineering approach with
separation of configuration from logic, critical for reproducible research.
"""

from pathlib import Path
from typing import Final

# ============================================================================
# HARDWARE CONFIGURATION
# ============================================================================

# GPIO Pin Assignments (BOARD numbering mode)
ESTOP_RELAY_PIN: Final[int] = 26  # Physical pin 26 - controls NC relay
ESTOP_SENSE_PIN: Final[int] = 32  # Physical pin 32 - reads E-Stop button

# I²C Configuration
I2C_BUS: Final[int] = 1  # Jetson I²C bus 1
PCA9685_ADDRESS: Final[int] = 0x40  # Servo driver address
SERVO_CHANNELS: Final[int] = 16  # Number of PWM channels

# ============================================================================
# FILE SYSTEM PATHS
# ============================================================================

# CRITICAL: Visual data MUST use /dev/shm (volatile RAM) only
SHM_DIR: Final[Path] = Path("/dev/shm/chitti")
SHM_FRAME_PATH: Final[Path] = SHM_DIR / "frame.jpg"

# Project data directory
DATA_DIR: Final[Path] = Path.home() / "chitti" / "data"

# Logs and evidence (text-only data, no images/audio)
LOG_DIR: Final[Path] = DATA_DIR / "logs"
EVIDENCE_DIR: Final[Path] = Path.home() / "chitti" / "docs" / "evidence"
PHASE_01_EVIDENCE: Final[Path] = EVIDENCE_DIR / "phase_01"

# ============================================================================
# OLLAMA / VLM CONFIGURATION
# ============================================================================

OLLAMA_URL: Final[str] = "http://127.0.0.1:11434/api/generate"
OLLAMA_MODEL: Final[str] = "moondream"  # Moondream 1.6B (828MB)
OLLAMA_TIMEOUT: Final[int] = 30  # seconds
OLLAMA_PROMPT: Final[str] = "Describe what you see in one short sentence."

# ============================================================================
# CAMERA CONFIGURATION
# ============================================================================

CAMERA_DEVICE: Final[str] = "/dev/video0"  # CSI camera via V4L2
CAPTURE_WIDTH: Final[int] = 640  # Optimized for Orin L1/L2 cache
CAPTURE_HEIGHT: Final[int] = 480
JPEG_QUALITY: Final[int] = 85  # Balance between size and inference accuracy
TARGET_FPS: Final[int] = 20

# ============================================================================
# SAFETY THRESHOLDS
# ============================================================================

# Heartbeat Watchdog
HEARTBEAT_TIMEOUT: Final[float] = 2.0  # seconds - trigger E-Stop if exceeded

# Thermal Limits (°C)
CPU_TEMP_LIMIT: Final[float] = 85.0  # Thermal throttling threshold
GPU_TEMP_LIMIT: Final[float] = 90.0  # Critical shutdown threshold

# Power Supply (Volts)
VOLTAGE_MIN: Final[float] = 4.75  # Below this triggers warning
VOLTAGE_MAX: Final[float] = 5.25  # Above this triggers warning

# VRAM Watchdog
VRAM_CHECK_INTERVAL: Final[float] = 5.0  # seconds between VRAM checks
MAX_RECOVERY_ATTEMPTS: Final[int] = 5  # Before triggering E-Stop

# ============================================================================
# BENCHMARK & PROFILING
# ============================================================================

THERMAL_LOG_INTERVAL: Final[float] = 2.0  # seconds - jtop sampling rate
BENCHMARK_WARMUP_RUNS: Final[int] = 2  # Discard for cache warming
BENCHMARK_TEST_RUNS: Final[int] = 10  # For statistical analysis

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_LEVEL: Final[str] = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT_JSON: Final[bool] = True  # Use JSON for machine-parseable evidence
