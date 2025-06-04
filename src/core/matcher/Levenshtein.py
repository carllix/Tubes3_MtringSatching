from typing import List, Tuple

class LevenshteinMatcher:
    """Levenshtein distance algorithm for fuzzy string matching"""
    
    @staticmethod
    def distance(s1: str, s2: str) -> int:
        """Calculate Levenshtein distance between two strings
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            Levenshtein distance (number of edits needed)
        """
        if not s1:
            return len(s2)
        if not s2:
            return len(s1)
        
        # Convert to lowercase for case-insensitive comparison
        s1 = s1.lower()
        s2 = s2.lower()
        
        # Create matrix
        rows = len(s1) + 1
        cols = len(s2) + 1
        dp = [[0] * cols for _ in range(rows)]
        
        # Initialize first row and column
        for i in range(rows):
            dp[i][0] = i
        for j in range(cols):
            dp[0][j] = j
        
        # Fill the matrix
        for i in range(1, rows):
            for j in range(1, cols):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i-1][j],      # deletion
                        dp[i][j-1],      # insertion
                        dp[i-1][j-1]     # substitution
                    )
        
        return dp[rows-1][cols-1]
    
    @staticmethod
    def similarity_ratio(s1: str, s2: str) -> float:
        """Calculate similarity ratio between two strings (0.0 to 1.0)
        
        Args:
            s1: First string
            s2: Second string
            
        Returns:
            Similarity ratio where 1.0 means identical strings
        """
        if not s1 and not s2:
            return 1.0
        if not s1 or not s2:
            return 0.0
        
        max_len = max(len(s1), len(s2))
        distance = LevenshteinMatcher.distance(s1, s2)
        return 1.0 - (distance / max_len)
    
    @staticmethod
    def find_similar_words(target: str, word_list: List[str], threshold: float = 0.7) -> List[Tuple[str, float]]:
        """Find words similar to target word based on Levenshtein distance
        
        Args:
            target: Target word to match against
            word_list: List of words to search in
            threshold: Minimum similarity ratio (0.0 to 1.0)
            
        Returns:
            List of (word, similarity_ratio) tuples sorted by similarity
        """
        matches = []
        
        for word in word_list:
            ratio = LevenshteinMatcher.similarity_ratio(target, word)
            if ratio >= threshold:
                matches.append((word, ratio))
        
        # Sort by similarity ratio (descending)
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
    
    @staticmethod
    def fuzzy_search_in_text(pattern: str, text: str, threshold: float = 0.7) -> List[Tuple[str, float, int]]:
        """Find fuzzy matches of pattern in text
        
        Args:
            pattern: Pattern to search for
            text: Text to search in
            threshold: Minimum similarity ratio
            
        Returns:
            List of (matched_word, similarity_ratio, position) tuples
        """
        if not pattern or not text:
            return []
        
        # Extract words from text
        import re
        words = re.findall(r'\b\w+\b', text.lower())
        matches = []
        
        for i, word in enumerate(words):
            ratio = LevenshteinMatcher.similarity_ratio(pattern.lower(), word)
            if ratio >= threshold:
                # Find position in original text
                position = text.lower().find(word)
                matches.append((word, ratio, position))
        
        # Sort by similarity ratio (descending)
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches
