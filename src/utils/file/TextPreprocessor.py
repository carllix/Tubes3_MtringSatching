# src/utils/text_preprocessor.py
import re
from typing import List

class TextPreprocessor:
    """Text cleaning and preprocessing utilities"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text while preserving document structure"""
        if not text:
            return ""
        
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            cleaned_line = re.sub(r'[ \t]+', ' ', line.strip())
            cleaned_lines.append(cleaned_line)
        
        text = '\n'.join(cleaned_lines)
        
        text = re.sub(r'[^\w\s\.\,\-\@\(\)\:\;\!\?\'\"\n\&\%\/\+\*\=\[\]]', '', text)
        
        text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces/tabs jdi single space
        text = re.sub(r' \n', '\n', text)    # Hapus spaces sblm newlines
        text = re.sub(r'\n ', '\n', text)    # Hapus spaces stlh newlines
        
        return text.strip()
    
    @staticmethod
    def clean_text_for_search(text: str) -> str:
        """Clean text specifically for pattern matching (removes formatting)"""
        if not text:
            return ""
            
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s\.\,\-\@\(\)]', '', text)
        
        return text.strip()
        
    @staticmethod
    def normalize_keywords(keywords: List[str]) -> List[str]:
        """Normalize list of keywords"""
        normalized = []
        for keyword in keywords:
            if keyword and keyword.strip():
                clean_keyword = TextPreprocessor.clean_text(keyword.strip().lower())
                if clean_keyword:
                    normalized.append(clean_keyword)
        return normalized
        
    @staticmethod
    def extract_words(text: str) -> List[str]:
        """Extract individual words from text"""
        if not text:
            return []
            
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if len(word) > 2]  # Filter short words