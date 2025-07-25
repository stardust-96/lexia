# Lexia Deployment Guide

This guide explains how to build and distribute Lexia as an installable application.

## Quick Build

To build the executable locally:

```bash
python build.py
```

This will create:
- `dist/Lexia.exe` - The standalone executable
- `release/` - Distribution folder with documentation
- `Lexia-v1.0.0-Windows.zip` - Release package

## Standard Deployment Process

### 1. Local Development Build

```bash
# Install build dependencies
pip install pyinstaller pillow

# Create the executable
python build.py
```

### 2. GitHub Releases (Automated)

The project is set up for automated releases via GitHub Actions:

1. **Create a version tag:**
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

2. **GitHub Actions automatically:**
   - Builds the Windows executable
   - Creates a release package
   - Publishes to GitHub Releases
   - Uploads installation files

### 3. Manual Release Process

If you prefer manual releases:

1. **Build locally:**
   ```bash
   python build.py
   ```

2. **Test the executable:**
   ```bash
   cd dist
   ./Lexia.exe
   ```

3. **Create GitHub release:**
   - Go to GitHub → Releases → New Release
   - Upload `Lexia-v*.zip` and `Lexia.exe`
   - Add release notes

## Distribution Files

The build process creates these files for distribution:

### Essential Files
- `Lexia.exe` - Main executable (standalone)
- `README.md` - User documentation
- `LICENSE` - License file
- `config.example.py` - Configuration template
- `INSTALLATION.txt` - Installation instructions

### Package Structure
```
Lexia-v1.0.0-Windows.zip
├── Lexia.exe
├── README.md
├── LICENSE
├── config.example.py
└── INSTALLATION.txt
```

## Publishing Platforms

### Free Options
1. **GitHub Releases** (Recommended)
   - Automatic via GitHub Actions
   - Built-in download tracking
   - Integration with Git tags

2. **SourceForge**
   - Upload manually or via API
   - Good for open source projects

### Paid Options
1. **Microsoft Store**
   - Requires developer account ($19)
   - MSIX package format needed
   - Code signing required

2. **Professional Distribution**
   - Code signing certificate ($200-400/year)
   - Custom installer (NSIS/Inno Setup)
   - Your own website/domain

## Version Management

Update version in these files before release:
- `version.py` - Main version info
- `version_info.py` - Windows executable metadata
- GitHub tag should match version number

## Code Signing (Optional)

For production releases, consider code signing:

1. **Get certificate** from a trusted CA
2. **Update build script** to sign executable
3. **Users won't see** "Unknown Publisher" warnings

```bash
# Example signing command
signtool sign /f certificate.p12 /p password /t http://timestamp.digicert.com dist/Lexia.exe
```

## Automated Updates

The app includes update checking via GitHub API. Users can:
- Check for updates in About dialog
- Download new versions automatically
- See release notes and changelogs

## Testing Before Release

Always test the built executable:

1. **Functional testing:**
   - Run on clean Windows system
   - Test hotkey functionality
   - Verify API connections work

2. **Security testing:**
   - Virus scan the executable
   - Test on different Windows versions
   - Verify no sensitive data leaks

## Support and Distribution

Once released, users can:
- Download from GitHub Releases
- Follow installation guide
- Report issues via GitHub Issues
- Check for updates within the app

For questions about deployment, check the project's GitHub repository or contact the maintainer.