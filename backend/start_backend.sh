#!/bin/bash
# Backend startup script with proper environment

export PYTHONPATH="/Volumes/Workspace/1-SideProject/File_Diff/backend"
cd "/Volumes/Workspace/1-SideProject/File_Diff/backend"

echo "🚀 Starting FastAPI Backend..."
echo "Python executable: $(which python)"
echo "Working directory: $(pwd)"
echo "PYTHONPATH: $PYTHONPATH"

# Start backend with virtual environment
exec "./venv/bin/python" main.py