#!/usr/bin/env python3
"""
Quick test of refactored pipeline.
Tests: Camera → /dev/shm → Moondream → TTS → Privacy Purge
"""

import sys
import logging

# Setup basic logging to see what's happening
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)

# Import refactored modules
from core.pipeline import PerceptionPipeline

def main():
    print("=" * 70)
    print("Testing Refactored Chitti Perception Pipeline")
    print("=" * 70)

    # Create pipeline
    pipeline = PerceptionPipeline()

    # Run single cycle
    print("\n🚀 Running single perception cycle...\n")
    result = pipeline.run_single_cycle()

    # Display results
    if result is None:
        print("\n❌ Pipeline failed!")
        return 1

    print("\n" + "=" * 70)
    print("✅ Chitti Perception Cycle Complete")
    print("=" * 70)
    print(f"Timestamp: {result['timestamp']}")
    print(f"Total Latency: {result['total_latency_sec']}s")

    if result['capture_success']:
        print("✅ Camera capture: SUCCESS")
    else:
        print("❌ Camera capture: FAILED")

    if result['inference_result']:
        inf = result['inference_result']
        print(f"\n🤖 Chitti sees: {inf['response']}")
        print(f"⏱️  Inference Latency: {inf['latency_sec']}s")
    else:
        print("\n❌ Inference: FAILED")

    if result['tts_success']:
        print("🔊 TTS: SUCCESS (ephemeral audio)")
    else:
        print("🔇 TTS: SKIPPED or FAILED")

    audit = result['audit_result']
    print(f"\n🛡️  SSD Audit:")
    print(f"   Initial: {audit['ssd_initial_gb']}GB")
    print(f"   Final: {audit['ssd_final_gb']}GB")
    print(f"   Delta: {audit['delta_gb']}GB")

    if audit['zero_retention_verified']:
        print("   Status: ✅ ZERO RETENTION VERIFIED")
    else:
        print("   Status: ⚠️  WARNING - SSD usage increased!")

    print("=" * 70 + "\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
