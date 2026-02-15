from jtop import jtop
import csv
import time

# File to store the logs
output_file = "gpu_spike_evidence.csv"

print(f"🚀 Logging GPU and RAM to {output_file}...")
print("Press CTRL+C to stop logging after your vision test.")

try:
    with jtop() as jetson:
        with open(output_file, 'w', newline='') as csvfile:
            # Get initial stats to set up headers
            stats = jetson.stats
            writer = csv.DictWriter(csvfile, fieldnames=stats.keys())
            writer.writeheader()

            while jetson.ok():
                # Write current hardware stats to CSV
                writer.writerow(jetson.stats)
                # Fast polling to catch the quick GPU spike
                time.sleep(0.5) 
except KeyboardInterrupt:
    print(f"\n✅ Log saved. You can now attach {output_file} to Task.")