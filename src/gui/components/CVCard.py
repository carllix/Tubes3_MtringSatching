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
            'border': '#404040',
            'hover': '#3a3a3a'
        }
        
        # Configure frame with professional styling
        self.configure(
            fg_color=self.colors['card_bg'],
            border_width=1,
            border_color=self.colors['border'],
            corner_radius=12,
            height=220
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
        
        # Keywords section
        self.setup_keywords(main_container)
        
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
            height=50
        )
        metrics_frame.pack(fill="x", pady=(0, 12))
        metrics_frame.pack_propagate(False)
        
        # Calculate metrics
        total_matches, total_words, keyword_count = self.calculate_metrics()
        
        # Metrics grid
        metrics_container = ctk.CTkFrame(metrics_frame, fg_color="transparent")
        metrics_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Create metric items
        metrics = [
            ("Keywords", str(keyword_count), self.colors['accent']),
            ("Matches", str(total_matches), self.colors['success']),
            ("Total Words", str(total_words), self.colors['warning'])
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
                font=ctk.CTkFont(size=9),
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
    
    def setup_keywords(self, parent):
        """Setup keywords section with tags"""
        # Get matched keywords
        matched_keywords = self.get_matched_keywords()
        exact_matches = self.result.get('exact_matches', {})
        
        if matched_keywords:
            keywords_frame = ctk.CTkFrame(
                parent,
                fg_color=self.colors['surface_light'],
                corner_radius=8
            )
            keywords_frame.pack(fill="x", pady=(0, 12))
            
            # Header
            header_label = ctk.CTkLabel(
                keywords_frame,
                text="Matched Keywords",
                font=ctk.CTkFont(size=10, weight="bold"),
                text_color=self.colors['text_secondary']
            )
            header_label.pack(anchor="w", padx=12, pady=(8, 4))
            
            # Keywords container with scrolling
            keywords_container = ctk.CTkFrame(keywords_frame, fg_color="transparent")
            keywords_container.pack(fill="x", padx=12, pady=(0, 8))
            
            # Create keyword tags
            self.create_keyword_tags(keywords_container, matched_keywords, exact_matches)
    
    def create_keyword_tags(self, parent, keywords, exact_matches):
        """Create keyword tags with counts"""
        # Create a frame for tags that can wrap
        tags_frame = ctk.CTkFrame(parent, fg_color="transparent")
        tags_frame.pack(fill="x")
        
        current_row_frame = None
        current_width = 0
        max_width = 650  # Approximate max width
        
        for keyword in keywords[:8]:  # Limit to 8 keywords for space
            # Get count if available
            count = exact_matches.get(keyword, 1) if isinstance(exact_matches, dict) else 1
            tag_text = f"{keyword} ({count})" if count > 1 else keyword
            
            # Estimate tag width (rough calculation)
            estimated_width = len(tag_text) * 8 + 20
            
            # Create new row if needed
            if current_row_frame is None or current_width + estimated_width > max_width:
                current_row_frame = ctk.CTkFrame(tags_frame, fg_color="transparent")
                current_row_frame.pack(fill="x", pady=1)
                current_width = 0
            
            # Create tag
            tag = ctk.CTkFrame(
                current_row_frame,
                fg_color=self.colors['primary'],
                corner_radius=12,
                height=24
            )
            tag.pack(side="left", padx=2, pady=1)
            tag.pack_propagate(False)
            
            tag_label = ctk.CTkLabel(
                tag,
                text=tag_text,
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color="white"
            )
            tag_label.pack(padx=8, pady=4)
            
            current_width += estimated_width
        
        # Show "more" indicator if there are additional keywords
        if len(keywords) > 8:
            more_count = len(keywords) - 8
            more_tag = ctk.CTkFrame(
                current_row_frame,
                fg_color=self.colors['text_muted'],
                corner_radius=12,
                height=24
            )
            more_tag.pack(side="left", padx=2, pady=1)
            more_tag.pack_propagate(False)
            
            more_label = ctk.CTkLabel(
                more_tag,
                text=f"+{more_count}",
                font=ctk.CTkFont(size=9, weight="bold"),
                text_color="white"
            )
            more_label.pack(padx=6, pady=4)
    
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
    
    def calculate_metrics(self):
        """Calculate match metrics for display"""
        # Get matched keywords
        matched_keywords = self.get_matched_keywords()
        keyword_count = len(matched_keywords)
        
        # Get total matches
        total_matches = (self.result.get('total_exact_matches', 0) or 
                        self.result.get('exact_matches_count', 0) or
                        keyword_count)
        
        # Calculate total word occurrences
        exact_matches = self.result.get('exact_matches', {})
        total_words = 0
        if isinstance(exact_matches, dict):
            total_words = sum(count for count in exact_matches.values() if isinstance(count, int))
        
        return total_matches, total_words, keyword_count
    
    def get_matched_keywords(self):
        """Get matched keywords from result data"""
        matched_keywords = self.result.get('matched_keywords', [])
        
        if isinstance(matched_keywords, dict):
            # PatternMatcher format: {'exact': [...], 'fuzzy': [...]}
            exact_keywords = matched_keywords.get('exact', [])
            fuzzy_keywords = matched_keywords.get('fuzzy', [])
            return exact_keywords + fuzzy_keywords
        elif isinstance(matched_keywords, list):
            # Demo/simple format: [keyword1, keyword2, ...]
            return matched_keywords
        else:
            return []
    
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