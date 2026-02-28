#!/usr/bin/env python3
"""Debug Ollama inference issue."""

import sys
sys.path.insert(0, '/home/rameshthiyagu/chitti')

from pathlib import Path
from core.camera import CameraCapture
from core.inference import VLMClient

print("=" * 70)
print("DEBUG: Ollama Inference Test")
print("=" * 70)

# Step 1: Capture frame
print("\n1️⃣ Capturing frame to /dev/shm...")
camera = CameraCapture()
camera.open()
success, frame, frame_path = camera.capture_frame()
camera.release()

if not success:
    print("❌ Camera capture failed!")
    exit(1)

print(f"✅ Frame captured: {frame_path}")
print(f"   Size: {frame_path.stat().st_size / 1024:.2f} KB")

# Step 2: Test VLM inference
print("\n2️⃣ Testing VLM inference...")
vlm = VLMClient()

# Add detailed error catching
import requests
import base64
import time

try:
    # Encode image
    with open(frame_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode('utf-8')
    print(f"✅ Image encoded: {len(img_b64)} bytes base64")

    # Prepare payload
    payload = {
        "model": "moondream",
        "prompt": "Describe what you see in one short sentence.",
        "stream": False,
        "images": [img_b64]
    }

    # Make request
    print(f"\n📡 Calling Ollama API...")
    print(f"   URL: {vlm.url}")
    print(f"   Model: {vlm.model}")
    print(f"   Timeout: {vlm.timeout}s")

    t_start = time.time()
    response = requests.post(vlm.url, json=payload, timeout=vlm.timeout)
    t_end = time.time()

    print(f"\n📊 Response received in {t_end - t_start:.2f}s")
    print(f"   Status Code: {response.status_code}")
    print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
    print(f"   Content-Length: {len(response.content)} bytes")

    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"   Response: {result.get('response', 'N/A')}")
    else:
        print(f"\n❌ ERROR - Status {response.status_code}")
        print(f"   Response body (first 500 chars):")
        print(f"   {response.text[:500]}")

except Exception as e:
    print(f"\n❌ EXCEPTION: {type(e).__name__}")
    print(f"   Message: {str(e)}")
    import traceback
    traceback.print_exc()

finally:
    # Cleanup
    if frame_path.exists():
        frame_path.unlink()
        print(f"\n🧹 Frame purged from {frame_path}")

print("\n" + "=" * 70)
