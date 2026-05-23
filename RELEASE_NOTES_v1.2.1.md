## 🎉 Lexia Release v1.2.1

### ✨ What's New
- **Installer-First Distribution** - Signed `Lexia-Setup-1.2.1.exe` is now the recommended download
- **OS Credential Store for API Keys** - Keys are stored via system credential manager (no plaintext/base64 settings storage)
- **Dev Mode for Safe UI Testing** - `LEXIA_DEV_MODE=1` allows startup and mock rewrites without API keys
- **Settings Reliability Improvements** - Fixed layout/visibility issues, default model persistence, and model/key validation
- **Thread-Safe UI Updates** - Rewriting/update flows now marshal UI changes safely on the main thread
- **Hotkey/Clipboard Robustness** - Better failure handling to avoid stuck states

### 📦 Installation (Super Easy!)
1. Download `Lexia-Setup-1.2.1.exe`
2. Run the installer
3. Launch Lexia from Start Menu/Desktop
4. Enter your API keys in the setup wizard
5. Start rewriting text with `Ctrl+Shift+R`!

### 🔧 Requirements
- Windows 10/11
- OpenAI API Key and/or Groq API Key (entered through GUI)
- Internet connection for AI processing

### 🚀 Features
- **Global Hotkey**: Works across all applications
- **Multiple AI Models**: GPT-4 (OpenAI) + Llama-4-Scout (Groq)
- **6 Preset Styles** + Custom instructions
- **Configurable Alternatives**: Choose 1–5 rewrites
- **Professional About Dialog** with update checking
- **Secure Key Storage** via OS credential store

**Made with ❤️ by Muhammad Jawad Bashir**

**Full Changelog**: https://github.com/stardust-96/lexia/commits/v1.2.1
