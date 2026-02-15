"""
Camera capture module for Project Chitti - Cognitive Edge Sentry.

EPIC 1 (Phase 1): Privacy-First Perception
Handles CSI camera frame capture with MANDATORY /dev/shm buffering.

EB-1A Relevance: Core component of zero-retention architecture.
Visual data NEVER touches persistent storage.
"""

import cv2
import logging
from pathlib import Path
from typing import Optional, Tuple
import numpy as np

from config.settings import (
    CAMERA_DEVICE,
    CAPTURE_WIDTH,
    CAPTURE_HEIGHT,
    SHM_DIR,
    SHM_FRAME_PATH,
    JPEG_QUALITY,
)

logger = logging.getLogger(__name__)


class CameraCapture:
    """
    CSI camera interface with privacy-first buffering.

    All frames are written exclusively to /dev/shm (tmpfs in RAM).
    No pixel data ever touches SSD.
    """

    def __init__(self, device: str = CAMERA_DEVICE) -> None:
        """
        Initialize camera capture.

        Args:
            device: V4L2 device path (default: /dev/video0)

        Raises:
            RuntimeError: If camera cannot be opened
        """
        self.device = device
        self.cap: Optional[cv2.VideoCapture] = None

        # Ensure /dev/shm directory exists
        SHM_DIR.mkdir(parents=True, exist_ok=True)

        logger.info(
            "camera_init",
            extra={
                "device": device,
                "resolution": f"{CAPTURE_WIDTH}x{CAPTURE_HEIGHT}",
                "shm_path": str(SHM_DIR),
            }
        )

    def open(self) -> None:
        """
        Open the camera device.

        Raises:
            RuntimeError: If camera fails to open
        """
        self.cap = cv2.VideoCapture(self.device)

        if not self.cap.isOpened():
            logger.error("camera_open_failed", extra={"device": self.device})
            raise RuntimeError(f"Failed to open camera: {self.device}")

        # Set resolution
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_HEIGHT)

        logger.info("camera_opened", extra={"device": self.device})

    def capture_frame(self) -> Tuple[bool, Optional[np.ndarray], Optional[Path]]:
        """
        Capture a single frame and save to /dev/shm.

        Returns:
            Tuple of (success, frame_array, frame_path)
            - success: True if capture succeeded
            - frame_array: NumPy array of frame (in RAM only)
            - frame_path: Path to /dev/shm JPEG file

        Raises:
            RuntimeError: If camera is not opened
        """
        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError("Camera not opened. Call open() first.")

        ret, frame = self.cap.read()

        if not ret or frame is None:
            logger.warning("frame_capture_failed")
            return False, None, None

        # Write to /dev/shm ONLY (volatile RAM)
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY]
        success = cv2.imwrite(str(SHM_FRAME_PATH), frame, encode_params)

        if not success:
            logger.error("shm_write_failed", extra={"path": str(SHM_FRAME_PATH)})
            return False, None, None

        frame_size_kb = SHM_FRAME_PATH.stat().st_size / 1024

        logger.info(
            "frame_captured",
            extra={
                "path": str(SHM_FRAME_PATH),
                "size_kb": round(frame_size_kb, 2),
                "shape": frame.shape,
            }
        )

        return True, frame, SHM_FRAME_PATH

    def release(self) -> None:
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            logger.info("camera_released")

    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release()
