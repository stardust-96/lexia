import tkinter as tk
from tkinter import ttk, Menu, scrolledtext, messagebox
import pyperclip
import threading
import webbrowser
import json
import urllib.request
from rewriter import rewrite_text_with_gpt
from settings import show_settings_window, load_settings
from version import VERSION_INFO, get_version_string

selected_tone = "Neutral"
selected_alternative = 0
alternatives = []
selected_model = None
is_rewriting = False

# Application metadata
APP_VERSION = VERSION_INFO["version"]
APP_NAME = VERSION_INFO["name"]
AUTHOR = VERSION_INFO["author"]
GITHUB_URL = "https://github.com/stardust-96/lexia"
RELEASE_API_URL = "https://api.github.com/repos/stardust-96/lexia/releases/latest"

def show_about_dialog(parent):
    """Show the About dialog with application information."""
    about_window = tk.Toplevel(parent)
    about_window.title(f"About {APP_NAME}")
    about_window.geometry("480x480")
    about_window.resizable(False, False)
    about_window.transient(parent)
    about_window.grab_set()
    
    # Center the window
    about_window.update_idletasks()
    x = (about_window.winfo_screenwidth() // 2) - (480 // 2)
    y = (about_window.winfo_screenheight() // 2) - (480 // 2)
    about_window.geometry(f"480x480+{x}+{y}")
    
    # Main container with padding
    main_frame = tk.Frame(about_window, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
    
    # App icon/logo area
    logo_frame = tk.Frame(main_frame, bg="white")
    logo_frame.pack(fill=tk.X, pady=(10, 20))
    
    # App name with large font
    tk.Label(logo_frame, text="✨ " + APP_NAME, font=("Arial", 26, "bold"), 
             bg="white", fg="#2c3e50").pack(pady=(0, 5))
    tk.Label(logo_frame, text="Intelligent Text Rewriting Assistant", 
             font=("Arial", 11), bg="white", fg="#7f8c8d").pack()
    
    # Version and author info
    info_frame = tk.Frame(main_frame, bg="white")
    info_frame.pack(fill=tk.X, pady=(0, 15))
    
    tk.Label(info_frame, text=get_version_string(), 
             font=("Arial", 12, "bold"), bg="white", fg="#34495e").pack(pady=2)
    
    tk.Label(info_frame, text=f"Created by {AUTHOR}", 
             font=("Arial", 10), bg="white", fg="#34495e").pack(pady=2)
    
    # Description with better spacing
    desc_frame = tk.Frame(main_frame, bg="white")
    desc_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
    
    desc_text = ("A powerful desktop application that provides intelligent "
                "text rewriting with customizable styles and multiple AI models.")
    tk.Label(desc_frame, text=desc_text, font=("Arial", 10), bg="white", 
             fg="#555", wraplength=400, justify=tk.CENTER).pack()
    
    # Buttons frame with spacing
    button_frame = tk.Frame(main_frame, bg="white")
    button_frame.pack(fill=tk.X, pady=(20, 0))
    
    # Check for updates button
    def check_updates():
        update_btn.config(text="Checking...", state="disabled")
        
        def check():
            try:
                # Simple version check against GitHub releases
                with urllib.request.urlopen(RELEASE_API_URL, timeout=5) as response:
                    data = json.loads(response.read())
                    latest_version = data.get("tag_name", "").lstrip("v")
                    
                    if latest_version and latest_version != APP_VERSION:
                        result = messagebox.askyesno(
                            "Update Available",
                            f"A new version ({latest_version}) is available!\n\n"
                            f"Current version: {APP_VERSION}\n\n"
                            "Would you like to visit the download page?",
                            parent=about_window
                        )
                        if result:
                            webbrowser.open(GITHUB_URL + "/releases/latest")
                    else:
                        messagebox.showinfo(
                            "No Updates",
                            f"{APP_NAME} is up to date!",
                            parent=about_window
                        )
            except Exception as e:
                messagebox.showerror(
                    "Update Check Failed",
                    f"Could not check for updates:\n{str(e)}",
                    parent=about_window
                )
            finally:
                update_btn.config(text="Check for Updates", state="normal")
        
        # Run in thread to avoid blocking UI
        threading.Thread(target=check, daemon=True).start()
    
    update_btn = tk.Button(button_frame, text="Check for Updates", 
                          command=check_updates, bg="#3498db", fg="white",
                          font=("Arial", 10), padx=20, pady=8, cursor="hand2",
                          relief=tk.RAISED, bd=2)
    update_btn.pack(pady=(10, 8))
    
    # GitHub link
    github_link = tk.Label(button_frame, text="View on GitHub", 
                          font=("Arial", 10, "underline"), bg="white", 
                          fg="#3498db", cursor="hand2")
    github_link.pack(pady=5)
    github_link.bind("<Button-1>", lambda e: webbrowser.open(GITHUB_URL))
    
    # Close button
    tk.Button(button_frame, text="Close", command=about_window.destroy,
             bg="#95a5a6", fg="white", font=("Arial", 10), 
             padx=35, pady=8, relief=tk.RAISED, bd=2).pack(pady=5)

def show_popup(original: str):
    def start_rewrite():
        global is_rewriting
        if is_rewriting:
            return  # Prevent multiple simultaneous rewrites
        
        is_rewriting = True
        effective_tone = get_effective_tone()
        loading_label.config(text=f"⏳ Rewriting in {effective_tone} tone...")
        submit_button.config(state='disabled')
        for widget in alternative_frame.winfo_children():
            widget.destroy()

        def process():
            global alternatives, selected_alternative
            
            # Show loading animation
            loading_label.config(text="⏳ Rewriting with " + model_var.get() + "...", fg="#0066cc")
            popup.update()
            
            # Override model for this rewrite
            import json
            temp_settings = load_settings()
            temp_settings['model'] = model_var.get()
            
            alternatives = rewrite_text_with_gpt(original, effective_tone, model_override=model_var.get())
            selected_alternative = 0
            
            print(f"Generated {len(alternatives)} alternatives")  # Debug
            
            for widget in alternative_frame.winfo_children():
                widget.destroy()
            
            radio_var.set(0)
            for i, alt in enumerate(alternatives):
                radio = tk.Radiobutton(alternative_frame, text=f"v{i+1}", 
                                     variable=radio_var, value=i, 
                                     command=lambda idx=i: update_alternative(idx),
                                     bg="white", font=("Arial", 10, "bold"), relief="raised", bd=2,
                                     padx=8, pady=4, selectcolor="#3498db")
                radio.pack(side=tk.LEFT, padx=3)
            
            update_alternative(0)
            
            loading_label.config(text="✅ Rewriting complete. Select an alternative:", fg="#009900")
            copy_button.config(state='normal')
            submit_button.config(state='normal')
            
            global is_rewriting
            is_rewriting = False  # Reset the flag

        threading.Thread(target=process).start()

    def update_alternative(idx):
        global selected_alternative
        selected_alternative = idx
        rewritten_box.config(state='normal')
        rewritten_box.delete("1.0", tk.END)
        rewritten_box.insert(tk.END, alternatives[idx])
        rewritten_box.config(state='normal')
        
        # Adjust height based on content - more aggressive sizing
        content = alternatives[idx]
        
        # Simple but effective line calculation
        char_count = len(content)
        estimated_lines = max(4, char_count // 60)  # Roughly 60 chars per line
        line_breaks = content.count('\n')
        total_lines = estimated_lines + line_breaks
        
        # Set height with generous range for better visibility
        new_height = max(12, min(25, total_lines + 3))  # Between 12-25 lines, +3 for padding
        rewritten_box.config(height=new_height)
        
        # Force layout update
        rewritten_box.update_idletasks()
    
    def copy_to_clipboard():
        text = rewritten_box.get("1.0", tk.END).strip()
        pyperclip.copy(text)
        popup.destroy()

    def get_effective_tone():
        # Get custom tone, but ignore placeholder text
        custom_tone = custom_tone_var.get().strip()
        if custom_tone and custom_tone != placeholder_text:
            return custom_tone
        else:
            return tone_var.get() if tone_var.get() != "Custom" else "Neutral"
    
    def update_tone(event):
        global selected_tone
        selected_tone = get_effective_tone()
        start_rewrite()  # re-run GPT with new tone
    
    def on_custom_tone_enter(event):
        global selected_tone
        selected_tone = get_effective_tone()
        # Only rewrite when user presses Enter
        if selected_tone.strip():  # Only if there's actual content
            start_rewrite()

    # Create enhanced styled window
    popup = tk.Tk()
    popup.title("Lexia - Text Enhancement")
    popup.geometry("900x800")
    popup.resizable(False, False)
    popup.configure(bg="#f5f5f5")
    
    # Custom style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Card.TLabelframe', background='#ffffff', relief='raised', borderwidth=2)
    style.configure('Card.TLabelframe.Label', background='#ffffff', font=('Arial', 10, 'bold'))
    style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
    style.configure('Success.TButton', font=('Arial', 10, 'bold'))
    style.configure('Danger.TButton', font=('Arial', 10, 'bold'))
    
    # Ensure window appears on top and not minimized
    popup.lift()
    popup.attributes('-topmost', True)
    popup.after(100, lambda: popup.attributes('-topmost', False))
    popup.focus_force()
    
    # Add menu bar
    menubar = Menu(popup)
    popup.config(menu=menubar)
    
    # File menu
    file_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Settings", command=lambda: show_settings_window(popup, update_model_settings))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=popup.destroy)
    
    # Help menu
    help_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=lambda: show_about_dialog(popup))
    
    settings = load_settings()
    model_display = "GPT-4 (OpenAI)" if settings['model'] == "gpt-4" else "Llama-4-Scout (Groq)"
    help_menu.add_command(label=f"Model: {model_display}", state='disabled')
    help_menu.add_command(label=f"Temperature: {settings['temperature']}", state='disabled')
    help_menu.add_command(label=f"Alternatives: {settings['num_alternatives']}", state='disabled')
    
    def update_model_settings(new_settings):
        # Update help menu with new settings
        model_display = "GPT-4 (OpenAI)" if new_settings['model'] == "gpt-4" else "Llama-4-Scout (Groq)"
        help_menu.entryconfig(0, label=f"Model: {model_display}")
        help_menu.entryconfig(1, label=f"Temperature: {new_settings['temperature']}")
        help_menu.entryconfig(2, label=f"Alternatives: {new_settings['num_alternatives']}")

    # Header
    header_frame = tk.Frame(popup, bg="#2c3e50", height=60)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)
    
    title_label = tk.Label(header_frame, text="✨ Lexia", 
                          font=("Arial", 16, "bold"), fg="white", bg="#2c3e50")
    title_label.pack(expand=True)

    # Model and Tone selection frame with cards
    selection_frame = tk.Frame(popup, bg="#f5f5f5")
    selection_frame.pack(fill=tk.X, padx=15, pady=15)
    
    # Model selection card
    model_card = ttk.LabelFrame(selection_frame, text="🚀 Model Selection", style='Card.TLabelframe', padding=15)
    model_card.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
    
    model_var = tk.StringVar(value=settings.get('model', 'llama-4-scout'))
    model_options = [("gpt-4", "GPT-4 (OpenAI)"), ("llama-4-scout", "Llama-4-Scout (Groq)")]
    
    def on_model_change():
        # Only trigger rewrite if not currently rewriting
        if not is_rewriting:
            start_rewrite()
    
    for value, display in model_options:
        rb = tk.Radiobutton(model_card, text=display, variable=model_var, 
                           value=value, command=on_model_change,
                           font=("Arial", 10), bg="white", relief="groove", bd=1)
        rb.pack(pady=5, anchor=tk.W, fill=tk.X)
    
    # Style and instructions card
    tone_card = ttk.LabelFrame(selection_frame, text="🎨 Style & Instructions", style='Card.TLabelframe', padding=15)
    tone_card.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
    
    tk.Label(tone_card, text="Preset Styles:", font=("Arial", 9), bg="white").pack(anchor=tk.W, pady=(0, 2))
    tone_var = tk.StringVar(value="Neutral")
    tone_options = ["Neutral", "Formal", "Friendly", "Professional", "Concise", "Creative", "Custom"]
    tone_dropdown = ttk.Combobox(tone_card, textvariable=tone_var, values=tone_options, 
                                state='readonly', width=20, font=("Arial", 10))
    tone_dropdown.current(0)
    tone_dropdown.bind("<<ComboboxSelected>>", update_tone)
    tone_dropdown.pack(pady=(0, 5), fill=tk.X)
    
    # Custom instructions text box
    tk.Label(tone_card, text="Custom Instructions:", font=("Arial", 9), bg="white").pack(anchor=tk.W, pady=(10, 2))
    custom_tone_var = tk.StringVar()
    custom_tone_entry = tk.Entry(tone_card, textvariable=custom_tone_var, font=("Arial", 10),
                                relief="sunken", bd=2)
    custom_tone_entry.pack(fill=tk.X, pady=(0, 5))
    custom_tone_entry.bind("<Return>", on_custom_tone_enter)
    
    # Add placeholder functionality
    placeholder_text = "e.g., 'in one line', 'as bullet points', 'more casual'... (Press Enter to apply)"
    
    def on_focus_in(event):
        if custom_tone_entry.get() == placeholder_text:
            custom_tone_entry.delete(0, tk.END)
            custom_tone_entry.config(fg='black')
    
    def on_focus_out(event):
        if not custom_tone_entry.get():
            custom_tone_entry.insert(0, placeholder_text)
            custom_tone_entry.config(fg='gray')
    
    # Set initial placeholder
    custom_tone_entry.insert(0, placeholder_text)
    custom_tone_entry.config(fg='gray')
    custom_tone_entry.bind("<FocusIn>", on_focus_in)
    custom_tone_entry.bind("<FocusOut>", on_focus_out)

    # Status and buttons at the bottom - create first to reserve space
    bottom_frame = tk.Frame(popup, bg="#f5f5f5", height=100)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=15, pady=15)
    bottom_frame.pack_propagate(False)  # Prevent shrinking
    
    loading_label = tk.Label(bottom_frame, text="Ready to rewrite", font=('Arial', 11, 'bold'), 
                           fg="#666666", bg="#f5f5f5")
    loading_label.pack(pady=(5, 10))

    button_frame = tk.Frame(bottom_frame, bg="#f5f5f5")
    button_frame.pack()

    # Enhanced styled buttons
    submit_button = tk.Button(button_frame, text="🔄 Rewrite", command=start_rewrite, 
                             bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                             relief="raised", bd=2, padx=20, pady=8)
    submit_button.pack(side=tk.LEFT, padx=5)

    copy_button = tk.Button(button_frame, text="📋 Copy & Close", command=copy_to_clipboard, 
                           state='disabled', bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
                           relief="raised", bd=2, padx=20, pady=8)
    copy_button.pack(side=tk.LEFT, padx=5)


    cancel_button = tk.Button(button_frame, text="❌ Cancel", command=popup.destroy, 
                             bg="#e74c3c", fg="white", font=("Arial", 11, "bold"),
                             relief="raised", bd=2, padx=20, pady=8)
    cancel_button.pack(side=tk.LEFT, padx=5)

    # Main content frame - now pack after bottom frame
    content_frame = tk.Frame(popup, bg="#f5f5f5")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=15)
    
    # Original text section
    orig_header = tk.Frame(content_frame, bg="#f5f5f5")
    orig_header.pack(fill=tk.X, pady=(0, 5))
    tk.Label(orig_header, text="📝 Original Text", font=('Arial', 10, 'bold'), bg="#f5f5f5").pack(side=tk.LEFT)
    
    # Calculate height based on text length - keep original text compact
    orig_lines = len(original.split('\n')) + (len(original) // 80)  # Estimate wrapped lines
    orig_height = max(2, min(4, orig_lines))  # Between 2-4 lines
    
    original_box = scrolledtext.ScrolledText(content_frame, height=orig_height, font=("Arial", 10), 
                                           wrap=tk.WORD, bg="white", relief="solid", bd=1)
    original_box.insert(tk.END, original)
    original_box.config(state='disabled')
    original_box.pack(fill=tk.X, pady=(0, 15))

    # Rewritten text section with inline buttons
    rewrite_header = tk.Frame(content_frame, bg="#f5f5f5")
    rewrite_header.pack(fill=tk.X, pady=(0, 5))
    
    tk.Label(rewrite_header, text="✨ Rewritten Text", font=('Arial', 10, 'bold'), bg="#f5f5f5").pack(side=tk.LEFT)
    
    alternative_frame = tk.Frame(rewrite_header, bg="#f5f5f5")
    radio_var = tk.IntVar(value=0)
    alternative_frame.pack(side=tk.RIGHT)
    
    rewritten_box = scrolledtext.ScrolledText(content_frame, height=20, font=("Arial", 10),
                                            wrap=tk.WORD, bg="white", relief="solid", bd=1)
    rewritten_box.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

    # Buttons are now created above in the proper order

    start_rewrite()
    popup.mainloop()