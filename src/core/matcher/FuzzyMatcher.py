from typing import List, Dict, Tuple
from .Levenshtein import LevenshteinMatcher
import re

class FuzzyMatcher:
    """Fuzzy matching coordinator using Levenshtein distance"""
    
    def __init__(self, similarity_threshold: float = 0.7):
        self.similarity_threshold = similarity_threshold
        self.levenshtein = LevenshteinMatcher()
    
    def extract_words_from_text(self, text: str) -> List[str]:
        """Extract unique words from text"""
        if not text:
            return []
        
        words = re.findall(r'\b\w+\b', text.lower())
        return list(set(words))  # Remove duplicates
    
    def fuzzy_match_keywords(self, keywords: List[str], text: str) -> Dict[str, List[Tuple[str, float]]]:
        """Find fuzzy matches for keywords in text
        
        Args:
            keywords: List of keywords to search for
            text: Text to search in
            
        Returns:
            Dictionary mapping keyword to list of (matched_word, similarity) tuples
        """
        results = {}
        text_words = self.extract_words_from_text(text)
        
        for keyword in keywords:
            keyword_clean = keyword.strip().lower()
            if not keyword_clean:
                continue
            
            matches = self.levenshtein.find_similar_words(
                keyword_clean, 
                text_words, 
                self.similarity_threshold
            )
            
            if matches:
                results[keyword] = matches
        
        return results
    
    def calculate_fuzzy_score(self, keywords: List[str], text: str) -> Dict[str, float]:
        """Calculate fuzzy matching score for each keyword
        
        Args:
            keywords: List of keywords to match
            text: Text to search in
            
        Returns:
            Dictionary mapping keyword to best similarity score
        """
        fuzzy_matches = self.fuzzy_match_keywords(keywords, text)
        scores = {}
        
        for keyword in keywords:
            if keyword in fuzzy_matches and fuzzy_matches[keyword]:
                # Take the best similarity score
                best_match = max(fuzzy_matches[keyword], key=lambda x: x[1])
                scores[keyword] = best_match[1]
            else:
                scores[keyword] = 0.0
        
        return scores
    
    def get_total_fuzzy_score(self, keywords: List[str], text: str) -> float:
        """Calculate total fuzzy matching score
        
        Args:
            keywords: List of keywords to match
            text: Text to search in
            
        Returns:
            Total fuzzy score (sum of individual scores)
        """
        scores = self.calculate_fuzzy_score(keywords, text)
        return sum(scores.values())