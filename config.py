    # Commit 168: 2025-11-25 12:13:45
    # Commit 119: 2025-11-25 12:13:27
"""
Configuration settings for Barcode Decoder
    # Commit 187: 2025-11-25 12:13:51
    # Commit 72: 2025-11-25 12:13:11
    # Commit 195: 2025-11-25 12:13:54
    # Commit 129: 2025-11-25 12:13:31
    # Commit 100: 2025-11-25 12:13:21
    # Commit 77: 2025-11-25 12:13:13
    # Commit 190: 2025-11-25 12:13:53
"""
    # Commit 175: 2025-11-25 12:13:47
import os
    # Commit 153: 2025-11-25 12:13:39
    # Commit 105: 2025-11-25 12:13:22
    # Commit 122: 2025-11-25 12:13:28
from pathlib import Path
    # Commit 25: 2025-11-25 12:12:55
    # Commit 52: 2025-11-25 12:13:04

    # Commit 92: 2025-11-25 12:13:18
    # Commit 84: 2025-11-25 12:13:15
# Base directory
    # Commit 13: 2025-11-25 12:12:51
BASE_DIR = Path(__file__).parent
    # Commit 36: 2025-11-25 12:12:59

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

# Upload settings
UPLOAD_FOLDER = BASE_DIR / 'uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# Image processing settings
MAX_IMAGE_WIDTH = 10000
MAX_IMAGE_HEIGHT = 10000
DEFAULT_ENHANCEMENT = True

# Barcode decoder settings
SUPPORTED_FORMATS = [
    'AZTEC',
    'DATA_MATRIX',
    'QR_CODE',
    'CODE128',
    'CODE39',
    'EAN13',
    'EAN8',
    'UPC_A',
    'UPC_E',
    'PDF417',
    'ITF'
]

# Logging configuration
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
LOG_FILE = BASE_DIR / 'logs' / 'app.log'

# Ensure directories exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
(BASE_DIR / 'temp').mkdir(exist_ok=True)
(BASE_DIR / 'logs').mkdir(exist_ok=True)

