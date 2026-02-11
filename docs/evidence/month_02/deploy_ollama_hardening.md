# Deploy Ollama & System Hardening

## Objective
Establish a persistent, privacy-first AI inference server on the NVIDIA Jetson Orin Nano (8GB) to serve as the "Sovereign Brain" for Chitti.

## Implementation Details
- **Architecture**: Integrated Ollama as a background system service via `systemd`.
- **Hardening Logic**: Custom `chitti_watchdog.sh` script enforces high-performance power modes and flushes system caches before model instantiation.
- **Privacy Enforcement**: Environmental variables `OLLAMA_KEEP_ALIVE=0` and `GGML_CUDA_ENABLE_UNIFIED_MEMORY=1` applied to prevent post-inference data persistence in VRAM.

## Commands Used
```bash
sudo nvapmodel -m 0
sudo systemctl enable chitti-watchdog.service
sudo systemctl start chitti-watchdog.service