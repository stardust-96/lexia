# DEPRECATED: This file is no longer used for API key storage
# API keys are now managed through the Settings UI
# 
# To configure API keys:
# 1. Run Lexia
# 2. Go to File → Settings → API Keys tab
# 3. Enter your API keys and save
#
# Keys are stored securely in settings.json with basic encoding

from settings import get_api_keys

# Backward compatibility - loads keys from new settings system
_keys = get_api_keys()
OPENAI_API_KEY = _keys.get("openai", "")
GROQ_API_KEY = _keys.get("groq", "")
