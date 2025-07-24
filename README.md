# Lexia

A powerful desktop application that provides intelligent text rewriting with customizable styles and AI models. Similar to Grammarly but with more flexibility and AI model options.

## Features

### 🚀 AI-Powered Rewriting
- **Multiple AI Models**: Choose between GPT-4 (OpenAI) and Llama-4-Scout (Groq)
- **Alternative Suggestions**: Get 3 different rewrite variations for each text
- **Real-time Processing**: Fast text rewriting with immediate results

### 🎨 Flexible Styling Options
- **Preset Styles**: Neutral, Formal, Friendly, Professional, Concise, Creative
- **Custom Instructions**: Define your own rewriting instructions
  - Format: "in one line", "as bullet points", "in 3 sentences"
  - Style: "like Shakespeare", "more casual", "academic style"
  - Purpose: "more persuasive", "for social media", "for children"

### ⚡ User-Friendly Interface
- **Global Hotkey**: Works across all applications (default: Ctrl+Shift+R)
- **Instant Access**: Select text anywhere and press hotkey
- **Clean UI**: Modern interface with dynamic text sizing
- **One-Click Copy**: Copy and close with single button

### ⚙️ Customizable Settings
- **Hotkey Configuration**: Set your preferred keyboard shortcut
- **Model Selection**: Switch between AI models on-the-fly
- **Temperature Control**: Adjust creativity level (0.0-1.0)
- **Alternative Count**: Choose number of rewrite suggestions (1-5)

## Installation

### Prerequisites
- Python 3.7+
- pip package manager

### Setup

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
   
   Create/edit `config.py` and add your API keys:
   ```python
   # OpenAI API Key (for GPT-4)
   OPENAI_API_KEY = "your-openai-api-key-here"
   
   # Groq API Key (for Llama-4-Scout)
   GROQ_API_KEY = "your-groq-api-key-here"
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

## Usage

### Quick Start

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Select text** in any application (browser, document, email, etc.)

3. **Press hotkey** (default: Ctrl+Shift+R)

4. **Choose options** in the popup window:
   - Select AI model (GPT-4 or Llama-4-Scout)
   - Choose preset style or enter custom instructions
   - Review the 3 alternative rewrites (v1, v2, v3)

5. **Copy result** and the window closes automatically

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

## Project Structure

```
lexia/
├── main.py              # Application entry point
├── ui_enhanced.py       # Main user interface
├── rewriter.py         # AI model integration
├── settings.py         # Settings management
├── config.py           # API keys and configuration
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .gitignore        # Git ignore rules
└── settings.json     # User settings (auto-generated)
```

## Technical Details

### AI Models
- **GPT-4**: OpenAI's flagship model, excellent for general text rewriting
- **Llama-4-Scout**: Groq's optimized model, faster inference with good quality

### Architecture
- **Global Hotkey**: Uses `keyboard` library for system-wide shortcuts
- **GUI Framework**: Tkinter with enhanced styling
- **Threading**: Non-blocking UI with background AI processing
- **Error Handling**: Robust error handling and graceful degradation

### Security
- API keys stored locally in `config.py`
- No data logging or external storage
- Text processing happens in real-time, not stored

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

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for GPT-4 API
- Groq for Llama model hosting
- Python community for excellent libraries

---

**Made with ❤️ by Muhammad Jawad Bashir**

**Lexia** - Your intelligent text rewriting assistant

For issues, suggestions, or contributions, please visit the [GitHub repository](https://github.com/stardust-96/lexia).
