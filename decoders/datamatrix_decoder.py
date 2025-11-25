    # Commit 80: 2025-11-25 12:13:14
"""
    # Commit 74: 2025-11-25 12:13:12
Specialized Data Matrix barcode decoder
    # Commit 36: 2025-11-25 12:12:59
    # Commit 96: 2025-11-25 12:13:20
    # Commit 88: 2025-11-25 12:13:17
    # Commit 55: 2025-11-25 12:13:05
    # Commit 50: 2025-11-25 12:13:03
    # Commit 11: 2025-11-25 12:12:51
"""
    # Commit 41: 2025-11-25 12:13:00
    # Commit 69: 2025-11-25 12:13:10
    # Commit 71: 2025-11-25 12:13:10
    # Commit 48: 2025-11-25 12:13:02
    # Commit 62: 2025-11-25 12:13:07
import cv2
import numpy as np
    # Commit 17: 2025-11-25 12:12:52
from typing import List, Dict, Optional
    # Commit 19: 2025-11-25 12:12:53
import logging

    # Commit 8: 2025-11-25 12:12:50
logger = logging.getLogger(__name__)


class DataMatrixDecoder:
    """Specialized decoder for Data Matrix barcodes"""
    
    def __init__(self):
        """Initialize Data Matrix decoder"""
        pass
    
    def decode(self, image: np.ndarray) -> List[Dict]:
        """
        Decode Data Matrix barcodes from image
        
        Args:
            image: Grayscale image as numpy array
        
        Returns:
            List of decoded Data Matrix barcodes
        """
        results = []
        
        try:
            # Data Matrix codes need specific preprocessing
            enhanced = self._preprocess_for_datamatrix(image)
            
            # Try multiple approaches
            approaches = ['adaptive', 'otsu', 'morphological']
            
            for approach in approaches:
                try:
                    processed = self._process_image(enhanced, approach)
                    decoded = self._decode_with_pyzbar(processed)
                    
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
                                'method': f'datamatrix_{approach}'
                            }
                            results.append(result)
                except Exception as e:
                    logger.debug(f"Data Matrix decoding with {approach} failed: {str(e)}")
                    continue
        
        except Exception as e:
            logger.warning(f"Data Matrix decoding error: {str(e)}")
        
        return results
    
    def _preprocess_for_datamatrix(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image specifically for Data Matrix codes"""
        # Apply CLAHE for contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
        
        # Sharpen
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        sharpened = cv2.filter2D(denoised, -1, kernel)
        
        return sharpened
    
    def _process_image(self, image: np.ndarray, approach: str) -> np.ndarray:
        """Process image with specific approach"""
        if approach == 'adaptive':
            return cv2.adaptiveThreshold(
                image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        elif approach == 'otsu':
            _, binary = cv2.threshold(
                image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
            return binary
        elif approach == 'morphological':
            # Apply morphological operations
            _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            kernel = np.ones((3, 3), np.uint8)
            cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            return cleaned
        else:
            return image
    
    def _decode_with_pyzbar(self, image: np.ndarray) -> List:
        """Decode using pyzbar"""
        from pyzbar import pyzbar
        return pyzbar.decode(image)

