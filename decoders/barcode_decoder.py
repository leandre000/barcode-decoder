
"""

Main barcode decoder class supporting multiple formats
"""
import cv2

import numpy as np

from PIL import Image
from pyzbar import pyzbar

import logging

from typing import List, Dict, Optional, Union

logger = logging.getLogger(__name__)

class BarcodeDecoder:
    """Main barcode decoder supporting Aztec, Data Matrix, and other formats"""
    
    def __init__(self):
        """Initialize the decoder"""
        self.supported_formats = [
            'AZTEC', 'DATA_MATRIX', 'QR_CODE', 'CODE128', 
            'CODE39', 'EAN13', 'EAN8', 'UPC_A', 'UPC_E'
        ]
    
    def decode(self, image: Union[str, np.ndarray, Image.Image], 
               formats: Optional[List[str]] = None) -> List[Dict]:
        """
        Decode barcodes from an image
        
        Args:
            image: Image path, numpy array, or PIL Image
            formats: Optional list of formats to decode (None = all)
        
        Returns:
            List of decoded barcode results
        """
        try:
            # Convert image to numpy array
            img_array = self._prepare_image(image)
            
            # Decode using pyzbar (supports many formats)
            results = self._decode_pyzbar(img_array, formats)
            
            # Try Aztec-specific decoder
            aztec_results = self._decode_aztec(img_array)
            if aztec_results:
                results.extend(aztec_results)
            
            # Try Data Matrix-specific decoder
            datamatrix_results = self._decode_datamatrix(img_array)
            if datamatrix_results:
                results.extend(datamatrix_results)
            
            return results
        
        except Exception as e:
            logger.error(f"Error decoding barcode: {str(e)}")
            return []
    
    def _prepare_image(self, image: Union[str, np.ndarray, Image.Image]) -> np.ndarray:
        """Convert image to numpy array"""
        if isinstance(image, str):
            img = cv2.imread(image)
        elif isinstance(image, Image.Image):
            img = np.array(image)
            if len(img.shape) == 3 and img.shape[2] == 3:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        elif isinstance(image, np.ndarray):
            img = image.copy()
        else:
            raise ValueError(f"Unsupported image type: {type(image)}")
        
        # Convert to grayscale if needed
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        return img
    
    def _decode_pyzbar(self, img_array: np.ndarray, 
                       formats: Optional[List[str]] = None) -> List[Dict]:
        """Decode using pyzbar library"""
        results = []
        try:
            decoded = pyzbar.decode(img_array)
            for barcode in decoded:
                format_name = barcode.type
                
                # Filter by format if specified
                if formats and format_name not in formats:
                    continue
                
                result = {
                    'type': format_name,
                    'data': barcode.data.decode('utf-8', errors='ignore'),
                    'rect': {
                        'x': barcode.rect.left,
                        'y': barcode.rect.top,
                        'width': barcode.rect.width,
                        'height': barcode.rect.height
                    },
                    'points': [(p.x, p.y) for p in barcode.polygon],
                    'quality': getattr(barcode, 'quality', None)
                }
                results.append(result)
        except Exception as e:
            logger.warning(f"Pyzbar decoding error: {str(e)}")
        
        return results
    
    def _decode_aztec(self, img_array: np.ndarray) -> List[Dict]:
        """Decode Aztec barcodes using specialized methods"""
        results = []
        try:
            # Aztec codes often need specific preprocessing
            # Enhance contrast and apply threshold
            enhanced = cv2.convertScaleAbs(img_array, alpha=1.5, beta=30)
            _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Try decoding with pyzbar on enhanced image
            decoded = pyzbar.decode(binary)
            for barcode in decoded:
                if barcode.type == 'AZTEC':
                    result = {
                        'type': 'AZTEC',
                        'data': barcode.data.decode('utf-8', errors='ignore'),
                        'rect': {
                            'x': barcode.rect.left,
                            'y': barcode.rect.top,
                            'width': barcode.rect.width,
                            'height': barcode.rect.height
                        },
                        'points': [(p.x, p.y) for p in barcode.polygon],
                        'method': 'enhanced_threshold'
                    }
                    results.append(result)
        except Exception as e:
            logger.debug(f"Aztec decoding error: {str(e)}")
        
        return results
    
    def _decode_datamatrix(self, img_array: np.ndarray) -> List[Dict]:
        """Decode Data Matrix barcodes using specialized methods"""
        results = []
        try:
            # Data Matrix codes benefit from noise reduction
            denoised = cv2.fastNlMeansDenoising(img_array, None, 10, 7, 21)
            
            # Apply adaptive threshold
            binary = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Try decoding with pyzbar
            decoded = pyzbar.decode(binary)
            for barcode in decoded:
                if barcode.type == 'DATA_MATRIX':
                    result = {
                        'type': 'DATA_MATRIX',
                        'data': barcode.data.decode('utf-8', errors='ignore'),
                        'rect': {
                            'x': barcode.rect.left,
                            'y': barcode.rect.top,
                            'width': barcode.rect.width,
                            'height': barcode.rect.height
                        },
                        'points': [(p.x, p.y) for p in barcode.polygon],
                        'method': 'adaptive_threshold'
                    }
                    results.append(result)
        except Exception as e:
            logger.debug(f"Data Matrix decoding error: {str(e)}")
        
        return results
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported barcode formats"""
        return self.supported_formats.copy()

