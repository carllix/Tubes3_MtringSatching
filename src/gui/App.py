# GUI Utama

import customtkinter as ctk

class App:
    def __init__(self):
        # Setup global appearance
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Create root window
        self.root = ctk.CTk()
        self.root.geometry("400x300")
        self.root.title("Test CustomTkinter")

        # Add components
        label = ctk.CTkLabel(self.root, text="Hello, CustomTkinter!")
        label.pack(pady=20)

        button = ctk.CTkButton(self.root, text="Click Me", command=lambda: print("Clicked!"))
        button.pack()

    def run(self):
        self.root.mainloop()


# # ================================================================
# # src/gui/main_window.py
# import customtkinter as ctk
# from typing import Dict, List
# import threading

# # Import backend components
# from core.cv_processor import CVProcessor
# from core.pattern_matcher import PatternMatcher
# from core.regex_extractor import RegexExtractor
# from config.app_config import AppConfig

# class MainWindow:
#     """Main GUI window for ATS application"""
    
#     def __init__(self):
#         self.setup_window()
#         self.setup_components()
#         self.setup_backend()
        
#     def setup_window(self):
#         """Initialize main window"""
#         ctk.set_appearance_mode("light")
#         ctk.set_default_color_theme("blue")
        
#         self.root = ctk.CTk()
#         self.root.title(AppConfig.APP_TITLE)
#         self.root.geometry(AppConfig.APP_GEOMETRY)
        
#     def setup_components(self):
#         """Setup GUI components"""
#         # Main title
#         self.title_label = ctk.CTkLabel(
#             self.root, 
#             text="CV Analyzer App",
#             font=ctk.CTkFont(size=24, weight="bold")
#         )
#         self.title_label.pack(pady=20)
        
#         # Keywords input
#         self.keywords_frame = ctk.CTkFrame(self.root)
#         self.keywords_frame.pack(pady=10, padx=20, fill="x")
        
#         ctk.CTkLabel(self.keywords_frame, text="Keywords:").pack(anchor="w", padx=10, pady=5)
#         self.keywords_entry = ctk.CTkEntry(
#             self.keywords_frame, 
#             placeholder_text="React, Express, HTML...",
#             width=400
#         )
#         self.keywords_entry.pack(padx=10, pady=5)
        
#         # Algorithm selection
#         self.algorithm_frame = ctk.CTkFrame(self.root)
#         self.algorithm_frame.pack(pady=10, padx=20, fill="x")
        
#         ctk.CTkLabel(self.algorithm_frame, text="Search Algorithm:").pack(anchor="w", padx=10, pady=5)
#         self.algorithm_var = ctk.StringVar(value="KMP")
        
#         algorithm_radio_frame = ctk.CTkFrame(self.algorithm_frame)
#         algorithm_radio_frame.pack(padx=10, pady=5)
        
#         ctk.CTkRadioButton(algorithm_radio_frame, text="KMP", variable=self.algorithm_var, value="KMP").pack(side="left", padx=10)
#         ctk.CTkRadioButton(algorithm_radio_frame, text="BM", variable=self.algorithm_var, value="BM").pack(side="left", padx=10)
        
#         # Top matches selector
#         self.matches_frame = ctk.CTkFrame(self.root)
#         self.matches_frame.pack(pady=10, padx=20, fill="x")
        
#         ctk.CTkLabel(self.matches_frame, text="Top Matches:").pack(anchor="w", padx=10, pady=5)
#         self.top_matches_var = ctk.StringVar(value="5")
#         self.matches_slider = ctk.CTkSlider(self.matches_frame, from_=1, to=20, number_of_steps=19, variable=self.top_matches_var)
#         self.matches_slider.pack(padx=10, pady=5)
        
#         # Search button
#         self.search_button = ctk.CTkButton(
#             self.root, 
#             text="Search", 
#             command=self.perform_search,
#             font=ctk.CTkFont(size=16, weight="bold")
#         )
#         self.search_button.pack(pady=20)
        
#         # Results frame
#         self.results_frame = ctk.CTkScrollableFrame(self.root, label_text="Results")
#         self.results_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
#         # Status label
#         self.status_label = ctk.CTkLabel(self.root, text="Ready")
#         self.status_label.pack(pady=5)
        
#     def setup_backend(self):
#         """Initialize backend components"""
#         self.cv_processor = CVProcessor()
#         self.pattern_matcher = PatternMatcher()
#         self.regex_extractor = RegexExtractor()
        
#         # Load CV data in background
#         self.cv_texts = {}
#         self.load_cv_data()
        
#     def load_cv_data(self):
#         """Load CV data in background thread"""
#         def load_data():
#             self.status_label.configure(text="Loading CV data...")
#             self.cv_texts = self.cv_processor.process_cv_directory(AppConfig.CV_DATA_PATH)
#             self.status_label.configure(text=f"Loaded {len(self.cv_texts)} CVs")
        
#         thread = threading.Thread(target=load_data)
#         thread.daemon = True
#         thread.start()
        
#     def perform_search(self):
#         """Perform CV search based on user input"""
#         keywords_text = self.keywords_entry.get().strip()
#         if not keywords_text:
#             self.status_label.configure(text="Please enter keywords")
#             return
            
