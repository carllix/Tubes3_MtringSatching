from typing import Dict, List, Tuple, Optional
import os
from .processor.CVProcessor import CVProcessor
from .processor.RegexExtractor import RegexExtractor
from .matcher.PatternMatcher import PatternMatcher
from src.database.DAO import ApplicationDAO
from src.database.Connection import DatabaseManager
from src.config.AppConfig import AppConfig

class CVService:
    """Main service for CV processing and pattern matching operations"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.cv_processor = CVProcessor()
        self.regex_extractor = RegexExtractor()
        self.pattern_matcher = PatternMatcher()
        self.application_dao = ApplicationDAO(db_manager)
        
        # Cache  CV texts (saat pertama kali load)
        self.cv_texts_cache: Dict[str, str] = {}
    
    def load_all_cv_texts(self) -> bool:
        """Load all CV texts from database CV paths into memory
        
        Returns:
            True if successful, False otherwise
        """
        try:
            applications_with_profiles = self.application_dao.getApplicationsWithProfiles()
            
            if not applications_with_profiles:
                print("⚠️  No applications found in database. Please run the seeder first.")
                return False
            
            cv_texts = {}
            processed_count = 0
            
            print(f"Loading CV texts for {len(applications_with_profiles)} applications...")
            
            for profile, detail in applications_with_profiles:
                cv_path = detail.cv_path
                if not cv_path:
                    print(f"⚠️  No CV path for application ID {detail.detail_id}")
                    continue
                
                # handle absolute/relative paths
                if not os.path.isabs(cv_path):
                    if cv_path.startswith('cv_files/'):
                        full_cv_path = os.path.join(AppConfig.BASE_DATA_PATH, cv_path)
                    else:
                        full_cv_path = os.path.join(AppConfig.BASE_DATA_PATH, 'cv_files', cv_path)
                else:
                    full_cv_path = cv_path
                
                print(f"📁 Checking CV path: {full_cv_path}")
                
                if os.path.exists(full_cv_path):
                    text = self.cv_processor.extract_text_from_pdf(full_cv_path)
                    if text:
                        cv_key = f"{detail.detail_id}_{os.path.basename(cv_path)}"
                        cv_texts[cv_key] = text
                        processed_count += 1
                        print(f"Loaded CV: {cv_key} ({len(text)} characters)")
                        # print(cv_texts[cv_key])  # Debug output of the text
                    else:
                        print(f"Failed to extract text from: {full_cv_path}")
                else:
                    print(f"CV file not found: {full_cv_path}")
            
            self.cv_texts_cache = cv_texts
            print(f"🎉 Successfully loaded {processed_count} CV texts into memory")
            return processed_count > 0
            
        except Exception as e:
            print(f"💥 Error loading CV texts: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def search_cvs(self, keywords: List[str], algorithm: str = "KMP", top_n: int = 10) -> Tuple[List[Dict], Dict]:
        """Search CVs using pattern matching algorithms
        
        Args:
            keywords: List of keywords to search for
            algorithm: Algorithm to use ("KMP" or "BM")
            top_n: Number of top results to return
            
        Returns:
            Tuple of (search_results, timing_info)
        """
        if not self.cv_texts_cache:
            print("No CV texts loaded. Call load_all_cv_texts() first.")
            return [], {}
        
        # Pattern matching search
        results, timing_info = self.pattern_matcher.search_multiple_cvs(
            keywords, self.cv_texts_cache, algorithm, top_n
        )
        
        # Enhance results with database information
        enhanced_results = []
        applications_with_profiles = self.application_dao.getApplicationsWithProfiles()
        
        app_lookup = {}
        for profile, detail in applications_with_profiles:
            cv_key = f"{detail.detail_id}_{os.path.basename(detail.cv_path)}"
            app_lookup[cv_key] = (profile, detail)
        
        for result in results:
            cv_file = result['cv_file']
            if cv_file in app_lookup:
                profile, detail = app_lookup[cv_file]
                result['profile'] = {
                    'applicant_id': profile.applicant_id,
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'date_of_birth': profile.date_of_birth,
                    'address': profile.address,
                    'phone_number': profile.phone_number
                }
                result['detail'] = {
                    'detail_id': detail.detail_id,
                    'applicant_id': detail.applicant_id,
                    'application_role': detail.application_role,
                    'cv_path': detail.cv_path
                }
                result['cv_text'] = self.cv_texts_cache.get(cv_file, '')
                
                result['applicant_profile'] = profile
                result['application_detail'] = detail
            
            enhanced_results.append(result)
        
        return enhanced_results, timing_info
    
    def get_cv_summary(self, cv_file: str) -> Optional[str]:
        """Get structured summary of a CV using regex extraction
        
        Args:
            cv_file: CV file key
            
        Returns:
            Formatted summary string or None if not found
        """
        if cv_file not in self.cv_texts_cache:
            return None
        
        cv_text = self.cv_texts_cache[cv_file]
        extracted_info = self.regex_extractor.extract_information(cv_text)
        return self.regex_extractor.format_summary(extracted_info)
    
    def get_cv_text(self, cv_file: str) -> Optional[str]:
        """Get raw CV text
        
        Args:
            cv_file: CV file key
            
        Returns:
            Raw CV text or None if not found
        """
        return self.cv_texts_cache.get(cv_file)
    
    def get_cv_statistics(self) -> Dict:
        """Get statistics about loaded CVs
        
        Returns:
            Dictionary containing CV statistics
        """
        return self.cv_processor.get_cv_statistics(self.cv_texts_cache)
    
    def process_and_cache_new_cv(self, cv_path: str, detail_id: int) -> bool:
        """Process a new CV and add it to cache
        
        Args:
            cv_path: Path to CV file
            detail_id: Application detail ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(cv_path):
                print(f"CV file not found: {cv_path}")
                return False
            
            text = self.cv_processor.extract_text_from_pdf(cv_path)
            if text:
                cv_key = f"{detail_id}_{os.path.basename(cv_path)}"
                self.cv_texts_cache[cv_key] = text
                print(f"Added new CV to cache: {cv_key}")
                return True
            else:
                print(f"Failed to extract text from: {cv_path}")
                return False
                
        except Exception as e:
            print(f"Error processing new CV: {e}")
            return False
