#!/bin/bash
export PATH=$PATH:/usr/local/bin:/usr/bin:/bin
# Force Ollama to use YOUR model directory
export OLLAMA_MODELS=/home/rameshthiyagu/.ollama/models

while true; do
  if ! curl -s http://127.0.0.1:11434/api/tags | grep -q "moondream"; then
    echo "$(date): Moondream not found. Restarting server..."
    # Kill any ghost instances first
    pkill -9 ollama
    /usr/local/bin/ollama serve > /home/rameshthiyagu/chitti/ollama.log 2>&1 &
    sleep 20
  fi
  echo 1 | tee /proc/sys/vm/compact_memory > /dev/null
  sleep 300
done
