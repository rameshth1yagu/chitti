#!/bin/bash
export PATH=$PATH:/usr/local/bin:/usr/bin:/bin
# Force Ollama to use YOUR model directory
export OLLAMA_MODELS=/home/rameshthiyagu/.ollama/models
# Privacy: disable keep-alive to free VRAM immediately after inference
export OLLAMA_KEEP_ALIVE=0
# Memory: enable unified memory for large models on Jetson
export GGML_CUDA_ENABLE_UNIFIED_MEMORY=1

LOG_DIR="$HOME/chitti/data/logs"
mkdir -p "$LOG_DIR"

while true; do
  if ! curl -s http://127.0.0.1:11434/api/tags | grep -q "moondream"; then
    echo "$(date): Moondream not found. Restarting server..."
    # Kill any ghost instances first
    pkill -9 ollama
    /usr/local/bin/ollama serve > "$LOG_DIR/ollama.log" 2>&1 &
    sleep 20
  fi
  echo 1 | tee /proc/sys/vm/compact_memory > /dev/null
  sleep 300
done
