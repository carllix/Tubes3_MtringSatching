import customtkinter as ctk
import os
import subprocess
from tkinter import messagebox
from typing import Dict, Any, List, Callable

class CVCard(ctk.CTkFrame):
    """CV Card component for displaying search results"""
    
    def __init__(self, parent, result: Dict[str, Any], rank: int = 1, 
                 on_view_details: Callable = None):
        super().__init__(parent)
        self.result = result
        self.rank = rank
        self.on_view_details = on_view_details
        
        # Configure frame appearance - clean white theme
        self.configure(
            fg_color="white",
            border_width=1,
            border_color="#e0e0e0",
            corner_radius=4
        )
        
        self.setup_card()
    
    def setup_card(self):
        """Setup the CV card layout"""
        # Header frame with ranking and name
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=16, pady=(16, 8))
        
        # Rank badge
        rank_label = ctk.CTkLabel(
            header_frame,
            text=f"#{self.rank}",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#f0f0f0",
            text_color="#666666",
            width=32,
            height=24,
            corner_radius=4
        )
        rank_label.pack(side="left", padx=(0, 12))
        
        # Name and details
        profile = self.result.get('profile', {})
        first_name = profile.get('first_name', 'Unknown')
        last_name = profile.get('last_name', '')
        name_text = f"{first_name} {last_name}".strip()
        
        # Get total matches - check multiple possible keys for compatibility
        total_matches = (self.result.get('total_exact_matches', 0) or 
                        self.result.get('exact_matches_count', 0))
        
        # Handle different data structures for matched_keywords
        matched_keywords = self.result.get('matched_keywords', [])
        if isinstance(matched_keywords, dict):
            # PatternMatcher format: {'exact': [...], 'fuzzy': [...]}
            exact_keywords = matched_keywords.get('exact', [])
            fuzzy_keywords = matched_keywords.get('fuzzy', [])
            if total_matches == 0:
                total_matches = len(exact_keywords) + len(fuzzy_keywords)
        elif isinstance(matched_keywords, list):
            # Demo/simple format: [keyword1, keyword2, ...]
            if total_matches == 0:
                total_matches = len(matched_keywords)
        
        # Calculate total word occurrences from exact_matches
        exact_matches = self.result.get('exact_matches', {})
        total_word_occurrences = 0
        if isinstance(exact_matches, dict):
            total_word_occurrences = sum(count for count in exact_matches.values() if isinstance(count, int))
        
        # Create a more informative header
        if total_word_occurrences > 0:
            header_text = f"{name_text} • {total_matches} keywords • {total_word_occurrences} total words"
        else:
            header_text = f"{name_text} • {total_matches} matches"
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=header_text,
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#333333",
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True)
        
        # Match details
        details_frame = ctk.CTkFrame(self, fg_color="transparent")
        details_frame.pack(fill="x", padx=16, pady=(0, 12))
        
        # Show matched keywords and counts
        matched_keywords = self.result.get('matched_keywords', [])
        exact_matches = self.result.get('exact_matches', {})
        
        # Handle different data structures for matched_keywords
        exact_keywords = []
        fuzzy_keywords = []
        
        if isinstance(matched_keywords, dict):
            # PatternMatcher format: {'exact': [...], 'fuzzy': [...]}
            exact_keywords = matched_keywords.get('exact', [])
            fuzzy_keywords = matched_keywords.get('fuzzy', [])
            # Combine for total list
            all_matched_keywords = exact_keywords + fuzzy_keywords
        elif isinstance(matched_keywords, list):
            # Demo/simple format: [keyword1, keyword2, ...]
            all_matched_keywords = matched_keywords
            exact_keywords = matched_keywords  # Assume all are exact for demo
        else:
            all_matched_keywords = []
        
        # Create match summary with clean styling
        match_summary_frame = ctk.CTkFrame(
            details_frame,
            fg_color="#f8f9fa",
            border_width=1,
            border_color="#e0e0e0",
            corner_radius=4
        )
        match_summary_frame.pack(fill="x", padx=8, pady=(6, 4))
        
        if all_matched_keywords and exact_matches:
            # Display matched keywords with counts
            match_details = []
            total_word_count = 0
            
            for keyword in all_matched_keywords:
                if isinstance(exact_matches, dict) and keyword in exact_matches:
                    count = exact_matches[keyword]
                    match_details.append(f"{keyword} ({count})")
                    total_word_count += count
                else:
                    match_details.append(keyword)
            
            # Show total word count prominently
            if total_word_count > 0:
                count_label = ctk.CTkLabel(
                    match_summary_frame,
                    text=f"Total Words Found: {total_word_count}",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    fg_color="#4a90e2",
                    text_color="white",
                    corner_radius=4,
                    height=24
                )
                count_label.pack(side="top", anchor="w", padx=8, pady=(6, 2))
            
            # Show keyword breakdown
            matches_text = "Keywords: " + ", ".join(match_details)
            matches_label = ctk.CTkLabel(
                match_summary_frame,
                text=matches_text,
                font=ctk.CTkFont(size=11),
                text_color="#333333",
                anchor="w",
                wraplength=700
            )
            matches_label.pack(anchor="w", padx=8, pady=(2, 6))
        elif all_matched_keywords:
            # Fallback if no exact_matches dict but we have keywords
            matches_text = "Keywords Found: " + ", ".join(all_matched_keywords)
            matches_label = ctk.CTkLabel(
                match_summary_frame,
                text=matches_text,
                font=ctk.CTkFont(size=11),
                text_color="#333333",
                anchor="w",
                wraplength=700
            )
            matches_label.pack(anchor="w", padx=8, pady=6)
        else:
            # No matches found
            no_matches_label = ctk.CTkLabel(
                match_summary_frame,
                text="No keyword matches found",
                font=ctk.CTkFont(size=11),
                text_color="#666666",
                anchor="w"
            )
            no_matches_label.pack(anchor="w", padx=8, pady=6)
        
        # Additional info frame
        info_frame = ctk.CTkFrame(
            details_frame,
            fg_color="#f8f9fa",
            border_width=1,
            border_color="#e0e0e0",
            corner_radius=4
        )
        info_frame.pack(fill="x", padx=8, pady=(0, 6))
        
        # Role information
        detail = self.result.get('detail', {})
        role = detail.get('application_role', 'Not specified')
        role_label = ctk.CTkLabel(
            info_frame,
            text=f"Role: {role}",
            font=ctk.CTkFont(size=11),
            text_color="#333333",
            anchor="w"
        )
        role_label.pack(anchor="w", padx=8, pady=(6, 2))
        
        # Score information
        score = self.result.get('combined_score', self.result.get('match_score', 0))
        if score > 0:
            score_label = ctk.CTkLabel(
                info_frame,
                text=f"Match Score: {score:.1f}",
                font=ctk.CTkFont(size=11),
                text_color="#333333",
                anchor="w"
            )
            score_label.pack(anchor="w", padx=8, pady=(0, 6))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        buttons_frame.pack(fill="x", padx=12, pady=(0, 12))
        
        # View Details button
        if self.on_view_details:
            view_button = ctk.CTkButton(
                buttons_frame,
                text="View Details",
                command=lambda: self.on_view_details(self.result),
                font=ctk.CTkFont(size=12),
                height=32,
                corner_radius=4,
                fg_color="#4a90e2",
                hover_color="#357abd"
            )
            view_button.pack(side="right", padx=8, pady=6)
        
        # Open CV button
        cv_path = detail.get('cv_path', '')
        if cv_path:
            open_button = ctk.CTkButton(
                buttons_frame,
                text="Open CV",
                command=lambda: self.open_cv_file(cv_path),
                font=ctk.CTkFont(size=12),
                height=32,
                corner_radius=4,
                fg_color="#6c757d",
                hover_color="#545b62"
            )
            open_button.pack(side="right", padx=(8, 0), pady=6)
    
    def open_cv_file(self, cv_path: str):
        """Open CV file in default application"""
        try:
            # Handle relative paths
            if not os.path.isabs(cv_path):
                # Assume CV files are in the data/cv_files directory
                from src.config.AppConfig import AppConfig
                if cv_path.startswith('cv_files/'):
                    full_path = os.path.join(AppConfig.BASE_DATA_PATH, cv_path)
                else:
                    full_path = os.path.join(AppConfig.BASE_DATA_PATH, 'cv_files', cv_path)
            else:
                full_path = cv_path
            
            if os.path.exists(full_path):
                # Use system default application to open the file
                if os.name == 'nt':  # Windows
                    os.startfile(full_path)
                elif os.name == 'posix':  # macOS and Linux
                    subprocess.run(['open', full_path], check=True)
                else:
                    subprocess.run(['xdg-open', full_path], check=True)
            else:
                messagebox.showerror("Error", f"CV file not found: {full_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open CV file: {str(e)}")
