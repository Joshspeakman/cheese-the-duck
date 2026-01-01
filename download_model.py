#!/usr/bin/env python3
"""
Download the LLM model for Cheese the Duck.
Run this once to enable AI-powered conversations and dynamic behavior!

This model powers:
- Real-time chat conversations with your duck
- Dynamic action commentary (what Cheese thinks while doing things)
- Visitor dialogue (unique conversations with duck friends)
- Special event narratives
"""
import os
import sys
import subprocess
import urllib.request
import urllib.error
import shutil
from pathlib import Path
from typing import Optional, Tuple

# Configuration
GAME_DIR = Path(__file__).parent
MODEL_DIR = GAME_DIR / "models"
VENV_DIR = GAME_DIR / ".venv"

# Default model (required for LLM features)
DEFAULT_MODEL = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

MODELS = {
    "llama": {
        "name": "Llama 3.2 3B (Best Quality - ~2GB)",
        "url": "https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF/resolve/main/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
        "filename": "Llama-3.2-3B-Instruct-Q4_K_M.gguf",
        "size_mb": 2000,
        "recommended_vram": 4000,  # 4GB VRAM recommended
    },
    "phi": {
        "name": "Phi-3 Mini 3.8B (~2.3GB)",
        "url": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf",
        "filename": "Phi-3-mini-4k-instruct-q4.gguf",
        "size_mb": 2300,
        "recommended_vram": 4000,
    },
    "qwen": {
        "name": "Qwen2.5 3B (~2GB)",
        "url": "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf",
        "filename": "qwen2.5-3b-instruct-q4_k_m.gguf",
        "size_mb": 2000,
        "recommended_vram": 4000,
    },
    "tiny": {
        "name": "TinyLlama 1.1B (Lightweight - ~700MB) ⭐ Default",
        "url": "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "filename": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "size_mb": 700,
        "recommended_vram": 2000,  # Runs well even on 2GB VRAM or CPU
    },
}


# ═══════════════════════════════════════════════════════════════════════════════
# GPU Detection Functions
# ═══════════════════════════════════════════════════════════════════════════════

