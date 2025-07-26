#!/usr/bin/env python3
"""
Simplified build script for GitHub Actions - direct PyInstaller call
"""

import subprocess
import sys
import os

print("Starting simplified Lexia build...")
print("Current directory:", os.getcwd())
print("Python version:", sys.version)

# Direct PyInstaller command with minimal options
cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--onefile',
    '--windowed',
    '--name=Lexia',
    '--icon=lexia.ico',
    '--nostrip',
    '--noupx',
    'main.py'
]

print("Running:", ' '.join(cmd))
result = subprocess.run(cmd)

if result.returncode == 0:
    print("Build completed successfully!")
    if os.path.exists('dist/Lexia.exe'):
        size = os.path.getsize('dist/Lexia.exe') / (1024 * 1024)
        print(f"Executable size: {size:.1f} MB")
else:
    print(f"Build failed with return code: {result.returncode}")
    sys.exit(1)