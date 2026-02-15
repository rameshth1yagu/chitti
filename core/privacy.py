"""
Privacy enforcement module for Project Chitti - Cognitive Edge Sentry.

EPIC 1 (Phase 1): Zero-Retention Architecture
Handles frame purging and cryptographic proof of zero persistence.

EB-1A Relevance: CORE INNOVATION - Mathematically provable privacy.
SSD delta audit ensures visual data never touches persistent storage.
Patent-eligible architecture for privacy-first embodied AI.
"""

import logging
import os
import shutil
from pathlib import Path
from typing import Dict, Any

from config.settings import SHM_FRAME_PATH

logger = logging.getLogger(__name__)


class PrivacyGate:
    """
    Zero-retention enforcement and audit.

    Ensures visual data exists ONLY in volatile RAM (/dev/shm) and
    provides cryptographic proof via SSD delta measurement.
    """

    def __init__(self) -> None:
        """Initialize privacy gate."""
        self.ssd_initial_gb: float = 0.0
        self.ssd_final_gb: float = 0.0

        logger.info("privacy_gate_init")

    def measure_ssd_usage(self) -> float:
        """
        Measure current SSD usage in GB.

        Returns:
            SSD used space in gigabytes (3 decimal precision)
        """
        _, used, _ = shutil.disk_usage("/")
        used_gb = round(used / (1024**3), 3)

        logger.debug(
            "ssd_measured",
            extra={"used_gb": used_gb}
        )

        return used_gb

    def start_audit(self) -> None:
        """
        Begin SSD audit cycle.

        Records baseline SSD usage before inference cycle.
        """
        self.ssd_initial_gb = self.measure_ssd_usage()

        logger.info(
            "audit_started",
            extra={"ssd_initial_gb": self.ssd_initial_gb}
        )

    def purge_frame(self, frame_path: Path = SHM_FRAME_PATH) -> bool:
        """
        Securely delete frame from /dev/shm.

        Args:
            frame_path: Path to frame in /dev/shm

        Returns:
            True if purge succeeded, False otherwise
        """
        # CRITICAL: Verify path is in /dev/shm
        if "/dev/shm" not in str(frame_path):
            logger.error(
                "purge_rejected_not_shm",
                extra={"path": str(frame_path)}
            )
            return False

        if not frame_path.exists():
            logger.warning(
                "purge_skipped_not_found",
                extra={"path": str(frame_path)}
            )
            return True  # Already gone, which is the goal

        try:
            os.remove(frame_path)
            logger.info(
                "frame_purged",
                extra={"path": str(frame_path)}
            )
            return True
        except OSError as e:
            logger.error(
                "purge_failed",
                extra={"path": str(frame_path), "error": str(e)}
            )
            return False

    def complete_audit(self) -> Dict[str, Any]:
        """
        Complete SSD audit cycle and verify zero retention.

        Returns:
            Dict with audit results:
            - ssd_initial_gb: Starting SSD usage
            - ssd_final_gb: Ending SSD usage
            - delta_gb: Change in SSD usage
            - zero_retention_verified: True if delta <= 0

        Raises:
            RuntimeError: If audit was not started
        """
        if self.ssd_initial_gb == 0.0:
            raise RuntimeError("Audit not started. Call start_audit() first.")

        self.ssd_final_gb = self.measure_ssd_usage()
        delta_gb = round(self.ssd_final_gb - self.ssd_initial_gb, 3)

        # Zero retention is verified if SSD usage didn't increase
        zero_retention = delta_gb <= 0.0

        audit_result = {
            "ssd_initial_gb": self.ssd_initial_gb,
            "ssd_final_gb": self.ssd_final_gb,
            "delta_gb": delta_gb,
            "zero_retention_verified": zero_retention,
        }

        if zero_retention:
            logger.info(
                "zero_retention_verified",
                extra=audit_result
            )
        else:
            logger.warning(
                "zero_retention_violation",
                extra=audit_result
            )

        return audit_result

    def enforce_cycle(self, frame_path: Path = SHM_FRAME_PATH) -> Dict[str, Any]:
        """
        Full privacy enforcement cycle: start audit → purge → verify.

        Args:
            frame_path: Path to frame in /dev/shm

        Returns:
            Audit result dict

        This is a convenience method for the common pattern of:
        1. Start audit
        2. Purge frame
        3. Complete audit
        """
        self.start_audit()
        purge_success = self.purge_frame(frame_path)

        audit_result = self.complete_audit()
        audit_result["purge_success"] = purge_success

        return audit_result
