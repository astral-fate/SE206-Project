"""
Utility functions for handling PDF files and text extraction.
This file provides a centralized location for PDF-related functionality and
handles graceful fallback when dependencies are not available.
"""

import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import PyMuPDF, providing graceful fallback if not available
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
    logger.info("PyMuPDF (fitz) is available for PDF text extraction")
except ImportError:
    PYMUPDF_AVAILABLE = False
    logger.warning("PyMuPDF not installed. PDF text extraction will be limited.")
    logger.warning("Install with: pip install PyMuPDF")

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text or empty string if extraction fails
    """
    if not PYMUPDF_AVAILABLE:
        logger.error("Cannot extract text: PyMuPDF not available")
        return ""
    
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return ""
    
    try:
        text = ""
        doc = fitz.open(file_path)
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        return ""

def get_file_text(file_path):
    """
    Get text from a file, handling different file types.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: Extracted text or empty string if extraction fails
        bool: Whether extraction was successful
    """
    if not os.path.exists(file_path):
        return "", False
    
    try:
        # For PDF files
        if file_path.lower().endswith('.pdf'):
            if PYMUPDF_AVAILABLE:
                text = extract_text_from_pdf(file_path)
                success = len(text.strip()) > 50
                return text, success
            else:
                return "", False
        # For text files
        elif file_path.lower().endswith(('.txt', '.text', '.md')):
            with open(file_path, 'r', errors='ignore') as f:
                text = f.read()
                success = len(text.strip()) > 0
                return text, success
        else:
            logger.warning(f"Unsupported file type: {file_path}")
            return "", False
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {str(e)}")
        return "", False
