"""
    # Commit 14: 2025-11-25 12:12:52
    # Commit 25: 2025-11-25 12:12:55
Image processing utilities for barcode decoding
    # Commit 2: 2025-11-25 12:12:48
"""
import cv2
import numpy as np
    # Commit 21: 2025-11-25 12:12:54
from PIL import Image
from typing import Union, Tuple
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Image preprocessing and enhancement for barcode decoding"""
    
    def __init__(self):
        """Initialize the image processor"""
        pass
    
    def preprocess(self, image_path: str, enhance: bool = False) -> np.ndarray:
        """
        Preprocess image for barcode decoding
        
        Args:
            image_path: Path to image file
            enhance: Whether to apply enhancement
        
        Returns:
            Preprocessed image as numpy array
        """
        try:
            # Load image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image: {image_path}")
            
            # Convert to grayscale
            if len(img.shape) == 3:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img.copy()
            
            # Apply enhancement if requested
            if enhance:
                gray = self.enhance_image(gray)
            
            return gray
        
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    def enhance_image(self, image: np.ndarray) -> np.ndarray:
        """
        Enhance image for better barcode detection
        
        Args:
            image: Grayscale image as numpy array
        
        Returns:
            Enhanced image
        """
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
        
        # Reduce noise
        denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
        
        # Sharpen
        kernel = np.array([[-1, -1, -1],
                          [-1,  9, -1],
                          [-1, -1, -1]])
        sharpened = cv2.filter2D(denoised, -1, kernel)
        
        return sharpened
    
    def adjust_contrast(self, image: np.ndarray, alpha: float = 1.5) -> np.ndarray:
        """Adjust image contrast"""
        return cv2.convertScaleAbs(image, alpha=alpha, beta=0)
    
    def adjust_brightness(self, image: np.ndarray, beta: int = 30) -> np.ndarray:
        """Adjust image brightness"""
        return cv2.convertScaleAbs(image, alpha=1.0, beta=beta)
    
    def resize_image(self, image: np.ndarray, 
                    max_dimension: int = 2000) -> np.ndarray:
        """
        Resize image if it's too large
        
        Args:
            image: Input image
            max_dimension: Maximum dimension (width or height)
        
        Returns:
            Resized image
        """
        height, width = image.shape[:2]
        max_size = max(height, width)
        
        if max_size > max_dimension:
            scale = max_dimension / max_size
            new_width = int(width * scale)
            new_height = int(height * scale)
            return cv2.resize(image, (new_width, new_height), 
                            interpolation=cv2.INTER_AREA)
        
        return image
    
    def rotate_image(self, image: np.ndarray, angle: float) -> np.ndarray:
        """Rotate image by specified angle"""
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, rotation_matrix, (width, height),
                                flags=cv2.INTER_LINEAR,
                                borderMode=cv2.BORDER_REPLICATE)
        
        return rotated
    
    def apply_threshold(self, image: np.ndarray, 
                       method: str = 'adaptive') -> np.ndarray:
        """
        Apply threshold to image
        
        Args:
            image: Input grayscale image
            method: 'adaptive' or 'otsu'
        
        Returns:
            Binary image
        """
        if method == 'adaptive':
            return cv2.adaptiveThreshold(
                image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        elif method == 'otsu':
            _, binary = cv2.threshold(
                image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
            return binary
        else:
            raise ValueError(f"Unknown threshold method: {method}")

