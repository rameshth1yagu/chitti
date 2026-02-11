# System Specification: Chitti Autonomous Watchdog Service

## 1. Overview
The `chitti-watchdog.service` is a systemd unit designed to manage the lifecycle of the onboard AI inference engine. It ensures that the Jetson Orin Nano is optimized for high-performance compute and that strict privacy protocols are enforced before the robot begins operation.

## 2. System Configuration (Unit File)
**File Location:** `/etc/systemd/system/chitti-watchdog.service`

```ini
[Unit]
Description=Chitti Privacy-First Watchdog & AI Server
After=network.target

[Service]
Type=simple
User=rameshthiyagu
WorkingDirectory=/home/rameshthiyagu/chitti
ExecStart=/home/rameshthiyagu/chitti/scripts/chitti_watchdog.sh
Restart=on-failure
StandardOutput=append:/home/rameshthiyagu/chitti/data/logs/watchdog.log
StandardError=append:/home/rameshthiyagu/chitti/data/logs/watchdog.log

[Install]
WantedBy=multi-user.target


Automation Logic (The Watchdog Script)
The underlying script (chitti_watchdog.sh) performs a sequence of "System Hardening" steps to ensure the 8GB Unified Memory is clean and the CPU is at maximum frequency.

Core Sequence:

Hardware Optimization: Invokes nvpmodel -m 0 to set the Jetson to Maximum Performance mode.

Deterministic Memory State: Executes a kernel-level cache flush (drop_caches) to free fragmented VRAM.

Environment Lockdown:

OLLAMA_KEEP_ALIVE=0: Ensures zero-persistence of model weights in memory post-inference.

GGML_CUDA_ENABLE_UNIFIED_MEMORY=1: Optimizes the shared RAM/VRAM buffer for the Orin architecture.

Service Orchestration: Kills zombie processes and initializes the Ollama REST API server.

Security & Permissions
To enable autonomous operation without human intervention (password entry), a "Least Privilege" Sudoers policy was implemented:

Plaintext
rameshthiyagu ALL=(ALL) NOPASSWD: /usr/bin/nvpmodel, /usr/bin/sync, /usr/bin/tee, /usr/bin/systemctl, /usr/bin/killall