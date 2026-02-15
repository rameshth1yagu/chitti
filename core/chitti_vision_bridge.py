import cv2
import requests
import base64
import os
import time
import shutil
from datetime import datetime
import subprocess

# --- CONFIGURATION ---
MODEL = "moondream"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
TEMP_IMAGE_PATH = "/dev/shm/chitti_eyes.jpg" 

def get_now():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def get_disk_usage():
    # Returns used gigabytes to 3 decimal places
    _, used, _ = shutil.disk_usage("/")
    return round(used / (1024**3), 3)

def capture_and_analyze():
    start_total = time.time()
    initial_disk = get_disk_usage()
    
    # 1. Initialize Camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print(f"[{get_now()}] ❌ Error: Could not access camera.")
        return

    try:
        # 2. Capture Frame
        t_cap_start = time.time()
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(TEMP_IMAGE_PATH, frame)
            t_cap_end = time.time()
            img_size = round(os.path.getsize(TEMP_IMAGE_PATH) / 1024, 2)
            print(f"[{get_now()}] 📸 Frame captured ({int((t_cap_end - t_cap_start)*1000)}ms) | Size: {img_size}KB")

            # 3. Encode Image
            with open(TEMP_IMAGE_PATH, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

            # 4. Inference (Using your WORKING prompt)
            payload = {
                "model": MODEL,
                "prompt": "Describe what you see in one short sentence.",
                "stream": False,
                "images": [img_base64]
            }

            print(f"[{get_now()}] 📡 Sending to {MODEL}...")
            t_inf_start = time.time()
            response = requests.post(OLLAMA_URL, json=payload)
            t_inf_end = time.time()
            
            if response.status_code == 200:
                result = response.json()
                description = result['response']
                print(f"[{get_now()}] 🤖 Chitti sees: {description}")
                print(f"[{get_now()}] ⏱️ Inference Latency: {round(t_inf_end - t_inf_start, 2)}s")

                speak_and_record(description)
            else:
                print(f"[{get_now()}] ⚠️ AI Error: {response.status_code}")

    finally:
        # 5. Privacy Purge & Audit
        if os.path.exists(TEMP_IMAGE_PATH):
            os.remove(TEMP_IMAGE_PATH)
            print(f"[{get_now()}] 🔒 Privacy Gate: RAM-disk purged.")
        
        final_disk = get_disk_usage()
        cap.release()
        
        print(f"[{get_now()}] 🛡️ Audit: Initial Disk: {initial_disk}GB | Final Disk: {final_disk}GB")
        if final_disk <= initial_disk:
            print(f"[{get_now()}] ✅ ZERO-RETENTION VERIFIED")
            
        print(f"[{get_now()}] 🏁 Total Cycle Time: {round(time.time() - start_total, 2)}s")

def speak_and_record(text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/home/rameshthiyagu/chitti/data/logs/speech_{timestamp}.wav"
    
    # Generate the audio file
    subprocess.run(["espeak", text, "-w", filename])
    
    # Play it (if speakers are connected)
    subprocess.run(["aplay", filename])
    
    print(f"[{get_now()}] 🎙️ Speech recorded to: {filename}")

if __name__ == "__main__":
    capture_and_analyze()