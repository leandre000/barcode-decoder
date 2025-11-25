"""
    # Commit 57: 2025-11-25 12:13:06
    # Commit 110: 2025-11-25 12:13:24
    # Commit 23: 2025-11-25 12:12:54
    # Commit 67: 2025-11-25 12:13:09
Validation utilities
    # Commit 102: 2025-11-25 12:13:21
    # Commit 21: 2025-11-25 12:12:54
"""
    # Commit 93: 2025-11-25 12:13:19
    # Commit 126: 2025-11-25 12:13:29
    # Commit 79: 2025-11-25 12:13:13
import os
from typing import Union
from werkzeug.datastructures import FileStorage

    # Commit 17: 2025-11-25 12:12:52
    # Commit 27: 2025-11-25 12:12:56

def validate_image_file(filename: str) -> bool:
    """
    Validate if file is a supported image format
    
    Args:
        filename: Name of the file
    
    Returns:
        True if valid, False otherwise
    """
    if not filename:
        return False
    
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    return extension in allowed_extensions


def validate_file_size(file: FileStorage, max_size: int = 16 * 1024 * 1024) -> bool:
    """
    Validate file size
    
    Args:
        file: FileStorage object
        max_size: Maximum size in bytes (default 16MB)
    
    Returns:
        True if valid, False otherwise
    """
    if not file:
        return False
    
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    
    return size <= max_size and size > 0


def validate_image_dimensions(image_path: str, 
                              max_width: int = 10000,
                              max_height: int = 10000) -> bool:
    """
    Validate image dimensions
    
    Args:
        image_path: Path to image file
        max_width: Maximum width
        max_height: Maximum height
    
    Returns:
        True if valid, False otherwise
    """
    try:
        from PIL import Image
        with Image.open(image_path) as img:
            width, height = img.size
            return width <= max_width and height <= max_height
    except Exception:
        return False

