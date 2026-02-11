import cv2
import requests
import base64
import os
import time

# --- CONFIGURATION ---
MODEL = "moondream"
OLLAMA_URL = "http://localhost:11434/api/generate"
# Using /dev/shm (RAM-disk) to ensure the image never touches the SSD
TEMP_IMAGE_PATH = "/dev/shm/chitti_eyes.jpg" 

def capture_and_analyze():
    # 1. Initialize Camera
    cap = cv2.VideoCapture(0) # Change to CSI index if using Jetson Camera
    
    if not cap.isOpened():
        print("❌ Error: Could not access camera.")
        return

    try:
        # 2. Capture a single frame
        ret, frame = cap.read()
        if ret:
            # Save frame to RAM-disk
            cv2.imwrite(TEMP_IMAGE_PATH, frame)
            print(f"📸 Frame captured to {TEMP_IMAGE_PATH}")

            # 3. Encode image to Base64
            with open(TEMP_IMAGE_PATH, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

            # 4. Send to the Hardened AI Brain
            payload = {
                "model": MODEL,
                "prompt": "Describe what you see in this image in one short sentence.",
                "stream": False,
                "images": [img_base64]
            }

            print(f"📡 Sending to {MODEL}...")
            response = requests.post(OLLAMA_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"🤖 Chitti sees: {result['response']}")
            else:
                print(f"⚠️ AI Error: {response.status_code}")

    finally:
        # 5. THE PRIVACY GATE: Immediate Purge
        if os.path.exists(TEMP_IMAGE_PATH):
            os.remove(TEMP_IMAGE_PATH)
            print("🔒 Privacy Gate: Temporary image purged from RAM.")
        
        cap.release()

if __name__ == "__main__":
    capture_and_analyze()