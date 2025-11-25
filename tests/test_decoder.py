    # Commit 66: 2025-11-25 12:13:09
    # Commit 2: 2025-11-25 12:12:48
    # Commit 37: 2025-11-25 12:12:59
    # Commit 5: 2025-11-25 12:12:49
"""
Tests for barcode decoder
    # Commit 58: 2025-11-25 12:13:06
    # Commit 9: 2025-11-25 12:12:50
    # Commit 71: 2025-11-25 12:13:10
"""
import unittest
import numpy as np
from decoders.barcode_decoder import BarcodeDecoder


class TestBarcodeDecoder(unittest.TestCase):
    """Test cases for BarcodeDecoder class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.decoder = BarcodeDecoder()
    
    def test_decoder_initialization(self):
        """Test decoder initialization"""
        self.assertIsNotNone(self.decoder)
        self.assertIsInstance(self.decoder.supported_formats, list)
        self.assertGreater(len(self.decoder.supported_formats), 0)
    
    def test_get_supported_formats(self):
        """Test getting supported formats"""
        formats = self.decoder.get_supported_formats()
        self.assertIsInstance(formats, list)
        self.assertIn('AZTEC', formats)
        self.assertIn('DATA_MATRIX', formats)
    
    def test_prepare_image_from_array(self):
        """Test image preparation from numpy array"""
        test_image = np.zeros((100, 100), dtype=np.uint8)
        result = self.decoder._prepare_image(test_image)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (100, 100))
    
    def test_prepare_image_grayscale_conversion(self):
        """Test grayscale conversion"""
        # Create a 3-channel image
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        result = self.decoder._prepare_image(test_image)
        self.assertEqual(len(result.shape), 2)  # Should be grayscale
    
    def test_decode_empty_image(self):
        """Test decoding empty image"""
        empty_image = np.zeros((100, 100), dtype=np.uint8)
        results = self.decoder.decode(empty_image)
        self.assertIsInstance(results, list)


if __name__ == '__main__':
    unittest.main()

