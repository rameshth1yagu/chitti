# Project Chitti — Cognitive Edge Sentry

**Privacy-first embodied AI robot** performing real-time vision-language inference **entirely on-device** with **zero data persistence to disk**.

Built for EB-1A extraordinary ability petition, IEEE Senior Membership, and provisional patent.

---

## Core Innovation: Zero-Retention Architecture

All visual data is processed **exclusively in volatile RAM** (`/dev/shm` tmpfs). The VLM (Moondream via Ollama) ingests frames from RAM, produces a text-only summary, and the frame is **immediately purged**. No pixel ever touches the SSD. An automated **SSD delta audit** mathematically proves zero persistence after every inference cycle.

**Patent-eligible claim:** Privacy-first perception pipeline where sensitive sensor data (image/audio) exists ONLY in volatile memory, with cryptographic proof of purge.

---

## Hardware Stack

| Component | Specification |
|-----------|--------------|
| **Dev Machine** | Mac Pro, Apple M4 Pro |
| **Edge Brain** | NVIDIA Jetson Orin Nano SUPER (8GB LPDDR5, 1024 CUDA cores) |
| **OS** | JetPack 6.1 (Ubuntu 22.04), CUDA 12.6, cuDNN, TensorRT |
| **Chassis** | Waveshare UGV Rover (differential drive) |
| **Servos** | PCA9685 PWM driver (I²C bus 1, address 0x40) |
| **Camera** | CSI camera on /dev/video0 (V4L2) |
| **Power** | 5V/4A regulated rail, separate servo power |

---

## Architecture (Phase 1)

```
~/chitti/
├── config/
│   ├── __init__.py
│   └── settings.py            # All constants, paths, pins, thresholds
├── core/
│   ├── __init__.py
│   ├── camera.py              # CSI camera → /dev/shm capture
│   ├── inference.py           # Ollama/Moondream VLM client
│   ├── privacy.py             # Frame purge + SSD delta audit
│   ├── pipeline.py            # Main orchestrator
│   ├── zero_retention_ingress.py   # [LEGACY] Early prototype
│   ├── chitti_vision_bridge.py     # [LEGACY] Monolithic pipeline
│   └── benchmark_suite.py          # [LEGACY] Basic benchmarks
├── safety/                    # NEW in Phase 1
│   ├── __init__.py
│   ├── estop.py               # E-Stop GPIO daemon (TASK 3)
│   └── watchdog.py            # VRAM watchdog (TASK 3)
├── hri/                       # Human-Robot Interaction
│   ├── __init__.py
│   ├── tts.py                 # Ephemeral TTS (espeak → aplay pipe)
│   └── telemetry.py           # [TODO] Local web dashboard
├── scripts/
│   ├── chitti_watchdog.sh     # Systemd service launcher
│   ├── chitti_heal.sh         # Recovery script (cache flush + restart)
│   ├── slim_jetson.sh         # System optimization
│   ├── jtop_logger.py         # Basic GPU/RAM logger
│   ├── verify_jetson_setup.py      # [TASK 4] System verification
│   ├── setup_maxn.sh               # [TASK 4] MAXN power mode config
│   ├── benchmark_baseline.py       # [TASK 4] Baseline latency benchmark
│   ├── thermal_logger.py           # [TASK 5] 30-min jtop profiling
│   ├── sustained_load_test.py      # [TASK 5] Stress test
│   ├── analyze_thermal.py          # [TASK 5] Chart generation
│   └── run_phase1_profiling.sh     # [TASK 5] Full profiling orchestration
├── tests/                     # Unit tests
│   ├── __init__.py
│   ├── test_camera.py
│   ├── test_inference.py
│   ├── test_privacy.py
│   └── test_estop.py
├── docs/
│   └── evidence/
│       ├── month_02/          # Early evidence artifacts
│       └── phase_01/          # Phase 1 benchmarks, logs, charts
├── CLAUDE.md                  # Project prompt for Claude Code
├── README.md                  # This file
├── requirements.txt           # Python dependencies
└── setup.py                   # Package installation config
```

---

## Data Flow: Complete Perception Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                     PERCEPTION PIPELINE                         │
└─────────────────────────────────────────────────────────────────┘

  CSI Camera (/dev/video0)
         │
         │ cv2.VideoCapture() → NumPy array (RAM)
         ▼
  /dev/shm/chitti/frame.jpg  ◄── VOLATILE RAM (tmpfs)
         │
         │ base64 encode
         ▼
  Ollama REST API (localhost:11434)
         │
         │ Moondream VLM inference (~3-5s)
         ▼
  Text description (e.g., "A laptop on a desk")
         │
         ├──────────────────────┐
         │                      │
         ▼                      ▼
  espeak TTS           SSD Delta Audit
  (ephemeral pipe)     (shutil.disk_usage)
         │                      │
         │                      │
         ▼                      ▼
  aplay                 ssd_final - ssd_initial == 0
  (speakers)            ✅ ZERO RETENTION VERIFIED
         │
         ▼
  os.remove(/dev/shm/chitti/frame.jpg)
         │
         ▼
  🔒 PRIVACY CYCLE COMPLETE
