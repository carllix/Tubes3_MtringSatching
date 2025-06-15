import customtkinter as ctk
import os
import subprocess
from tkinter import messagebox
from typing import Dict, Any, List, Callable

class CVCard(ctk.CTkFrame):
    """Professional CV Card component for displaying search results"""
    
    def __init__(self, parent, result: Dict[str, Any], rank: int = 1, 
                 on_view_details: Callable = None):
        super().__init__(parent)
        self.result = result
        self.rank = rank
        self.on_view_details = on_view_details
        
        # Professional color scheme
        self.colors = {
            'card_bg': '#2b2b2b',
            'surface': '#333333',
            'surface_light': '#404040',
            'primary': '#1f538d',
            'accent': '#36719e',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'text_muted': '#808080',
            'success': '#4caf50',
            'warning': '#ff9800',
            'fuzzy': '#9c27b0',
            'border': '#404040',
            'hover': '#3a3a3a'
        }
        
        # Configure frame with professional styling
        self.configure(
            fg_color=self.colors['card_bg'],
            border_width=1,
            border_color=self.colors['border'],
            corner_radius=12,
            height=280  # Increased height for fuzzy matches
        )
        
        # Add hover effect
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
        self.setup_card()
    
    def on_enter(self, event):
        """Hover effect on mouse enter"""
        self.configure(border_color=self.colors['accent'])
    
    def on_leave(self, event):
        """Remove hover effect on mouse leave"""
        self.configure(border_color=self.colors['border'])
    
    def setup_card(self):
        """Setup the professional CV card layout"""
        # Main container with padding
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Header section
        self.setup_header(main_container)
        
        # Metrics section
        self.setup_metrics(main_container)
        
        # Keywords section with fuzzy matches
        self.setup_keywords_with_fuzzy(main_container)
        
        # Actions section
        self.setup_actions(main_container)
    
    def setup_header(self, parent):
        """Setup card header with rank and name"""
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 12))
        
        # Rank badge with modern design
        rank_badge = ctk.CTkFrame(
            header_frame,
            fg_color=self.colors['primary'],
            corner_radius=8,
            width=40,
            height=28
        )
        rank_badge.pack(side="left", padx=(0, 15))
        rank_badge.pack_propagate(False)
        
        rank_label = ctk.CTkLabel(
            rank_badge,
            text=f"#{self.rank}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="white"
        )
        rank_label.pack(expand=True)
        
        # Name and basic info
        info_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_container.pack(side="left", fill="x", expand=True)
        
        # Get profile info
        profile = self.result.get('profile', {})
        first_name = profile.get('first_name', 'Unknown')
        last_name = profile.get('last_name', '')
        name_text = f"{first_name} {last_name}".strip()
        
        # Name label
        name_label = ctk.CTkLabel(
            info_container,
            text=name_text,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # Role label
        detail = self.result.get('detail', {})
        role = detail.get('application_role', 'Position not specified')
        role_label = ctk.CTkLabel(
            info_container,
            text=role,
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        role_label.pack(anchor="w", pady=(2, 0))
    
    def setup_metrics(self, parent):
        """Setup metrics section with match statistics"""
        metrics_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface'],
            corner_radius=8,
            height=80
        )
        metrics_frame.pack(fill="x", pady=(0, 12))
        metrics_frame.pack_propagate(False)
        
        # Calculate metrics including fuzzy matches
        exact_count, fuzzy_count, total_words = self.calculate_detailed_metrics()
        
        # Metrics grid
        metrics_container = ctk.CTkFrame(metrics_frame, fg_color="transparent")
        metrics_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Create metric items
        metrics = [
            ("Exact", str(exact_count), self.colors['success']),
            ("Fuzzy", str(fuzzy_count), self.colors['fuzzy']),
            ("Words", str(total_words), self.colors['warning'])
        ]
        
        for i, (label, value, color) in enumerate(metrics):
            metric_frame = ctk.CTkFrame(metrics_container, fg_color="transparent")
            metric_frame.pack(side="left", fill="x", expand=True)
            
            # Value (large)
            value_label = ctk.CTkLabel(
                metric_frame,
                text=value,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color
            )
            value_label.pack()
            
            # Label (small)
            label_label = ctk.CTkLabel(
                metric_frame,
                text=label,
                font=ctk.CTkFont(size=13),
                text_color=self.colors['text_muted']
            )
            label_label.pack()
            
            # Add separator (except for last item)
            if i < len(metrics) - 1:
                separator = ctk.CTkFrame(
                    metrics_container,
                    fg_color=self.colors['border'],
                    width=1,
                    height=30
                )
                separator.pack(side="left", padx=10)
    
    def setup_keywords_with_fuzzy(self, parent):
        """Setup keywords section with both exact and fuzzy matches"""
        # Get match data
        exact_keywords, fuzzy_keywords = self.get_separated_keywords()
        exact_matches = self.result.get('exact_matches', {})
        fuzzy_matches = self.result.get('fuzzy_matches', {})
        fuzzy_matches_detail = self.result.get('fuzzy_matches_detail', {})
        
        if exact_keywords or fuzzy_keywords:
            keywords_frame = ctk.CTkFrame(
                parent,
                fg_color=self.colors['surface_light'],
                corner_radius=8
            )
            keywords_frame.pack(fill="x", pady=(0, 12))
            
            # Create sections for exact and fuzzy matches
            if exact_keywords:
                self.create_exact_matches_section(keywords_frame, exact_keywords, exact_matches)
            
            if fuzzy_keywords:
                self.create_fuzzy_matches_section(keywords_frame, fuzzy_keywords, fuzzy_matches, fuzzy_matches_detail)
    
    def create_exact_matches_section(self, parent, exact_keywords, exact_matches):
        """Create exact matches section"""
        # Exact matches header
        exact_header = ctk.CTkLabel(
            parent,
            text="Exact Matches",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.colors['success']
        )
        exact_header.pack(anchor="w", padx=12, pady=(8, 4))
        
        # Exact keywords container
        exact_container = ctk.CTkFrame(parent, fg_color="transparent")
        exact_container.pack(fill="x", padx=12, pady=(0, 4))
        
        self.create_keyword_tags(exact_container, exact_keywords, exact_matches, self.colors['success'])
    
    def create_fuzzy_matches_section(self, parent, fuzzy_keywords, fuzzy_matches, fuzzy_matches_detail):
        """Create fuzzy matches section with detailed information"""
        # Fuzzy matches header
        fuzzy_header = ctk.CTkLabel(
            parent,
            text="Fuzzy Matches",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=self.colors['fuzzy']
        )
        fuzzy_header.pack(anchor="w", padx=12, pady=(4, 4))
        
        # Fuzzy matches container
        fuzzy_container = ctk.CTkFrame(parent, fg_color="transparent")
        fuzzy_container.pack(fill="x", padx=12, pady=(0, 8))
        
        # Create detailed fuzzy match display
        for keyword in fuzzy_keywords[:4]:  # Limit for space
            keyword_frame = ctk.CTkFrame(fuzzy_container, fg_color="transparent")
            keyword_frame.pack(fill="x", pady=1)
            
            # Get fuzzy match details
            score = fuzzy_matches.get(keyword, 0) if isinstance(fuzzy_matches, dict) else 0
            
            # Create keyword tag with score
            tag_frame = ctk.CTkFrame(
                keyword_frame,
                fg_color=self.colors['fuzzy'],
                corner_radius=12,
                height=20
            )
            tag_frame.pack(side="left", pady=1)
            tag_frame.pack_propagate(False)
            
            # Keyword and score
            tag_text = f"{keyword} ({score:.2f})" if score > 0 else keyword
            tag_label = ctk.CTkLabel(
                tag_frame,
                text=tag_text,
                font=ctk.CTkFont(size=8, weight="bold"),
                text_color="white"
            )
            tag_label.pack(padx=6, pady=2)
            
            # Show ALL matches with the highest similarity score
            if (fuzzy_matches_detail and keyword in fuzzy_matches_detail and 
                fuzzy_matches_detail[keyword]):
                matches = fuzzy_matches_detail[keyword]
                if isinstance(matches, list) and len(matches) > 0:
                    # Find the highest score
                    highest_score = max(match[1] for match in matches)
                    # Get all matches with that score
                    best_matches = [match for match in matches if match[1] == highest_score]
                    
                    if len(best_matches) == 1:
                        # Single best match
                        similar_word = best_matches[0][0]
                        similarity_score = best_matches[0][1]
                        detail_label = ctk.CTkLabel(
                            keyword_frame,
                            text=f"→ '{similar_word}' ({similarity_score:.2f})",
                            font=ctk.CTkFont(size=10),
                            text_color=self.colors['text_muted']
                        )
                        detail_label.pack(side="left", padx=(8, 0))
                    else:
                        # Multiple matches with same score - show all
                        words = ", ".join([f"'{match[0]}'" for match in best_matches])
                        similarity_score = best_matches[0][1]
                        detail_label = ctk.CTkLabel(
                            keyword_frame,
                            text=f"→ {words} ({similarity_score:.2f})",
                            font=ctk.CTkFont(size=10),
                            text_color=self.colors['text_muted'],
                            wraplength=400
                        )
                        detail_label.pack(side="left", padx=(8, 0))
        
        # Show "more" indicator if there are additional fuzzy matches
        if len(fuzzy_keywords) > 4:
            more_count = len(fuzzy_keywords) - 4
            more_frame = ctk.CTkFrame(fuzzy_container, fg_color="transparent")
            more_frame.pack(fill="x", pady=1)
            
            more_tag = ctk.CTkFrame(
                more_frame,
                fg_color=self.colors['text_muted'],
                corner_radius=12,
                height=20
            )
            more_tag.pack(side="left")
            more_tag.pack_propagate(False)
            
            more_label = ctk.CTkLabel(
                more_tag,
                text=f"+{more_count} more fuzzy matches",
                font=ctk.CTkFont(size=8, weight="bold"),
                text_color="white"
            )
            more_label.pack(padx=6, pady=2)
    
    def create_keyword_tags(self, parent, keywords, matches, color):
        """Create keyword tags with counts"""
        # Create a frame for tags that can wrap
        tags_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tags_frame.pack(fill="x")
        
        current_row_frame = None
        current_width = 0
        max_width = 650
        
        for keyword in keywords[:6]:  # Limit for space
            # Get count if available
            count = matches.get(keyword, 1) if isinstance(matches, dict) else 1
            tag_text = f"{keyword} ({count})" if count > 1 else keyword
            
            # Estimate tag width
            estimated_width = len(tag_text) * 8 + 20
            
            # Create new row if needed
            if current_row_frame is None or current_width + estimated_width > max_width:
                current_row_frame = ctk.CTkFrame(tags_frame, fg_color="transparent")
                current_row_frame.pack(fill="x", pady=1)
                current_width = 0
            
            # Create tag
            tag = ctk.CTkFrame(
                current_row_frame,
                fg_color=color,
                corner_radius=12,
                height=22
            )
            tag.pack(side="left", padx=2, pady=1)
            tag.pack_propagate(False)
            
            tag_label = ctk.CTkLabel(
                tag,
                text=tag_text,
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color="white"
            )
            tag_label.pack(padx=6, pady=3)
            
            current_width += estimated_width
        
        # Show "more" indicator if there are additional keywords
        if len(keywords) > 6:
            more_count = len(keywords) - 6
            more_tag = ctk.CTkFrame(
                current_row_frame,
                fg_color=self.colors['text_muted'],
                corner_radius=12,
                height=22
            )
            more_tag.pack(side="left", padx=2, pady=1)
            more_tag.pack_propagate(False)
            
            more_label = ctk.CTkLabel(
                more_tag,
                text=f"+{more_count}",
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color="white"
            )
            more_label.pack(padx=6, pady=3)
    
    def setup_actions(self, parent):
        """Setup action buttons"""
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.pack(fill="x", side="bottom")
        
        # Score display (if available)
        score = self.result.get('combined_score', self.result.get('match_score', 0))
        if score > 0:
            score_frame = ctk.CTkFrame(
                actions_frame,
                fg_color=self.colors['surface'],
                corner_radius=6,
                height=24
            )
            score_frame.pack(side="left", padx=(0, 10))
            score_frame.pack_propagate(False)
            
            score_label = ctk.CTkLabel(
                score_frame,
                text=f"Score: {score:.1f}",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=self.colors['accent']
            )
            score_label.pack(padx=8, pady=4)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        # View Details button
        if self.on_view_details:
            view_button = ctk.CTkButton(
                buttons_frame,
                text="Details",
                command=lambda: self.on_view_details(self.result),
                font=ctk.CTkFont(size=11, weight="bold"),
                height=32,
                width=80,
                corner_radius=8,
                fg_color=self.colors['primary'],
                hover_color=self.colors['accent']
            )
            view_button.pack(side="right", padx=(8, 0))
        
        # Open CV button
        detail = self.result.get('detail', {})
        cv_path = detail.get('cv_path', '')
        if cv_path:
            open_button = ctk.CTkButton(
                buttons_frame,
                text="Open CV",
                command=lambda: self.open_cv_file(cv_path),
                font=ctk.CTkFont(size=11, weight="bold"),
                height=32,
                width=80,
                corner_radius=8,
                fg_color=self.colors['surface'],
                hover_color=self.colors['hover'],
                border_width=1,
                border_color=self.colors['border']
            )
            open_button.pack(side="right", padx=(8, 0))
    
    def calculate_detailed_metrics(self):
        """Calculate detailed match metrics including fuzzy matches"""
        exact_keywords, fuzzy_keywords = self.get_separated_keywords()
        
        # Calculate total word occurrences for exact matches
        exact_matches = self.result.get('exact_matches', {})
        total_words = 0
        if isinstance(exact_matches, dict):
            total_words = sum(count for count in exact_matches.values() if isinstance(count, int))
        
        # Calculate total fuzzy matches (count all matched words, not just keywords)
        fuzzy_matches_detail = self.result.get('fuzzy_matches_detail', {})
        total_fuzzy_matches = 0
        
        if isinstance(fuzzy_matches_detail, dict):
            for keyword in fuzzy_keywords:
                if keyword in fuzzy_matches_detail:
                    matches = fuzzy_matches_detail[keyword]
                    if isinstance(matches, list):
                        total_fuzzy_matches += len(matches)
                        # Count actual word occurrences in CV text for each matched word
                        cv_text = self.get_cv_text()
                        if cv_text:
                            for match_word, similarity in matches:
                                # Count how many times this matched word appears in the CV
                                word_count = self.count_word_in_text(match_word, cv_text)
                                total_words += word_count
                        else:
                            # Fallback: count unique matched words
                            unique_words = set(match[0] for match in matches)
                            total_words += len(unique_words)
                    else:
                        total_fuzzy_matches += 1
                        total_words += 1
        else:
            # Fallback to keyword count if detailed info not available
            total_fuzzy_matches = len(fuzzy_keywords)
            total_words += len(fuzzy_keywords)
        
        return len(exact_keywords), total_fuzzy_matches, total_words
    
    def get_cv_text(self):
        """Get the CV text content for word counting"""
        # Try to get CV text from various possible locations in the result
        detail = self.result.get('detail', {})
        
        # Check common text fields
        cv_text = (detail.get('cv_text') or 
                  detail.get('text') or 
                  detail.get('content') or
                  self.result.get('cv_text') or
                  self.result.get('text') or
                  self.result.get('content'))
        
        return cv_text.lower() if cv_text else None
    
    def count_word_in_text(self, word, text):
        """Count occurrences of a word in text (case-insensitive)"""
        if not word or not text:
            return 0
        
        import re
        # Use word boundaries to match whole words only
        pattern = r'\b' + re.escape(word.lower()) + r'\b'
        matches = re.findall(pattern, text.lower())
        return len(matches)
    
    def get_separated_keywords(self):
        """Get exact and fuzzy keywords separately"""
        matched_keywords = self.result.get('matched_keywords', [])
        
        if isinstance(matched_keywords, dict):
            # PatternMatcher format: {'exact': [...], 'fuzzy': [...]}
            exact_keywords = matched_keywords.get('exact', [])
            fuzzy_keywords = matched_keywords.get('fuzzy', [])
            return exact_keywords, fuzzy_keywords
        elif isinstance(matched_keywords, list):
            # Demo/simple format: assume all are exact
            return matched_keywords, []
        else:
            return [], []
    
    def open_cv_file(self, cv_path: str):
        """Open CV file with professional error handling"""
        try:
            # Handle relative paths
            if not os.path.isabs(cv_path):
                try:
                    from src.config.AppConfig import AppConfig
                    if cv_path.startswith('cv_files/'):
                        full_path = os.path.join(AppConfig.BASE_DATA_PATH, cv_path)
                    else:
                        full_path = os.path.join(AppConfig.BASE_DATA_PATH, 'cv_files', cv_path)
                except ImportError:
                    # Fallback if AppConfig is not available
                    full_path = cv_path
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
                # Professional error dialog
                self.show_file_not_found_dialog(cv_path)
                
        except Exception as e:
            self.show_error_dialog(f"Failed to open CV file: {str(e)}")
    
    def show_file_not_found_dialog(self, cv_path):
        """Show professional file not found dialog"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("File Not Found")
        dialog.geometry("400x200")
        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Content
        content_frame = ctk.CTkFrame(dialog)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Error icon and message
        ctk.CTkLabel(
            content_frame,
            text="File Not Found",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#f44336"
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            content_frame,
            text=f"The CV file could not be located:\n{cv_path}",
            font=ctk.CTkFont(size=11),
            wraplength=350
        ).pack(pady=(0, 20))
        
        # Close button
        ctk.CTkButton(
            content_frame,
            text="Close",
            command=dialog.destroy,
            width=100
        ).pack(pady=(0, 10))
    
    def show_error_dialog(self, error_message):
        """Show professional error dialog"""
        messagebox.showerror("Error", error_message)