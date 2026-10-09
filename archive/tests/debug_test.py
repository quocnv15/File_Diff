#!/usr/bin/env python3
import os
import sys
from pathlib import Path

print("🔍 Debug Test Script")
print(f"Current directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")

# Check backend directory
backend_dir = Path("backend")
print(f"Backend dir exists: {backend_dir.exists()}")

if backend_dir.exists():
    venv_python = backend_dir / "venv" / "bin" / "python"
    print(f"Venv Python path: {venv_python}")
    print(f"Venv Python exists: {venv_python.exists()}")

    if venv_python.exists():
        print("✅ Venv Python found!")
    else:
        print("❌ Venv Python not found!")
        # Check alternatives
        alt_paths = [
            backend_dir / "venv" / "Scripts" / "python.exe",
            backend_dir / "venv" / "bin" / "python3",
        ]
        for path in alt_paths:
            print(f"Checking alternative: {path} - exists: {path.exists()}")