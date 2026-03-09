#!/usr/bin/env python3
"""Direct test of Ollama API with base64 image."""

import requests
import base64
from pathlib import Path

# Check if there's a test image in /dev/shm
shm_path = Path("/dev/shm/chitti/frame.jpg")
if shm_path.exists():
    print(f"✅ Found existing frame: {shm_path}")
    with open(shm_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode('utf-8')
    print(f"📦 Base64 length: {len(img_b64)}")
else:
    print(f"❌ No frame at {shm_path}")
    exit(1)

# Try the API call
url = "http://127.0.0.1:11434/api/generate"
payload = {
    "model": "moondream",
    "prompt": "Describe what you see in one short sentence.",
    "stream": False,
    "images": [img_b64]
}

print(f"\n📡 Calling Ollama API...")
print(f"URL: {url}")
print(f"Model: {payload['model']}")

response = requests.post(url, json=payload, timeout=30)

print(f"\n📊 Response Status: {response.status_code}")
print(f"Response Headers: {dict(response.headers)}")

if response.status_code == 200:
    result = response.json()
    print(f"\n✅ SUCCESS!")
    print(f"Response: {result.get('response', 'N/A')}")
else:
    print(f"\n❌ ERROR!")
    print(f"Response body: {response.text[:500]}")
