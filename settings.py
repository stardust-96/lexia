import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import base64
import binascii
import webbrowser

try:
    import keyring
except ImportError:
    keyring = None

SETTINGS_FILE = "settings.json"
KEYRING_SERVICE = "Lexia"
DEFAULT_SETTINGS = {
    "hotkey": "ctrl+shift+r",
    "model": "gpt-4",
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

def _decode_legacy_key(value):
    """Decode a legacy base64 value if possible, otherwise return the original value."""
    if not value:
        return ""
    try:
        decoded = base64.b64decode(value.encode(), validate=True).decode()
        return decoded
    except (binascii.Error, UnicodeDecodeError):
        return value

def _get_key_from_keyring(name):
    if keyring is None:
        return ""
    try:
        return keyring.get_password(KEYRING_SERVICE, name) or ""
    except Exception:
        return ""

def _set_key_in_keyring(name, value):
    if keyring is None:
        return False
    try:
        if value:
            keyring.set_password(KEYRING_SERVICE, name, value)
        else:
            try:
                keyring.delete_password(KEYRING_SERVICE, name)
            except Exception:
                pass
        return True
    except Exception:
        return False

def save_settings(settings):
    try:
        settings_to_save = settings.copy()

        # Save API keys in OS keychain, not in settings.json
        openai_key = settings_to_save.pop("openai_api_key", None)
        groq_key = settings_to_save.pop("groq_api_key", None)

        if openai_key is not None and not _set_key_in_keyring("openai_api_key", openai_key):
            print("Error saving OpenAI API key to keychain")
            return False
        if groq_key is not None and not _set_key_in_keyring("groq_api_key", groq_key):
            print("Error saving Groq API key to keychain")
            return False
            
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

            # One-time migration: move legacy keys from settings.json to keychain
            migrated = False
            legacy_openai = settings.pop("openai_api_key", None)
            legacy_groq = settings.pop("groq_api_key", None)
            if legacy_openai is not None:
                decoded = _decode_legacy_key(legacy_openai)
                _set_key_in_keyring("openai_api_key", decoded)
                migrated = True
            if legacy_groq is not None:
                decoded = _decode_legacy_key(legacy_groq)
                _set_key_in_keyring("groq_api_key", decoded)
                migrated = True
            if migrated:
                with open(SETTINGS_FILE, 'w') as f:
                    json.dump(settings, f, indent=2)
                
            # Ensure all default keys exist
            for key, value in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = value

            # Populate UI fields from keychain
            settings["openai_api_key"] = _get_key_from_keyring("openai_api_key")
            settings["groq_api_key"] = _get_key_from_keyring("groq_api_key")
                    
            return settings
        except:
            return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def get_api_keys():
    """Get API keys from settings"""
    return {
        "openai": _get_key_from_keyring("openai_api_key"),
        "groq": _get_key_from_keyring("groq_api_key")
    }

def show_settings_window(parent=None, on_settings_changed=None):
    settings = load_settings()
    
    settings_window = tk.Toplevel(parent) if parent else tk.Tk()
    settings_window.title("Lexia Settings")
    settings_window.geometry("560x560")
    settings_window.minsize(560, 560)
    settings_window.resizable(True, True)
    settings_window.grid_rowconfigure(0, weight=1)
    settings_window.grid_columnconfigure(0, weight=1)
    
    # Create notebook for tabs
    notebook = ttk.Notebook(settings_window)
    notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))
    
    # General Settings Tab
    general_frame = ttk.Frame(notebook)
    notebook.add(general_frame, text="General")
    
    # API Keys Tab
    api_frame = ttk.Frame(notebook)
    notebook.add(api_frame, text="API Keys")
    api_frame.grid_rowconfigure(0, weight=1)
    api_frame.grid_columnconfigure(0, weight=1)

    api_canvas = tk.Canvas(api_frame, highlightthickness=0)
    api_scrollbar = ttk.Scrollbar(api_frame, orient="vertical", command=api_canvas.yview)
    api_content = ttk.Frame(api_canvas)

    api_content.bind(
        "<Configure>",
        lambda e: api_canvas.configure(scrollregion=api_canvas.bbox("all"))
    )
    api_canvas.bind(
        "<Configure>",
        lambda e: api_canvas.itemconfigure("api_content_window", width=e.width)
    )
    api_canvas.create_window((0, 0), window=api_content, anchor="nw", tags="api_content_window")
    api_canvas.configure(yscrollcommand=api_scrollbar.set)

    api_canvas.grid(row=0, column=0, sticky="nsew")
    api_scrollbar.grid(row=0, column=1, sticky="ns")
    
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

    # Default model
    model_frame = tk.Frame(general_frame)
    model_frame.pack(pady=5)

    tk.Label(model_frame, text="Default Model:").pack(side=tk.LEFT, padx=5)
    model_var = tk.StringVar(value=settings.get("model", "gpt-4"))
    model_options = [("gpt-4", "GPT-4 (OpenAI)"), ("llama-4-scout", "Llama-4-Scout (Groq)")]
    model_dropdown = ttk.Combobox(
        model_frame,
        textvariable=model_var,
        values=[label for _, label in model_options],
        state='readonly',
        width=24
    )
    selected_label = next((label for value, label in model_options if value == model_var.get()), "GPT-4 (OpenAI)")
    model_dropdown.set(selected_label)
    model_dropdown.pack(side=tk.LEFT, padx=5)
    
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
    tk.Label(api_content, text="API Configuration", font=('Arial', 14, 'bold')).pack(pady=(15, 10))
    
    # Description
    desc_text = ("Enter your API keys below. Keys are stored in your OS credential store.\n"
                "You only need one API key to use Lexia.")
    tk.Label(
        api_content,
        text=desc_text,
        font=('Arial', 9),
        fg="gray",
        justify=tk.CENTER,
        wraplength=500
    ).pack(pady=(0, 15), padx=10)
    if keyring is None:
        tk.Label(
            api_content,
            text="Credential-store support is unavailable in this Python environment.\nInstall 'keyring' to save API keys.",
            font=('Arial', 9, 'bold'),
            fg="#c0392b",
            justify=tk.CENTER
        ).pack(pady=(0, 10))
    
    # OpenAI API Key
    openai_frame = tk.LabelFrame(api_content, text="OpenAI (for GPT-4)", font=('Arial', 10, 'bold'), padx=10, pady=10)
    openai_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
    
    tk.Label(openai_frame, text="API Key:", font=('Arial', 9)).pack(anchor=tk.W)
    openai_key_row = tk.Frame(openai_frame)
    openai_key_row.pack(fill=tk.X, pady=(2, 5))
    openai_var = tk.StringVar(value=settings.get("openai_api_key", ""))
    openai_entry = tk.Entry(openai_key_row, textvariable=openai_var, show="*", font=('Arial', 9))
    openai_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
    
    def toggle_openai_visibility():
        if openai_entry.cget('show') == '*':
            openai_entry.config(show='')
            openai_show_btn.config(text="Hide")
        else:
            openai_entry.config(show='*')
            openai_show_btn.config(text="Show")
    
    openai_show_btn = tk.Button(openai_key_row, text="Show", command=toggle_openai_visibility, font=('Arial', 8), width=6)
    openai_show_btn.pack(side=tk.RIGHT)
    
    openai_link = tk.Label(
        openai_frame,
        text="Get your key at: https://platform.openai.com/api-keys",
        font=('Arial', 8, 'underline'),
        fg="blue",
        cursor="hand2"
    )
    openai_link.pack(anchor=tk.W, pady=(5, 0))
    openai_link.bind("<Button-1>", lambda e: webbrowser.open("https://platform.openai.com/api-keys"))
    
    # Groq API Key
    groq_frame = tk.LabelFrame(api_content, text="Groq (for Llama-4-Scout)", font=('Arial', 10, 'bold'), padx=10, pady=10)
    groq_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
    
    tk.Label(groq_frame, text="API Key:", font=('Arial', 9)).pack(anchor=tk.W)
    groq_key_row = tk.Frame(groq_frame)
    groq_key_row.pack(fill=tk.X, pady=(2, 5))
    groq_var = tk.StringVar(value=settings.get("groq_api_key", ""))
    groq_entry = tk.Entry(groq_key_row, textvariable=groq_var, show="*", font=('Arial', 9))
    groq_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
    
    def toggle_groq_visibility():
        if groq_entry.cget('show') == '*':
            groq_entry.config(show='')
            groq_show_btn.config(text="Hide")
        else:
            groq_entry.config(show='*')
            groq_show_btn.config(text="Show")
    
    groq_show_btn = tk.Button(groq_key_row, text="Show", command=toggle_groq_visibility, font=('Arial', 8), width=6)
    groq_show_btn.pack(side=tk.RIGHT)
    
    groq_link = tk.Label(
        groq_frame,
        text="Get your key at: https://console.groq.com/keys",
        font=('Arial', 8, 'underline'),
        fg="blue",
        cursor="hand2"
    )
    groq_link.pack(anchor=tk.W, pady=(5, 0))
    groq_link.bind("<Button-1>", lambda e: webbrowser.open("https://console.groq.com/keys"))
    
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
    
    test_button = tk.Button(api_content, text="Test API Keys", command=test_api_keys, 
                           bg="#3498db", fg="white", font=('Arial', 9))
    test_button.pack(pady=10)
    
    # Buttons
    button_frame = tk.Frame(settings_window)
    button_frame.grid(row=1, column=0, pady=15, sticky="ew")
    
    def save_and_close():
        if keyring is None:
            messagebox.showerror(
                "Credential Store Unavailable",
                "Cannot save API keys because keyring support is missing.\n\n"
                "Install dependency: pip install keyring"
            )
            return

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
            "model": next((value for value, label in model_options if label == model_dropdown.get()), "gpt-4"),
            "temperature": temp_var.get(),
            "num_alternatives": alt_var.get(),
            "openai_api_key": openai_key,
            "groq_api_key": groq_key
        }
        
        if save_settings(new_settings):
            messagebox.showinfo("Success", "Settings saved successfully!\n\nAPI keys are stored in your OS credential store.")
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
    return settings_window

if __name__ == "__main__":
    show_settings_window()
