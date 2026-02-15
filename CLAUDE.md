# Claude Code — Project Chitti Phase 1 Prompt

## How to Use This File

There are three ways to use this with Claude Code:

### Option A: Feed the full prompt as a single command
```bash
cd ~/chitti
cat CLAUDE_PHASE1_PROMPT.md | claude
```

### Option B: Use as a CLAUDE.md project file (recommended)
```bash
# Copy the SYSTEM CONTEXT section below into your project's CLAUDE.md
cp CLAUDE_PHASE1_PROMPT.md ~/chitti/CLAUDE.md
cd ~/chitti
claude
```

### Option C: Paste sections interactively
```bash
cd ~/chitti
claude
# Then paste each task one at a time from the TASKS section below
```

---

## SYSTEM CONTEXT — Paste into CLAUDE.md at project root

```markdown
# CLAUDE.md — Project Chitti (Cognitive Edge Sentry)

## Project Identity
- **Name**: Project Chitti — Cognitive Edge Sentry
- **Repo**: ~/chitti (local) / github.com/rameshth1yagu/chitti (remote)
- **Purpose**: Privacy-first embodied AI robot that performs real-time vision-language inference entirely on-device with zero data persistence to disk.
- **Goal**: Simultaneously build a working robot AND compile technical evidence for an EB-1A extraordinary ability visa petition, IEEE Senior Membership, and a provisional patent.

## Hardware Stack
- **Dev Machine**: Mac Pro, Apple M4 Pro — used for compilation, model quantization, orchestration
- **Edge Brain**: NVIDIA Jetson Orin Nano SUPER Developer Kit (8GB unified LPDDR5, 1024 CUDA cores, Ampere arch)
- **OS**: JetPack 6.1 (Ubuntu 22.04 LTS), CUDA 12.6, cuDNN, TensorRT
- **Chassis**: Waveshare UGV Rover (differential drive), PCA9685 PWM servo driver over I²C
- **Camera**: CSI camera on /dev/video0 via V4L2
- **Power**: 5V/4A regulated rail to Jetson, separate servo power rail

## Core Innovation: Zero-Retention Inference
All visual data is processed exclusively in volatile RAM (/dev/shm tmpfs). The VLM (Moondream via Ollama) ingests frames from RAM, produces a text-only summary, and the frame is immediately purged. No pixel ever touches the SSD. An automated SSD delta audit mathematically proves zero persistence after every inference cycle.

## Current Architecture (as of Feb 2026)
```
~/chitti/
├── commands/        # CLI command scripts
├── core/            # Core inference and pipeline logic
├── scripts/         # Utility scripts (audit, watchdog, benchmarks)
├── docs/
│   └── evidence/
│       └── month_02/  # EB-1A evidence artifacts
└── README.md
```

## Tech Stack
- **Language**: Python 3.10+ (primary), Bash (scripts/automation)
- **AI Runtime**: Ollama (localhost:11434) serving Moondream VLM
- **Vision**: OpenCV (cv2) for frame capture and preprocessing
- **GPIO/Servos**: Jetson.GPIO, adafruit-circuitpython-pca9685, adafruit-servokit
- **Monitoring**: jetson-stats (jtop) for power/thermal telemetry
- **Comms**: espeak-ng (TTS), Flask/FastAPI (telemetry gateway)

## Code Standards
- All Python files must have module-level docstrings explaining purpose and EB-1A relevance
- Use type hints on all function signatures
- Every module must be importable independently (no circular imports)
- Camera frames MUST go to /dev/shm only — never write images to SSD paths
- All scripts must log to /var/log/chitti/ with ISO timestamps
- Use structured logging (JSON format preferred for machine-parseable evidence)
- Git commits must be descriptive — these are EB-1A timeline evidence

## Current Status
- EPIC 1 (Perception/Privacy): 90% complete — VLM running, /dev/shm pipeline working, SSD audit working, VRAM watchdog working. Model quantization in-progress.
- EPIC 2 (Voice/HRI): In-progress — espeak TTS started, telemetry gateway started.
- EPIC 3 (Kinematics): Not started.
- EPIC 4 (Professional Recognition): IEEE Senior Membership submitted.

## IMPORTANT CONSTRAINTS
- This runs on a Jetson Orin Nano with only 8GB unified RAM. Memory efficiency is critical.
- No cloud APIs, no internet required at runtime. 100% edge autonomous.
- nvidia-smi does NOT work on Jetson. Use jtop (jetson-stats) instead.
- NEVER write image/video data to SSD paths. Only /dev/shm is acceptable for visual data.
- PCA9685 is on I²C bus 1 at address 0x40.
```

