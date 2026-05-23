import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

from settings_store import (
    DEV_MODE,
    keyring_available,
    load_settings,
    save_settings,
    validate_onboarding_state,
)
from app_paths import apply_window_icon


def run_onboarding_wizard(parent=None):
    if DEV_MODE:
        return True

    settings = load_settings()
    result = {"completed": False}

    wizard = tk.Toplevel(parent) if parent else tk.Tk()
    wizard.title("Lexia Setup Wizard")
    apply_window_icon(wizard)
    wizard.geometry("700x560")
    wizard.minsize(620, 500)
    wizard.resizable(True, True)
    wizard.protocol("WM_DELETE_WINDOW", lambda: None)
    wizard.grid_rowconfigure(0, weight=1)
    wizard.grid_columnconfigure(0, weight=1)

    container = tk.Frame(wizard, padx=16, pady=16)
    container.grid(row=0, column=0, sticky="nsew")
    container.grid_rowconfigure(2, weight=1)
    container.grid_columnconfigure(0, weight=1)

    title_label = tk.Label(container, text="Welcome to Lexia", font=("Arial", 16, "bold"))
    title_label.grid(row=0, column=0, sticky="w", pady=(0, 8))

    body_label = tk.Label(container, text="", justify=tk.LEFT, wraplength=560, font=("Arial", 10))
    body_label.grid(row=1, column=0, sticky="ew")

    content_holder = tk.Frame(container)
    content_holder.grid(row=2, column=0, sticky="nsew", pady=(12, 0))
    content_holder.grid_rowconfigure(0, weight=1)
    content_holder.grid_columnconfigure(0, weight=1)

    form_canvas = tk.Canvas(content_holder, highlightthickness=0)
    form_scrollbar = ttk.Scrollbar(content_holder, orient="vertical", command=form_canvas.yview)
    form_frame = tk.Frame(form_canvas)

    form_frame.bind(
        "<Configure>",
        lambda e: form_canvas.configure(scrollregion=form_canvas.bbox("all"))
    )
    form_canvas.bind(
        "<Configure>",
        lambda e: form_canvas.itemconfigure("form_window", width=e.width)
    )
    form_canvas.create_window((0, 0), window=form_frame, anchor="nw", tags="form_window")
    form_canvas.configure(yscrollcommand=form_scrollbar.set)

    form_canvas.grid(row=0, column=0, sticky="nsew")
    form_scrollbar.grid(row=0, column=1, sticky="ns")

    button_row = tk.Frame(container)
    button_row.grid(row=3, column=0, sticky="ew", pady=(12, 0))

    back_btn = tk.Button(button_row, text="Back", width=10)
    back_btn.pack(side=tk.LEFT)

    cancel_btn = tk.Button(button_row, text="Exit Setup", width=12)
    cancel_btn.pack(side=tk.LEFT, padx=(8, 0))

    next_btn = tk.Button(button_row, text="Next", width=10, bg="#3498db", fg="white")
    next_btn.pack(side=tk.RIGHT)

    step = {"index": 0}
    openai_var = tk.StringVar(value=settings.get("openai_api_key", ""))
    groq_var = tk.StringVar(value=settings.get("groq_api_key", ""))
    model_var = tk.StringVar(value=settings.get("model", ""))

    def clear_form():
        for child in form_frame.winfo_children():
            child.destroy()
        form_canvas.yview_moveto(0.0)

    def key_presence():
        return {"openai": openai_var.get().strip(), "groq": groq_var.get().strip()}

    def is_valid_state():
        local_settings = {"model": model_var.get().strip()}
        valid, msg = validate_onboarding_state(local_settings, key_presence())
        return valid, msg

    def update_buttons():
        back_btn.config(state="normal" if step["index"] > 0 else "disabled")
        next_btn.config(text="Finish" if step["index"] == 3 else "Next")

    def render_welcome():
        title_label.config(text="Welcome to Lexia")
        body_label.config(
            text=(
                "This setup will configure your API keys and default model.\n"
                "You must complete setup before Lexia starts."
            )
        )

    def render_keys():
        title_label.config(text="Step 1: API Keys")
        body_label.config(text="Add at least one API key.")

        if not keyring_available():
            tk.Label(
                form_frame,
                text="Credential store (keyring) is unavailable. Setup cannot continue.",
                fg="#b00020",
                font=("Arial", 10, "bold"),
            ).pack(anchor=tk.W, pady=(0, 10))

        openai_frame = tk.LabelFrame(form_frame, text="OpenAI", padx=10, pady=10)
        openai_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(openai_frame, text="API Key:").pack(anchor=tk.W)
        tk.Entry(openai_frame, textvariable=openai_var, show="*").pack(fill=tk.X, pady=(4, 4))
        openai_link = tk.Label(openai_frame, text="https://platform.openai.com/api-keys", fg="blue", cursor="hand2")
        openai_link.pack(anchor=tk.W)
        openai_link.bind("<Button-1>", lambda e: webbrowser.open("https://platform.openai.com/api-keys"))

        groq_frame = tk.LabelFrame(form_frame, text="Groq", padx=10, pady=10)
        groq_frame.pack(fill=tk.X)
        tk.Label(groq_frame, text="API Key:").pack(anchor=tk.W)
        tk.Entry(groq_frame, textvariable=groq_var, show="*").pack(fill=tk.X, pady=(4, 4))
        groq_link = tk.Label(groq_frame, text="https://console.groq.com/keys", fg="blue", cursor="hand2")
        groq_link.pack(anchor=tk.W)
        groq_link.bind("<Button-1>", lambda e: webbrowser.open("https://console.groq.com/keys"))

    def render_model():
        title_label.config(text="Step 2: Default Model")
        body_label.config(text="Choose the default model. Only models with configured keys are enabled.")

        keys = key_presence()
        openai_ok = bool(keys["openai"])
        groq_ok = bool(keys["groq"])

        model_box = tk.LabelFrame(form_frame, text="Model", padx=10, pady=10)
        model_box.pack(fill=tk.X)

        rb_openai = tk.Radiobutton(
            model_box,
            text="GPT (OpenAI)",
            variable=model_var,
            value="gpt-4",
            state="normal" if openai_ok else "disabled",
        )
        rb_openai.pack(anchor=tk.W, pady=2)

        rb_groq = tk.Radiobutton(
            model_box,
            text="Llama-4-Scout (Groq)",
            variable=model_var,
            value="llama-4-scout",
            state="normal" if groq_ok else "disabled",
        )
        rb_groq.pack(anchor=tk.W, pady=2)

        if not model_var.get():
            if openai_ok:
                model_var.set("gpt-4")
            elif groq_ok:
                model_var.set("llama-4-scout")

    def render_review():
        title_label.config(text="Step 3: Review")
        keys = key_presence()
        key_summary = []
        if keys["openai"]:
            key_summary.append("OpenAI key: configured")
        if keys["groq"]:
            key_summary.append("Groq key: configured")

        if model_var.get() == "gpt-4":
            model_name = "GPT (OpenAI)"
        elif model_var.get() == "llama-4-scout":
            model_name = "Llama-4-Scout (Groq)"
        else:
            model_name = "Not selected"

        body_label.config(
            text=(
                "Review your setup before finishing:\n\n"
                + "\n".join(key_summary if key_summary else ["No keys configured"])
                + f"\nDefault model: {model_name}"
            )
        )

    def render():
        clear_form()
        if step["index"] == 0:
            render_welcome()
        elif step["index"] == 1:
            render_keys()
        elif step["index"] == 2:
            render_model()
        else:
            render_review()
        update_buttons()

    def do_finish():
        valid, msg = is_valid_state()
        if not keyring_available():
            messagebox.showerror("Credential Store Unavailable", "Setup cannot continue without keyring support.")
            return
        if not valid:
            messagebox.showwarning("Setup Incomplete", msg)
            return

        payload = {
            "hotkey": settings.get("hotkey", "ctrl+shift+r"),
            "model": model_var.get().strip(),
            "temperature": settings.get("temperature", 0.7),
            "num_alternatives": settings.get("num_alternatives", 3),
            "openai_api_key": openai_var.get().strip(),
            "groq_api_key": groq_var.get().strip(),
            "onboarding_completed": True,
            "tray_notice_shown": settings.get("tray_notice_shown", False),
        }
        if not save_settings(payload):
            messagebox.showerror("Save Failed", "Could not save onboarding settings.")
            return
        result["completed"] = True
        wizard.destroy()

    def on_next():
        if step["index"] == 0:
            step["index"] = 1
        elif step["index"] == 1:
            if not keyring_available():
                messagebox.showerror(
                    "Credential Store Unavailable",
                    "Lexia cannot complete setup without keyring support.\n\n"
                    "Install dependency: pip install keyring\n"
                    "Then restart setup."
                )
                return
            if not openai_var.get().strip() and not groq_var.get().strip():
                messagebox.showwarning("API Key Required", "Add at least one API key to continue.")
                return
            step["index"] = 2
        elif step["index"] == 2:
            valid, msg = is_valid_state()
            if not valid:
                messagebox.showwarning("Setup Incomplete", msg)
                return
            step["index"] = 3
        else:
            do_finish()
            return
        render()

    def on_back():
        if step["index"] > 0:
            step["index"] -= 1
            render()

    def on_cancel():
        if messagebox.askyesno("Exit Setup", "Lexia setup is not complete. Exit now?"):
            result["completed"] = False
            wizard.destroy()

    back_btn.config(command=on_back)
    next_btn.config(command=on_next)
    cancel_btn.config(command=on_cancel)

    render()
    if not parent:
        wizard.mainloop()
    else:
        wizard.wait_window()
    return result["completed"]
