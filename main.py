#!/usr/bin/env python3
"""
Lexia - Main Application Entry Point

A desktop application that provides intelligent text rewriting with customizable
styles and multiple AI models. Works globally across all applications using
a configurable hotkey.

Author: Muhammad Jawad Bashir
License: MIT
"""

import pyperclip
import keyboard
import pyautogui
import threading
import time
import os
import sys
import pystray
from PIL import Image, ImageDraw
from ui_enhanced import show_popup
from settings import load_settings, get_api_keys, show_settings_window
import tkinter as tk

last_hotkey_time = 0
window_open = False
tray_icon = None

def create_icon_image():
    """Create a simple icon for the system tray"""
    # Create a 64x64 image with a white background
    img = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a blue 'L' for Lexia
    draw.rectangle([10, 10, 54, 54], fill='#2196F3')
    draw.text((22, 15), 'L', fill='white', font=None)
    
    return img

def quit_app(icon, item):
    """Quit the application from system tray"""
    print("Exiting Lexia...")
    icon.stop()
    keyboard.unhook_all()
    # Clean up lock file
    lock_file = "app.lock"
    if os.path.exists(lock_file):
        os.remove(lock_file)
    os._exit(0)

def show_settings(icon, item):
    """Show settings window from system tray"""
    root = tk.Tk()
    root.withdraw()
    show_settings_window(root)
    root.destroy()

def show_about(icon, item):
    """Show about dialog from system tray"""
    from ui_enhanced import show_about_dialog
    root = tk.Tk()
    root.withdraw()
    show_about_dialog(root)
    root.destroy()

def run_tray_icon():
    """Run the system tray icon"""
    global tray_icon
    
    # Create menu
    menu = pystray.Menu(
        pystray.MenuItem("Lexia - Text Rewriter", lambda: None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Settings", show_settings),
        pystray.MenuItem("About", show_about),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", quit_app)
    )
    
    # Create icon
    image = create_icon_image()
    tray_icon = pystray.Icon("Lexia", image, "Lexia - Press Ctrl+Shift+R", menu)
    
    # Run the icon
    tray_icon.run()

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
    # Set process name for Task Manager
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("Lexia - Text Rewriter")
    except:
        pass
    
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
        print("Look for Lexia icon in system tray to exit")
        
        # Show which API keys are configured
        if keys["openai"]:
            print("✓ OpenAI API key configured")
        if keys["groq"]:
            print("✓ Groq API key configured")
        
        # Start system tray icon in a separate thread
        tray_thread = threading.Thread(target=run_tray_icon, daemon=True)
        tray_thread.start()
        
        # Register hotkey
        keyboard.add_hotkey(hotkey, handle_hotkey)
        
        # Keep the main thread alive
        try:
            keyboard.wait()
        except KeyboardInterrupt:
            pass
        
    finally:
        # Clean up
        if tray_icon:
            tray_icon.stop()
        keyboard.unhook_all()
        if os.path.exists(lock_file):
            os.remove(lock_file)
