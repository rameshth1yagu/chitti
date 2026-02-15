"""
Setup configuration for Project Chitti - Cognitive Edge Sentry.

Install in development mode:
    pip install -e .

This allows clean imports:
    from core.camera import CameraCapture
    from config.settings import OLLAMA_URL
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text() if readme_path.exists() else ""

setup(
    name="chitti",
    version="0.1.0-phase1",
    author="Ramesh Thiyagu",
    author_email="rameshth1yagu@example.com",  # Update with real email
    description="Privacy-first embodied AI robot with zero data retention",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rameshth1yagu/chitti",
    packages=find_packages(exclude=["tests", "docs", "data", "models"]),
    python_requires=">=3.10",
    install_requires=[
        "opencv-python>=4.10.0",
        "numpy>=1.26.0",
        "requests>=2.32.0",
        "adafruit-circuitpython-pca9685>=3.4.0",
        "adafruit-servokit>=1.3.0",
        "jetson-stats>=4.2.0; platform_machine=='aarch64'",
        "pytest>=8.3.0",
        "matplotlib>=3.9.0",
        "pandas>=2.2.0",
    ],
    extras_require={
        "dev": [
            "pytest-cov>=5.0.0",
            "pytest-mock>=3.14.0",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Hardware :: Symmetric Multi-processing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
    ],
    keywords="robotics edge-ai privacy jetson vision-language embodied-ai",
    project_urls={
        "Bug Reports": "https://github.com/rameshth1yagu/chitti/issues",
        "Documentation": "https://github.com/rameshth1yagu/chitti/blob/main/README.md",
    },
)
