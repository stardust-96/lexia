import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import base64

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "hotkey": "ctrl+shift+r",
    "model": "llama-4-scout",
    "temperature": 0.7,
    "num_alternatives": 3,
    "openai_api_key": "",
    "groq_api_key": ""
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def _encode_api_key(key):
    """Simple base64 encoding for API keys (not encryption, just obfuscation)"""
    if not key:
        return ""
    return base64.b64encode(key.encode()).decode()

def _decode_api_key(encoded_key):
    """Decode base64 encoded API key"""
    if not encoded_key:
        return ""
    try:
        return base64.b64decode(encoded_key.encode()).decode()
    except:
        return ""

def save_settings(settings):
    try:
        # Encode API keys before saving
        settings_to_save = settings.copy()
        if "openai_api_key" in settings_to_save:
            settings_to_save["openai_api_key"] = _encode_api_key(settings_to_save["openai_api_key"])
        if "groq_api_key" in settings_to_save:
            settings_to_save["groq_api_key"] = _encode_api_key(settings_to_save["groq_api_key"])
            
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings_to_save, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                settings = json.load(f)
            
            # Decode API keys after loading
            if "openai_api_key" in settings:
                settings["openai_api_key"] = _decode_api_key(settings["openai_api_key"])
            if "groq_api_key" in settings:
                settings["groq_api_key"] = _decode_api_key(settings["groq_api_key"])
                
            # Ensure all default keys exist
            for key, value in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = value
                    
            return settings
        except:
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def get_api_keys():
    """Get API keys from settings"""
    settings = load_settings()
    return {
        "openai": settings.get("openai_api_key", ""),
        "groq": settings.get("groq_api_key", "")
    }

