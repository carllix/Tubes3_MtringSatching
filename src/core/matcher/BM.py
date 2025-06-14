from typing import List, Dict

class BoyerMooreMatcher:
    """Boyer-Moore string matching algorithm implementation"""
    
    @staticmethod
    def build_bad_character_table(pattern: str) -> Dict[str, int]:
        """Build bad character table using last occurrence for Boyer-Moore algorithm"""
        table = {}
        m = len(pattern)
        
        # Store the rightmost occurrence of each character
        for i in range(m):
            table[pattern[i]] = i
        
        return table
    
    @staticmethod
    def build_good_suffix_table(pattern: str) -> List[int]:
        """Build good suffix table for Boyer-Moore algorithm"""
        m = len(pattern)
        good_suffix = [m] * m
        
        # Compute border array
        border = [0] * m
        i = m
        j = m + 1
        border[i - 1] = j
        
        while i > 1:
            while j <= m and pattern[i - 1] != pattern[j - 1]:
                if good_suffix[j - 1] == m:
                    good_suffix[j - 1] = j - i
                j = border[j - 1]
            i -= 1
            j -= 1
            border[i - 1] = j
        
        # Fill remaining entries
        j = border[0]
        for i in range(m):
            if good_suffix[i] == m:
                good_suffix[i] = j
            if i == j:
                j = border[j]
        
        return good_suffix
    
    @staticmethod
    def search(text: str, pattern: str) -> List[int]:
        """Search for pattern in text using Boyer-Moore algorithm
        
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
        n = len(text)
        m = len(pattern)
        
        if m > n:
            return matches
        
        # Build tables
        bad_char = BoyerMooreMatcher.build_bad_character_table(pattern)
        good_suffix = BoyerMooreMatcher.build_good_suffix_table(pattern)
        
        i = 0  # text index
        
        while i <= n - m:
            j = m - 1  # pattern index (start from end)
            
            # Match pattern from right to left
            while j >= 0 and pattern[j] == text[i + j]:
                j -= 1
            
            if j < 0:
                # Pattern found
                matches.append(i)
                # Use good suffix rule for next shift
                i += good_suffix[0] if good_suffix[0] > 0 else 1
            else:
                # Mismatch occurred at position j
                # Calculate bad character shift
                mismatched_char = text[i + j]
                
                if mismatched_char in bad_char:
                    # Shift based on last occurrence
                    bad_char_shift = max(1, j - bad_char[mismatched_char])
                else:
                    # Character not in pattern, shift by pattern length
                    bad_char_shift = j + 1
                
                good_suffix_shift = good_suffix[j]
                i += max(bad_char_shift, good_suffix_shift)
        
        return matches
    
    @staticmethod
    def count_occurrences(text: str, pattern: str) -> int:
        """Count the number of occurrences of pattern in text"""
        return len(BoyerMooreMatcher.search(text, pattern))
