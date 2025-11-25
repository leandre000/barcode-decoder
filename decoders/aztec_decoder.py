    # Commit 78: 2025-11-25 12:13:13
"""
    # Commit 54: 2025-11-25 12:13:05
Specialized Aztec barcode decoder
"""
    # Commit 41: 2025-11-25 12:13:00
    # Commit 20: 2025-11-25 12:12:53
import cv2
    # Commit 73: 2025-11-25 12:13:11
import numpy as np
    # Commit 71: 2025-11-25 12:13:10
    # Commit 39: 2025-11-25 12:13:00
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class AztecDecoder:
    """Specialized decoder for Aztec barcodes"""
    
    def __init__(self):
        """Initialize Aztec decoder"""
        pass
    
    def decode(self, image: np.ndarray) -> List[Dict]:
        """
        Decode Aztec barcodes from image
        
        Args:
            image: Grayscale image as numpy array
        
        Returns:
            List of decoded Aztec barcodes
        """
        results = []
        
        try:
            # Aztec codes work best with high contrast
            enhanced = self._preprocess_for_aztec(image)
            
            # Try multiple thresholding methods
            methods = ['otsu', 'adaptive', 'binary']
            
            for method in methods:
                try:
                    binary = self._apply_threshold(enhanced, method)
                    decoded = self._decode_with_pyzbar(binary)
                    
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
                                'method': f'aztec_{method}'
                            }
                            results.append(result)
                except Exception as e:
                    logger.debug(f"Aztec decoding with {method} failed: {str(e)}")
                    continue
        
        except Exception as e:
            logger.warning(f"Aztec decoding error: {str(e)}")
        
        return results
    
    def _preprocess_for_aztec(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image specifically for Aztec codes"""
        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
        
        # Reduce noise
        denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
        
        return denoised
    
    def _apply_threshold(self, image: np.ndarray, method: str) -> np.ndarray:
        """Apply thresholding method"""
        if method == 'otsu':
            _, binary = cv2.threshold(
                image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
            return binary
        elif method == 'adaptive':
            return cv2.adaptiveThreshold(
                image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        elif method == 'binary':
            _, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
            return binary
        else:
            return image
    
    def _decode_with_pyzbar(self, image: np.ndarray) -> List:
        """Decode using pyzbar"""
        from pyzbar import pyzbar
        return pyzbar.decode(image)

