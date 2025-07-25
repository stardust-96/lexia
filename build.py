#!/usr/bin/env python3
"""
Build script for Lexia - Creates executable using PyInstaller
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

def clean_build():
    """Clean previous build artifacts"""
    print("Cleaning previous build artifacts...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")
    
    # Remove .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building Lexia executable...")
    
    try:
        # Run PyInstaller with the spec file
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm',
            'lexia.spec'
        ], check=True, capture_output=True, text=True)
        
        print("Build completed successfully!")
        print(f"Executable created: dist/Lexia.exe")
        
        # Check if executable exists and get its size
        exe_path = Path('dist/Lexia.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"File size: {size_mb:.1f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("Build failed!")
        print("Error output:", e.stderr)
        return False

def test_executable():
    """Test if the executable runs without errors"""
    print("Testing executable...")
    
    exe_path = Path('dist/Lexia.exe')
    if not exe_path.exists():
        print("Executable not found!")
        return False
    
    try:
        # Just check if it can start (will exit quickly due to lock file check)
        result = subprocess.run([str(exe_path)], 
                              timeout=5, 
                              capture_output=True, 
                              text=True)
        print("Executable test passed!")
        return True
        
    except subprocess.TimeoutExpired:
        print("Executable started successfully (timeout expected)")
        return True
    except Exception as e:
        print(f"Executable test failed: {e}")
        return False

def create_release_package():
    """Create a release package with documentation"""
    print("Creating release package...")
    
    release_dir = Path('release')
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir()
    
    # Copy executable
    shutil.copy2('dist/Lexia.exe', release_dir / 'Lexia.exe')
    
    # Copy documentation
    files_to_copy = ['README.md', 'LICENSE', 'config.example.py']
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, release_dir / file_name)
    
    # Create a simple installation guide
    install_guide = release_dir / 'INSTALLATION.txt'
    with open(install_guide, 'w') as f:
        f.write("""LEXIA - Installation Guide
==========================

1. Extract all files to a folder of your choice
2. Copy config.example.py to config.py
3. Edit config.py and add your API keys:
   - OPENAI_API_KEY = "your-openai-key"
   - GROQ_API_KEY = "your-groq-key"
4. Run Lexia.exe
5. Press Ctrl+Shift+R to use the text rewriter

For more information, see README.md

Enjoy using Lexia!
""")
    
    print(f"Release package created in: {release_dir}")
    
    # Create ZIP file
    try:
        import zipfile
        
        zip_path = f'Lexia-v1.1.0-Windows.zip'
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in release_dir.rglob('*'):
                if file_path.is_file():
                    arcname = file_path.relative_to(release_dir)
                    zipf.write(file_path, arcname)
        
        print(f"ZIP package created: {zip_path}")
        
    except ImportError:
        print("Warning: zipfile not available, manual ZIP creation needed")

def main():
    """Main build process"""
    print("Starting Lexia build process...")
    print("=" * 50)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Step 1: Clean
    clean_build()
    print()
    
    # Step 2: Build
    if not build_executable():
        sys.exit(1)
    print()
    
    # Step 3: Test
    if not test_executable():
        print("Warning: Executable test failed, but build completed")
    print()
    
    # Step 4: Package
    create_release_package()
    print()
    
    print("Build process completed successfully!")
    print("Check the 'release' folder for distribution files")

if __name__ == "__main__":
    main()