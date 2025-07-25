# Lexia ✨

A powerful desktop application that provides intelligent text rewriting with customizable styles and AI models. Similar to Grammarly but with more flexibility and AI model options.

[![Release](https://img.shields.io/github/v/release/stardust-96/lexia)](https://github.com/stardust-96/lexia/releases)
[![Downloads](https://img.shields.io/github/downloads/stardust-96/lexia/total)](https://github.com/stardust-96/lexia/releases)
[![License](https://img.shields.io/github/license/stardust-96/lexia)](LICENSE)

## 🚀 Quick Start

### **Option 1: Download Executable (Recommended)**
1. Go to [Releases](https://github.com/stardust-96/lexia/releases/latest)
2. Download `Lexia-v*-Windows.zip`
3. Extract and follow `INSTALLATION.txt`
4. Run `Lexia.exe` - No Python installation needed!

### **Option 2: Run from Source**
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
- **Global Hotkey**: Works across all applications (default: `Ctrl+Shift+R`)
- **Instant Access**: Select text anywhere and press hotkey
- **Modern UI**: Clean interface with dynamic text sizing
- **One-Click Copy**: Copy and close with single button
- **Auto-Updates**: Built-in update checker

### ⚙️ Customization
- **Hotkey Configuration**: Set your preferred keyboard shortcut
- **Model Selection**: Switch between AI models on-the-fly
- **Temperature Control**: Adjust creativity level (0.0-1.0)
- **Alternative Count**: Choose number of rewrite suggestions (1-5)

## 🛠️ Installation

### **Windows Executable (Easy)**
1. **Download** the latest release from [GitHub Releases](https://github.com/stardust-96/lexia/releases/latest)
2. **Extract** `Lexia-v*-Windows.zip` to a folder
3. **Configure** API keys in `config.py` (copy from `config.example.py`)
4. **Run** `Lexia.exe`

### **From Source (Developers)**

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

3. **Configure API Keys**
   ```bash
   cp config.example.py config.py
   # Edit config.py with your API keys
   ```

### Getting API Keys

#### OpenAI API Key
1. Visit [OpenAI API](https://platform.openai.com/api-keys)
2. Create an account or sign in
3. Generate a new API key
4. Add billing information if required

#### Groq API Key
1. Visit [Groq Console](https://console.groq.com/)
2. Create an account or sign in
3. Generate a new API key
4. Copy the key to your config

## 📖 Usage

### Quick Start Guide

1. **Launch Lexia**
   - **Executable**: Double-click `Lexia.exe`
   - **Source**: Run `python main.py`

2. **Select text** anywhere (browser, Word, email, etc.)

3. **Press hotkey** (default: `Ctrl+Shift+R`)

4. **Configure and rewrite**:
   - Choose AI model (GPT-4 or Llama-4-Scout)
   - Select preset style or enter custom instructions
   - Click "🔄 Rewrite" to generate alternatives

5. **Select and copy** your preferred version

6. **Done!** Text is copied to clipboard and ready to paste

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
- **Local Storage**: API keys stored locally in `config.py`
- **No Telemetry**: No usage data collection or external logging
- **Real-time Processing**: Text processed immediately, not stored
- **Open Source**: Full transparency with MIT license

## Troubleshooting

### Common Issues

1. **"Application already running" error**
   - Delete `app.lock` file and restart
   - Only one instance can run at a time

2. **API errors**
   - Check your API keys in `config.py`
   - Ensure you have API credits/billing set up
   - Check internet connection

3. **Hotkey not working**
   - Try running as administrator
   - Check if hotkey conflicts with other applications
   - Change hotkey in settings

4. **Dependencies issues**
   - Ensure Python 3.7+ is installed
   - Run `pip install -r requirements.txt` again
   - Try creating a virtual environment

### Getting Help

- Check console output for error messages
- Ensure all dependencies are installed correctly
- Verify API keys are valid and have sufficient credits

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