---

## TASK 1 — Understand & Audit Existing Codebase

Paste this into Claude Code first, before any development work:

```
I need you to thoroughly understand the Project Chitti codebase before we make any changes. Please do the following in order:

1. **Map the entire repo structure**:
   - Run `find ~/chitti -type f -name "*.py" -o -name "*.sh" -o -name "*.md" | head -80` to see all source files
   - Read every Python and shell script file in the repo (there should be ~5-15 files based on the repo size)
   - Read the README.md

2. **For each file, document**:
   - File path and purpose
   - Key functions/classes and what they do
   - External dependencies (imports)
   - How it interacts with hardware (camera, GPIO, I²C, /dev/shm)
   - Any hardcoded paths, ports, or config values
   - Code quality issues (missing type hints, no error handling, no logging, etc.)

3. **Map the data flow**:
   - Trace the complete path of a camera frame from capture to VLM inference to purge
   - Identify where /dev/shm is used vs. where SSD paths might accidentally be used
   - Find how Ollama is called (REST API? Python SDK?)
   - Check if VRAM watchdog is running as a separate process or inline

4. **Identify architectural problems**:
   - Circular imports or tight coupling between modules
   - Missing error handling (especially around camera capture, Ollama API, GPIO)
   - Hardcoded values that should be in config
   - Missing logging
   - Any code that writes to SSD paths (CRITICAL BUG if found)
   - Scripts that aren't executable or have wrong shebangs

5. **Output a structured report** in this format:
   ```
   ## Codebase Audit Report

   ### File Inventory
   | File | Lines | Purpose | Quality (1-5) |
   ...

   ### Data Flow Diagram (text-based)
   Camera → [file] → /dev/shm → [file] → Ollama → [file] → purge

   ### Critical Issues (fix immediately)
   1. ...

   ### Refactoring Opportunities
   1. ...

   ### Missing Components Needed for Phase 1
   1. ...
   ```

Do NOT make any changes yet. Just read and report.
```

---

## TASK 2 — Refactor Existing Code into Clean Module Structure

Paste this after Task 1 is complete:

