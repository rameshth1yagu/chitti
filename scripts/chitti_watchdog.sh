#!/bin/bash

# 1. Hardening with absolute paths
sudo /usr/bin/nvpmodel -m 0
sudo /usr/bin/sync && echo 3 | sudo /usr/bin/tee /proc/sys/vm/drop_caches

# 2. Cleanup - Kill any existing instances to prevent port conflicts
sudo /usr/bin/systemctl stop ollama 2>/dev/null
sudo /usr/bin/killall ollama 2>/dev/null

# 3. Privacy-First Environment
export GGML_CUDA_ENABLE_UNIFIED_MEMORY=1
export OLLAMA_KEEP_ALIVE=0

# 4. Launch (Stay in foreground so the service doesn't deactivate)
echo "🚀 Starting Chitti Brain (Ollama) in Privacy-First mode..."
/usr/local/bin/ollama serve