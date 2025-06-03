# src/utils/file_handler.py
import os
import shutil
from typing import List
from pathlib import Path

class FileHandler:
    """Utility class for file operations"""
    
    @staticmethod
    def ensure_directory_exists(directory_path: str):
        """Create directory if it doesn't exist"""
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        
    @staticmethod
    def get_pdf_files(directory_path: str) -> List[str]:
        """Get list of PDF files in directory"""
        pdf_files = []
        if os.path.exists(directory_path):
            for root, dirs, files in os.walk(directory_path):
                for file in files:
                    if file.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(root, file))
        return pdf_files
        
    @staticmethod
    def copy_file(source_path: str, destination_path: str):
        """Copy file from source to destination"""
        FileHandler.ensure_directory_exists(os.path.dirname(destination_path))
        shutil.copy2(source_path, destination_path)
        
    @staticmethod
    def save_text_file(content: str, file_path: str):
        """Save text content to file"""
        FileHandler.ensure_directory_exists(os.path.dirname(file_path))
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    @staticmethod
    def read_text_file(file_path: str) -> str:
        """Read text content from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""