#         keywords = [k.strip() for k in keywords_text.split(',') if k.strip()]
#         algorithm = self.algorithm_var.get()
#         top_n = int(float(self.top_matches_var.get()))
        
#         # Clear previous results
#         for widget in self.results_frame.winfo_children():
#             widget.destroy()
            
#         self.status_label.configure(text="Searching...")
        
#         def search_thread():
#             try:
#                 results, timing_info = self.pattern_matcher.search_cvs(
#                     self.cv_texts, keywords, algorithm, top_n
#                 )
                
#                 # Update GUI in main thread
#                 self.root.after(0, lambda: self.display_results(results, timing_info))
                
#             except Exception as e:
#                 self.root.after(0, lambda: self.status_label.configure(text=f"Error: {e}"))
        
#         thread = threading.Thread(target=search_thread)
#         thread.daemon = True
#         thread.start()
        
#     def display_results(self, results: List[Dict], timing_info: Dict):
#         """Display search results in GUI"""
#         # Display timing information
#         timing_text = f"Exact Match: {len(self.cv_texts)} CVs scanned in {timing_info['exact_match_time']:.2f}ms\n"
#         timing_text += f"Fuzzy Match: {len(self.cv_texts)} CVs scanned in {timing_info['fuzzy_match_time']:.2f}ms"
        
#         timing_label = ctk.CTkLabel(self.results_frame, text=timing_text, font=ctk.CTkFont(size=12))
#         timing_label.pack(pady=10)
        
#         # Display CV results
#         for i, result in enumerate(results):
#             self.create_cv_card(result, i)
            
#         self.status_label.configure(text=f"Found {len(results)} matching CVs")
        
#     def create_cv_card(self, result: Dict, index: int):
#         """Create CV result card"""
#         card_frame = ctk.CTkFrame(self.results_frame)
#         card_frame.pack(fill="x", padx=10, pady=5)
        
#         # CV name and score
#         name_label = ctk.CTkLabel(
#             card_frame, 
#             text=f"{result['cv_file']} - {result['total_exact_matches']} match(es)",
#             font=ctk.CTkFont(size=14, weight="bold")
#         )
#         name_label.pack(anchor="w", padx=10, pady=5)
        
#         # Matched keywords
#         exact_keywords = [k for k, count in result['exact_matches'].items() if count > 0]
#         fuzzy_keywords = [k for k, score in result['fuzzy_matches'].items() if score > 0]
        
#         if exact_keywords:
#             exact_text = f"Exact matches: {', '.join(exact_keywords)}"
#             exact_label = ctk.CTkLabel(card_frame, text=exact_text, font=ctk.CTkFont(size=12))
#             exact_label.pack(anchor="w", padx=10)
            
#         if fuzzy_keywords:
#             fuzzy_text = f"Fuzzy matches: {', '.join(fuzzy_keywords)}"
#             fuzzy_label = ctk.CTkLabel(card_frame, text=fuzzy_text, font=ctk.CTkFont(size=12))
#             fuzzy_label.pack(anchor="w", padx=10)
        
#         # Action buttons
#         button_frame = ctk.CTkFrame(card_frame)
#         button_frame.pack(fill="x", padx=10, pady=5)
        
#         summary_btn = ctk.CTkButton(
#             button_frame, 
#             text="Summary", 
#             width=100,
#             command=lambda: self.show_cv_summary(result['cv_file'])
#         )
#         summary_btn.pack(side="left", padx=5)
        
#         view_btn = ctk.CTkButton(
#             button_frame, 
#             text="View CV", 
#             width=100,
#             command=lambda: self.view_cv(result['cv_file'])
#         )
#         view_btn.pack(side="left", padx=5)
        
#     def show_cv_summary(self, cv_file: str):
#         """Show CV summary window"""
#         if cv_file not in self.cv_texts:
#             return
            
#         # Extract information using regex
#         cv_text = self.cv_texts[cv_file]
#         extracted_info = self.regex_extractor.extract_information(cv_text)
#         summary = self.regex_extractor.format_summary(extracted_info)
        
#         # Create summary window
#         summary_window = ctk.CTkToplevel(self.root)
#         summary_window.title(f"CV Summary - {cv_file}")
#         summary_window.geometry("600x400")
        
#         # Summary content
#         summary_text = ctk.CTkTextbox(summary_window)
#         summary_text.pack(fill="both", expand=True, padx=20, pady=20)
#         summary_text.insert("1.0", summary if summary else "No structured information found")
#         summary_text.configure(state="disabled")
        
#     def view_cv(self, cv_file: str):
#         """View original CV content"""
#         if cv_file not in self.cv_texts:
#             return
            
#         # Create CV viewer window
#         cv_window = ctk.CTkToplevel(self.root)
#         cv_window.title(f"CV Content - {cv_file}")
#         cv_window.geometry("800x600")
        
#         # CV content
#         cv_text = ctk.CTkTextbox(cv_window)
#         cv_text.pack(fill="both", expand=True, padx=20, pady=20)
#         cv_text.insert("1.0", self.cv_texts[cv_file])
#         cv_text.configure(state="disabled")
        
#     def run(self):
#         """Start the application"""
#         self.root.mainloop()
