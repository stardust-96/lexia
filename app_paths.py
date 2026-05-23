import os
import sys


def get_icon_path():
    candidates = []

    if getattr(sys, "frozen", False):
        candidates.append(os.path.join(os.path.dirname(sys.executable), "lexia.ico"))

    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates.append(os.path.join(meipass, "lexia.ico"))

    candidates.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lexia.ico"))
    candidates.append(os.path.abspath("lexia.ico"))

    for path in candidates:
        if os.path.exists(path):
            return path
    return None


def apply_window_icon(window):
    icon_path = get_icon_path()
    if not icon_path:
        return
    try:
        window.iconbitmap(icon_path)
    except Exception:
        pass

