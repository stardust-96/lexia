import binascii
import json
import os
from pathlib import Path

try:
    import keyring
except ImportError:
    keyring = None

KEYRING_SERVICE = "Lexia"
DEV_MODE = os.getenv("LEXIA_DEV_MODE", "0") == "1"

DEFAULT_SETTINGS = {
    "hotkey": "ctrl+shift+r",
    "model": "",
    "temperature": 0.7,
    "num_alternatives": 3,
    "onboarding_completed": False,
    "tray_notice_shown": False,
}


def _get_runtime_data_dir():
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data:
        runtime_dir = Path(local_app_data) / "Lexia"
    else:
        runtime_dir = Path.home() / ".lexia"
    runtime_dir.mkdir(parents=True, exist_ok=True)
    return runtime_dir


SETTINGS_FILE = _get_runtime_data_dir() / "settings.json"
LEGACY_SETTINGS_FILE = Path("settings.json")


def _decode_legacy_key(value):
    if not value:
        return ""
    try:
        import base64

        return base64.b64decode(value.encode(), validate=True).decode()
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


def _pick_first_available_model(openai_key, groq_key):
    if openai_key:
        return "gpt-4"
    if groq_key:
        return "llama-4-scout"
    return ""


def _normalize_model(settings, openai_key, groq_key):
    model = settings.get("model", "")
    has_openai = bool(openai_key)
    has_groq = bool(groq_key)

    if not has_openai and not has_groq:
        settings["model"] = ""
        return

    if not model:
        settings["model"] = _pick_first_available_model(openai_key, groq_key)
        return

    if model == "gpt-4" and not has_openai:
        settings["model"] = _pick_first_available_model(openai_key, groq_key)
    elif model == "llama-4-scout" and not has_groq:
        settings["model"] = _pick_first_available_model(openai_key, groq_key)
    elif model not in ("gpt-4", "llama-4-scout"):
        settings["model"] = _pick_first_available_model(openai_key, groq_key)


def validate_onboarding_state(settings, keys):
    has_openai = bool(keys.get("openai"))
    has_groq = bool(keys.get("groq"))
    model = settings.get("model", "")

    if not has_openai and not has_groq:
        return False, "At least one API key is required."
    if model not in ("gpt-4", "llama-4-scout"):
        return False, "Please select a default model."
    if model == "gpt-4" and not has_openai:
        return False, "Selected model requires OpenAI API key."
    if model == "llama-4-scout" and not has_groq:
        return False, "Selected model requires Groq API key."
    return True, ""


def is_onboarding_complete(settings=None):
    settings_obj = settings if settings is not None else load_settings()
    keys = get_api_keys()
    valid, _ = validate_onboarding_state(settings_obj, keys)
    return bool(settings_obj.get("onboarding_completed")) and valid


def save_settings(settings):
    try:
        settings_to_save = settings.copy()
        openai_key = settings_to_save.pop("openai_api_key", None)
        groq_key = settings_to_save.pop("groq_api_key", None)

        if openai_key is not None and not _set_key_in_keyring("openai_api_key", openai_key):
            print("Error saving OpenAI API key to keychain")
            return False
        if groq_key is not None and not _set_key_in_keyring("groq_api_key", groq_key):
            print("Error saving Groq API key to keychain")
            return False

        _normalize_model(settings_to_save, openai_key, groq_key)
        effective_keys = {
            "openai": openai_key if openai_key is not None else _get_key_from_keyring("openai_api_key"),
            "groq": groq_key if groq_key is not None else _get_key_from_keyring("groq_api_key"),
        }
        valid_onboarding, _ = validate_onboarding_state(settings_to_save, effective_keys)
        settings_to_save["onboarding_completed"] = valid_onboarding

        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings_to_save, f, indent=2)
        return True
    except (OSError, TypeError, ValueError) as e:
        print(f"Error saving settings: {e}")
        return False


def load_settings():
    if not SETTINGS_FILE.exists() and LEGACY_SETTINGS_FILE.exists():
        try:
            LEGACY_SETTINGS_FILE.replace(SETTINGS_FILE)
        except OSError:
            pass

    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)

            migrated = False
            legacy_openai = settings.pop("openai_api_key", None)
            legacy_groq = settings.pop("groq_api_key", None)

            if legacy_openai is not None:
                _set_key_in_keyring("openai_api_key", _decode_legacy_key(legacy_openai))
                migrated = True
            if legacy_groq is not None:
                _set_key_in_keyring("groq_api_key", _decode_legacy_key(legacy_groq))
                migrated = True

            if migrated:
                with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                    json.dump(settings, f, indent=2)

            for key, value in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = value

            settings["openai_api_key"] = _get_key_from_keyring("openai_api_key")
            settings["groq_api_key"] = _get_key_from_keyring("groq_api_key")
            _normalize_model(settings, settings["openai_api_key"], settings["groq_api_key"])
            valid_onboarding, _ = validate_onboarding_state(
                settings,
                {"openai": settings["openai_api_key"], "groq": settings["groq_api_key"]}
            )
            if valid_onboarding and not settings.get("onboarding_completed", False):
                settings["onboarding_completed"] = True
                save_settings(settings)
            elif not valid_onboarding and settings.get("onboarding_completed", False):
                settings["onboarding_completed"] = False
                save_settings(settings)
            return settings
        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            return DEFAULT_SETTINGS.copy()

    return DEFAULT_SETTINGS.copy()


def get_api_keys():
    return {
        "openai": _get_key_from_keyring("openai_api_key"),
        "groq": _get_key_from_keyring("groq_api_key"),
    }


def keyring_available():
    return keyring is not None
