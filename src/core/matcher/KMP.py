from typing import List

class KMPMatcher:
    """Knuth-Morris-Pratt string matching algorithm implementation"""
    
    @staticmethod
    def build_failure_function(pattern: str) -> List[int]:
        """Build the failure function (border array) for KMP algorithm
        Border: longest proper prefix which is also a suffix"""
        if not pattern:
            return []
            
        m = len(pattern)
        failure = [0] * m
        
        # failure[0] is always 0 (no proper prefix for single character)
        j = 0  # length of previous longest prefix suffix
        
        # Calculate failure[i] for i = 1 to m-1
        for i in range(1, m):
            # pattern[i] doesn't match pattern[j]
            while j > 0 and pattern[i] != pattern[j]:
                j = failure[j - 1]
            
            # pattern[i] matches pattern[j]
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
        
        n = len(text)
        m = len(pattern)
        
        if m > n:
            return []
        
        matches = []
        failure = KMPMatcher.build_failure_function(pattern)
        
        i = 0  # index for text
        j = 0  # index for pattern
        
        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1
            
            if j == m:
                # Found a match
                matches.append(i - j)
                j = failure[j - 1]  # Get next position to check
            elif i < n and pattern[j] != text[i]:
                # Mismatch after j matches
                if j != 0:
                    j = failure[j - 1]
                else:
                    i += 1
        
        return matches
    
    @staticmethod
    def count_occurrences(text: str, pattern: str) -> int:
        """Count the number of occurrences of pattern in text"""
        return len(KMPMatcher.search(text, pattern))
