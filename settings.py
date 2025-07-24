import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "hotkey": "ctrl+shift+r",
    "model": "llama-4-scout",
    "temperature": 0.7,
    "num_alternatives": 3
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False

def show_settings_window(parent=None, on_settings_changed=None):
    settings = load_settings()
    
    settings_window = tk.Toplevel(parent) if parent else tk.Tk()
    settings_window.title("Settings")
    settings_window.geometry("400x300")
    settings_window.resizable(False, False)
    
    # Hotkey Section
    tk.Label(settings_window, text="Hotkey Settings", font=('Arial', 12, 'bold')).pack(pady=(10, 5))
    
    hotkey_frame = tk.Frame(settings_window)
    hotkey_frame.pack(pady=5)
    
    tk.Label(hotkey_frame, text="Rewrite Hotkey:").pack(side=tk.LEFT, padx=5)
    hotkey_var = tk.StringVar(value=settings["hotkey"])
    hotkey_entry = tk.Entry(hotkey_frame, textvariable=hotkey_var, width=20)
    hotkey_entry.pack(side=tk.LEFT, padx=5)
    
    # Model Section (removed - now in main UI)
    tk.Label(settings_window, text="Model Settings", font=('Arial', 12, 'bold')).pack(pady=(20, 5))
    
    # Temperature
    temp_frame = tk.Frame(settings_window)
    temp_frame.pack(pady=5)
    
    tk.Label(temp_frame, text="Temperature:").pack(side=tk.LEFT, padx=5)
    temp_var = tk.DoubleVar(value=settings["temperature"])
    temp_scale = tk.Scale(temp_frame, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, variable=temp_var, length=150)
    temp_scale.pack(side=tk.LEFT, padx=5)
    
    # Alternatives
    alt_frame = tk.Frame(settings_window)
    alt_frame.pack(pady=5)
    
    tk.Label(alt_frame, text="Number of Alternatives:").pack(side=tk.LEFT, padx=5)
    alt_var = tk.IntVar(value=settings["num_alternatives"])
    alt_spinbox = tk.Spinbox(alt_frame, from_=1, to=5, textvariable=alt_var, width=10)
    alt_spinbox.pack(side=tk.LEFT, padx=5)
    
    # Info Label
    info_label = tk.Label(settings_window, text="Note: Restart the application for hotkey changes to take effect", 
                         font=('Arial', 9, 'italic'), fg="gray")
    info_label.pack(pady=10)
    
    # Buttons
    button_frame = tk.Frame(settings_window)
    button_frame.pack(pady=10)
    
    def save_and_close():
        new_settings = {
            "hotkey": hotkey_var.get(),
            "model": settings["model"],  # Keep existing model
            "temperature": temp_var.get(),
            "num_alternatives": alt_var.get()
        }
        
        if save_settings(new_settings):
            messagebox.showinfo("Success", "Settings saved successfully!")
            if on_settings_changed:
                on_settings_changed(new_settings)
            settings_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to save settings")
    
    def cancel():
        settings_window.destroy()
    
    save_button = tk.Button(button_frame, text="Save", command=save_and_close, width=10)
    save_button.pack(side=tk.LEFT, padx=5)
    
    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel, width=10)
    cancel_button.pack(side=tk.LEFT, padx=5)
    
    if not parent:
        settings_window.mainloop()

if __name__ == "__main__":
    show_settings_window()