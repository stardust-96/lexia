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
import msvcrt
from PIL import Image, ImageDraw
from ui_enhanced import show_popup
from settings import load_settings, get_api_keys, show_settings_window
import tkinter as tk
from tkinter import messagebox
from settings_store import save_settings, is_onboarding_complete, clear_stored_api_keys
from onboarding import run_onboarding_wizard
from app_paths import get_icon_path, apply_window_icon

last_hotkey_time = 0
window_open = False
tray_icon = None
DEV_MODE = os.getenv("LEXIA_DEV_MODE", "0") == "1"
instance_lock_handle = None


def get_runtime_data_dir():
    """Return a per-user writable directory for runtime files."""
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data:
        runtime_dir = os.path.join(local_app_data, "Lexia")
    else:
        runtime_dir = os.path.join(os.path.expanduser("~"), ".lexia")
    os.makedirs(runtime_dir, exist_ok=True)
    return runtime_dir

def create_icon_image():
    """Load Lexia icon for tray; fallback to generated icon if unavailable."""
    icon_path = get_icon_path()
    if icon_path:
        try:
            return Image.open(icon_path)
        except Exception:
            pass

    img = Image.new('RGB', (64, 64), color='white')
    draw = ImageDraw.Draw(img)
    draw.rectangle([10, 10, 54, 54], fill='#2196F3')
    draw.text((22, 15), 'L', fill='white', font=None)
    return img

def quit_app(icon, item):
    """Quit the application from system tray"""
    print("Exiting Lexia...")
    icon.stop()
    keyboard.unhook_all()
    os._exit(0)


def acquire_single_instance_lock():
    """Acquire an OS-level file lock to ensure single-instance execution."""
    lock_path = os.path.join(get_runtime_data_dir(), "app.lock")
    handle = open(lock_path, "a+")
    handle.seek(0)
    try:
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
    except OSError:
        handle.close()
        return None
    handle.truncate(0)
    handle.write(str(os.getpid()))
    handle.flush()
    return handle

def show_settings(icon, item):
    """Show settings window from system tray"""
    show_settings_window()

def show_about(icon, item):
    """Show about dialog from system tray"""
    from ui_enhanced import show_about_dialog
    root = tk.Tk()
    root.withdraw()
    apply_window_icon(root)
    about = show_about_dialog(root)
    root.wait_window(about)
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


def run_hotkey_listener(hotkey):
    """Register and keep hotkey listener alive on a background thread."""
    keyboard.add_hotkey(hotkey, handle_hotkey)
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        pass

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

    try:
        # Simulate Ctrl+C to copy selected text
        try:
            pyautogui.hotkey('ctrl', 'c')
        except Exception as e:
            print(f"Failed to trigger copy hotkey: {e}")
            return

        time.sleep(0.2)  # Give clipboard time to update

        try:
            original_text = pyperclip.paste().strip()
        except Exception as e:
            print(f"Failed to read clipboard: {e}")
            return

        if not original_text:
            print("No text selected.")
            return

        # Open the UI window
        show_popup(original_text)
    except Exception as e:
        print(f"Unexpected error while handling hotkey: {e}")
    finally:
        window_open = False  # Always reset state

if __name__ == "__main__":
    if "--cleanup-secrets" in sys.argv:
        clear_stored_api_keys()
        sys.exit(0)

    # Set process name for Task Manager
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("Lexia - Text Rewriter")
    except:
        pass
    
    # Acquire single-instance lock.
    instance_lock_handle = acquire_single_instance_lock()
    if instance_lock_handle is None:
        print("Application already running! Please close the existing instance first.")
        sys.exit(1)

    try:
        settings = load_settings()

        # Hard gate: onboarding must complete before app runs (except in dev mode).
        if not DEV_MODE and not is_onboarding_complete(settings):
            print("First-time setup required. Opening onboarding wizard...")
            setup_root = tk.Tk()
            setup_root.withdraw()
            completed = run_onboarding_wizard(setup_root)
            setup_root.destroy()
            if not completed:
                print("Onboarding not completed. Exiting...")
                sys.exit(1)
            settings = load_settings()

        # One-time startup notice so users know the app lives in the tray.
        if not settings.get("tray_notice_shown", False):
            notice_root = tk.Tk()
            notice_root.withdraw()
            apply_window_icon(notice_root)
            messagebox.showinfo(
                "Lexia is Running",
                "Lexia runs in the system tray.\n\n"
                "Use Ctrl+Shift+R to open rewrite window.\n"
                "Right-click the tray icon for Settings and Quit."
            )
            notice_root.destroy()
            settings["tray_notice_shown"] = True
            save_settings(settings)

        keys = get_api_keys()
        
        hotkey = settings.get("hotkey", "ctrl+shift+r")
        
        model_name = settings.get('model', '')
        if model_name == "gpt-4":
            display_name = "GPT (OpenAI)"
        elif model_name == "llama-4-scout":
            display_name = "Llama-4-Scout (Groq)"
        else:
            display_name = "Not Set"
        
        print("Lexia running...")
        if DEV_MODE:
            print("[DEV MODE] Running with LEXIA_DEV_MODE=1")
        print(f"Press {hotkey.upper()} to rewrite selected text")
        print(f"Using model: {display_name}")
        print("Look for Lexia icon in system tray to exit")
        
        # Show which API keys are configured
        if keys["openai"]:
            print("[OK] OpenAI API key configured")
        if keys["groq"]:
            print("[OK] Groq API key configured")
        
        # Keep Tk interactions on the main thread by running tray loop here.
        hotkey_thread = threading.Thread(target=run_hotkey_listener, args=(hotkey,), daemon=True)
        hotkey_thread.start()
        run_tray_icon()
        
    finally:
        # Clean up
        if tray_icon:
            tray_icon.stop()
        keyboard.unhook_all()
        if instance_lock_handle:
            try:
                instance_lock_handle.seek(0)
                msvcrt.locking(instance_lock_handle.fileno(), msvcrt.LK_UNLCK, 1)
            except OSError:
                pass
            instance_lock_handle.close()
