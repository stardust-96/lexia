import binascii
import json
import os

try:
    import keyring
except ImportError:
    keyring = None

SETTINGS_FILE = "settings.json"
KEYRING_SERVICE = "Lexia"
DEV_MODE = os.getenv("LEXIA_DEV_MODE", "0") == "1"

DEFAULT_SETTINGS = {
    "hotkey": "ctrl+shift+r",
    "model": "gpt-4",
    "temperature": 0.7,
    "num_alternatives": 3,
}


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

        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings_to_save, f, indent=2)
        return True
    except (OSError, TypeError, ValueError) as e:
        print(f"Error saving settings: {e}")
        return False


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
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
                with open(SETTINGS_FILE, "w") as f:
                    json.dump(settings, f, indent=2)

            for key, value in DEFAULT_SETTINGS.items():
                if key not in settings:
                    settings[key] = value

            settings["openai_api_key"] = _get_key_from_keyring("openai_api_key")
            settings["groq_api_key"] = _get_key_from_keyring("groq_api_key")
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
