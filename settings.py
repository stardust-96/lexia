import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import threading
from settings_store import DEV_MODE, get_api_keys, keyring_available, load_settings, save_settings
from app_paths import apply_window_icon

def show_settings_window(parent=None, on_settings_changed=None):
    settings = load_settings()
    
    settings_window = tk.Toplevel(parent) if parent else tk.Tk()
    settings_window.title("Lexia Settings")
    apply_window_icon(settings_window)
    settings_window.geometry("560x560")
    settings_window.minsize(560, 560)
    settings_window.resizable(True, True)
    settings_window.grid_rowconfigure(0, weight=1)
    settings_window.grid_columnconfigure(0, weight=1)
    if parent:
        settings_window.transient(parent)
    settings_window.grab_set()
    settings_window.focus_force()
    
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
    model_var = tk.StringVar(value=settings.get("model", ""))
    model_options = [("gpt-4", "GPT (OpenAI)"), ("llama-4-scout", "Llama-4-Scout (Groq)")]
    model_labels = ["Select model"] + [label for _, label in model_options]
    model_dropdown = ttk.Combobox(
        model_frame,
        textvariable=model_var,
        values=model_labels,
        state='readonly',
        width=24
    )
    selected_label = next((label for value, label in model_options if value == model_var.get()), "Select model")
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
    if not keyring_available():
        tk.Label(
            api_content,
            text="Credential-store support is unavailable in this Python environment.\nInstall 'keyring' to save API keys.",
            font=('Arial', 9, 'bold'),
            fg="#c0392b",
            justify=tk.CENTER
        ).pack(pady=(0, 10))
    
    # OpenAI API Key
    openai_frame = tk.LabelFrame(api_content, text="OpenAI (for GPT)", font=('Arial', 10, 'bold'), padx=10, pady=10)
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
            messagebox.showwarning("No API Keys", "Please enter at least one API key to test.", parent=settings_window)
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
        
        messagebox.showinfo("API Key Test", "\n".join(messages), parent=settings_window)
    
    test_button = tk.Button(api_content, text="Test API Keys", command=test_api_keys, 
                           bg="#3498db", fg="white", font=('Arial', 9))
    test_button.pack(pady=10)
    
    # Buttons
    button_frame = tk.Frame(settings_window)
    button_frame.grid(row=1, column=0, pady=15, sticky="ew")
    status_var = tk.StringVar(value="")
    status_label = tk.Label(button_frame, textvariable=status_var, font=('Arial', 9), fg="gray")
    status_label.pack(side=tk.RIGHT, padx=10)
    
    def save_and_close():
        if not keyring_available():
            messagebox.showerror(
                "Credential Store Unavailable",
                "Cannot save API keys because keyring support is missing.\n\n"
                "Install dependency: pip install keyring",
                parent=settings_window
            )
            return

        # Validate that at least one API key is provided (except in dev mode)
        openai_key = openai_var.get().strip()
        groq_key = groq_var.get().strip()
        
        if not DEV_MODE and not openai_key and not groq_key:
            messagebox.showwarning("API Keys Required", 
                                 "Please enter at least one API key to use Lexia.\n\n"
                                 "You can get API keys from:\n"
                                 "• OpenAI: https://platform.openai.com/api-keys\n"
                                 "• Groq: https://console.groq.com/keys",
                                 parent=settings_window)
            return

        selected_model = next((value for value, label in model_options if label == model_dropdown.get()), "")
        if not DEV_MODE:
            if not selected_model:
                messagebox.showwarning(
                    "Default Model Required",
                    "Please select a default model after adding an API key.",
                    parent=settings_window
                )
                return
            if selected_model == "gpt-4" and not openai_key:
                messagebox.showwarning(
                    "Model Requires OpenAI Key",
                    "GPT is selected as default model, but no OpenAI API key is configured.",
                    parent=settings_window
                )
                return
            if selected_model == "llama-4-scout" and not groq_key:
                messagebox.showwarning(
                    "Model Requires Groq Key",
                    "Llama-4-Scout is selected as default model, but no Groq API key is configured.",
                    parent=settings_window
                )
                return
        
        new_settings = {
            "hotkey": hotkey_var.get(),
            "model": selected_model,
            "temperature": temp_var.get(),
            "num_alternatives": alt_var.get(),
            "openai_api_key": openai_key,
            "groq_api_key": groq_key,
            "onboarding_completed": settings.get("onboarding_completed", False),
            "tray_notice_shown": settings.get("tray_notice_shown", False),
        }
        
        save_button.config(state='disabled')
        cancel_button.config(state='disabled')
        test_button.config(state='disabled')
        status_var.set("Saving...")

        def worker():
            ok = save_settings(new_settings)

            def done():
                status_var.set("")
                save_button.config(state='normal')
                cancel_button.config(state='normal')
                test_button.config(state='normal')
                if ok:
                    messagebox.showinfo(
                        "Success",
                        "Settings saved successfully.\n\n"
                        "API keys are stored in your OS credential store.\n"
                        "Restart Lexia to apply hotkey changes.",
                        parent=settings_window
                    )
                    if on_settings_changed:
                        on_settings_changed(new_settings)
                    settings_window.destroy()
                else:
                    messagebox.showerror("Error", "Failed to save settings", parent=settings_window)

            settings_window.after(0, done)

        threading.Thread(target=worker, daemon=True).start()
    
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
