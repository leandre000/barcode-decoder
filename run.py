"""
Application entry point
    # Commit 18: 2025-11-25 12:12:53
    # Commit 12: 2025-11-25 12:12:51
"""
from app import app
from utils.logger import setup_logger
import config

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

