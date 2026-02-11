import requests
import time
import csv
import os

# Configuration
MODELS = ["moondream", "llava"]
TEST_PROMPT = "What is the main object in this room? Answer in one word."
LOG_FILE = "/home/rameshthiyagu/chitti/data/logs/inference_benchmarks.csv"

def run_test(model_name):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model_name,
        "prompt": TEST_PROMPT,
        "stream": False
    }
    
    print(f"📡 Testing {model_name}...")
    start_time = time.time()
    try:
        response = requests.post(url, json=payload, timeout=60)
        end_time = time.time()
        
        if response.status_code == 200:
            latency = round((end_time - start_time) * 1000, 2)
            return latency, "Success"
        else:
            return 0, f"Error {response.status_code}"
    except Exception as e:
        return 0, str(e)

def main():
    # Ensure log directory exists
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Model", "Latency_ms", "Status"])
        
        for model in MODELS:
            latency, status = run_test(model)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, model, latency, status])
            print(f"📊 {model}: {latency}ms | {status}")

if __name__ == "__main__":
    main()