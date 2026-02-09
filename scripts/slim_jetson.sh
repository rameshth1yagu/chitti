#!/bin/bash

echo "🚀 Starting Chitti System Optimization..."

# 1. Kill and Mask the File Indexer (Tracker)
# This is usually the #1 CPU thief on idle Jetsons
echo "🛑 Disabling Tracker Miner (File Indexer)..."
tracker daemon -t
gsettings set org.freedesktop.Tracker.Miner.Files crawling-interval -2
gsettings set org.freedesktop.Tracker.Miner.Files enable-monitors false

# 2. Disable Automatic Update Checks
# Prevents random spikes during benchmarks
echo "🛑 Disabling Automatic Update Checks..."
sudo systemctl stop apt-daily.timer
sudo systemctl disable apt-daily.timer
sudo systemctl mask apt-daily.service
sudo systemctl stop unattended-upgrades.service
sudo systemctl disable unattended-upgrades.service

# 3. Stop the ROS 2 Daemon (if it's hanging around)
echo "🛑 Cleaning up ROS 2 Daemon..."
ros2 daemon stop

# 4. Set Power Mode to High Performance (15W)
# This ensures cores don't 'jitter' during your tests
echo "⚡ Setting Power Mode to 15W (High Performance)..."
sudo nvpmodel -m 0 # Mode 0 is usually the highest performance mode on Orin Nano

# 5. Check Results
echo "✅ Optimization Complete."
echo "📊 Current Top Processes (Wait 5 seconds for jtop to stabilize):"
sleep 5
top -o %CPU -n 1 | head -n 15