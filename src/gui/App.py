# ATS CV Checker GUI

import customtkinter as ctk
import threading
import subprocess
import os
import webbrowser
import time
import random
from typing import Dict, List, Any
from tkinter import messagebox

from src.database.Connection import DatabaseManager
from src.core.CVService import CVService
from src.config.AppConfig import AppConfig
from src.database.Models import SearchResult
from src.gui.components.CVCard import CVCard
from src.gui.view.SummaryView import SummaryView
from src.core.matcher.PatternMatcher import PatternMatcher

class App:
    def __init__(self):
        # Setup global appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Initialize backend services
        self.setup_backend()
        
        # Create root window
        self.root = ctk.CTk()
        self.root.geometry("1600x900")  # Wider for side-by-side layout
        self.root.title("ATS CV Checker - Pattern Matching System")
        self.root.resizable(True, True)
        self.root.minsize(1200, 700)  # Set minimum size
        
        # Initialize variables
        self.algorithm_var = ctk.StringVar(value="KMP")
        self.num_matches_var = ctk.IntVar(value=5)
        
        # Setup GUI components
        self.setup_gui()
        
        # Bind keyboard shortcuts
        self.setup_keyboard_shortcuts()
        
        # Load CV data in background
        self.load_cv_data()
    
    def setup_backend(self):
        """Initialize backend services"""
        self.database_connected = False
        # Initialize pattern matcher for both database and demo modes
        self.pattern_matcher = PatternMatcher(fuzzy_threshold=0.6, debug=True)
        
        try:
            self.db_manager = DatabaseManager()
            # Try to connect to database
            if self.db_manager.connect():
                self.cv_service = CVService(self.db_manager, debug=False)
                self.database_connected = True
                print("✅ Database connected successfully")
            else:
                print("❌ Database connection failed")
                self.setup_demo_mode()
        except Exception as e:
            print(f"❌ Database error: {e}")
            self.setup_demo_mode()
    
    def setup_demo_mode(self):
        """Setup demo mode when database is not available"""
        print("🔧 Setting up demo mode...")
        self.cv_service = None
        # Create some demo data for testing the GUI with more varied content for fuzzy matching
        self.demo_cv_data = {
            "John_Doe_CV.pdf": "Software Engineer with 5 years experience in Python, Java, React, Node.js, SQL, Git, AWS Cloud Computing Machine Learning Programming Development",
            "Jane_Smith_CV.pdf": "Data Scientist with expertise in Python, R, Machine Learning, TensorFlow, Pandas, SQL, Statistics Deep Learning Analytics Visualization",
            "Mike_Johnson_CV.pdf": "Full Stack Developer skilled in JavaScript, React, Node.js, MongoDB, Express, HTML, CSS Frontend Backend Development Web Applications",
            "Sarah_Wilson_CV.pdf": "DevOps Engineer with experience in Docker, Kubernetes, AWS, Python, Linux, CI/CD, Terraform Infrastructure Automation Deployment",
            "David_Brown_CV.pdf": "Mobile Developer with expertise in React Native, Swift, Kotlin, Java, iOS, Android development Mobile Applications Programming"
        }
        # Instead of setting cv_service to None, create a SimpleCVService with demo data
        self.cv_service = SimpleCVService(self.demo_cv_data, debug=False)
    
    def setup_gui(self):
        """Setup the main GUI components"""
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main container using grid
        main_container = ctk.CTkFrame(self.root)
        main_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_container.grid_rowconfigure(1, weight=1)  # Content row gets all space
        main_container.grid_columnconfigure(1, weight=1)  # Right column gets remaining space
        
        # Title
        title_label = ctk.CTkLabel(
            main_container,
            text="ATS CV Checker",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="ew")
        
        # Left panel - Search controls (fixed width)
        left_panel = ctk.CTkFrame(main_container, width=380)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=(0, 10))
        left_panel.grid_propagate(False)  # Maintain fixed width
        
        # Right panel - Results (expandable)
        right_panel = ctk.CTkFrame(main_container)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(0, 10))
        right_panel.grid_rowconfigure(1, weight=1)  # Results area gets all space
        right_panel.grid_columnconfigure(0, weight=1)
        
        # Setup sections
        self.setup_search_section(left_panel)
        self.setup_results_section(right_panel)
        
        # Status bar
        self.status_label = ctk.CTkLabel(
            main_container,
            text="Ready - No CV data loaded",
            font=ctk.CTkFont(size=11)
        )
        self.status_label.grid(row=2, column=0, columnspan=2, pady=(5, 10), sticky="ew")
    
    def setup_search_section(self, parent):
        """Setup the search input section"""
        # Make parent scrollable for smaller screens
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Scrollable container for all controls
        scrollable_search = ctk.CTkScrollableFrame(parent)
        scrollable_search.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Control panel title
        ctk.CTkLabel(
            scrollable_search,
            text="Search Controls",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 15))
        
        # Keywords input section
        keywords_frame = ctk.CTkFrame(scrollable_search)
        keywords_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        ctk.CTkLabel(
            keywords_frame,
            text="Keywords:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=12, pady=(12, 5))
        
        self.keywords_entry = ctk.CTkEntry(
            keywords_frame,
            placeholder_text="e.g., python, java, react",
            font=ctk.CTkFont(size=11),
            height=32
        )
        self.keywords_entry.pack(fill="x", padx=12, pady=(0, 12))
        
        # Algorithm selection
        algorithm_frame = ctk.CTkFrame(scrollable_search)
        algorithm_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        ctk.CTkLabel(
            algorithm_frame,
            text="Pattern Matching Algorithm:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=12, pady=(12, 8))
        
        ctk.CTkRadioButton(
            algorithm_frame,
            text="KMP (Knuth-Morris-Pratt)",
            variable=self.algorithm_var,
            value="KMP",
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=15, pady=2)
        
        ctk.CTkRadioButton(
            algorithm_frame,
            text="BM (Boyer-Moore)",
            variable=self.algorithm_var,
            value="BM",
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=15, pady=2)
        
        ctk.CTkRadioButton(
            algorithm_frame,
            text="AC (Aho-Corasick)",
            variable=self.algorithm_var,
            value="AC",
            font=ctk.CTkFont(size=11)
        ).pack(anchor="w", padx=15, pady=(2, 12))
        
        # Number of matches
        matches_frame = ctk.CTkFrame(scrollable_search)
        matches_frame.pack(fill="x", padx=10, pady=(0, 15))
        
        ctk.CTkLabel(
            matches_frame,
            text="Number of Top Matches:",
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(anchor="w", padx=12, pady=(12, 5))
        
        self.matches_slider = ctk.CTkSlider(
            matches_frame,
            from_=1,
            to=20,
            number_of_steps=19,
            variable=self.num_matches_var
        )
        self.matches_slider.pack(fill="x", padx=12, pady=4)
        
        self.matches_label = ctk.CTkLabel(
            matches_frame,
            text=f"Top {self.num_matches_var.get()} matches",
            font=ctk.CTkFont(size=11)
        )
        self.matches_label.pack(padx=12, pady=(0, 12))
        
        # Update label when slider changes
        self.matches_slider.configure(command=self.update_matches_label)
        
        # Search button
        search_button = ctk.CTkButton(
            scrollable_search,
            text="Search CVs",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            command=self.perform_search
        )
        search_button.pack(fill="x", padx=10, pady=(0, 15))
        
        
    
    def setup_results_section(self, parent):
        """Setup the results display section"""
        # Results header
        header_frame = ctk.CTkFrame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        
        self.results_header = ctk.CTkLabel(
            header_frame,
            text="Search Results",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.results_header.pack(pady=12)
        
        # Scrollable frame for results with better scrolling
        self.results_scrollable = ctk.CTkScrollableFrame(
            parent,
            label_text="CV Matches",
            label_font=ctk.CTkFont(size=14, weight="bold")
        )
        self.results_scrollable.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Enable mouse wheel scrolling
        self.setup_scrolling(self.results_scrollable)
    
    def update_matches_label(self, value):
        """Update the matches label when slider changes"""
        num_matches = int(value)
        self.matches_label.configure(text=f"Top {num_matches} matches")
    
    def load_cv_data(self):
        """Load CV data in background thread"""
        def load_data():
            if self.database_connected and self.cv_service:
                self.status_label.configure(text="Loading CV data from database...")
                success = self.cv_service.load_all_cv_texts()
                
                if success:
                    stats = self.cv_service.get_cv_statistics()
                    total_cvs = stats.get('total_files', 0)
                    self.root.after(0, lambda: self.status_label.configure(
                        text=f"Ready - {total_cvs} CVs loaded from database"
                    ))
                else:
                    self.root.after(0, lambda: self.status_label.configure(
                        text="Failed to load CV data - Check database connection"
                    ))
            else:
                # Demo mode
                self.root.after(0, lambda: self.status_label.configure(
                    text=f"Demo Mode - {len(self.demo_cv_data)} sample CVs available"
                ))
        
        thread = threading.Thread(target=load_data, daemon=True)
        thread.start()
    
    def perform_search(self):
        """Perform CV search based on user input"""
        keywords_text = self.keywords_entry.get().strip()
        if not keywords_text:
            messagebox.showwarning("Warning", "Please enter keywords to search")
            return
        
        # Parse keywords
        keywords = [k.strip() for k in keywords_text.split(',') if k.strip()]
        algorithm = self.algorithm_var.get()
        num_matches = self.num_matches_var.get()
        
        # Clear previous results
        for widget in self.results_scrollable.winfo_children():
            widget.destroy()
        
        # Update status
        self.status_label.configure(text=f"Searching for {len(keywords)} keywords using {algorithm} algorithm...")
        
        def search_thread():
            try:
                # Use cv_service for all searches - the service handles database or demo mode internally
                results, timing_info = self.cv_service.search_cvs(keywords, algorithm, num_matches)
                
                # Update GUI in main thread
                self.root.after(0, lambda: self.display_results(results, timing_info, keywords, algorithm))
                
            except Exception as e:
                self.root.after(0, lambda: self.status_label.configure(
                    text=f"Search failed: {str(e)}"
                ))
                self.root.after(0, lambda: messagebox.showerror("Search Error", f"Search failed: {str(e)}"))
        
        thread = threading.Thread(target=search_thread, daemon=True)
        thread.start()
    
    def perform_demo_search(self, keywords: List[str], algorithm: str, num_matches: int):
        """Perform demo search on sample data with fuzzy matching"""
        start_time = time.time()
        results = []
        
        # Search through demo CV data using PatternMatcher
        for cv_name, cv_text in self.demo_cv_data.items():
            # Use PatternMatcher for comprehensive search
            search_result = self.pattern_matcher.search_single_cv(
                keywords, cv_text, algorithm, cv_name
            )
            
            # Only include CVs with at least one match (exact or fuzzy)
            if (search_result['total_exact_matches'] > 0 or 
                search_result['total_fuzzy_score'] > 0):
                
                # Create result in expected format
                result = {
                    'cv_file': cv_name,
                    'profile': {
                        'first_name': cv_name.replace('_', ' ').replace('.pdf', '').split()[0],
                        'last_name': ' '.join(cv_name.replace('_', ' ').replace('.pdf', '').split()[1:]),
                        'phone_number': f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                        'address': f"{random.randint(100, 999)} Main St, City, State"
                    },
                    'detail': {
                        'application_role': random.choice(['Software Engineer', 'Data Scientist', 'DevOps Engineer', 'Full Stack Developer']),
                        'cv_path': f"demo/cv_files/{cv_name}"
                    },
                    'total_exact_matches': search_result['total_exact_matches'],
                    'exact_matches': search_result['exact_matches'],
                    'fuzzy_matches': search_result['fuzzy_matches'],
                    'fuzzy_matches_detail': search_result.get('fuzzy_matches_detail', {}),
                    'matched_keywords': search_result['matched_keywords'],
                    'combined_score': search_result['combined_score'],
                    'match_score': search_result['combined_score'],
                    'cv_text': cv_text,
                    'timing': search_result['timing']
                }
                
                results.append(result)
        
        # Sort by combined score (descending) and limit results
        results.sort(key=lambda x: x['combined_score'], reverse=True)
        results = results[:num_matches]
        
        end_time = time.time()
        
        # Calculate total timing
        total_exact_time = sum(r['timing']['exact_match_time'] for r in results)
        total_fuzzy_time = sum(r['timing']['fuzzy_match_time'] for r in results)
        
        timing_info = {
            'total_exact_match_time': total_exact_time,
            'total_fuzzy_match_time': total_fuzzy_time,
            'total_search_time': (end_time - start_time) * 1000
        }
        
        return results, timing_info
    
    def display_results(self, results: List[Dict[str, Any]], timing_info: Dict, keywords: List[str], algorithm: str):
        """Display search results"""
        # Update status with timing info
        total_time = timing_info.get('total_exact_match_time', 0) + timing_info.get('total_fuzzy_match_time', 0)
        self.status_label.configure(
            text=f"Found {len(results)} matches in {total_time:.2f}ms using {algorithm} algorithm"
        )
        
        # Display timing information in a compact header
        if results:  # Only show timing if we have results
            timing_frame = ctk.CTkFrame(self.results_scrollable)
            timing_frame.pack(fill="x", padx=5, pady=(5, 10))
            
            timing_text = f"Search Time: {total_time:.2f}ms"
            if timing_info.get('total_exact_match_time', 0) > 0:
                timing_text += f" (Exact: {timing_info.get('total_exact_match_time', 0):.2f}ms"
                if timing_info.get('total_fuzzy_match_time', 0) > 0:
                    timing_text += f", Fuzzy: {timing_info.get('total_fuzzy_match_time', 0):.2f}ms)"
                else:
                    timing_text += ")"
            
            ctk.CTkLabel(
                timing_frame,
                text=timing_text,
                font=ctk.CTkFont(size=11)
            ).pack(pady=8)
        
        # Display results
        if not results:
            no_results_frame = ctk.CTkFrame(self.results_scrollable)
            no_results_frame.pack(fill="x", padx=20, pady=50)
            
            ctk.CTkLabel(
                no_results_frame,
                text="No matching CVs found",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=20)
            
            ctk.CTkLabel(
                no_results_frame,
                text="Try different keywords or check your spelling",
                font=ctk.CTkFont(size=12)
            ).pack(pady=(0, 20))
        else:
            for i, result in enumerate(results, 1):
                cv_card = CVCard(
                    parent=self.results_scrollable,
                    result=result,
                    rank=i,
                    on_view_details=self.show_cv_summary
                )
                cv_card.pack(fill="x", padx=5, pady=5)
    
    def show_cv_summary(self, result: Dict[str, Any]):
        """Show CV summary in a new window"""
        summary_view = SummaryView(self.root, result)
    
    def view_cv(self, result: Dict[str, Any]):
        """Open the original CV file"""
        profile = result.get('profile', {})
        detail = result.get('detail', {})
        
        # Get CV path from detail section
        cv_path = detail.get('cv_path', '')
        name = f"{profile.get('first_name', 'Unknown')} {profile.get('last_name', '')}".strip()
        
        # Check if we're in demo mode
        if not self.database_connected:
            messagebox.showinfo("Demo Mode", 
                f"In demo mode, CV viewing is simulated.\n\n"
                f"Would open CV for: {name}\n"
                f"Path: {cv_path}\n\n"
                f"In real mode, this would open the actual PDF file.")
            return
        
        if not cv_path:
            messagebox.showwarning("Warning", f"CV file path not available for {name}")
            return
        
        # Convert relative path to absolute path
        if not cv_path.startswith('/'):
            # If it's a relative path, prepend the data directory
            from config.AppConfig import AppConfig
            if cv_path.startswith('cv_files/'):
                full_cv_path = os.path.join(AppConfig.BASE_DATA_PATH, cv_path)
            else:
                full_cv_path = os.path.join(AppConfig.BASE_DATA_PATH, 'cv_files', cv_path)
        else:
            full_cv_path = cv_path
        
        # Check if file exists
        if not os.path.exists(full_cv_path):
            messagebox.showerror("Error", f"CV file not found for {name}:\n{full_cv_path}")
            return
        
        try:
            # Try to open with default system application
            if os.name == 'nt':  # Windows
                os.startfile(full_cv_path)
            elif os.name == 'posix':  # macOS and Linux
                subprocess.call(['open', full_cv_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open CV file for {name}: {e}")

    def run(self):
        self.root.mainloop()
    
    def setup_scrolling(self, scrollable_frame):
        """Setup mouse wheel scrolling for the scrollable frame"""
        def on_mousewheel(event):
            scrollable_frame._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mouse wheel events to the scrollable frame and its canvas
        scrollable_frame.bind("<MouseWheel>", on_mousewheel)  # Windows
        scrollable_frame.bind("<Button-4>", lambda e: scrollable_frame._parent_canvas.yview_scroll(-1, "units"))  # Linux
        scrollable_frame.bind("<Button-5>", lambda e: scrollable_frame._parent_canvas.yview_scroll(1, "units"))   # Linux
        
        # For macOS, bind to the canvas as well
        if hasattr(scrollable_frame, '_parent_canvas'):
            scrollable_frame._parent_canvas.bind("<MouseWheel>", on_mousewheel)
            scrollable_frame._parent_canvas.bind("<Button-4>", lambda e: scrollable_frame._parent_canvas.yview_scroll(-1, "units"))
            scrollable_frame._parent_canvas.bind("<Button-5>", lambda e: scrollable_frame._parent_canvas.yview_scroll(1, "units"))
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for the application"""
        # Bind Enter key to search when in keywords entry
        self.keywords_entry.bind("<Return>", lambda e: self.perform_search())
        self.keywords_entry.bind("<KP_Enter>", lambda e: self.perform_search())
        
        # Bind Ctrl+F to focus on keywords entry
        self.root.bind("<Control-f>", lambda e: self.keywords_entry.focus())
        self.root.bind("<Command-f>", lambda e: self.keywords_entry.focus())  # macOS
        
        # Bind Escape to clear search
        self.root.bind("<Escape>", lambda e: self.clear_search())
    
    def clear_search(self):
        """Clear search results and keywords"""
        self.keywords_entry.delete(0, 'end')
        for widget in self.results_scrollable.winfo_children():
            widget.destroy()
        self.status_label.configure(text="Search cleared")

