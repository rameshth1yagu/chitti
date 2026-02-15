"""
Main inference pipeline for Project Chitti - Cognitive Edge Sentry.

EPIC 1 (Phase 1): Complete Zero-Retention Perception Pipeline
Orchestrates: Camera → /dev/shm → VLM → TTS → Privacy Purge → SSD Audit

EB-1A Relevance: End-to-end demonstration of privacy-first embodied AI.
Complete perception cycle with cryptographic proof of zero data persistence.
"""

import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime

from core.camera import CameraCapture
from core.inference import VLMClient
from core.privacy import PrivacyGate
from hri.tts import TTSEngine

logger = logging.getLogger(__name__)


class PerceptionPipeline:
    """
    Complete perception pipeline with zero-retention guarantees.

    Pipeline flow:
    1. Capture frame to /dev/shm
    2. VLM inference (Moondream)
    3. TTS output (ephemeral audio)
    4. Frame purge
    5. SSD audit verification
    """

    def __init__(self) -> None:
        """Initialize all pipeline components."""
        self.camera = CameraCapture()
        self.vlm = VLMClient()
        self.privacy = PrivacyGate()
        self.tts = TTSEngine()

        logger.info("pipeline_init_complete")

    def run_cycle(self) -> Optional[Dict[str, Any]]:
        """
        Execute one complete perception cycle.

        Returns:
            Dict with cycle metrics:
            - timestamp: ISO timestamp
            - capture_success: bool
            - inference_result: dict or None
            - tts_success: bool
            - audit_result: dict
            - total_latency_sec: float

        Returns None if cycle fails critically.
        """
        cycle_start = time.time()
        timestamp = datetime.now().isoformat()

        logger.info("cycle_start", extra={"timestamp": timestamp})

        # Initialize result
        result: Dict[str, Any] = {
            "timestamp": timestamp,
            "capture_success": False,
            "inference_result": None,
            "tts_success": False,
            "audit_result": {},
            "total_latency_sec": 0.0,
        }

        try:
            # STEP 1: Start SSD audit
            self.privacy.start_audit()

            # STEP 2: Capture frame
            success, frame, frame_path = self.camera.capture_frame()
            result["capture_success"] = success

            if not success or frame_path is None:
                logger.error("cycle_failed_capture")
                # Still purge and audit even on failure
                result["audit_result"] = self.privacy.enforce_cycle()
                return result

            # STEP 3: VLM Inference
            inference_result = self.vlm.infer(frame_path)
            result["inference_result"] = inference_result

            if inference_result is None:
                logger.error("cycle_failed_inference")
                # Purge and audit
                result["audit_result"] = self.privacy.enforce_cycle(frame_path)
                return result

            # STEP 4: TTS Output (ephemeral)
            description = inference_result.get("response", "")
            if description:
                tts_success = self.tts.speak(description)
                result["tts_success"] = tts_success
            else:
                logger.warning("cycle_no_description_to_speak")

            # STEP 5: Privacy Purge & Audit
            audit_result = self.privacy.enforce_cycle(frame_path)
            result["audit_result"] = audit_result

            # STEP 6: Compute metrics
            cycle_end = time.time()
            result["total_latency_sec"] = round(cycle_end - cycle_start, 3)

            logger.info(
                "cycle_complete",
                extra={
                    "total_latency_sec": result["total_latency_sec"],
                    "zero_retention": audit_result.get("zero_retention_verified", False),
                }
            )

            return result

        except Exception as e:
            logger.error(
                "cycle_exception",
                extra={"error": str(e), "type": type(e).__name__}
            )

            # Emergency purge attempt
            try:
                self.privacy.purge_frame()
            except:
                pass

            return None

    def run_single_cycle(self) -> Optional[Dict[str, Any]]:
        """
        Run a single perception cycle with proper resource management.

        Opens camera, runs one cycle, releases camera.
        Suitable for one-shot inference or testing.

        Returns:
            Cycle result dict or None
        """
        try:
            self.camera.open()
            result = self.run_cycle()
            return result
        finally:
            self.camera.release()

    def run_continuous(self, max_cycles: Optional[int] = None) -> None:
        """
        Run continuous perception loop.

        Args:
            max_cycles: Max number of cycles (None = infinite)

        This is the main robot operation mode.
        """
        logger.info(
            "continuous_mode_start",
            extra={"max_cycles": max_cycles}
        )

        try:
            self.camera.open()
            cycle_count = 0

            while True:
                result = self.run_cycle()

                if result is not None:
                    cycle_count += 1

                    if max_cycles is not None and cycle_count >= max_cycles:
                        logger.info(
                            "continuous_mode_complete",
                            extra={"cycles_completed": cycle_count}
                        )
                        break

                # Small sleep to prevent tight loop
                time.sleep(0.1)

        except KeyboardInterrupt:
            logger.info(
                "continuous_mode_interrupted",
                extra={"cycles_completed": cycle_count}
            )
        finally:
            self.camera.release()
            logger.info("continuous_mode_shutdown")


if __name__ == "__main__":
    # Demo: run a single perception cycle
    pipeline = PerceptionPipeline()
    result = pipeline.run_single_cycle()

    if result:
        print(f"\n{'='*60}")
        print(f"Chitti Perception Cycle Complete")
        print(f"{'='*60}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Total Latency: {result['total_latency_sec']}s")

        if result['inference_result']:
            print(f"\nChitti sees: {result['inference_result']['response']}")
            print(f"Inference Latency: {result['inference_result']['latency_sec']}s")

        audit = result['audit_result']
        print(f"\nSSD Audit:")
        print(f"  Initial: {audit['ssd_initial_gb']}GB")
        print(f"  Final: {audit['ssd_final_gb']}GB")
        print(f"  Delta: {audit['delta_gb']}GB")
        print(f"  Zero Retention: {'✅ VERIFIED' if audit['zero_retention_verified'] else '❌ VIOLATION'}")
        print(f"{'='*60}\n")
