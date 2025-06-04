# src/utils/text_preprocessor.py
import re
from typing import List

class TextPreprocessor:
    """Text cleaning and preprocessing utilities"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
            
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep alphanumeric and basic punctuation
        text = re.sub(r'[^\w\s\.\,\-\@\(\)]', '', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
        
    @staticmethod
    def normalize_keywords(keywords: List[str]) -> List[str]:
        """Normalize list of keywords"""
        normalized = []
        for keyword in keywords:
            if keyword and keyword.strip():
                # Clean and convert to lowercase
                clean_keyword = TextPreprocessor.clean_text(keyword.strip().lower())
                if clean_keyword:
                    normalized.append(clean_keyword)
        return normalized
        
    @staticmethod
    def extract_words(text: str) -> List[str]:
        """Extract individual words from text"""
        if not text:
            return []
            
        # Split on whitespace and punctuation
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if len(word) > 2]  # Filter short words