```
Based on your audit, refactor the existing codebase into a clean modular structure. Here is the target layout:

```
~/chitti/
├── config/
│   ├── __init__.py
│   └── settings.py            # All constants, paths, pin numbers, URLs in one place
├── core/
│   ├── __init__.py
│   ├── camera.py              # CSI camera capture to /dev/shm
│   ├── inference.py           # Ollama/Moondream VLM inference client
│   ├── privacy.py             # Frame purge + SSD delta audit
│   └── pipeline.py            # Orchestrates: capture → infer → purge cycle
├── safety/
│   ├── __init__.py
│   ├── estop.py               # E-Stop GPIO daemon (NEW — Phase 1)
│   └── watchdog.py            # VRAM watchdog (EXISTING — refactored)
├── hri/
│   ├── __init__.py
│   ├── tts.py                 # espeak text-to-speech (EXISTING or stub)
│   └── telemetry.py           # Local web server (EXISTING or stub)
├── scripts/
│   ├── benchmark_baseline.py  # NEW — Phase 1 baseline latency test
│   ├── thermal_logger.py      # NEW — Phase 1 jtop CSV logger
│   ├── sustained_load_test.py # NEW — Phase 1 30-min load test
│   ├── analyze_thermal.py     # NEW — Phase 1 thermal analysis + chart
│   └── ssd_audit.sh           # EXISTING — SSD delta verification
├── docs/
│   └── evidence/
│       └── phase_01/          # All Phase 1 evidence artifacts go here
├── tests/
│   ├── __init__.py
│   ├── test_camera.py         # Verify camera captures to /dev/shm
│   ├── test_inference.py      # Verify Ollama connectivity and response
│   ├── test_privacy.py        # Verify frame purge leaves zero residue
│   └── test_estop.py          # Verify GPIO E-Stop (requires hardware)
├── CLAUDE.md                  # This project context file
├── README.md                  # Updated with architecture diagram
├── requirements.txt           # All pip dependencies
└── setup.py                   # Package setup for clean imports
```

**Refactoring rules:**

1. **Move ALL configuration** (pin numbers, paths, URLs, thresholds, timeouts) into `config/settings.py` as typed constants:
   ```python
   # config/settings.py
   from pathlib import Path

   # Hardware
   ESTOP_RELAY_PIN: int = 26          # Physical pin 26 on Jetson
   ESTOP_SENSE_PIN: int = 32          # Physical pin 32
   I2C_BUS: int = 1
   PCA9685_ADDRESS: int = 0x40
   SERVO_CHANNELS: int = 16

   # Paths — CRITICAL: only /dev/shm for visual data
   SHM_DIR: Path = Path("/dev/shm/chitti")
   LOG_DIR: Path = Path("/var/log/chitti")
   EVIDENCE_DIR: Path = Path("docs/evidence")

   # Ollama
   OLLAMA_URL: str = "http://localhost:11434/api/generate"
   OLLAMA_MODEL: str = "moondream"
   OLLAMA_TIMEOUT: int = 30

   # Camera
   CAMERA_DEVICE: str = "/dev/video0"
   CAPTURE_WIDTH: int = 640
   CAPTURE_HEIGHT: int = 480
   JPEG_QUALITY: int = 85

   # Safety
   HEARTBEAT_TIMEOUT: float = 2.0
   CPU_TEMP_LIMIT: float = 85.0
   GPU_TEMP_LIMIT: float = 90.0
   VOLTAGE_MIN: float = 4.75
   VOLTAGE_MAX: float = 5.25

   # Watchdog
   VRAM_CHECK_INTERVAL: float = 5.0
   MAX_RECOVERY_ATTEMPTS: int = 5
   ```

2. **Preserve all existing functionality** — nothing should break. The refactor is structural only.

3. **Add module docstrings** to every file explaining its purpose and which EPIC/Phase it belongs to.

4. **Add type hints** to all function signatures.

5. **Add structured logging** using Python's logging module with JSON formatter:
   ```python
   import logging, json

   class JSONFormatter(logging.Formatter):
       def format(self, record):
           return json.dumps({
               "timestamp": self.formatTime(record),
               "level": record.levelname,
               "module": record.module,
               "message": record.getMessage(),
               "extra": getattr(record, "extra", {})
           })
   ```

6. **Add error handling** around all I/O operations (camera, Ollama API, GPIO, file ops).

7. **Create `requirements.txt`** listing all dependencies with pinned versions.

8. **Update README.md** with the new module structure and a text-based architecture diagram.

After refactoring, run these verification checks:
- `python -c "from core.camera import CameraCapture; print('camera OK')"` 
- `python -c "from core.inference import VLMClient; print('inference OK')"`
- `python -c "from core.privacy import PrivacyGate; print('privacy OK')"`
- `python -c "from config.settings import OLLAMA_URL; print(OLLAMA_URL)"`

Commit the refactor with: `git commit -m "refactor: modular structure for Phase 1 — config, core, safety, hri, tests"`
```

---

## TASK 3 — Implement Step 1: E-Stop & Safety Failsafe

