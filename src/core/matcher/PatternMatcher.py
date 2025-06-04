from typing import List, Dict, Tuple, Any
import time
from .KMP import KMPMatcher
from .BM import BoyerMooreMatcher
from .FuzzyMatcher import FuzzyMatcher

class PatternMatcher:
    """Main pattern matching coordinator for ATS system"""
    
    def __init__(self, fuzzy_threshold: float = 0.7, debug: bool = False):
        self.kmp = KMPMatcher()
        self.bm = BoyerMooreMatcher()
        self.fuzzy_matcher = FuzzyMatcher(fuzzy_threshold)
        self.debug = debug
    
    def exact_match_keywords(self, keywords: List[str], text: str, algorithm: str = "KMP") -> Dict[str, int]:
        """Perform exact matching of keywords in text
        
        Args:
            keywords: List of keywords to search for
            text: Text to search in
            algorithm: Algorithm to use ("KMP" or "BM")
            
        Returns:
            Dictionary mapping keyword to occurrence count
        """
        results = {}
        
        for keyword in keywords:
            keyword_clean = keyword.strip()
            if not keyword_clean:
                continue
            
            if algorithm.upper() == "KMP":
                count = self.kmp.count_occurrences(text, keyword_clean)
                if self.debug and count > 0:
                    positions = self.kmp.search(text, keyword_clean)
                    print(f"🎯 EXACT MATCH [{algorithm}]: '{keyword_clean}' found {count} times at positions: {positions}")
            elif algorithm.upper() == "BM":
                count = self.bm.count_occurrences(text, keyword_clean)
                if self.debug and count > 0:
                    positions = self.bm.search(text, keyword_clean)
                    print(f"🎯 EXACT MATCH [{algorithm}]: '{keyword_clean}' found {count} times at positions: {positions}")
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
        if self.debug:
            print(f"\n📄 Analyzing CV: {cv_file}")
            print(f"🔍 Searching for keywords: {keywords}")
            print(f"⚙️  Using algorithm: {algorithm}")
        
        # Exact matching
        start_time = time.time()
        exact_matches = self.exact_match_keywords(keywords, cv_text, algorithm)
        exact_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Find keywords with no exact matches for fuzzy matching
        unmatched_keywords = [k for k, count in exact_matches.items() if count == 0]
        
        # Fuzzy matching for unmatched keywords
        start_time = time.time()
        fuzzy_scores = {}
        fuzzy_matches_detail = {}
        if unmatched_keywords:
            fuzzy_scores = self.fuzzy_matcher.calculate_fuzzy_score(unmatched_keywords, cv_text)
            if self.debug:
                fuzzy_matches_detail = self.fuzzy_matcher.fuzzy_match_keywords(unmatched_keywords, cv_text)
                for keyword, matches in fuzzy_matches_detail.items():
                    if matches:
                        best_match = max(matches, key=lambda x: x[1])
                        print(f"🔤 FUZZY MATCH: '{keyword}' → '{best_match[0]}' (similarity: {best_match[1]:.3f})")
        fuzzy_time = (time.time() - start_time) * 1000
        
        # Calculate total matches and scores
        total_exact_matches = sum(exact_matches.values())
        total_fuzzy_score = sum(fuzzy_scores.values())
        combined_score = total_exact_matches + (total_fuzzy_score * 0.5)  # Weight fuzzy matches lower
        
        if self.debug:
            matched_exact = [k for k, count in exact_matches.items() if count > 0]
            matched_fuzzy = [k for k, score in fuzzy_scores.items() if score > 0]
            
            print(f"✅ Exact matches: {matched_exact} (total count: {total_exact_matches})")
            print(f"🔤 Fuzzy matches: {matched_fuzzy} (total score: {total_fuzzy_score:.2f})")
            print(f"🏆 Combined score: {combined_score:.2f}")
            print(f"⏱️  Timing - Exact: {exact_time:.2f}ms, Fuzzy: {fuzzy_time:.2f}ms")
        
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
        if self.debug:
            print(f"\n🔍 Starting search across {len(cv_texts)} CVs")
            print(f"🎯 Keywords: {keywords}")
            print(f"⚙️  Algorithm: {algorithm}")
            print("=" * 60)
        
        results = []
        total_exact_time = 0
        total_fuzzy_time = 0
        
        # Search each CV
        for cv_file, cv_text in cv_texts.items():
            result = self.search_single_cv(keywords, cv_text, algorithm, cv_file)
            
            # Add CV filename to result
            result['cv_file'] = cv_file
            results.append(result)
            
            # Accumulate timing
            total_exact_time += result['timing']['exact_match_time']
            total_fuzzy_time += result['timing']['fuzzy_match_time']
        
        # Sort by combined score (descending)
        results.sort(key=lambda x: x['combined_score'], reverse=True)
        
        if self.debug:
            print("\n" + "=" * 60)
            print("🏆 TOP RESULTS SUMMARY:")
            for i, result in enumerate(results[:min(5, len(results))], 1):
                print(f"{i}. {result['cv_file']}")
                print(f"   📊 Score: {result['combined_score']:.2f}")
                print(f"   ✅ Exact: {result['matched_keywords']['exact']}")
                print(f"   🔤 Fuzzy: {result['matched_keywords']['fuzzy']}")
        
        # Return top N results
        top_results = results[:top_n]
        
        timing_info = {
            'total_exact_match_time': total_exact_time,
            'total_fuzzy_match_time': total_fuzzy_time,
            'average_exact_match_time': total_exact_time / len(cv_texts) if cv_texts else 0,
            'average_fuzzy_match_time': total_fuzzy_time / len(cv_texts) if cv_texts else 0,
            'total_cvs_processed': len(cv_texts)
        }
        
        return top_results, timing_info
    
    def set_debug(self, debug: bool):
        """Enable or disable debug output"""
        self.debug = debug
