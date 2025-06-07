import os
import re
import PyPDF2
from typing import Dict, List, Optional
from src.utils.file.FileHandler import FileHandler
from src.utils.file.TextPreprocessor import TextPreprocessor

class CVProcessor:
    """CV processing utilities for extracting text from PDF files"""
    
    def __init__(self):
        self.file_handler = FileHandler()
        self.text_preprocessor = TextPreprocessor()
    
    def sanitize_filename(self, filename: str) -> str:
        """Sanitize filename by removing invalid characters"""
        # Remove invalid characters for filename
        return re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    def extract_text_pypdf2(self, pdf_path: str) -> str:
        """Extract text from PDF using PyPDF2"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting text with PyPDF2 from {pdf_path}: {e}")
            return ""
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file using PyPDF2
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Extracted text content
        """
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            return ""
        
        # Extract text using PyPDF2
        text = self.extract_text_pypdf2(pdf_path)
        
        # Clean the extracted text
        if text:
            text = self.text_preprocessor.clean_text(text)
        
        return text
    
    def process_cv_file(self, pdf_path: str, save_extracted: bool = True, output_dir: str = None) -> str:
        """Process a single CV file and optionally save extracted text
        
        Args:
            pdf_path: Path to PDF file
            save_extracted: Whether to save extracted text to file
            output_dir: Directory to save extracted text files
            
        Returns:
            Extracted text content
        """
        # Extract text from PDF
        text = self.extract_text_from_pdf(pdf_path)
        
        if not text:
            print(f"No text extracted from {pdf_path}")
            return ""
        
        # Save extracted text if requested
        if save_extracted and output_dir:
            filename = os.path.basename(pdf_path)
            name_without_ext = os.path.splitext(filename)[0]
            text_filename = f"{self.sanitize_filename(name_without_ext)}.txt"
            text_path = os.path.join(output_dir, text_filename)
            
            self.file_handler.save_text_file(text, text_path)
            print(f"Saved extracted text to: {text_path}")
        
        return text
    
    def process_cv_directory(self, directory_path: str, save_extracted: bool = True, 
                           output_dir: str = None) -> Dict[str, str]:
        """Process all CV files in a directory
        
        Args:
            directory_path: Directory containing PDF files
            save_extracted: Whether to save extracted text files
            output_dir: Directory to save extracted text files
            
        Returns:
            Dictionary mapping filename to extracted text
        """
        if not os.path.exists(directory_path):
            print(f"Directory not found: {directory_path}")
            return {}
        
        # Get all PDF files
        pdf_files = self.file_handler.get_pdf_files(directory_path)
        
        if not pdf_files:
            print(f"No PDF files found in: {directory_path}")
            return {}
        
        # Setup output directory if saving
        if save_extracted and output_dir:
            self.file_handler.ensure_directory_exists(output_dir)
        
        cv_texts = {}
        processed_count = 0
        
        print(f"Processing {len(pdf_files)} CV files...")
        
        for pdf_path in pdf_files:
            filename = os.path.basename(pdf_path)
            print(f"Processing: {filename}")
            
            text = self.process_cv_file(
                pdf_path, 
                save_extracted=save_extracted, 
                output_dir=output_dir
            )
            
            if text:
                cv_texts[filename] = text
                processed_count += 1
            else:
                print(f"Failed to extract text from: {filename}")
        
        print(f"Successfully processed {processed_count}/{len(pdf_files)} CV files")
        return cv_texts
    
    def get_cv_statistics(self, cv_texts: Dict[str, str]) -> Dict[str, any]:
        """Get statistics about processed CV texts
        
        Args:
            cv_texts: Dictionary of CV texts
            
        Returns:
            Dictionary containing statistics
        """
        if not cv_texts:
            return {}
        
        total_files = len(cv_texts)
        total_words = 0
        total_chars = 0
        word_counts = []
        
        for filename, text in cv_texts.items():
            words = self.text_preprocessor.extract_words(text)
            word_count = len(words)
            char_count = len(text)
            
            total_words += word_count
            total_chars += char_count
            word_counts.append(word_count)
        
        avg_words = total_words / total_files if total_files > 0 else 0
        avg_chars = total_chars / total_files if total_files > 0 else 0
        
        return {
            'total_files': total_files,
            'total_words': total_words,
            'total_characters': total_chars,
            'average_words_per_cv': avg_words,
            'average_characters_per_cv': avg_chars,
            'min_words': min(word_counts) if word_counts else 0,
            'max_words': max(word_counts) if word_counts else 0
        }
