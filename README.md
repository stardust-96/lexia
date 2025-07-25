# Lexia ✨

A powerful desktop application that provides intelligent text rewriting with customizable styles and AI models. Similar to Grammarly but with more flexibility and AI model options.

[![Release](https://img.shields.io/github/v/release/stardust-96/lexia)](https://github.com/stardust-96/lexia/releases)
[![Downloads](https://img.shields.io/github/downloads/stardust-96/lexia/total)](https://github.com/stardust-96/lexia/releases)
[![License](https://img.shields.io/github/license/stardust-96/lexia)](LICENSE)

## 🚀 Quick Start

### **🎯 Super Easy Installation (Recommended)**
1. Go to [Releases](https://github.com/stardust-96/lexia/releases/latest)
2. Download `Lexia-v1.1.0-Windows.zip`
3. Extract to any folder
4. Run `Lexia.exe`
5. **First-time setup wizard opens automatically**
6. Enter your API keys in the GUI (no file editing!)
7. Start rewriting with `Ctrl+Shift+R`!

**✨ No Python installation, no config files, no technical setup required!**

### **🛠️ Developer Option: Run from Source**
```bash
git clone https://github.com/stardust-96/lexia.git
cd lexia
pip install -r requirements.txt
python main.py
```

## ✨ Features

### 🤖 AI-Powered Rewriting
- **Multiple AI Models**: GPT-4 (OpenAI) and Llama-4-Scout (Groq)
- **Alternative Suggestions**: Get 3 different rewrite variations for each text
- **Real-time Processing**: Fast text rewriting with immediate results

### 🎨 Flexible Styling Options
- **Preset Styles**: Neutral, Formal, Friendly, Professional, Concise, Creative
- **Custom Instructions**: Define your own rewriting instructions
  - Format: *"in one line"*, *"as bullet points"*, *"in 3 sentences"*
  - Style: *"like Shakespeare"*, *"more casual"*, *"academic style"*
  - Purpose: *"more persuasive"*, *"for social media"*, *"for children"*

### ⚡ User Experience
- **🎯 Zero-Setup Installation**: Download → Run → Enter API Keys → Done!
- **🔧 First-Time Setup Wizard**: Automatic configuration on first launch
- **⚙️ GUI-Based Settings**: Professional tabbed interface for all settings
- **🔑 Secure API Key Management**: No config file editing required
- **🌐 Global Hotkey**: Works across all applications (default: `Ctrl+Shift+R`)
- **⚡ Instant Access**: Select text anywhere and press hotkey
- **🎨 Modern UI**: Clean interface with dynamic text sizing
- **📋 One-Click Copy**: Copy and close with single button
- **🔄 Auto-Updates**: Built-in update checker

### ⚙️ Customization
- **Hotkey Configuration**: Set your preferred keyboard shortcut
- **Model Selection**: Switch between AI models on-the-fly
- **Temperature Control**: Adjust creativity level (0.0-1.0)
- **Alternative Count**: Choose number of rewrite suggestions (1-5)

## 🛠️ Installation

### **🎯 Windows Executable (Recommended - Super Easy!)**
1. **Download** the latest release from [GitHub Releases](https://github.com/stardust-96/lexia/releases/latest)
2. **Extract** `Lexia-v1.1.0-Windows.zip` to any folder
3. **Run** `Lexia.exe`
4. **🎨 First-time setup opens automatically**
5. **Enter your API keys** in the professional GUI interface
6. **Done!** No config files, no command line needed

### **💻 From Source (Developers)**

#### Prerequisites
- Python 3.7+
- pip package manager

#### Setup Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/stardust-96/lexia.git
   cd lexia
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run with GUI Setup**
   ```bash
   python main.py
   # First-time setup wizard opens automatically
   # Enter API keys through the GUI interface
   ```

### **🔑 Getting API Keys (Done Through GUI)**

Lexia's setup wizard will guide you, but here's where to get keys:

#### **OpenAI API Key** (for GPT-4)
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create account or sign in
3. Generate new API key
4. Add billing information if required

#### **Groq API Key** (for Llama-4-Scout) 
1. Visit [Groq Console](https://console.groq.com/keys)
2. Create account or sign in  
3. Generate new API key
4. Copy the key (it's free!)

**💡 You only need ONE API key to use Lexia!** The setup wizard makes it easy to configure either or both.

## 📖 Usage

### **🎯 Quick Start Guide**

1. **🚀 Launch Lexia**
   - **Executable**: Double-click `Lexia.exe`
   - **First-time**: Setup wizard opens automatically
   - **Returning users**: Runs in background

2. **📝 Select text** anywhere (browser, Word, email, etc.)

3. **⌨️ Press hotkey** (default: `Ctrl+Shift+R`)

4. **🤖 Configure and rewrite**:
   - Choose AI model (GPT-4 or Llama-4-Scout)
   - Select preset style or enter custom instructions
   - Click "🔄 Rewrite" to generate 3 alternatives

5. **✨ Select and copy** your preferred version

6. **🎉 Done!** Text is copied to clipboard and ready to paste

### **⚙️ Access Settings**
- **During setup**: Automatic first-time wizard
- **Anytime**: File → Settings in the rewrite window
- **Configure**: API keys, hotkeys, temperature, alternatives count

### Custom Instructions Examples

Instead of just tone, you can give specific instructions:

- **Format**: `"in one line"`, `"as bullet points"`, `"in 3 sentences"`
- **Length**: `"make it shorter"`, `"expand this"`, `"compress to 50 words"`
- **Style**: `"like Shakespeare"`, `"more casual"`, `"academic style"`
- **Purpose**: `"more persuasive"`, `"for social media"`, `"for children"`
- **Structure**: `"with numbered steps"`, `"as pros and cons"`

### Settings Configuration

Access settings through the popup menu: **File → Settings**

- **Hotkey**: Change keyboard shortcut
- **Temperature**: Adjust AI creativity (0.0 = conservative, 1.0 = creative)
- **Alternatives**: Set number of rewrite suggestions (1-5)

## Configuration Files

- `settings.json`: User preferences (hotkey, model, temperature, etc.)
- `config.py`: API keys and model configurations
- `app.lock`: Prevents multiple instances (auto-managed)

## 📁 Project Structure

```
lexia/
├── 📄 Core Application
│   ├── main.py              # Application entry point
│   ├── ui_enhanced.py       # Main user interface
│   ├── rewriter.py         # AI model integration
│   ├── settings.py         # Settings management
│   └── version.py          # Version management
│
├── ⚙️ Configuration
│   ├── config.py           # API keys (created from example)
│   ├── config.example.py   # Configuration template
│   └── settings.json       # User preferences (auto-generated)
│
├── 🔨 Build System
│   ├── build.py            # Build script for executables
│   ├── lexia.spec          # PyInstaller configuration
│   ├── version_info.py     # Windows executable metadata
│   ├── create_icon.py      # Icon generation script
│   └── lexia.ico          # Application icon
│
├── 🚀 Deployment
│   ├── .github/workflows/  # GitHub Actions for releases
│   ├── DEPLOYMENT.md       # Deployment guide
│   └── release/           # Distribution folder (generated)
│
└── 📚 Documentation
    ├── README.md          # This file
    ├── LICENSE           # MIT License
    └── requirements.txt  # Python dependencies
```

## 🔧 Technical Details

### **AI Models**
- **GPT-4** (OpenAI): Premium quality, excellent for complex rewrites
- **Llama-4-Scout** (Groq): Fast inference, cost-effective alternative

### **Architecture**
- **Global Hotkey**: System-wide text capture using `keyboard` library
- **GUI Framework**: Modern Tkinter interface with enhanced styling
- **Threading**: Non-blocking UI with background AI processing
- **Update System**: Built-in GitHub API integration for version checking

### **Deployment**
- **PyInstaller**: Creates standalone Windows executables
- **GitHub Actions**: Automated building and release publishing
- **Version Management**: Centralized versioning with build metadata

### **Security & Privacy**
- **🔒 Secure Local Storage**: API keys stored locally with base64 encoding
- **🚫 No Telemetry**: No usage data collection or external logging
- **⚡ Real-time Processing**: Text processed immediately, not stored
- **🔓 Open Source**: Full transparency with MIT license
- **🛡️ No Cloud Dependencies**: Everything runs on your computer

## Troubleshooting

### **🔧 Common Issues**

1. **🔄 "Application already running" error**
   - Delete `app.lock` file and restart
   - Only one instance can run at a time

2. **🔑 API key issues**
   - Go to **File → Settings → API Keys** tab
   - Re-enter your API keys in the GUI
   - Test keys using the "Test API Keys" button
   - Ensure you have API credits/billing set up

3. **⌨️ Hotkey not working**
   - Try running as administrator  
   - Check if hotkey conflicts with other applications
   - Change hotkey in **File → Settings → General** tab

4. **🐍 Running from source issues**
   - Ensure Python 3.7+ is installed
   - Run `pip install -r requirements.txt` again
   - Try creating a virtual environment

5. **🎯 First-time setup issues**
   - Restart Lexia.exe to re-trigger setup wizard
   - Manually open settings: **File → Settings → API Keys**

6. **🛡️ Antivirus/Windows Defender warnings**
   - **This is a false positive** - very common with PyInstaller apps
   - **Safe to ignore**: The executable is clean (check source code)
   - **Chrome/Edge**: Click "Keep" when downloading
   - **Windows Defender**: Click "More info" → "Run anyway"
   - **Add exclusion**: Add Lexia folder to antivirus exclusions
   - **Why this happens**: Unsigned executables trigger heuristic detection

### **🆘 Getting Help**

- Check console output for error messages
- Verify API keys are valid with sufficient credits
- Use the built-in "Test API Keys" feature in settings
- Report issues at [GitHub Issues](https://github.com/stardust-96/lexia/issues)

## 🏗️ Development

### **Building from Source**
```bash
# Clone and setup
git clone https://github.com/stardust-96/lexia.git
cd lexia
pip install -r requirements.txt

# Run in development
python main.py

# Build executable
python build.py
```

### **Creating Releases**
```bash
# Update version in version.py
# Create and push tag
git tag v1.0.1
git push origin v1.0.1

# GitHub Actions automatically builds and releases
```

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes and test thoroughly
4. **Commit** with clear messages (`git commit -m 'Add amazing feature'`)
5. **Push** to your branch (`git push origin feature/amazing-feature`)
6. **Open** a Pull Request with detailed description

### **Development Guidelines**
- Follow existing code style and patterns
- Test on Windows before submitting
- Update documentation for new features
- Ensure executable builds successfully

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API and excellent documentation
- **Groq** for Llama model hosting and fast inference
- **Python Community** for amazing libraries (Tkinter, PyInstaller, etc.)
- **GitHub** for free hosting and automated CI/CD

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### **✨ Lexia - Your Intelligent Text Rewriting Assistant ✨**

**Made with ❤️ by [Muhammad Jawad Bashir](https://github.com/stardust-96)**

[![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)](https://github.com/stardust-96/lexia)
[![Download](https://img.shields.io/badge/Download-Latest-blue?logo=download)](https://github.com/stardust-96/lexia/releases/latest)
[![Issues](https://img.shields.io/badge/Issues-Report-red?logo=github)](https://github.com/stardust-96/lexia/issues)

**Transform your writing with AI-powered intelligence** 🚀

</div>