```
Implement the hardware E-Stop and safety failsafe system. Create `safety/estop.py` with the following requirements:

**Class: EStopDaemon**

Requirements:
- Uses Jetson.GPIO in BOARD mode
- ESTOP_RELAY_PIN (from config) controls an NC relay on the motor power rail
  - GPIO HIGH = relay energized = motors enabled
  - GPIO LOW = relay de-energized = motors CUT (fail-safe)
- ESTOP_SENSE_PIN reads the physical E-Stop button state (active LOW with pull-up)
- Hardware interrupt on ESTOP_SENSE_PIN FALLING edge triggers immediate motor cut
- Heartbeat watchdog: if no heartbeat() call within HEARTBEAT_TIMEOUT seconds, auto-cut motors
- System health monitor checks:
  - CPU temp via /sys/devices/virtual/thermal/thermal_zone0/temp (cut if > CPU_TEMP_LIMIT)
  - GPU temp via /sys/devices/virtual/thermal/thermal_zone1/temp (cut if > GPU_TEMP_LIMIT)
- All events logged to /var/log/chitti/estop.log in JSON format
- Thread-safe: monitor_loop runs in a daemon thread
- Clean shutdown on SIGINT/SIGTERM (releases GPIO)

**Methods needed:**
- `__init__(self)` — setup GPIO, register interrupt, start monitor thread
- `arm(self) -> None` — energize relay, enable motors
- `disarm(self, reason: str = "manual") -> None` — de-energize relay, log reason
- `heartbeat(self) -> None` — reset watchdog timer
- `check_system_health(self) -> bool` — read thermals, return False if unsafe
- `monitor_loop(self) -> None` — runs in thread, checks heartbeat + health every 100ms
- `shutdown(self) -> None` — clean GPIO release
- `is_armed(self) -> bool` — current state

**Also create:**

1. `safety/watchdog.py` — Refactor the existing VRAM watchdog to:
   - Import EStopDaemon and call estop.disarm() on unrecoverable OOM
   - Add exponential backoff: 1s, 2s, 4s, 8s between recovery attempts
   - Max MAX_RECOVERY_ATTEMPTS then trigger E-Stop
   - Log all recovery events with VRAM state, duration, attempt number

2. `tests/test_estop.py` — Unit tests that work WITHOUT hardware (mock GPIO):
   - Test: arm() sets relay HIGH
   - Test: disarm() sets relay LOW and logs reason
   - Test: heartbeat timeout triggers disarm after HEARTBEAT_TIMEOUT
   - Test: thermal limit triggers disarm
   - Test: multiple rapid arm/disarm cycles don't raise exceptions
   - Test: SIGINT handler calls shutdown()

3. `scripts/estop_hardware_test.py` — Hardware integration test (runs ON Jetson only):
   - Test 1: arm → verify relay pin HIGH → disarm → verify relay pin LOW
   - Test 2: arm → wait for HEARTBEAT_TIMEOUT + 1s → verify auto-disarm
   - Test 3: 10 rapid arm/disarm cycles with timing measurements
   - Print results as a markdown table for docs/evidence/phase_01/estop_test_log.md

4. Update `core/pipeline.py` to integrate E-Stop:
   - Import EStopDaemon at pipeline startup
   - Call estop.arm() before entering main loop
   - Call estop.heartbeat() on every inference cycle
   - Wrap main loop in try/finally that calls estop.shutdown()

After implementation:
- Run `python -m pytest tests/test_estop.py -v` to verify unit tests pass
- Commit: `git commit -m "feat(safety): E-Stop daemon with heartbeat watchdog, thermal limits, GPIO interrupt — Phase 1 Step 1"`
```

---

## TASK 4 — Implement Step 2: Jetson Configuration & Baseline

```
Create the configuration scripts and baseline benchmarking for the Jetson setup. Build these files:

**1. `scripts/verify_jetson_setup.py`** — System verification script that checks:
- JetPack version (parse /etc/nv_tegra_release)
- CUDA version (parse nvcc --version output)
- cuDNN installed (check dpkg -l | grep cudnn)
- TensorRT installed (check dpkg -l | grep tensorrt)
- Power mode (parse nvpmodel -q output — WARN if not MAXN)
- Clocks pinned (parse jetson_clocks --show — WARN if not max)
- Camera accessible (/dev/video0 exists and readable)
- I²C bus scan (i2cdetect -y 1 — check for PCA9685 at 0x40)
- Ollama running (curl localhost:11434/api/tags — check moondream listed)
- OLLAMA_KEEP_ALIVE set (check environment or service override)
- /dev/shm writable and has sufficient space (need at least 100MB free)
- /var/log/chitti exists and writable

Output: structured report as both terminal output AND JSON saved to docs/evidence/phase_01/jetson_setup_verification.json

Each check should be PASS/WARN/FAIL with a specific message.
Print a summary: "X/12 checks passed, Y warnings, Z failures"

**2. `scripts/setup_maxn.sh`** — Idempotent setup script:
```bash
#!/bin/bash
# Configure Jetson Orin Nano SUPER for maximum AI performance
# Safe to run multiple times

set -euo pipefail

echo "=== Chitti: Jetson MAXN Configuration ==="

# Set MAXN power mode
sudo nvpmodel -m 0
echo "[OK] Power mode set to MAXN (25W)"

# Pin clocks at maximum
sudo jetson_clocks
echo "[OK] Clocks pinned at maximum frequency"

