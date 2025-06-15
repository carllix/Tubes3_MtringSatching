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

    def get_best_matches(self, keywords: List[str], text: str) -> Dict[str, List[Tuple[str, float]]]:
        """
        Finds the best fuzzy matches for keywords, including all ties.

        If multiple words share the same highest similarity score for a given
        keyword, all of them are returned.

        Args:
            keywords: A list of keywords to search for.
            text: The text to search within.

        Returns:
            A dictionary where each key is a keyword and the value is a list
            of its best matches, each as a (word, score) tuple.
        """
        all_matches = self.fuzzy_match_keywords(keywords, text)
        best_matches_result = {}

        for keyword, matches in all_matches.items():
            if not matches:
                continue

            # The first match has the highest score because find_similar_words sorts them
            highest_score = matches[0][1]

            # Filter for all other matches that have the same top score
            top_matches = [match for match in matches if match[1] == highest_score]
            
            if top_matches:
                best_matches_result[keyword] = top_matches
                
        return best_matches_result
    
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