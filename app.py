"""
    # Commit 3: 2025-11-25 12:12:48
    # Commit 51: 2025-11-25 12:13:03
Main Flask application for Barcode Decoder
    # Commit 7: 2025-11-25 12:12:49
    # Commit 35: 2025-11-25 12:12:58
"""
    # Commit 29: 2025-11-25 12:12:56
    # Commit 43: 2025-11-25 12:13:01
from flask import Flask, render_template, request, jsonify
import os
    # Commit 50: 2025-11-25 12:13:03
from werkzeug.utils import secure_filename
from decoders.barcode_decoder import BarcodeDecoder
    # Commit 34: 2025-11-25 12:12:58
    # Commit 9: 2025-11-25 12:12:50
from utils.image_processor import ImageProcessor
from utils.validators import validate_image_file
from utils.logger import setup_logger
import config

# Setup logging
logger = setup_logger('barcode_decoder', str(config.LOG_FILE), config.LOG_LEVEL)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = str(config.UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.config['ALLOWED_EXTENSIONS'] = config.ALLOWED_EXTENSIONS
app.config['SECRET_KEY'] = config.SECRET_KEY

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('temp', exist_ok=True)

# Initialize decoder and processor
decoder = BarcodeDecoder()
image_processor = ImageProcessor()


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/decode', methods=['POST'])
def decode_barcode():
    """API endpoint for decoding barcodes"""
    try:
        logger.info("Received decode request")
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not validate_image_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Get processing options
        enhance = request.form.get('enhance', 'false').lower() == 'true'
        formats = request.form.get('formats', '').split(',') if request.form.get('formats') else []
        
        # Process and decode
        processed_image = image_processor.preprocess(filepath, enhance=enhance)
        results = decoder.decode(processed_image, formats=formats if formats else None)
        
        # Clean up
        os.remove(filepath)
        
        logger.info(f"Successfully decoded {len(results)} barcode(s)")
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        logger.error(f"Error decoding barcode: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch', methods=['POST'])
def batch_decode():
    """API endpoint for batch processing multiple images"""
    try:
        logger.info(f"Received batch decode request with {len(request.files.getlist('images'))} files")
        if 'images' not in request.files:
            return jsonify({'error': 'No image files provided'}), 400
        
        files = request.files.getlist('images')
        if not files:
            return jsonify({'error': 'No files selected'}), 400
        
        results = []
        enhance = request.form.get('enhance', 'false').lower() == 'true'
        
        for file in files:
            if file.filename and validate_image_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                try:
                    processed_image = image_processor.preprocess(filepath, enhance=enhance)
                    decode_results = decoder.decode(processed_image)
                    results.append({
                        'filename': filename,
                        'results': decode_results,
                        'success': True
                    })
                except Exception as e:
                    results.append({
                        'filename': filename,
                        'error': str(e),
                        'success': False
                    })
                finally:
                    if os.path.exists(filepath):
                        os.remove(filepath)
        
        logger.info(f"Batch processing completed: {len(results)} files processed")
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        })
    
    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'barcode-decoder'})


if __name__ == '__main__':
    logger.info("Starting Barcode Decoder application")
    app.run(debug=config.DEBUG, host='0.0.0.0', port=5000)

