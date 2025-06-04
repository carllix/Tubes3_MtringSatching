from typing import List

class KMPMatcher:
    """Knuth-Morris-Pratt string matching algorithm implementation"""
    
    @staticmethod
    def build_failure_function(pattern: str) -> List[int]:
        """Build the failure function (partial match table) for KMP algorithm"""
        if not pattern:
            return []
            
        failure = [0] * len(pattern)
        j = 0
        
        for i in range(1, len(pattern)):
            while j > 0 and pattern[i] != pattern[j]:
                j = failure[j - 1]
            
            if pattern[i] == pattern[j]:
                j += 1
            
            failure[i] = j
        
        return failure
    
    @staticmethod
    def search(text: str, pattern: str) -> List[int]:
        """Search for pattern in text using KMP algorithm
        
        Args:
            text: The text to search in
            pattern: The pattern to search for
            
        Returns:
            List of starting indices where pattern is found
        """
        if not text or not pattern:
            return []
        
        # Convert to lowercase for case-insensitive matching
        text = text.lower()
        pattern = pattern.lower()
        
        matches = []
        failure = KMPMatcher.build_failure_function(pattern)
        
        i = 0  # text index
        j = 0  # pattern index
        
        while i < len(text):
            if text[i] == pattern[j]:
                i += 1
                j += 1
                
                if j == len(pattern):
                    matches.append(i - j)
                    j = failure[j - 1]
            else:
                if j > 0:
                    j = failure[j - 1]
                else:
                    i += 1
        
        return matches
    
    @staticmethod
    def count_occurrences(text: str, pattern: str) -> int:
        """Count the number of occurrences of pattern in text"""
        return len(KMPMatcher.search(text, pattern))
