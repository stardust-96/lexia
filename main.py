#!/usr/bin/env python3
"""
Lexia - Main Application Entry Point

A desktop application that provides intelligent text rewriting with customizable
styles and multiple AI models. Works globally across all applications using
a configurable hotkey.

Author: Your Name
License: MIT
"""

import pyperclip
import keyboard
import pyautogui
import threading
import time
import os
import sys
from ui_enhanced import show_popup
from settings import load_settings, get_api_keys, show_settings_window

last_hotkey_time = 0
window_open = False

def handle_hotkey():
    global last_hotkey_time, window_open
    current_time = time.time()
    
    # Prevent multiple windows
    if window_open:
        print("Window already open, ignoring hotkey")
        return
    
    # Debounce - ignore if called within 1 second
    if current_time - last_hotkey_time < 1.0:
        print("Hotkey ignored (too soon)")
        return
    
    last_hotkey_time = current_time
    window_open = True
    
    # Simulate Ctrl+C to copy selected text
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)  # Give clipboard time to update

    original_text = pyperclip.paste().strip()
    if not original_text:
        print("No text selected.")
        window_open = False
        return

    # Open the UI window
    show_popup(original_text)
    window_open = False  # Reset when window closes

if __name__ == "__main__":
    # Check for lock file to prevent multiple instances
    lock_file = "app.lock"
    if os.path.exists(lock_file):
        # Check if the process is actually running
        try:
            with open(lock_file, 'r') as f:
                old_pid = int(f.read().strip())
            
            # Try to check if process is still running (Windows)
            try:
                import psutil
                if psutil.pid_exists(old_pid):
                    print("Application already running! Please close the existing instance first.")
                    sys.exit(1)
                else:
                    print("Removing stale lock file...")
                    os.remove(lock_file)
            except ImportError:
                # psutil not available, remove old lock file
                print("Removing stale lock file...")
                os.remove(lock_file)
        except:
            # Invalid lock file, remove it
            os.remove(lock_file)
    
    # Create lock file
    try:
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
        
        settings = load_settings()
        
        # Check for API keys on first run
        keys = get_api_keys()
        if not keys["openai"] and not keys["groq"]:
            print("Welcome to Lexia!")
            print("First-time setup: Please configure your API keys...")
            print("Opening settings window...")
            
            # Show settings window for first-time setup
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            show_settings_window(root)
            root.destroy()
            
            # Reload settings after setup
            settings = load_settings()
            keys = get_api_keys()
            
            # Check again if keys were added
            if not keys["openai"] and not keys["groq"]:
                print("No API keys configured. Exiting...")
                sys.exit(1)
        
        hotkey = settings.get("hotkey", "ctrl+shift+r")
        
        model_name = settings.get('model', 'llama-4-scout')
        display_name = "GPT-4 (OpenAI)" if model_name == "gpt-4" else "Llama-4-Scout (Groq)"
        
        print("Lexia running...")
        print(f"Press {hotkey.upper()} to rewrite selected text")
        print(f"Using model: {display_name}")
        
        # Show which API keys are configured
        if keys["openai"]:
            print("✓ OpenAI API key configured")
        if keys["groq"]:
            print("✓ Groq API key configured")
        
        keyboard.add_hotkey(hotkey, handle_hotkey)
        keyboard.wait()
        
    finally:
        # Clean up lock file
        if os.path.exists(lock_file):
            os.remove(lock_file)
