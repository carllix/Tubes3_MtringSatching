# src/main.py
import sys
import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.gui.App import App
from src.database.Connection import DatabaseManager
from src.core.CVService import CVService
from src.database.Models import ApplicantProfile, ApplicationDetail
from src.database.DAO import ApplicantDAO, ApplicationDAO

def test_cv_service(cv_service: CVService):
    """Test the CV service functionality"""
    print("=" * 50)
    print("TESTING CV SERVICE")
    print("=" * 50)
    
    # Enable debug mode for detailed output
    cv_service.set_debug(True)
    
    # Load all CV texts
    print("Loading CV texts...")
    success = cv_service.load_all_cv_texts()
    if not success:
        print("Failed to load CV texts")
        return
    
    # Get statistics
    stats = cv_service.get_cv_statistics()
    print(f"\nCV Statistics:")
    print(f"Total CVs loaded: {stats.get('total_files', 0)}")
    print(f"Average words per CV: {stats.get('average_words_per_cv', 0):.1f}")
    
    # Test search functionality
    print("\n" + "=" * 30)
    print("TESTING SEARCH FUNCTIONALITY")
    print("=" * 30)
    
    # Test keywords
    test_keywords = ["python", "javascript", "react", "mysql", "experience"]
    print(f"Searching for keywords: {test_keywords}")
    
    # Test with KMP algorithm
    print("\n--- KMP Algorithm ---")
    results_kmp, timing_kmp = cv_service.search_cvs(test_keywords, "KMP", 5)
    print(f"\n📊 SUMMARY - Found {len(results_kmp)} matching CVs")
    print(f"⏱️  Total exact match time: {timing_kmp.get('total_exact_match_time', 0):.2f}ms")
    print(f"⏱️  Total fuzzy match time: {timing_kmp.get('total_fuzzy_match_time', 0):.2f}ms")
    
    # Display detailed results
    print(f"\n🏆 TOP {min(3, len(results_kmp))} RESULTS:")
    for i, result in enumerate(results_kmp[:3], 1):
        print(f"\n{i}. CV: {result['cv_file']}")
        print(f"   📊 Combined Score: {result['combined_score']:.2f}")
        print(f"   ✅ Exact matches: {result['total_exact_matches']}")
        print(f"   🔤 Fuzzy score: {result['total_fuzzy_score']:.2f}")
        
        # Show which specific keywords matched
        exact_keywords = [k for k, count in result['exact_matches'].items() if count > 0]
        fuzzy_keywords = [k for k, score in result['fuzzy_matches'].items() if score > 0]
        
        if exact_keywords:
            print(f"   🎯 Exact keyword matches: {exact_keywords}")
            for keyword in exact_keywords:
                count = result['exact_matches'][keyword]
                print(f"      • '{keyword}': {count} occurrences")
        
        if fuzzy_keywords:
            print(f"   🔤 Fuzzy keyword matches: {fuzzy_keywords}")
            for keyword in fuzzy_keywords:
                score = result['fuzzy_matches'][keyword]
                print(f"      • '{keyword}': similarity {score:.3f}")
        
        if 'applicant_profile' in result:
            profile = result['applicant_profile']
            print(f"   👤 Applicant: {profile.first_name} {profile.last_name}")
            
        if not exact_keywords and not fuzzy_keywords:
            print(f"   ❌ No keyword matches found")
    
    # Test with Boyer-Moore algorithm (brief)
    print(f"\n--- Boyer-Moore Algorithm (Brief) ---")
    cv_service.set_debug(False)  # Disable debug for BM test
    results_bm, timing_bm = cv_service.search_cvs(test_keywords, "BM", 3)
    print(f"Found {len(results_bm)} matching CVs")
    print(f"Total exact match time: {timing_bm.get('total_exact_match_time', 0):.2f}ms")
    print(f"Total fuzzy match time: {timing_bm.get('total_fuzzy_match_time', 0):.2f}ms")
    
    # Test summary extraction
    if results_kmp:
        print("\n" + "=" * 30)
        print("TESTING SUMMARY EXTRACTION")
        print("=" * 30)
        
        top_cv = results_kmp[0]['cv_file']
        summary = cv_service.get_cv_summary(top_cv)
        if summary:
            print(f"Summary for {top_cv}:")
            print(summary[:500] + "..." if len(summary) > 500 else summary)
        else:
            print(f"No summary could be extracted for {top_cv}")

def main():
    try:
        # Initialize database connection
        db_manager = DatabaseManager()
        if not db_manager.connect():
            print("❌ Failed to connect to database")
            return
        
        # Check if we have data in database
        application_dao = ApplicationDAO(db_manager)
        applications = application_dao.getApplicationsWithProfiles()
        
        if not applications:
            print("⚠️  No applications found in database.")
            print("🔧 Please run the seeder first:")
            print("   python -m src.database.Seeder")
            print("\n📁 Make sure you have PDF files in data/cv_files/ directory")
            
            # Ask user if they want to continue anyway
            response = input("\nDo you want to continue and run GUI only? (y/n): ").lower()
            if response != 'y':
                return
        
        # Initialize CV Service with debug enabled for testing
        cv_service = CVService(db_manager, debug=False)  # Will be enabled in test function
        
        # Test CV Service functionality only if we have data
        if applications:
            test_cv_service(cv_service)
        
        # Initialize and run GUI
        print("\n🚀 Starting GUI application...")
        app = App()
        app.run()
        
    except Exception as e:
        print(f"💥 Error starting application: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup database connection
        if 'db_manager' in locals():
            db_manager.disconnect()

if __name__ == "__main__":
    main()