def detect_gpu_info() -> Tuple[Optional[str], int]:
    """
    Detect GPU type and available VRAM.
    Returns: (gpu_type, vram_mb) where gpu_type is 'nvidia', 'amd', or None
    """
    # Try NVIDIA
    if shutil.which("nvidia-smi"):
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                vram_mb = int(result.stdout.strip().split('\n')[0])
                return ("nvidia", vram_mb)
        except Exception:
            pass
    
    # Try AMD
    if shutil.which("rocm-smi"):
        try:
            result = subprocess.run(
                ["rocm-smi", "--showmeminfo", "vram", "--json"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                import json
                data = json.loads(result.stdout)
                # Parse AMD output (format varies by version)
                for card in data.values():
                    if isinstance(card, dict) and "VRAM Total Memory (B)" in card:
                        vram_mb = int(card["VRAM Total Memory (B)"]) // (1024 * 1024)
                        return ("amd", vram_mb)
        except Exception:
            pass
    
    return (None, 0)


def get_recommended_model(gpu_type: Optional[str], vram_mb: int) -> str:
    """Get recommended model based on GPU capabilities."""
    if gpu_type is None or vram_mb < 2000:
        return "tiny"  # CPU or very limited VRAM
    elif vram_mb >= 4000:
        return "llama"  # Best quality for capable GPUs
    else:
        return "tiny"  # Safe choice for 2-4GB VRAM


# ═══════════════════════════════════════════════════════════════════════════════
# Model Check Functions (for use by the game)
# ═══════════════════════════════════════════════════════════════════════════════

def find_model() -> Optional[Path]:
    """
    Find the first available GGUF model in the models directory.
    Returns the path to the model file or None if not found.
    """
    if not MODEL_DIR.exists():
        return None
    
    models = list(MODEL_DIR.glob("*.gguf"))
    if not models:
        return None
    
    # Prefer the default model if it exists
    default_path = MODEL_DIR / DEFAULT_MODEL
    if default_path.exists():
        return default_path
    
    # Otherwise return the first model found
    return models[0]


def is_model_available() -> bool:
    """Check if any LLM model is available."""
    return find_model() is not None


def get_model_status() -> dict:
    """
    Get detailed status of the LLM model setup.
    Returns a dict with status information.
    """
    model_path = find_model()
    gpu_type, vram_mb = detect_gpu_info()
    
    return {
        "model_available": model_path is not None,
        "model_path": str(model_path) if model_path else None,
        "model_name": model_path.name if model_path else None,
        "gpu_type": gpu_type,
        "vram_mb": vram_mb,
        "gpu_available": gpu_type is not None,
    }


def print_header():
    """Print a nice header."""
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║       🦆 CHEESE THE DUCK - AI MODEL DOWNLOADER 🦆          ║")
    print("║                                                            ║")
    print("║  Download an AI model to enable:                           ║")
    print("║  • Chat conversations with your duck                       ║")
    print("║  • Dynamic action commentary                               ║")
    print("║  • Unique visitor dialogue                                 ║")
    print("║  • Special event narratives                                ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()


def print_gpu_status():
    """Print GPU detection status."""
    gpu_type, vram_mb = detect_gpu_info()
    
    print("🖥️  Hardware Detection:")
    if gpu_type == "nvidia":
        print(f"   ✓ NVIDIA GPU detected with {vram_mb}MB VRAM")
        print(f"   → GPU acceleration will be enabled automatically!")
    elif gpu_type == "amd":
        print(f"   ✓ AMD GPU detected with {vram_mb}MB VRAM")
        print(f"   → GPU acceleration will be enabled automatically!")
    else:
        print("   • No GPU detected - will use CPU (still fast!)")
        print("   → TinyLlama runs great on CPU")
    print()
    
    return gpu_type, vram_mb


def check_existing_models():
    """Check for already downloaded models."""
    if not MODEL_DIR.exists():
        return []
    return list(MODEL_DIR.glob("*.gguf"))


def download_with_progress(url: str, filepath: Path, expected_size_mb: int):
    """Download a file with progress bar."""
    print(f"\n📥 Downloading to: {filepath}")
    print(f"   Expected size: ~{expected_size_mb}MB")
    print()
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        
        with urllib.request.urlopen(req) as response:
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            chunk_size = 1024 * 1024  # 1MB chunks
            
            MODEL_DIR.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'wb') as f:
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    # Progress bar
                    if total_size > 0:
                        pct = downloaded / total_size * 100
                        bar_len = 40
                        filled = int(bar_len * downloaded / total_size)
                        bar = "█" * filled + "░" * (bar_len - filled)
                        mb_done = downloaded / (1024 * 1024)
                        mb_total = total_size / (1024 * 1024)
                        sys.stdout.write(f"\r   [{bar}] {pct:5.1f}% ({mb_done:.0f}/{mb_total:.0f}MB)")
                        sys.stdout.flush()
            
            print()
            print()
            print("✅ Download complete!")
            return True
            
    except urllib.error.URLError as e:
        print(f"\n❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def setup_venv():
    """Set up virtual environment with llama-cpp-python."""
    print("🔧 Setting up Python environment for AI...")
    print()
    
    # Check if venv exists
    venv_python = VENV_DIR / "bin" / "python"
    if venv_python.exists():
        print("   ✓ Virtual environment exists")
    else:
        print("   Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], check=True)
            print("   ✓ Created virtual environment")
        except Exception as e:
            print(f"   ✗ Failed to create venv: {e}")
            return False
    
    # Check if llama-cpp-python is installed
    venv_pip = VENV_DIR / "bin" / "pip"
    try:
        result = subprocess.run(
            [str(venv_python), "-c", "import llama_cpp; print('ok')"],
            capture_output=True, text=True
        )
        if "ok" in result.stdout:
            print("   ✓ llama-cpp-python is installed")
            return True
    except Exception:
        pass
    
    # Install llama-cpp-python
    print("   Installing llama-cpp-python (this may take a few minutes)...")
    print()
    try:
        # Install blessed and llama-cpp-python
        subprocess.run(
            [str(venv_pip), "install", "--upgrade", "pip"],
            check=True, capture_output=True
        )
        subprocess.run(
            [str(venv_pip), "install", "blessed", "llama-cpp-python"],
            check=True
        )
        print()
        print("   ✓ Installed llama-cpp-python")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n   ✗ Installation failed: {e}")
        print("   You can still play without AI - Cheese will use pre-written responses.")
        return False


def main():
    """Main entry point."""
    print_header()
    
    # Step 1: Detect GPU
    gpu_type, vram_mb = print_gpu_status()
    
    # Step 2: Set up the virtual environment
    venv_ok = setup_venv()
    print()
    
    # Step 3: Check for existing models
    existing = check_existing_models()
    if existing:
        print("📁 Found existing model(s):")
        for m in existing:
            size_mb = m.stat().st_size / (1024 * 1024)
            status = "⭐ Active" if m.name == DEFAULT_MODEL else ""
            print(f"   • {m.name} ({size_mb:.0f}MB) {status}")
        print()
        print("✅ You already have a model installed!")
        print()
        
        response = input("🔄 Download a different model anyway? [y/N]: ").strip().lower()
        if response != 'y':
            print("\n👍 Setup complete! Run the game with: ./run_game.sh")
            return 0
        print()
    
    # Get recommended model based on hardware
    recommended = get_recommended_model(gpu_type, vram_mb)
    
    # Show model options
    print("📦 Available models:")
    print()
    for key, model in MODELS.items():
        rec_badge = " ← Recommended for your hardware" if key == recommended else ""
        print(f"   [{key}] {model['name']}{rec_badge}")
    print()
    
    # Get user choice
    print(f"   Default: {recommended}")
    print()
    choice = input(f"🎯 Which model? [llama/phi/qwen/tiny] (default: {recommended}): ").strip().lower()
    if choice not in MODELS:
        choice = recommended
    
    model = MODELS[choice]
    filepath = MODEL_DIR / model["filename"]
    
    print()
    print(f"🦆 Selected: {model['name']}")
    
    # Download
    if download_with_progress(model["url"], filepath, model["size_mb"]):
        print()
        print("╔════════════════════════════════════════════════════════════╗")
        print("║              🎉 AI BRAIN INSTALLED! 🎉                     ║")
        print("║                                                            ║")
        print("║  Cheese now has a real AI-powered personality!             ║")
        print("║                                                            ║")
        if gpu_type:
            print("║  🚀 GPU acceleration enabled for fast responses!          ║")
        else:
            print("║  💻 Running on CPU (TinyLlama is optimized for this)       ║")
        print("║                                                            ║")
        print("║  Run the game with: ./run_game.sh                          ║")
        print("║  Press [T] to talk to your duck!                           ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        return 0
    else:
        print()
        print("╔════════════════════════════════════════════════════════════╗")
        print("║              ❌ DOWNLOAD FAILED                            ║")
        print("║                                                            ║")
        print("║  The AI model is required for the full game experience.    ║")
        print("║                                                            ║")
        print("║  Please check:                                             ║")
        print("║  • Your internet connection                                ║")
        print("║  • You have enough disk space (~700MB - 2GB)               ║")
        print("║  • Firewall isn't blocking huggingface.co                  ║")
        print("║                                                            ║")
        print("║  Then try again: python download_model.py                  ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        return 1


def check_and_prompt_download() -> bool:
    """
    Check if model is available, if not prompt user to download.
    This is called by the game on startup.
    Returns True if a model is available (or user skips), False to exit.
    """
    if is_model_available():
        return True
    
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         🦆 AI MODEL REQUIRED                               ║")
    print("║                                                            ║")
    print("║  Cheese the Duck needs an AI model for:                    ║")
    print("║  • Dynamic conversations                                   ║")
    print("║  • Personality-driven behavior                             ║")
    print("║  • Unique visitor interactions                             ║")
    print("║                                                            ║")
    print("║  Run: python download_model.py                             ║")
    print("║  (Takes 1-5 minutes depending on your connection)          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    response = input("Download now? [Y/n]: ").strip().lower()
    if response in ('', 'y', 'yes'):
        # Run the download
        return main() == 0
    
    print()
    print("⚠️  Starting without AI model.")
    print("   Cheese will use pre-written template responses.")
    print()
    return True  # Allow game to start without AI


if __name__ == "__main__":
    sys.exit(main())
