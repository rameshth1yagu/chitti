"""
VLM inference module for Project Chitti - Cognitive Edge Sentry.

EPIC 1 (Phase 1): Vision-Language Perception
Handles Ollama API communication for Moondream vision-language inference.

EB-1A Relevance: Demonstrates edge AI deployment with privacy-preserving
image-to-semantic transformation. Visual data remains in RAM, only text
extracted for decision-making.
"""

import base64
import logging
import requests
from pathlib import Path
from typing import Optional, Dict, Any

from config.settings import (
    OLLAMA_URL,
    OLLAMA_MODEL,
    OLLAMA_TIMEOUT,
    OLLAMA_PROMPT,
)

logger = logging.getLogger(__name__)


class VLMClient:
    """
    Ollama Vision-Language Model client.

    Handles base64 encoding of images and REST API communication
    for semantic scene understanding.
    """

    def __init__(
        self,
        url: str = OLLAMA_URL,
        model: str = OLLAMA_MODEL,
        timeout: int = OLLAMA_TIMEOUT,
    ) -> None:
        """
        Initialize VLM client.

        Args:
            url: Ollama API endpoint
            model: Model name (e.g., "moondream")
            timeout: Request timeout in seconds
        """
        self.url = url
        self.model = model
        self.timeout = timeout

        logger.info(
            "vlm_client_init",
            extra={
                "url": url,
                "model": model,
                "timeout": timeout,
            }
        )

    def encode_image(self, image_path: Path) -> str:
        """
        Encode image to base64 for Ollama API.

        Args:
            image_path: Path to JPEG image (must be in /dev/shm)

        Returns:
            Base64-encoded image string

        Raises:
            FileNotFoundError: If image doesn't exist
            ValueError: If image path is not in /dev/shm
        """
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")

        # CRITICAL: Verify image is in /dev/shm (RAM only)
        if "/dev/shm" not in str(image_path):
            raise ValueError(
                f"Privacy violation: Image must be in /dev/shm, got {image_path}"
            )

        with open(image_path, "rb") as img_file:
            img_bytes = img_file.read()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        size_kb = len(img_bytes) / 1024
        logger.info(
            "image_encoded",
            extra={
                "path": str(image_path),
                "size_kb": round(size_kb, 2),
                "base64_length": len(img_base64),
            }
        )

        return img_base64

    def infer(
        self,
        image_path: Path,
        prompt: str = OLLAMA_PROMPT
    ) -> Optional[Dict[str, Any]]:
        """
        Run VLM inference on image.

        Args:
            image_path: Path to image in /dev/shm
            prompt: Query prompt for VLM

        Returns:
            Dict with 'response' (str) and 'latency_sec' (float)
            None if inference fails

        Raises:
            ValueError: If image not in /dev/shm
        """
        import time

        # Encode image
        try:
            img_base64 = self.encode_image(image_path)
        except (FileNotFoundError, ValueError) as e:
            logger.error("image_encode_failed", extra={"error": str(e)})
            return None

        # Prepare payload
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "images": [img_base64]
        }

        logger.info(
            "inference_start",
            extra={
                "model": self.model,
                "prompt": prompt,
            }
        )

        # Call Ollama API
        t_start = time.time()
        try:
            response = requests.post(
                self.url,
                json=payload,
                timeout=self.timeout
            )
            t_end = time.time()
            latency_sec = round(t_end - t_start, 3)

            if response.status_code == 200:
                result = response.json()
                description = result.get('response', '')

                logger.info(
                    "inference_success",
                    extra={
                        "latency_sec": latency_sec,
                        "response_length": len(description),
                    }
                )

                return {
                    "response": description,
                    "latency_sec": latency_sec,
                    "model": self.model,
                }
            else:
                logger.error(
                    "inference_api_error",
                    extra={
                        "status_code": response.status_code,
                        "latency_sec": latency_sec,
                    }
                )
                return None

        except requests.exceptions.Timeout:
            logger.error(
                "inference_timeout",
                extra={"timeout": self.timeout}
            )
            return None
        except requests.exceptions.RequestException as e:
            logger.error(
                "inference_request_failed",
                extra={"error": str(e)}
            )
            return None
