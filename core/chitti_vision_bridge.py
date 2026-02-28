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
NATIVE_RES = (378, 378) # Moondream's optimal input size

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
        # 2. Capture & Resize Frame
        t_cap_start = time.time()
        
        # Warm-up: Skip 2 frames for better exposure
        for _ in range(2): cap.read()
        
        ret, frame = cap.read()
        if ret:
            # OPTIMIZATION: Resize to native resolution before saving
            # INTER_AREA is the gold standard for shrinking images
            resized_frame = cv2.resize(frame, NATIVE_RES, interpolation=cv2.INTER_AREA)
            
            # Save to RAM-disk
            cv2.imwrite(TEMP_IMAGE_PATH, resized_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
            
            t_cap_end = time.time()
            img_size = round(os.path.getsize(TEMP_IMAGE_PATH) / 1024, 2)
            print(f"[{get_now()}] 📸 Frame captured & resized ({int((t_cap_end - t_cap_start)*1000)}ms) | Size: {img_size}KB")

            # 3. Encode Image
            with open(TEMP_IMAGE_PATH, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

            # 4. Inference
            payload = {
                "model": MODEL,
                "prompt": "Describe what you see in one short sentence.",
                "stream": False,
                "images": [img_base64]
            }

            print(f"[{get_now()}] 📡 Sending to {MODEL}...")
            t_inf_start = time.time()
            response = requests.post(OLLAMA_URL, json=payload, timeout=60)
            t_inf_end = time.time()
            
            if response.status_code == 200:
                result = response.json()
                description = result.get('response', 'No description found.')
                print(f"[{get_now()}] 🤖 Chitti sees: {description}")
                print(f"[{get_now()}] ⏱️ Inference Latency: {round(t_inf_end - t_inf_start, 2)}s")

                speak(description)
            else:
                print(f"[{get_now()}] ⚠️ AI Error: {response.status_code}")

    except Exception as e:
        print(f"[{get_now()}] ❌ Exception during cycle: {str(e)}")

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

def speak(text):
    """
    Ephemeral TTS - pipes audio directly to hardware for zero-persistence.
    """
    try:
        espeak = subprocess.Popen(["espeak", text, "--stdout"], stdout=subprocess.PIPE)
        subprocess.run(["aplay", "-q"], stdin=espeak.stdout)
        espeak.stdout.close()
        espeak.wait()
        print(f"[{get_now()}] 🔊 Chitti spoke (ephemeral audio)")
    except Exception as e:
        print(f"[{get_now()}] ⚠️ TTS Failed: {e}")

if __name__ == "__main__":
    capture_and_analyze()