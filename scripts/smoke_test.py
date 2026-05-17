#!/usr/bin/env python3
import os
import sys
import tempfile
from pathlib import Path


def main():
    # Force dev mode before importing project modules.
    os.environ["LEXIA_DEV_MODE"] = "1"
    repo_root = Path(__file__).resolve().parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    import settings_store
    import settings
    import rewriter

    # Isolate settings.json to a temp directory.
    tmp_dir = tempfile.TemporaryDirectory()
    settings_path = Path(tmp_dir.name) / "settings.json"
    settings_store.SETTINGS_FILE = str(settings_path)

    # Keep key storage in-memory for smoke tests (no OS keychain writes).
    key_mem = {"openai_api_key": "", "groq_api_key": ""}

    def fake_set_key(name, value):
        key_mem[name] = value or ""
        return True

    def fake_get_key(name):
        return key_mem.get(name, "")

    settings_store._set_key_in_keyring = fake_set_key
    settings_store._get_key_from_keyring = fake_get_key

    # 1) Save settings in dev mode without keys should succeed.
    save_payload = {
        "hotkey": "ctrl+shift+r",
        "model": "gpt-4",
        "temperature": 0.6,
        "num_alternatives": 2,
        "openai_api_key": "",
        "groq_api_key": "",
    }
    assert settings.save_settings(save_payload) is True, "save_settings failed in dev mode"

    # 2) Reload settings and verify persisted preferences.
    loaded = settings.load_settings()
    assert loaded["model"] == "gpt-4", "model persistence failed"
    assert loaded["temperature"] == 0.6, "temperature persistence failed"
    assert loaded["num_alternatives"] == 2, "num_alternatives persistence failed"

    # 3) Mock rewrite behavior in dev mode.
    out = rewriter.rewrite_text_with_gpt("Hello Lexia", tone="Formal", num_alternatives=2)
    assert len(out) == 2, "unexpected rewrite alternative count"
    assert out[0].startswith("[DEV MOCK - Formal]"), "dev-mode mock prefix missing"

    print("Smoke test passed.")
    tmp_dir.cleanup()


if __name__ == "__main__":
    main()