# Create persistent systemd service
# ... (create jetson-maxperf.service if not exists)

# Configure Ollama keep-alive
# ... (create override.conf if not exists)

# Create required directories
sudo mkdir -p /var/log/chitti
sudo chown $USER:$USER /var/log/chitti
mkdir -p /dev/shm/chitti

echo "=== Configuration complete. Run verify_jetson_setup.py to confirm. ==="
```

**3. `scripts/benchmark_baseline.py`** — Baseline inference benchmark:
- Capture a test frame from CSI camera to /dev/shm
- Warm up Moondream with 2 discarded inference runs
- Run 10 timed inference cycles using the SAME frame (controlled test)
- For each run, measure:
  - `capture_ms`: time to capture frame from camera
  - `encode_ms`: time to base64 encode the JPEG
  - `inference_ms`: time for Ollama API call (the big one)
  - `total_ms`: end-to-end from capture start to response received
- Compute: mean, median, stdev, min, max, p95 for each metric
- Save results to docs/evidence/phase_01/baseline_latency.json with:
  - All raw run data
  - Summary statistics
  - System config (model name, quantization, power mode, clocks)
  - Timestamp of benchmark run
- Print a clean summary table to terminal
- IMPORTANT: purge /dev/shm frame after each run (maintain zero-retention even in benchmarks)

**4. Update `README.md`** with:
- Updated module structure tree
- Quick-start setup instructions referencing setup_maxn.sh and verify_jetson_setup.py
- Baseline performance numbers placeholder (to be filled after first benchmark run)

After implementation:
- Run `python scripts/verify_jetson_setup.py` and save output
- Run `python scripts/benchmark_baseline.py` and save results
- Commit: `git commit -m "feat(setup): Jetson verification, MAXN config, baseline benchmark — Phase 1 Step 2"`
```

---

## TASK 5 — Implement Step 3: Thermal & Power Profiling

```
Create the thermal and power profiling tools for IEEE benchmarking evidence. Build these files:

**1. `scripts/thermal_logger.py`** — 30-minute telemetry recorder:
- Uses jtop Python API (from jetson-stats package)
- Records every 2 seconds for configurable duration (default: 30 min)
- CSV columns: timestamp, cpu_temp_c, gpu_temp_c, power_total_mw, power_gpu_mw, gpu_util_pct, cpu_util_pct, ram_used_mb, ram_total_mb, fan_speed_pct, nvpmodel_mode
- Flush after every write (crash-safe)
- Print progress every 60 seconds: "Minute X/30 — CPU: XXC, GPU: XXC, Power: XXW"
- Handle graceful Ctrl+C: save partial data and print summary
- Save to docs/evidence/phase_01/thermal_profile.csv
- Also save a metadata JSON with: start_time, end_time, total_samples, system_info

**2. `scripts/sustained_load_test.py`** — Continuous inference stress test:
- Runs inference in a tight loop for configurable duration (default: 30 min)
- Captures a FRESH frame each cycle (simulates real operation)
- Logs per-cycle: cycle_number, latency_sec, timestamp
- Saves cycle log to docs/evidence/phase_01/sustained_load_log.csv
- Integrates with E-Stop: imports EStopDaemon, calls heartbeat() every cycle
- CRITICAL: purge /dev/shm frame after every cycle (zero-retention even under stress)
- On completion, print summary: total cycles, mean/min/max latency, latency drift over time

**3. `scripts/analyze_thermal.py`** — Post-test analysis and chart generation:
- Reads thermal_profile.csv
- Generates a publication-quality matplotlib figure with 4 subplots:
  - Panel 1: CPU + GPU temperature over time, with 80°C throttle threshold line
  - Panel 2: Total power draw (W) over time, with 25W MAXN TDP line  
  - Panel 3: GPU utilization (%) over time
  - Panel 4: Inference latency over time (from sustained_load_log.csv) to show thermal-induced slowdown
- Style: clean white background, labeled axes, legend, title, 12pt fonts
- Save as docs/evidence/phase_01/thermal_profile_chart.png at 200dpi
- Also print a text summary:
  - Peak/avg/min temperatures
  - Peak/avg power draw
  - Number of thermal throttle events (detected as >5% GPU clock drop from max)
  - Latency drift: compare first-5-min avg vs last-5-min avg

**4. `docs/evidence/phase_01/power_rail_template.md`** — Template for manual multimeter readings:
- Pre-formatted markdown table with columns: Time, State, Voltage_V, Current_A, Notes
- Pre-filled rows for: idle, inference start, sustained inference, inference+servo, peak load, cooldown
- Instructions at the top explaining how to take measurements

**5. Create `scripts/run_phase1_profiling.sh`** — Orchestration script:
```bash
#!/bin/bash
# Run the full Phase 1 thermal profiling session
# Start thermal logger in background, run sustained load, then analyze

