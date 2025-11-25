

"""
Configuration settings for Barcode Decoder

"""
import os

from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

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

