#!/usr/bin/env python3
"""
Download the LLM model for Cheese the Duck.
Run this once to enable AI-powered conversations!
"""
import os
import sys
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

# Configuration
GAME_DIR = Path(__file__).parent
MODEL_DIR = GAME_DIR / "models"
VENV_DIR = GAME_DIR / ".venv"

MODELS = {
    "tiny": {
        "name": "TinyLlama 1.1B (Recommended - ~700MB)",
        "url": "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "filename": "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf",
        "size_mb": 700,
    },
    "small": {
        "name": "Phi-3 Mini 3.8B (Better quality - ~2.3GB)",
        "url": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf",
        "filename": "Phi-3-mini-4k-instruct-q4.gguf",
        "size_mb": 2300,
    },
}


def print_header():
    """Print a nice header."""
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         🦆 CHEESE THE DUCK - AI MODEL DOWNLOADER 🦆        ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()


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
    
    # Step 1: Set up the virtual environment
    venv_ok = setup_venv()
    print()
    
    # Step 2: Check for existing models
    existing = check_existing_models()
    if existing:
        print("📁 Found existing model(s):")
        for m in existing:
            size_mb = m.stat().st_size / (1024 * 1024)
            print(f"   • {m.name} ({size_mb:.0f}MB)")
        print()
        
        response = input("🔄 Download a new model anyway? [y/N]: ").strip().lower()
        if response != 'y':
            print("\n👍 Setup complete! Run the game with: ./run_game.sh")
            return 0
        print()
    
    # Show model options
    print("📦 Available models:")
    print()
    for key, model in MODELS.items():
        print(f"   [{key}] {model['name']}")
    print()
    
    # Get user choice
    choice = input("🎯 Which model? [tiny/small] (default: tiny): ").strip().lower()
    if choice not in MODELS:
        choice = "tiny"
    
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
        print("║  Cheese can now have real conversations with you!          ║")
        print("║  Run the game with: ./run_game.sh                          ║")
        print("║  Press [T] to talk to your duck!                           ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print()
        return 0
    else:
        print()
        print("❌ Download failed. Please check your internet connection.")
        print("   You can still play the game - Cheese will use pre-written responses.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
