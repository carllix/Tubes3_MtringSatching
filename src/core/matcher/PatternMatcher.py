from typing import List, Dict, Tuple, Any
import time
from .KMP import KMPMatcher
from .BM import BoyerMooreMatcher
from .FuzzyMatcher import FuzzyMatcher
from .AhoCorasick import AhoCorasick

class PatternMatcher:
    """Main pattern matching coordinator for ATS system"""
    
    def __init__(self, fuzzy_threshold: float = 0.7):
        self.kmp = KMPMatcher()
        self.bm = BoyerMooreMatcher()
        self.fuzzy_matcher = FuzzyMatcher(fuzzy_threshold)
    
    def exact_match_keywords(self, keywords: List[str], text: str, algorithm: str = "KMP") -> Dict[str, int]:
        """Perform exact matching of keywords in text
        
        Args:
            keywords: List of keywords to search for
            text: Text to search in
            algorithm: Algorithm to use ("KMP", "BM", or "AC")
            
        Returns:
            Dictionary mapping keyword to occurrence count
        """
        results = {}
        
        # Aho-Corasick
        if algorithm.upper() == "AC":
            clean_lowercase_keywords = []
            lowercase_to_original = {}
            
            for keyword in keywords:
                keyword_clean = keyword.strip()
                if not keyword_clean:
                    continue
                
                lowercase = keyword_clean.lower()
                clean_lowercase_keywords.append(lowercase)
                lowercase_to_original[lowercase] = keyword
            
            ac = AhoCorasick(clean_lowercase_keywords)
            
            matches = ac.search(text.lower())
            
            for keyword_lower, positions in matches.items():
                original_keyword = lowercase_to_original[keyword_lower]
                count = len(positions)
                results[original_keyword] = count
                
            for keyword in keywords:
                if keyword not in results:
                    results[keyword] = 0
            
            return results
        
        # KMP and BM algorithms
        for keyword in keywords:
            keyword_clean = keyword.strip()
            if not keyword_clean:
                continue
            
            if algorithm.upper() == "KMP":
                count = self.kmp.count_occurrences(text, keyword_clean)
            elif algorithm.upper() == "BM":
                count = self.bm.count_occurrences(text, keyword_clean)
            else:
                raise ValueError(f"Unknown algorithm: {algorithm}")
            
            results[keyword] = count
        
        return results
    
    def search_single_cv(self, keywords: List[str], cv_text: str, algorithm: str = "KMP", cv_file: str = "") -> Dict[str, Any]:
        """Search keywords in a single CV text
        
        Args:
            keywords: List of keywords to search for
            cv_text: CV text content
            algorithm: Algorithm to use for exact matching
            cv_file: CV filename for debug output
            
        Returns:
            Dictionary containing match results and timing info
        """
        
        start_time = time.time()
        exact_matches = self.exact_match_keywords(keywords, cv_text, algorithm)
        exact_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        unmatched_keywords = [k for k, count in exact_matches.items() if count == 0]
        
        start_time = time.time()
        fuzzy_scores = {}
        fuzzy_matches_detail = {}
        if unmatched_keywords:
            fuzzy_scores = self.fuzzy_matcher.calculate_fuzzy_score(unmatched_keywords, cv_text)
            fuzzy_matches_detail = self.fuzzy_matcher.fuzzy_match_keywords(unmatched_keywords, cv_text)
            
        fuzzy_time = (time.time() - start_time) * 1000
        
        total_exact_matches = sum(exact_matches.values())
        total_fuzzy_score = sum(fuzzy_scores.values())
        combined_score = total_exact_matches + (total_fuzzy_score * 0.5)  # Weight fuzzy matches lower
        
        
        return {
            'exact_matches': exact_matches,
            'fuzzy_matches': fuzzy_scores,
            'fuzzy_matches_detail': fuzzy_matches_detail,
            'total_exact_matches': total_exact_matches,
            'total_fuzzy_score': total_fuzzy_score,
            'combined_score': combined_score,
            'matched_keywords': {
                'exact': [k for k, count in exact_matches.items() if count > 0],
                'fuzzy': [k for k, score in fuzzy_scores.items() if score > 0]
            },
            'timing': {
                'exact_match_time': exact_time,
                'fuzzy_match_time': fuzzy_time
            }
        }
    
    def search_multiple_cvs(self, keywords: List[str], cv_texts: Dict[str, str], 
                        algorithm: str = "KMP", top_n: int = 10) -> Tuple[List[Dict], Dict]:
        """Search keywords across multiple CV texts
        
        Args:
            keywords: List of keywords to search for
            cv_texts: Dictionary mapping CV filename to text content
            algorithm: Algorithm to use for exact matching
            top_n: Number of top results to return
            
        Returns:
            Tuple of (results_list, timing_info)
        """
        
        results = []
        total_exact_time = 0
        total_fuzzy_time = 0
        
        for cv_file, cv_text in cv_texts.items():
            result = self.search_single_cv(keywords, cv_text, algorithm, cv_file)
            
            result['cv_file'] = cv_file
            results.append(result)
            
            total_exact_time += result['timing']['exact_match_time']
            total_fuzzy_time += result['timing']['fuzzy_match_time']
        
        results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        top_results = results[:top_n]
        
        timing_info = {
            'total_exact_match_time': total_exact_time,
            'total_fuzzy_match_time': total_fuzzy_time,
            'average_exact_match_time': total_exact_time / len(cv_texts) if cv_texts else 0,
            'average_fuzzy_match_time': total_fuzzy_time / len(cv_texts) if cv_texts else 0,
            'total_cvs_processed': len(cv_texts)
        }
        
        return top_results, timing_info
