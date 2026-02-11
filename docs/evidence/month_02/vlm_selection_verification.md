
# Pull Llama3/VILA Models (Model Selection)

## Objective
Acquire and verify Vision-Language Models (VLM) for real-time hazard detection and behavioral cloning.

## Models Evaluated
1. **Moondream (1.6B)**: ~828MB. Selected for its low memory footprint and high inference speed on edge hardware.
2. **LLaVA (7.24B)**: ~4.7GB. Used as a heavyweight benchmark for comparative analysis.

## Commands Used
```bash
ollama pull moondream
ollama pull llava
ollama list