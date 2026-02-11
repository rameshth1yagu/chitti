### Install Ollama

# Set high-performance power mode 
sudo nvpmodel -m 0 

# Clear system memory caches 
sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches 

# Stop background ROS 2 and Ubuntu update services 
sudo systemctl stop apt-daily.timer 
ros2 daemon stop

# Install the Ollama framework 
curl -fsSL https://ollama.com/install.sh | sh 
# Verify the version 
ollama --version 
# Stop the default background service to apply custom research settings 
sudo systemctl stop ollama

# Enable Unified Memory and set immediate purge (0s) 
export GGML_CUDA_ENABLE_UNIFIED_MEMORY=1
export OLLAMA_KEEP_ALIVE=0 
# Start the server (manually, to monitor the CUDA logs) 
ollama serve

# Pull and run the Moondream vision-language model 
ollama run moondream 
# (Optional) Verify vision capability with a static file 
ollama run moondream "Describe this image: /home/rameshthiyagu/chitti/test_frame.jpg"