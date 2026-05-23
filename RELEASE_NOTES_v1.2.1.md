## 🎉 Lexia Release v1.2.1

<img src="https://raw.githubusercontent.com/stardust-96/lexia/main/lexia.ico" width="64" />

### ✨ What's New
- **Installer-First Distribution** - Signed `Lexia-Setup-1.2.1.exe` is now the recommended download
- **OS Credential Store for API Keys** - Keys are stored via system credential manager (no plaintext/base64 settings storage)
- **Dev Mode for Safe UI Testing** - `LEXIA_DEV_MODE=1` allows startup and mock rewrites without API keys
- **First-Run Onboarding Wizard** - Setup now enforces at least one API key + valid default model before normal app use
- **Settings Reliability Improvements** - Fixed layout/visibility issues, model/key validation, and save responsiveness
- **Single-Instance Enforcement** - Prevents launching a second Lexia instance while one is already running
- **Icon/Branding Consistency** - Tray and app windows now use Lexia icon
- **Uninstall Cleanup Option** - Optional removal of local settings and stored API keys during uninstall
- **Hotkey Improvements** - New default hotkey is `Ctrl+Alt+Space`; onboarding now collects hotkey during setup

### 📦 Installation (Super Easy!)
1. Download `Lexia-Setup-1.2.1.exe`
2. Run the installer
3. Launch Lexia from Start Menu/Desktop
4. Enter your API keys in the setup wizard
5. Start rewriting text with `Ctrl+Alt+Space`!

### 🔧 Requirements
- Windows 10/11
- OpenAI API Key and/or Groq API Key (entered through GUI)
- Internet connection for AI processing

### 🚀 Features
- **Global Hotkey**: Works across all applications
- **Multiple AI Models**: GPT (OpenAI) + Llama-4-Scout (Groq)
- **6 Preset Styles** + Custom instructions
- **Configurable Alternatives**: Choose 1–5 rewrites
- **Professional About Dialog** with update checking
- **Secure Key Storage** via OS credential store

**Made with ❤️ by Muhammad Jawad Bashir**

**Full Changelog**: https://github.com/stardust-96/lexia/commits/v1.2.1
