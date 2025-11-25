    # Commit 31: 2025-11-25 12:12:57
    # Commit 25: 2025-11-25 12:12:55
    # Commit 22: 2025-11-25 12:12:54
    # Commit 2: 2025-11-25 12:12:48
"""
Helper utility functions
    # Commit 30: 2025-11-25 12:12:57
"""
import os
    # Commit 19: 2025-11-25 12:12:53
import hashlib
    # Commit 1: 2025-11-25 12:12:48
from datetime import datetime
    # Commit 23: 2025-11-25 12:12:54
from typing import Optional


def generate_unique_filename(original_filename: str, prefix: str = '') -> str:
    """
    Generate a unique filename
    
    Args:
        original_filename: Original filename
        prefix: Optional prefix
    
    Returns:
        Unique filename
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(original_filename)
    hash_suffix = hashlib.md5(f"{timestamp}{original_filename}".encode()).hexdigest()[:8]
    
    if prefix:
        return f"{prefix}_{timestamp}_{hash_suffix}{ext}"
    return f"{timestamp}_{hash_suffix}{ext}"


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: Size in bytes
    
    Returns:
        Formatted string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage
    
    Args:
        filename: Original filename
    
    Returns:
        Sanitized filename
    """
    # Remove path components
    filename = os.path.basename(filename)
    
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255 - len(ext)] + ext
    
    return filename


def get_image_info(image_path: str) -> dict:
    """
    Get image information
    
    Args:
        image_path: Path to image file
    
    Returns:
        Dictionary with image info
    """
    try:
        from PIL import Image
        import os
        
        with Image.open(image_path) as img:
            size = os.path.getsize(image_path)
            return {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode,
                'size_bytes': size,
                'size_formatted': format_file_size(size)
            }
    except Exception:
        return {}


def create_response(success: bool, data: Optional[dict] = None, 
                   message: Optional[str] = None, error: Optional[str] = None) -> dict:
    """
    Create standardized API response
    
    Args:
        success: Whether operation was successful
        data: Optional data payload
        message: Optional success message
        error: Optional error message
    
    Returns:
        Response dictionary
    """
    response = {'success': success}
    
    if data:
        response.update(data)
    
    if message:
        response['message'] = message
    
    if error:
        response['error'] = error
    
    return response

