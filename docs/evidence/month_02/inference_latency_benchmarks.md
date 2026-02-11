
# Test Inference Latency via API

## Objective
Benchmark the "Image-to-Semantic" latency to determine the feasibility of real-time robotic interventions.

## Experimental Setup
- **Hardware**: Jetson Orin Nano (Shared Memory Architecture).
- **Available VRAM**: 3.9 GiB (observed via CUDA runner logs).
- **Test Script**: `benchmark_suite.py` (Automated HTTP/REST calls to local Ollama API).

## Results & Findings


| Model | Status | Outcome |
| :--- | :--- | :--- |
| Moondream | Success | Validated for real-time use. |
| LLaVA | Failed | Triggered `SIGKILL` / `CUDA OOM` (Out of Memory). |

## Technical Insight for IEEE Paper
The LLaVA 7B model requires a ~2.5 GiB contiguous CUDA buffer. On an 8GB Jetson with an active GUI/ROS 2 stack, the fragmented unified memory cannot satisfy this allocation. This empirically justifies the project's transition to **Small Language Models (SLMs)** for safety-critical edge robotics.

## Problem Resolved
Fixed "Connection Refused" errors by implementing a 4GB NVMe-backed swap file to prevent the AI runner from being terminated by the Linux OOM Killer during model loading.