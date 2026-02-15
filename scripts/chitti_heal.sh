#!/bin/bash

# 1. Colors for the Terminal (Makes for great demo videos)
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}[1/3] Flushing Kernel Page Caches...${NC}"
# Clears PageCache, dentries, and inodes to defragment RAM
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches > /dev/null

echo -e "${BLUE}[2/3] Hard Restarting Watchdog Service...${NC}"
# This triggers your Task 105 privacy environment variables
sudo systemctl restart chitti-watchdog.service

echo -e "${BLUE}[3/3] Re-initializing GPU Buffers...${NC}"
# Wait for the service to bind the port (11434)
for i in {1..15}; do
    if ss -tulpn | grep -q ":11434"; then
        echo -e "${GREEN}✅ Chitti is Healthy and Listening!${NC}"
        exit 0
    fi
    echo -n "."
    sleep 1
done

echo -e "\n⚠️  Warning: Ollama is taking longer than usual to start."