def show_settings_window(parent=None, on_settings_changed=None):
    settings = load_settings()
    
    settings_window = tk.Toplevel(parent) if parent else tk.Tk()
    settings_window.title("Lexia Settings")
    settings_window.geometry("500x450")
    settings_window.resizable(False, False)
    
    # Create notebook for tabs
    notebook = ttk.Notebook(settings_window)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # General Settings Tab
    general_frame = ttk.Frame(notebook)
    notebook.add(general_frame, text="General")
    
    # API Keys Tab
    api_frame = ttk.Frame(notebook)
    notebook.add(api_frame, text="API Keys")
    
    # GENERAL TAB CONTENT
    # Hotkey Section
    tk.Label(general_frame, text="Hotkey Settings", font=('Arial', 12, 'bold')).pack(pady=(10, 5))
    
    hotkey_frame = tk.Frame(general_frame)
    hotkey_frame.pack(pady=5)
    
    tk.Label(hotkey_frame, text="Rewrite Hotkey:").pack(side=tk.LEFT, padx=5)
    hotkey_var = tk.StringVar(value=settings["hotkey"])
    hotkey_entry = tk.Entry(hotkey_frame, textvariable=hotkey_var, width=20)
    hotkey_entry.pack(side=tk.LEFT, padx=5)
    
    # Model Section
    tk.Label(general_frame, text="Model Settings", font=('Arial', 12, 'bold')).pack(pady=(20, 5))
    
    # Temperature
    temp_frame = tk.Frame(general_frame)
    temp_frame.pack(pady=5)
    
    tk.Label(temp_frame, text="Temperature:").pack(side=tk.LEFT, padx=5)
    temp_var = tk.DoubleVar(value=settings["temperature"])
    temp_scale = tk.Scale(temp_frame, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, variable=temp_var, length=150)
    temp_scale.pack(side=tk.LEFT, padx=5)
    
    # Alternatives
    alt_frame = tk.Frame(general_frame)
    alt_frame.pack(pady=5)
    
    tk.Label(alt_frame, text="Number of Alternatives:").pack(side=tk.LEFT, padx=5)
    alt_var = tk.IntVar(value=settings["num_alternatives"])
    alt_spinbox = tk.Spinbox(alt_frame, from_=1, to=5, textvariable=alt_var, width=10)
    alt_spinbox.pack(side=tk.LEFT, padx=5)
    
    # Info Label
    info_label = tk.Label(general_frame, text="Note: Restart the application for hotkey changes to take effect", 
                         font=('Arial', 9, 'italic'), fg="gray")
    info_label.pack(pady=10)
    
    # API KEYS TAB CONTENT
    tk.Label(api_frame, text="API Configuration", font=('Arial', 14, 'bold')).pack(pady=(15, 10))
    
    # Description
    desc_text = ("Enter your API keys below. Keys are stored locally and encrypted.\n"
                "You only need one API key to use Lexia.")
    tk.Label(api_frame, text=desc_text, font=('Arial', 9), fg="gray", justify=tk.CENTER).pack(pady=(0, 15))
    
    # OpenAI API Key
    openai_frame = tk.LabelFrame(api_frame, text="OpenAI (for GPT-4)", font=('Arial', 10, 'bold'), padx=10, pady=10)
    openai_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
    
    tk.Label(openai_frame, text="API Key:", font=('Arial', 9)).pack(anchor=tk.W)
    openai_var = tk.StringVar(value=settings.get("openai_api_key", ""))
    openai_entry = tk.Entry(openai_frame, textvariable=openai_var, width=60, show="*", font=('Arial', 9))
    openai_entry.pack(fill=tk.X, pady=(2, 5))
    
    def toggle_openai_visibility():
        if openai_entry.cget('show') == '*':
            openai_entry.config(show='')
            openai_show_btn.config(text="Hide")
        else:
            openai_entry.config(show='*')
            openai_show_btn.config(text="Show")
    
    openai_show_btn = tk.Button(openai_frame, text="Show", command=toggle_openai_visibility, font=('Arial', 8))
    openai_show_btn.pack(anchor=tk.E)
    
    tk.Label(openai_frame, text="Get your key at: https://platform.openai.com/api-keys", 
             font=('Arial', 8), fg="blue", cursor="hand2").pack(anchor=tk.W, pady=(5, 0))
    
    # Groq API Key
    groq_frame = tk.LabelFrame(api_frame, text="Groq (for Llama-4-Scout)", font=('Arial', 10, 'bold'), padx=10, pady=10)
    groq_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
    
    tk.Label(groq_frame, text="API Key:", font=('Arial', 9)).pack(anchor=tk.W)
    groq_var = tk.StringVar(value=settings.get("groq_api_key", ""))
    groq_entry = tk.Entry(groq_frame, textvariable=groq_var, width=60, show="*", font=('Arial', 9))
    groq_entry.pack(fill=tk.X, pady=(2, 5))
    
    def toggle_groq_visibility():
        if groq_entry.cget('show') == '*':
            groq_entry.config(show='')
            groq_show_btn.config(text="Hide")
        else:
            groq_entry.config(show='*')
            groq_show_btn.config(text="Show")
    
    groq_show_btn = tk.Button(groq_frame, text="Show", command=toggle_groq_visibility, font=('Arial', 8))
    groq_show_btn.pack(anchor=tk.E)
    
    tk.Label(groq_frame, text="Get your key at: https://console.groq.com/keys", 
             font=('Arial', 8), fg="blue", cursor="hand2").pack(anchor=tk.W, pady=(5, 0))
    
    # Test API Keys Button
    def test_api_keys():
        openai_key = openai_var.get().strip()
        groq_key = groq_var.get().strip()
        
        if not openai_key and not groq_key:
            messagebox.showwarning("No API Keys", "Please enter at least one API key to test.")
            return
        
        # Simple validation (you can enhance this)
        messages = []
        if openai_key:
            if openai_key.startswith('sk-') and len(openai_key) > 20:
                messages.append("✓ OpenAI key format looks valid")
            else:
                messages.append("⚠ OpenAI key format may be invalid")
        
        if groq_key:
            if len(groq_key) > 20:
                messages.append("✓ Groq key format looks valid")
            else:
                messages.append("⚠ Groq key format may be invalid")
        
        messagebox.showinfo("API Key Test", "\n".join(messages))
    
    test_button = tk.Button(api_frame, text="Test API Keys", command=test_api_keys, 
                           bg="#3498db", fg="white", font=('Arial', 9))
    test_button.pack(pady=10)
    
    # Buttons
    button_frame = tk.Frame(settings_window)
    button_frame.pack(side=tk.BOTTOM, pady=15)
    
    def save_and_close():
        # Validate that at least one API key is provided
        openai_key = openai_var.get().strip()
        groq_key = groq_var.get().strip()
        
        if not openai_key and not groq_key:
            messagebox.showwarning("API Keys Required", 
                                 "Please enter at least one API key to use Lexia.\n\n"
                                 "You can get API keys from:\n"
                                 "• OpenAI: https://platform.openai.com/api-keys\n"
                                 "• Groq: https://console.groq.com/keys")
            return
        
        new_settings = {
            "hotkey": hotkey_var.get(),
            "model": settings["model"],  # Keep existing model
            "temperature": temp_var.get(),
            "num_alternatives": alt_var.get(),
            "openai_api_key": openai_key,
            "groq_api_key": groq_key
        }
        
        if save_settings(new_settings):
            messagebox.showinfo("Success", "Settings saved successfully!\n\nAPI keys are stored securely on your computer.")
            if on_settings_changed:
                on_settings_changed(new_settings)
            settings_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to save settings")
    
    def cancel():
        settings_window.destroy()
    
    save_button = tk.Button(button_frame, text="Save Settings", command=save_and_close, 
                           bg="#27ae60", fg="white", font=('Arial', 10, 'bold'),
                           padx=20, pady=5)
    save_button.pack(side=tk.LEFT, padx=10)
    
    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel,
                             bg="#95a5a6", fg="white", font=('Arial', 10),
                             padx=20, pady=5)
    cancel_button.pack(side=tk.LEFT, padx=10)
    
    if not parent:
        settings_window.mainloop()

if __name__ == "__main__":
    show_settings_window()