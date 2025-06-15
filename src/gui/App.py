# ATS CV Checker GUI - Professional Version

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
        # Setup global appearance with dark theme for professional look
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize backend services
        self.setup_backend()
        
        # Create root window
        self.root = ctk.CTk()
        self.root.geometry("1600x900")
        self.root.title("ATS CV Checker - Pattern Matching System")
        self.root.resizable(True, True)
        self.root.minsize(1200, 700)
        
        # Color scheme for professional look
        self.colors = {
            'primary': '#1f538d',
            'secondary': '#14375e',
            'accent': '#36719e',
            'surface': '#212121',
            'background': '#1a1a1a',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336'
        }
        
        # Initialize variables
        self.algorithm_var = ctk.StringVar(value="KMP")
        self.num_matches_var = ctk.IntVar(value=5)
        self.is_searching = False
        
        # Setup GUI components
        self.setup_gui()
        
        # Bind keyboard shortcuts
        self.setup_keyboard_shortcuts()
        
        # Load CV data in background
        self.load_cv_data()
        
        # Add hover effects
        self.setup_hover_effects()
    
    def setup_backend(self):
        """Initialize backend services"""
        self.database_connected = False
        # Initialize pattern matcher for both database and demo modes
        self.pattern_matcher = PatternMatcher(fuzzy_threshold=0.6)
        
        try:
            self.db_manager = DatabaseManager()
            if self.db_manager.connect():
                self.cv_service = CVService(self.db_manager)
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
        self.demo_cv_data = {
            "John_Doe_CV.pdf": "Software Engineer with 5 years experience in Python, Java, React, Node.js, SQL, Git, AWS",
            "Jane_Smith_CV.pdf": "Data Scientist with expertise in Python, R, Machine Learning, TensorFlow, Pandas, SQL, Statistics",
            "Mike_Johnson_CV.pdf": "Full Stack Developer skilled in JavaScript, React, Node.js, MongoDB, Express, HTML, CSS",
            "Sarah_Wilson_CV.pdf": "DevOps Engineer with experience in Docker, Kubernetes, AWS, Python, Linux, CI/CD, Terraform",
            "David_Brown_CV.pdf": "Mobile Developer with expertise in React Native, Swift, Kotlin, Java, iOS, Android development"
        }
        self.cv_service = SimpleCVService(self.demo_cv_data, debug=False)
    
    def setup_gui(self):
        """Setup the main GUI components"""
        # Configure grid weights for responsive layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Main container
        main_container = ctk.CTkFrame(self.root, fg_color="transparent")
        main_container.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        
        # Header with gradient-like effect
        header_frame = ctk.CTkFrame(main_container, height=80, corner_radius=12)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        header_frame.grid_propagate(False)
        
        # Title with better typography
        title_label = ctk.CTkLabel(
            header_frame,
            text="ATS CV Checker",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title_label.pack(side="left", padx=25, pady=20)
        
        # Connection status indicator
        self.connection_status = ctk.CTkLabel(
            header_frame,
            text="● Connected" if self.database_connected else "● Demo Mode",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors['success'] if self.database_connected else self.colors['warning']
        )
        self.connection_status.pack(side="right", padx=25, pady=20)
        
        # Left panel - Search controls
        left_panel = ctk.CTkFrame(main_container, width=500, corner_radius=12)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left_panel.grid_propagate(False)
        
        # Right panel - Results
        right_panel = ctk.CTkFrame(main_container, corner_radius=12)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 0))
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        # Setup sections
        self.setup_search_section(left_panel)
        self.setup_results_section(right_panel)
        
        # Status bar with modern design
        status_frame = ctk.CTkFrame(main_container, height=40, corner_radius=8)
        status_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        status_frame.grid_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready - System initialized",
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_secondary']
        )
        self.status_label.pack(pady=12)
        
        # Progress bar (hidden by default)
        self.progress_bar = ctk.CTkProgressBar(status_frame, height=3, corner_radius=2)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 8))
        self.progress_bar.pack_forget()  # Hide initially
    
    def setup_search_section(self, parent):
        """Setup the search input section with modern design"""
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # Header section
        header_section = ctk.CTkFrame(parent, corner_radius=8, height=60)
        header_section.pack(fill="x", padx=15, pady=(15, 10))
        header_section.pack_propagate(False)
        
        ctk.CTkLabel(
            header_section,
            text="Search Configuration",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=18)
        
        # Scrollable container with gray scrollbar
        scrollable_search = ctk.CTkScrollableFrame(
            parent, 
            corner_radius=8,
            scrollbar_button_color="gray40",
            scrollbar_button_hover_color="gray50"
        )
        scrollable_search.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # Keywords input section
        keywords_section = ctk.CTkFrame(scrollable_search, corner_radius=8)
        keywords_section.pack(fill="x", pady=(10, 15))
        
        # Section header
        keywords_header = ctk.CTkFrame(keywords_section, corner_radius=6, height=35)
        keywords_header.pack(fill="x", padx=15, pady=(15, 8))
        keywords_header.pack_propagate(False)
        
        ctk.CTkLabel(
            keywords_header,
            text="Search Keywords",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=8)
        
        # Enhanced entry with better styling
        self.keywords_entry = ctk.CTkEntry(
            keywords_section,
            placeholder_text="Enter keywords separated by commas (e.g., python, java, react)",
            font=ctk.CTkFont(size=12),
            height=40,
            corner_radius=8,
            border_width=2
        )
        self.keywords_entry.pack(fill="x", padx=15, pady=(0, 15))
        
        # Algorithm selection with modern radio buttons
        algorithm_section = ctk.CTkFrame(scrollable_search, corner_radius=8)
        algorithm_section.pack(fill="x", pady=(0, 15))
        
        # Section header
        algo_header = ctk.CTkFrame(algorithm_section, corner_radius=6, height=35)
        algo_header.pack(fill="x", padx=15, pady=(15, 10))
        algo_header.pack_propagate(False)
        
        ctk.CTkLabel(
            algo_header,
            text="Pattern Matching Algorithm",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=8)
        
        # Algorithm options with descriptions
        algorithms = [
            ("KMP", "Knuth-Morris-Pratt", "Optimal for long patterns"),
            ("BM", "Boyer-Moore", "Fast for large text searches"),
            ("AC", "Aho-Corasick", "Efficient for multiple patterns")
        ]
        
        for value, name, desc in algorithms:
            algo_frame = ctk.CTkFrame(algorithm_section, corner_radius=6)
            algo_frame.pack(fill="x", padx=15, pady=2)
            
            radio_btn = ctk.CTkRadioButton(
                algo_frame,
                text=f"{name}",
                variable=self.algorithm_var,
                value=value,
                font=ctk.CTkFont(size=12, weight="bold"),
                radiobutton_width=20,
                radiobutton_height=20
            )
            radio_btn.pack(side="left", padx=15, pady=10)
            
            desc_label = ctk.CTkLabel(
                algo_frame,
                text=desc,
                font=ctk.CTkFont(size=10),
                text_color=self.colors['text_secondary']
            )
            desc_label.pack(side="right", padx=15, pady=10)
        
        # Number of matches with modern slider
        matches_section = ctk.CTkFrame(scrollable_search, corner_radius=8)
        matches_section.pack(fill="x", pady=(0, 15))
        
        # Section header
        matches_header = ctk.CTkFrame(matches_section, corner_radius=6, height=35)
        matches_header.pack(fill="x", padx=15, pady=(15, 10))
        matches_header.pack_propagate(False)
        
        ctk.CTkLabel(
            matches_header,
            text="Maximum Results",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=8)
        
        # Slider with value display
        slider_frame = ctk.CTkFrame(matches_section, fg_color="transparent")
        slider_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        self.matches_slider = ctk.CTkSlider(
            slider_frame,
            from_=1,
            to=100,
            number_of_steps=99,
            variable=self.num_matches_var,
            height=20,
            button_length=20,
            button_color="gray50",
            button_hover_color="gray60",
            progress_color="gray40"
        )
        self.matches_slider.pack(fill="x", pady=(5, 8))
        
        self.matches_label = ctk.CTkLabel(
            slider_frame,
            text=f"Show top {self.num_matches_var.get()} matches",
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_secondary']
        )
        self.matches_label.pack()
        
        self.matches_slider.configure(command=self.update_matches_label)
        
        # Enhanced search button
        self.search_button = ctk.CTkButton(
            scrollable_search,
            text="Search CVs",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=45,
            corner_radius=10,
            command=self.perform_search,
            hover_color=self.colors['accent']
        )
        self.search_button.pack(fill="x", padx=10, pady=(10, 15))
        
        # Clear button
        self.clear_button = ctk.CTkButton(
            scrollable_search,
            text="Clear Search",
            font=ctk.CTkFont(size=12),
            height=35,
            corner_radius=8,
            fg_color="transparent",
            border_width=2,
            text_color=self.colors['text_secondary'],
            hover_color=("gray70", "gray30"),
            command=self.clear_search
        )
        self.clear_button.pack(fill="x", padx=10, pady=(0, 15))
    
    def setup_results_section(self, parent):
        """Setup the results display section with modern design"""
        # Results header with stats
        header_frame = ctk.CTkFrame(parent, corner_radius=8, height=60)
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        header_frame.grid_propagate(False)
        header_frame.grid_columnconfigure(1, weight=1)
        
        self.results_header = ctk.CTkLabel(
            header_frame,
            text="Search Results",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        )
        self.results_header.grid(row=0, column=0, padx=20, pady=18, sticky="w")
        
        # Results counter
        self.results_counter = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_secondary']
        )
        self.results_counter.grid(row=0, column=1, padx=20, pady=18, sticky="e")
        
        # Modern scrollable frame for results with gray scrollbar
        self.results_scrollable = ctk.CTkScrollableFrame(
            parent,
            corner_radius=8,
            scrollbar_button_color="gray40",
            scrollbar_button_hover_color="gray50"
        )
        self.results_scrollable.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Initial empty state
        self.show_empty_state()
        
        # Enable smooth scrolling
        self.setup_scrolling(self.results_scrollable)
    
    def show_empty_state(self):
        """Show empty state with modern design"""
        empty_frame = ctk.CTkFrame(self.results_scrollable, corner_radius=10)
        empty_frame.pack(fill="both", expand=True, padx=20, pady=50)
        
        # Icon placeholder
        icon_frame = ctk.CTkFrame(empty_frame, width=80, height=80, corner_radius=40)
        icon_frame.pack(pady=(40, 20))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text="CV",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['accent']
        ).pack(expand=True)
        
        ctk.CTkLabel(
            empty_frame,
            text="No Search Results",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="Enter keywords and click 'Search CVs' to find matching resumes",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_secondary']
        ).pack(pady=(0, 40))
    
    def update_matches_label(self, value):
        """Update matches label with animation effect"""
        num_matches = int(value)
        self.matches_label.configure(text=f"Show top {num_matches} matches")
        
        # Brief highlight effect
        original_color = self.matches_label.cget("text_color")
        self.matches_label.configure(text_color=self.colors['accent'])
        self.root.after(200, lambda: self.matches_label.configure(text_color=original_color))
    
    def load_cv_data(self):
        """Load CV data with progress indication"""
        def load_data():
            if self.database_connected and self.cv_service:
                self.root.after(0, lambda: self.update_status("Loading CV data from database...", "loading"))
                success = self.cv_service.load_all_cv_texts()
                
                if success:
                    stats = self.cv_service.get_cv_statistics()
                    total_cvs = stats.get('total_files', 0)
                    self.root.after(0, lambda: self.update_status(
                        f"Ready - {total_cvs} CVs loaded successfully", "success"
                    ))
                    self.root.after(0, lambda: self.connection_status.configure(
                        text=f"● {total_cvs} CVs loaded"
                    ))
                else:
                    self.root.after(0, lambda: self.update_status(
                        "Failed to load CV data - Check database connection", "error"
                    ))
            else:
                self.root.after(0, lambda: self.update_status(
                    f"Demo mode active - {len(self.demo_cv_data)} sample CVs available", "warning"
                ))
        
        thread = threading.Thread(target=load_data, daemon=True)
        thread.start()
    
    def update_status(self, message, status_type="info"):
        """Update status with color coding"""
        colors = {
            "info": self.colors['text_secondary'],
            "success": self.colors['success'],
            "warning": self.colors['warning'],
            "error": self.colors['error'],
            "loading": self.colors['accent']
        }
        
        self.status_label.configure(
            text=message,
            text_color=colors.get(status_type, self.colors['text_secondary'])
        )
        
        if status_type == "loading":
            self.show_progress()
        else:
            self.hide_progress()
    
    def show_progress(self):
        """Show progress bar with animation"""
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 8))
        self.progress_bar.set(0)
        self.animate_progress()
    
    def hide_progress(self):
        """Hide progress bar"""
        self.progress_bar.pack_forget()
    
    def animate_progress(self):
        """Animate progress bar"""
        if self.is_searching:
            current = self.progress_bar.get()
            if current < 0.9:
                self.progress_bar.set(current + 0.1)
                self.root.after(100, self.animate_progress)
    
    def perform_search(self):
        """Perform CV search with enhanced UI feedback"""
        keywords_text = self.keywords_entry.get().strip()
        if not keywords_text:
            messagebox.showwarning("Input Required", "Please enter keywords to search for CVs")
            self.keywords_entry.focus()
            return
        
        # Disable search button and show loading state
        self.is_searching = True
        self.search_button.configure(text="Searching...", state="disabled")
        self.clear_button.configure(state="disabled")
        
        # Parse keywords
        keywords = [k.strip() for k in keywords_text.split(',') if k.strip()]
        algorithm = self.algorithm_var.get()
        num_matches = self.num_matches_var.get()
        
        # Clear previous results
        for widget in self.results_scrollable.winfo_children():
            widget.destroy()
        
        # Show searching state
        searching_frame = ctk.CTkFrame(self.results_scrollable, corner_radius=10)
        searching_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            searching_frame,
            text="Searching CVs...",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['accent']
        ).pack(pady=20)
        
        self.update_status(f"Searching {len(keywords)} keywords using {algorithm} algorithm...", "loading")
        
        def search_thread():
            try:
                results, timing_info = self.cv_service.search_cvs(keywords, algorithm, num_matches)
                self.root.after(0, lambda: self.display_results(results, timing_info, keywords, algorithm))
                
            except Exception as e:
                self.root.after(0, lambda: self.handle_search_error(str(e)))
            finally:
                self.root.after(0, self.reset_search_state)
        
        thread = threading.Thread(target=search_thread, daemon=True)
        thread.start()
    
    def reset_search_state(self):
        """Reset search button state"""
        self.is_searching = False
        self.search_button.configure(text="Search CVs", state="normal")
        self.clear_button.configure(state="normal")
    
    def handle_search_error(self, error_msg):
        """Handle search errors with user-friendly messages"""
        self.update_status(f"Search failed: {error_msg}", "error")
        
        # Clear results and show error state
        for widget in self.results_scrollable.winfo_children():
            widget.destroy()
        
        error_frame = ctk.CTkFrame(self.results_scrollable, corner_radius=10)
        error_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            error_frame,
            text="Search Error",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['error']
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            error_frame,
            text=error_msg,
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_secondary'],
            wraplength=400
        ).pack(pady=(0, 20))
    
    def display_results(self, results: List[Dict[str, Any]], timing_info: Dict, keywords: List[str], algorithm: str):
        """Display search results with enhanced UI"""
        # Clear searching state
        for widget in self.results_scrollable.winfo_children():
            widget.destroy()
        
        # Update status and counter
        total_time = timing_info.get('total_exact_match_time', 0) + timing_info.get('total_fuzzy_match_time', 0)
        self.update_status(
            f"Found {len(results)} matches in {total_time:.2f}ms using {algorithm} algorithm",
            "success" if results else "warning"
        )
        self.results_counter.configure(text=f"{len(results)} results found")
        
        if not results:
            self.show_no_results(keywords)
            return
        
        # Display timing information
        timing_frame = ctk.CTkFrame(self.results_scrollable, corner_radius=8)
        timing_frame.pack(fill="x", padx=10, pady=(10, 15))
        
        timing_grid = ctk.CTkFrame(timing_frame, fg_color="transparent")
        timing_grid.pack(fill="x", padx=15, pady=10)
        
        # Performance metrics
        metrics = [
            ("Algorithm", algorithm),
            ("Total Time", f"{total_time:.2f}ms"),
            ("Keywords", f"{len(keywords)} terms"),
            ("Results", f"{len(results)} matches")
        ]
        
        for i, (label, value) in enumerate(metrics):
            metric_frame = ctk.CTkFrame(timing_grid, corner_radius=6)
            metric_frame.pack(side="left", fill="x", expand=True, padx=2)
            
            ctk.CTkLabel(
                metric_frame,
                text=label,
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=self.colors['text_secondary']
            ).pack(pady=(8, 2))
            
            ctk.CTkLabel(
                metric_frame,
                text=value,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=self.colors['accent']
            ).pack(pady=(0, 8))
        
        # Display results with enhanced cards
        for i, result in enumerate(results, 1):
            cv_card = CVCard(
                parent=self.results_scrollable,
                result=result,
                rank=i,
                on_view_details=self.show_cv_summary
            )
            cv_card.pack(fill="x", padx=10, pady=5)
    
    def show_no_results(self, keywords):
        """Show no results state with suggestions"""
        no_results_frame = ctk.CTkFrame(self.results_scrollable, corner_radius=10)
        no_results_frame.pack(fill="x", padx=20, pady=30)
        
        # Icon
        icon_frame = ctk.CTkFrame(no_results_frame, width=60, height=60, corner_radius=30)
        icon_frame.pack(pady=(30, 15))
        icon_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            icon_frame,
            text="?",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['warning']
        ).pack(expand=True)
        
        ctk.CTkLabel(
            no_results_frame,
            text="Sorry, no result",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            no_results_frame,
            text=f"No CVs match your search for: {', '.join(keywords)}",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_secondary']
        ).pack(pady=(0, 15))
        
        # Suggestions
        suggestions_frame = ctk.CTkFrame(no_results_frame, fg_color="transparent")
        suggestions_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            suggestions_frame,
            text="Try these suggestions:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w", pady=(0, 5))
        
        suggestions = [
            "• Check your spelling",
            "• Use more general terms",
            "• Try different keywords",
            "• Use fewer search terms"
        ]
        
        for suggestion in suggestions:
            ctk.CTkLabel(
                suggestions_frame,
                text=suggestion,
                font=ctk.CTkFont(size=10),
                text_color=self.colors['text_secondary']
            ).pack(anchor="w", pady=1)
    
    def show_cv_summary(self, result: Dict[str, Any]):
        """Show CV summary in a new window"""
        summary_view = SummaryView(self.root, result)
    
    def clear_search(self):
        """Clear search with smooth animation"""
        self.keywords_entry.delete(0, 'end')
        
        # Clear results with fade effect
        for widget in self.results_scrollable.winfo_children():
            widget.destroy()
        
        self.show_empty_state()
        self.results_counter.configure(text="")
        self.update_status("Search cleared", "info")
        self.keywords_entry.focus()
    
    def setup_hover_effects(self):
        """Setup hover effects for interactive elements"""
        def on_enter(widget, hover_color):
            def handler(event):
                widget.configure(fg_color=hover_color)
            return handler
        
        def on_leave(widget, normal_color):
            def handler(event):
                widget.configure(fg_color=normal_color)
            return handler
        
        # Add hover effects to buttons and interactive elements
        # This would be implemented for custom widgets
    
    def setup_scrolling(self, scrollable_frame):
        """Setup smooth mouse wheel scrolling"""
        def on_mousewheel(event):
            scrollable_frame._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        scrollable_frame.bind("<MouseWheel>", on_mousewheel)
        scrollable_frame.bind("<Button-4>", lambda e: scrollable_frame._parent_canvas.yview_scroll(-1, "units"))
        scrollable_frame.bind("<Button-5>", lambda e: scrollable_frame._parent_canvas.yview_scroll(1, "units"))
        
        if hasattr(scrollable_frame, '_parent_canvas'):
            scrollable_frame._parent_canvas.bind("<MouseWheel>", on_mousewheel)
    
    def setup_keyboard_shortcuts(self):
        """Setup enhanced keyboard shortcuts"""
        # Search shortcuts
        self.keywords_entry.bind("<Return>", lambda e: self.perform_search())
        self.keywords_entry.bind("<KP_Enter>", lambda e: self.perform_search())
        
        # Focus shortcuts
        self.root.bind("<Control-f>", lambda e: self.keywords_entry.focus())
        self.root.bind("<Command-f>", lambda e: self.keywords_entry.focus())  # macOS
        
        # Clear shortcuts
        self.root.bind("<Escape>", lambda e: self.clear_search())
        self.root.bind("<Control-r>", lambda e: self.clear_search())
        
        # Quick algorithm switching
        self.root.bind("<Control-1>", lambda e: self.algorithm_var.set("KMP"))
        self.root.bind("<Control-2>", lambda e: self.algorithm_var.set("BM"))
        self.root.bind("<Control-3>", lambda e: self.algorithm_var.set("AC"))
        
        # Results navigation
        self.root.bind("<Control-plus>", lambda e: self.increase_results())
        self.root.bind("<Control-minus>", lambda e: self.decrease_results())
    
    def increase_results(self):
        """Increase number of results"""
        current = self.num_matches_var.get()
        if current < 100:
            new_value = current + 1
            self.num_matches_var.set(new_value)
            self.update_matches_label(new_value)
    
    def decrease_results(self):
        """Decrease number of results"""
        current = self.num_matches_var.get()
        if current > 1:
            new_value = current - 1
            self.num_matches_var.set(new_value)
            self.update_matches_label(new_value)
    
    def view_cv(self, result: Dict[str, Any]):
        """Open the original CV file with enhanced error handling"""
        profile = result.get('profile', {})
        detail = result.get('detail', {})
        
        cv_path = detail.get('cv_path', '')
        name = f"{profile.get('first_name', 'Unknown')} {profile.get('last_name', '')}".strip()
        
        if not self.database_connected:
            # Enhanced demo mode dialog
            demo_dialog = ctk.CTkToplevel(self.root)
            demo_dialog.geometry("400x250")
            demo_dialog.title("Demo Mode - CV Viewer")
            demo_dialog.transient(self.root)
            demo_dialog.grab_set()
            
            # Center the dialog
            demo_dialog.update_idletasks()
            x = (demo_dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (demo_dialog.winfo_screenheight() // 2) - (250 // 2)
            demo_dialog.geometry(f"400x250+{x}+{y}")
            
            # Content
            content_frame = ctk.CTkFrame(demo_dialog)
            content_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(
                content_frame,
                text="Demo Mode Active",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=(20, 10))
            
            ctk.CTkLabel(
                content_frame,
                text=f"CV for: {name}",
                font=ctk.CTkFont(size=12, weight="bold")
            ).pack(pady=5)
            
            ctk.CTkLabel(
                content_frame,
                text=f"Path: {cv_path}",
                font=ctk.CTkFont(size=10),
                text_color="gray"
            ).pack(pady=5)
            
            ctk.CTkLabel(
                content_frame,
                text="In production mode, this would open the actual PDF file.",
                font=ctk.CTkFont(size=11),
                wraplength=350
            ).pack(pady=10)
            
            ctk.CTkButton(
                content_frame,
                text="Close",
                command=demo_dialog.destroy
            ).pack(pady=(10, 20))
            
            return
        
        if not cv_path:
            messagebox.showwarning("File Not Found", f"CV file path not available for {name}")
            return
        
        # Convert relative path to absolute path
        if not cv_path.startswith('/'):
            from config.AppConfig import AppConfig
            if cv_path.startswith('cv_files/'):
                full_cv_path = os.path.join(AppConfig.BASE_DATA_PATH, cv_path)
            else:
                full_cv_path = os.path.join(AppConfig.BASE_DATA_PATH, 'cv_files', cv_path)
        else:
            full_cv_path = cv_path
        
        # Check if file exists
        if not os.path.exists(full_cv_path):
            messagebox.showerror("File Not Found", f"CV file not found for {name}:\n{full_cv_path}")
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
        """Run the application with enhanced error handling"""
        try:
            # Set window icon if available
            try:
                # You can add an icon file here
                # self.root.iconbitmap("icon.ico")
                pass
            except:
                pass
            
            # Center window on screen
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            
            # Start the main loop
            self.root.mainloop()
            
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        except Exception as e:
            print(f"Application error: {e}")
            messagebox.showerror("Application Error", f"An unexpected error occurred: {e}")
        finally:
            # Cleanup
            if hasattr(self, 'db_manager') and self.db_manager:
                try:
                    self.db_manager.close()
                except:
                    pass

# Simple CV Service for demo mode
class SimpleCVService:
    def __init__(self, demo_data, debug=False):
        self.demo_data = demo_data
        self.debug = debug
    
    def load_all_cv_texts(self):
        return True
    
    def get_cv_statistics(self):
        return {'total_files': len(self.demo_data)}
    
    def search_cvs(self, keywords, algorithm, num_matches):
        """Simple demo search implementation"""
        import time
        import random
        
        start_time = time.time()
        
        results = []
        for filename, content in self.demo_data.items():
            score = 0
            matched_keywords = []
            
            for keyword in keywords:
                if keyword.lower() in content.lower():
                    score += content.lower().count(keyword.lower())
                    matched_keywords.append(keyword)
            
            if score > 0:
                # Create demo result structure
                name_parts = filename.replace('_CV.pdf', '').split('_')
                first_name = name_parts[0] if name_parts else "Unknown"
                last_name = name_parts[1] if len(name_parts) > 1 else ""
                
                result = {
                    'profile': {
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': f"{first_name.lower()}.{last_name.lower()}@email.com",
                        'phone': f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
                    },
                    'detail': {
                        'cv_path': f"cv_files/{filename}",
                        'summary': content
                    },
                    'match_info': {
                        'total_score': score,
                        'matched_keywords': matched_keywords,
                        'match_percentage': min(100, (score / len(keywords)) * 25)
                    }
                }
                results.append(result)
        
        # Sort by score and limit results
        results.sort(key=lambda x: x['match_info']['total_score'], reverse=True)
        results = results[:num_matches]
        
        end_time = time.time()
        timing_info = {
            'total_exact_match_time': (end_time - start_time) * 1000,
            'total_fuzzy_match_time': 0
        }
        
        return results, timing_info

if __name__ == "__main__":
    app = App()
    app.run()