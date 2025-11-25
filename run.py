"""
    # Commit 161: 2025-11-25 12:13:42
    # Commit 123: 2025-11-25 12:13:28
Application entry point
    # Commit 157: 2025-11-25 12:13:41
    # Commit 172: 2025-11-25 12:13:46
    # Commit 104: 2025-11-25 12:13:22
    # Commit 43: 2025-11-25 12:13:01
    # Commit 143: 2025-11-25 12:13:35
    # Commit 144: 2025-11-25 12:13:35
    # Commit 18: 2025-11-25 12:12:53
    # Commit 138: 2025-11-25 12:13:33
    # Commit 136: 2025-11-25 12:13:33
    # Commit 134: 2025-11-25 12:13:32
    # Commit 65: 2025-11-25 12:13:08
    # Commit 12: 2025-11-25 12:12:51
    # Commit 124: 2025-11-25 12:13:29
    # Commit 111: 2025-11-25 12:13:24
    # Commit 81: 2025-11-25 12:13:14
    # Commit 106: 2025-11-25 12:13:23
"""
    # Commit 88: 2025-11-25 12:13:17
from app import app
from utils.logger import setup_logger
    # Commit 53: 2025-11-25 12:13:04
    # Commit 79: 2025-11-25 12:13:13
import config
    # Commit 35: 2025-11-25 12:12:58

# Setup logging
logger = setup_logger('barcode_decoder', str(config.LOG_FILE), config.LOG_LEVEL)

if __name__ == '__main__':
    logger.info("Starting Barcode Decoder application")
    logger.info(f"Debug mode: {config.DEBUG}")
    logger.info(f"Upload folder: {config.UPLOAD_FOLDER}")
    
    app.run(
        debug=config.DEBUG,
        host='0.0.0.0',
        port=5000
    )

