"""
GPU and thermal telemetry logger using jtop (jetson-stats).

Phase 1: Records hardware stats to CSV for benchmarking evidence.
"""

import argparse
import csv
import time
from pathlib import Path

from jtop import jtop

from config.settings import LOG_DIR


def main(output_path: Path) -> None:
    """Log jtop stats to CSV until interrupted."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Logging GPU and RAM to {output_path}...")
    print("Press CTRL+C to stop.")

    try:
        with jtop() as jetson:
            with open(output_path, "w", newline="") as csvfile:
                stats = jetson.stats
                writer = csv.DictWriter(csvfile, fieldnames=stats.keys())
                writer.writeheader()

                while jetson.ok():
                    writer.writerow(jetson.stats)
                    time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\nLog saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log Jetson GPU/thermal stats")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=LOG_DIR / "gpu_spike_evidence.csv",
        help="Output CSV path",
    )
    args = parser.parse_args()
    main(args.output)