echo "Starting thermal logger (30 min)..."
python3 scripts/thermal_logger.py --duration 30 &
LOGGER_PID=$!
sleep 5  # Let logger stabilize

echo "Starting sustained inference load (30 min)..."
python3 scripts/sustained_load_test.py --duration 30

echo "Waiting for thermal logger to finish..."
wait $LOGGER_PID

echo "Running analysis..."
python3 scripts/analyze_thermal.py

echo "Phase 1 profiling complete. Check docs/evidence/phase_01/"
```

After implementation:
- Verify thermal_logger.py runs for 30 seconds in test mode: `python scripts/thermal_logger.py --duration 0.5`
- Verify analyze_thermal.py generates chart from sample data
- Commit: `git commit -m "feat(profiling): thermal logger, sustained load test, analysis charts — Phase 1 Step 3"`
```

---

## TASK 6 — Phase 1 Completion: Evidence Package & Exit Checklist

```
Finalize Phase 1 by creating the evidence package and verifying all exit criteria. Do the following:

**1. Create `scripts/phase1_exit_check.py`** — Automated exit checklist:
- Programmatically verify each Phase 1 exit criterion:
  - [ ] safety/estop.py exists and imports cleanly
  - [ ] tests/test_estop.py passes (run pytest)
  - [ ] config/settings.py has all required constants
  - [ ] verify_jetson_setup.py reports 0 failures
  - [ ] baseline_latency.json exists and contains 10+ runs
  - [ ] thermal_profile.csv exists and has 800+ rows (≈27 min of data)
  - [ ] thermal_profile_chart.png exists
  - [ ] All Python files have module docstrings
  - [ ] All Python files have type hints on public functions
  - [ ] No Python file imports from SSD paths for image data (grep for dangerous patterns)
  - [ ] /var/log/chitti/ directory exists
  - [ ] requirements.txt exists and is up to date
- Print: "Phase 1 Exit: X/12 criteria met. [READY / NOT READY] for Phase 2"

**2. Create `docs/evidence/phase_01/EVIDENCE_INDEX.md`**:
- Table mapping every artifact to its EB-1A criterion
- Include file paths, descriptions, and dates
- This becomes the master evidence tracker

**3. Update `.gitignore`** to exclude:
- __pycache__/
- *.pyc
- .pytest_cache/
- /dev/shm/* (should never be committed anyway)
- *.egg-info/

**4. Final commits:**
```bash
git add -A
git commit -m "feat: Phase 1 complete — E-Stop, Jetson MAXN, thermal profiling, baseline benchmarks. All exit criteria verified."
git tag -a v0.1.0-phase1 -m "Phase 1: Foundation & Safety complete"
git push origin main --tags
```

**5. Print a summary** of what was accomplished in Phase 1 and what the baseline numbers are, formatted as a ClickUp task update I can paste directly.
```

---

## TIPS FOR BEST RESULTS WITH CLAUDE CODE

1. **Run tasks sequentially** — don't skip Task 1 (audit). Claude Code needs to read your existing code first.

2. **If Claude Code asks clarifying questions**, it's because it found something unexpected in your codebase. Answer honestly — the audit may reveal issues.

3. **Test on Jetson, not Mac** — Tasks 3-5 have hardware-specific code. Run Claude Code via SSH on the Jetson:
   ```bash
   ssh jetson@<jetson-ip>
   cd ~/chitti
   claude
   ```

4. **For GPIO-dependent code** — Claude Code can write and lint the code on Mac, but hardware tests only run on Jetson. Use `@mock.patch` for unit tests.

5. **Commit frequently** — After each task completes successfully, commit. These git timestamps are EB-1A evidence.

6. **If something breaks** — Tell Claude Code exactly what error you see. Paste the full traceback. It's much better at fixing specific errors than vague "it doesn't work" reports.
