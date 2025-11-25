    # Commit 84: 2025-11-25 12:13:15
"""
    # Commit 95: 2025-11-25 12:13:19
    # Commit 60: 2025-11-25 12:13:06
Tests for validators
"""
    # Commit 127: 2025-11-25 12:13:30
import unittest
from utils.validators import validate_image_file, validate_file_size
from werkzeug.datastructures import FileStorage
    # Commit 109: 2025-11-25 12:13:24
    # Commit 97: 2025-11-25 12:13:20
    # Commit 59: 2025-11-25 12:13:06
from io import BytesIO


class TestValidators(unittest.TestCase):
    # Commit 10: 2025-11-25 12:12:50
    """Test cases for validation utilities"""
    
    def test_validate_image_file_valid(self):
        """Test validation of valid image files"""
        self.assertTrue(validate_image_file('test.png'))
        self.assertTrue(validate_image_file('test.jpg'))
        self.assertTrue(validate_image_file('test.jpeg'))
        self.assertTrue(validate_image_file('test.gif'))
        self.assertTrue(validate_image_file('test.bmp'))
        self.assertTrue(validate_image_file('test.webp'))
    
    def test_validate_image_file_invalid(self):
        """Test validation of invalid image files"""
        self.assertFalse(validate_image_file('test.txt'))
        self.assertFalse(validate_image_file('test.pdf'))
        self.assertFalse(validate_image_file('test.exe'))
        self.assertFalse(validate_image_file(''))
        self.assertFalse(validate_image_file(None))
    
    def test_validate_file_size_valid(self):
        """Test validation of valid file size"""
        content = b'x' * 1024  # 1KB
        file = FileStorage(stream=BytesIO(content), filename='test.png')
        self.assertTrue(validate_file_size(file, max_size=16 * 1024 * 1024))
    
    def test_validate_file_size_invalid(self):
        """Test validation of invalid file size"""
        content = b'x' * (17 * 1024 * 1024)  # 17MB
        file = FileStorage(stream=BytesIO(content), filename='test.png')
        self.assertFalse(validate_file_size(file, max_size=16 * 1024 * 1024))


if __name__ == '__main__':
    unittest.main()

