"""
Tests for image processor
"""
import unittest
import numpy as np
from utils.image_processor import ImageProcessor


class TestImageProcessor(unittest.TestCase):
    """Test cases for ImageProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = ImageProcessor()
    
    def test_processor_initialization(self):
        """Test processor initialization"""
        self.assertIsNotNone(self.processor)
    
    def test_adjust_contrast(self):
        """Test contrast adjustment"""
        test_image = np.ones((100, 100), dtype=np.uint8) * 128
        result = self.processor.adjust_contrast(test_image, alpha=1.5)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, test_image.shape)
    
    def test_adjust_brightness(self):
        """Test brightness adjustment"""
        test_image = np.ones((100, 100), dtype=np.uint8) * 128
        result = self.processor.adjust_brightness(test_image, beta=30)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, test_image.shape)
    
    def test_resize_image(self):
        """Test image resizing"""
        test_image = np.zeros((2000, 2000), dtype=np.uint8)
        result = self.processor.resize_image(test_image, max_dimension=1000)
        self.assertLessEqual(max(result.shape), 1000)
    
    def test_apply_threshold_adaptive(self):
        """Test adaptive threshold"""
        test_image = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        result = self.processor.apply_threshold(test_image, method='adaptive')
        self.assertIsInstance(result, np.ndarray)
        # Binary image should only have 0 and 255
        unique_values = np.unique(result)
        self.assertTrue(all(v in [0, 255] for v in unique_values))
    
    def test_apply_threshold_otsu(self):
        """Test Otsu threshold"""
        test_image = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        result = self.processor.apply_threshold(test_image, method='otsu')
        self.assertIsInstance(result, np.ndarray)
        unique_values = np.unique(result)
        self.assertTrue(all(v in [0, 255] for v in unique_values))


if __name__ == '__main__':
    unittest.main()

