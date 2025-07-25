"""
Version management for Lexia
"""

__version__ = "1.1.0"
__build__ = "20250125"
__author__ = "Muhammad Jawad Bashir"

# Version info for UI
VERSION_INFO = {
    "version": __version__,
    "build": __build__,
    "author": __author__,
    "name": "Lexia",
    "description": "Intelligent Text Rewriting Assistant"
}

def get_version_string():
    """Get formatted version string"""
    return f"v{__version__} (Build {__build__})"

def get_full_version_info():
    """Get complete version information"""
    return {
        "version": __version__,
        "build": __build__,
        "author": __author__,
        "full_version": get_version_string()
    }