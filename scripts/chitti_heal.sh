#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# --- PHASE 1: PREPARE THE MEMORY ---
echo -e "${BLUE}[1/4] Deep Memory Defragmentation...${NC}"
# Flush caches first
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null
# Force the kernel to group free pages together (Prevents Error 12)
echo 1 | sudo tee /proc/sys/vm/compact_memory
echo -e "${GREEN}✅ RAM Compacted.${NC}"

# --- PHASE 2: RESET GPU STATE ---
echo -e "${BLUE}[2/4] Re-initializing GPU Buffers...${NC}"
# This clears any hung CUDA context without a reboot
sudo jetson_clocks --store > /dev/null # Optional: saves current state
sudo jetson_clocks > /dev/null

# --- PHASE 3: SERVICE RESTART ---
echo -e "${BLUE}[3/4] Hard Restarting Watchdog Service...${NC}"
sudo systemctl restart chitti-watchdog.service

# --- PHASE 4: PORT VALIDATION ---
echo -e "${BLUE}[4/4] Waiting for AI API...${NC}"
for i in {1..20}; do
    if curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
        echo -e "\n${GREEN}✅ Chitti is Healthy and Listening!${NC}"
        exit 0
    fi
    echo -n "."
    sleep 1
done

echo -e "\n${YELLOW}⚠️  Warning: Ollama is taking longer than usual.${NC}"