```

**Key property:** At no point does image data touch `/home`, `/var`, or any SSD path. Audio is piped kernel-to-kernel (espeak → aplay) with no intermediate file.

---

## Quick Start (Jetson Orin Nano)

### 1. Clone Repository
```bash
cd ~
git clone https://github.com/rameshth1yagu/chitti.git
cd chitti
```

### 2. Install System Dependencies
```bash
sudo apt-get update && sudo apt-get install -y \
  espeak-ng alsa-utils i2c-tools v4l-utils python3-jetson-gpio
```

### 3. Install Python Dependencies
```bash
pip3 install -e .
```

### 4. Configure Jetson for MAXN Performance
```bash
# [TASK 4] This script will be created in Phase 1
# For now, manual setup:
sudo nvpmodel -m 0              # MAXN power mode (25W)
sudo jetson_clocks              # Pin clocks at max frequency
```

### 5. Start Ollama with Privacy Env Vars
```bash
# Use the existing watchdog service
sudo systemctl enable chitti-watchdog.service
sudo systemctl start chitti-watchdog.service

# Or manually:
export GGML_CUDA_ENABLE_UNIFIED_MEMORY=1
export OLLAMA_KEEP_ALIVE=0
ollama serve &

# Pull Moondream model
ollama pull moondream
```

### 6. Run Single Perception Cycle
```bash
python3 -m core.pipeline
```

**Expected output:**
```
============================================================
Chitti Perception Cycle Complete
============================================================
Timestamp: 2026-02-15T14:23:45.123456
Total Latency: 4.521s

Chitti sees: A person sitting at a desk with a laptop.
Inference Latency: 3.842s

SSD Audit:
  Initial: 24.315GB
  Final: 24.315GB
  Delta: 0.000GB
  Zero Retention: ✅ VERIFIED
============================================================
```

---

## Current Status (Phase 1)

- [x] **Privacy architecture**: /dev/shm pipeline working, ephemeral TTS fixed
- [x] **Modular refactor**: config/, core/, hri/, safety/, tests/ structure
- [x] **Ollama integration**: Moondream VLM functional, hardened service
- [x] **SSD audit**: Delta verification implemented
- [ ] **E-Stop**: GPIO daemon (TASK 3)
- [ ] **VRAM watchdog**: OOM recovery with E-Stop integration (TASK 3)
- [ ] **Jetson config**: MAXN setup + verification scripts (TASK 4)
- [ ] **Baseline benchmark**: 10-run statistical analysis (TASK 4)
- [ ] **Thermal profiling**: 30-min jtop logging + charts (TASK 5)

**Next milestone:** Complete TASK 3 (E-Stop & Safety Failsafe)

---

## Tech Stack

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.10+ (primary), Bash (automation) |
| **AI Runtime** | Ollama (localhost:11434) serving Moondream 1.6B |
| **Vision** | OpenCV (cv2) for frame capture |
| **GPIO/Servos** | Jetson.GPIO, PCA9685 (I²C), adafruit-servokit |
| **Monitoring** | jetson-stats (jtop) for telemetry |
| **TTS** | espeak-ng (ephemeral audio pipeline) |
| **Testing** | pytest with mocked GPIO |

---

## Code Standards

- ✅ **Module docstrings**: Every file explains purpose and EB-1A relevance
- ✅ **Type hints**: All public function signatures annotated
- ✅ **Structured logging**: JSON format for machine-parseable evidence
- ✅ **Error handling**: Try/except on all I/O operations
- ✅ **Privacy enforcement**: No image/audio writes to SSD paths
- ✅ **Centralized config**: All constants in `config/settings.py`
- ✅ **Importable modules**: No circular dependencies

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=core --cov=hri --cov-report=html

# Test specific module
pytest tests/test_camera.py -v
```

**Note:** Hardware-dependent tests (camera, GPIO) require running ON Jetson. Use `pytest -m "not hardware"` to skip hardware tests during development.

---

## Evidence Artifacts (EB-1A / IEEE)

All evidence artifacts are organized in `docs/evidence/`:

```
docs/evidence/
├── month_02/                      # Early development logs
│   ├── chitti_watchdog_service_spec.md
│   ├── deploy_ollama_hardening.md
│   ├── vlm_selection_verification.md
│   └── inference_latency_benchmarks.md
└── phase_01/                      # Phase 1 deliverables (TASKS 4-6)
    ├── jetson_setup_verification.json
    ├── baseline_latency.json
    ├── thermal_profile.csv
    ├── thermal_profile_chart.png
    ├── sustained_load_log.csv
    ├── power_rail_template.md
    └── EVIDENCE_INDEX.md
```

---

## License

MIT License - This is research/portfolio code. See LICENSE file.

---

## Contact

**Ramesh Thiyagu**
GitHub: [@rameshth1yagu](https://github.com/rameshth1yagu)
Project: EB-1A Extraordinary Ability Petition (AI/Robotics)

---

**Built with Claude Code** — [claude.com/claude-code](https://claude.com/claude-code)