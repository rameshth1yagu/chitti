#!/bin/bash
# 1. Hardening with absolute paths
sudo /usr/bin/nvpmodel -m 0
sudo /usr/bin/sync && echo 3 | sudo /usr/bin/tee /proc/sys/vm/drop_caches

# 2. Cleanup
sudo /usr/bin/systemctl stop ollama
sudo /usr/bin/killall ollama 2>/dev/null

# 3. Privacy-First Environment
export GGML_CUDA_ENABLE_UNIFIED_MEMORY=1
export OLLAMA_KEEP_ALIVE=0

# 4. Launch (Using absolute path for Ollama)
/usr/local/bin/ollama serve > /home/rameshthiyagu/chitti/data/logs/ollama.log 2>&1 &