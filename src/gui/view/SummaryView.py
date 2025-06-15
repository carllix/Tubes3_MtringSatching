import customtkinter as ctk
from typing import Dict, Any

class SummaryView(ctk.CTkToplevel):
    """Professional summary view window for displaying CV details"""
    
    def __init__(self, parent, result: Dict[str, Any]):
        super().__init__(parent)
        self.result = result
        
        # Professional color scheme matching main app
        self.colors = {
            'background': '#1a1a1a',
            'surface': '#2b2b2b',
            'surface_light': '#333333',
            'primary': '#1f538d',
            'accent': '#36719e',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'text_muted': '#808080',
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336',
            'border': '#404040'
        }
        
        self.setup_window()
        self.setup_content()
    
    def setup_window(self):
        """Setup the professional summary window"""
        # Get candidate name for title
        profile = self.result.get('profile', {})
        first_name = profile.get('first_name', 'Unknown')
        last_name = profile.get('last_name', '')
        candidate_name = f"{first_name} {last_name}".strip()
        
        self.title(f"CV Details - {candidate_name}")
        self.geometry("1000x750")
        self.resizable(True, True)
        self.minsize(800, 600)
        
        # Make window modal
        self.transient(self.master)
        self.grab_set()
        
        # Set colors
        self.configure(fg_color=self.colors['background'])
        
        # Center the window
        self.center_window()
        
        # Add close handler
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center window on screen"""
        self.update_idletasks()
        width = 1000
        height = 750
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_content(self):
        """Setup the professional content layout"""
        # Main container with modern styling
        main_container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header_section(main_container)
        
        # Content area with tabs
        self.create_tabbed_content(main_container)
        
        # Footer with actions
        self.create_footer_section(main_container)
    
    def create_header_section(self, parent):
        """Create professional header section"""
        header_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface'],
            corner_radius=12,
            height=100
        )
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = ctk.CTkFrame(header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Left side - candidate info
        left_info = ctk.CTkFrame(header_content, fg_color="transparent")
        left_info.pack(side="left", fill="both", expand=True)
        
        # Candidate name
        profile = self.result.get('profile', {})
        first_name = profile.get('first_name', 'Unknown')
        last_name = profile.get('last_name', '')
        candidate_name = f"{first_name} {last_name}".strip()
        
        name_label = ctk.CTkLabel(
            left_info,
            text=candidate_name,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # Role and contact info
        detail = self.result.get('detail', {})
        role = detail.get('application_role', 'Position not specified')
        phone = profile.get('phone_number', '')
        
        info_text = role
        if phone:
            info_text += f" • {phone}"
        
        info_label = ctk.CTkLabel(
            left_info,
            text=info_text,
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_secondary'],
            anchor="w"
        )
        info_label.pack(anchor="w", pady=(5, 0))
        
        # Right side - match statistics
        self.create_match_statistics(header_content)
    
    def create_match_statistics(self, parent):
        """Create match statistics panel"""
        stats_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_light'],
            corner_radius=8,
            width=250
        )
        stats_frame.pack(side="right", fill="y", padx=(20, 0))
        stats_frame.pack_propagate(False)
        
        # Stats header
        ctk.CTkLabel(
            stats_frame,
            text="Match Statistics",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors['text_secondary']
        ).pack(pady=(15, 10))
        
        # Calculate statistics
        matched_keywords = self.get_matched_keywords()
        exact_matches = self.result.get('exact_matches', {})
        total_words = sum(count for count in exact_matches.values() if isinstance(count, int)) if isinstance(exact_matches, dict) else 0
        score = self.result.get('combined_score', self.result.get('match_score', 0))
        
        # Statistics
        stats = [
            ("Keywords Found", len(matched_keywords), self.colors['accent']),
            ("Total Occurrences", total_words, self.colors['success']),
            ("Match Score", f"{score:.1f}" if score > 0 else "N/A", self.colors['warning'])
        ]
        
        for label, value, color in stats:
            stat_container = ctk.CTkFrame(stats_frame, fg_color="transparent")
            stat_container.pack(fill="x", padx=15, pady=2)
            
            # Value
            value_label = ctk.CTkLabel(
                stat_container,
                text=str(value),
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=color,
                anchor="w"
            )
            value_label.pack(anchor="w")
            
            # Label
            label_label = ctk.CTkLabel(
                stat_container,
                text=label,
                font=ctk.CTkFont(size=9),
                text_color=self.colors['text_muted'],
                anchor="w"
            )
            label_label.pack(anchor="w")
    
    def create_tabbed_content(self, parent):
        """Create tabbed content area"""
        # Tab container
        tab_container = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface'],
            corner_radius=12
        )
        tab_container.pack(fill="both", expand=True, pady=(0, 20))
        
        # Tab buttons
        tab_buttons_frame = ctk.CTkFrame(
            tab_container,
            fg_color="transparent",
            height=50
        )
        tab_buttons_frame.pack(fill="x", padx=20, pady=(20, 0))
        tab_buttons_frame.pack_propagate(False)
        
        # Create tab buttons
        self.active_tab = "profile"
        self.tab_buttons = {}
        
        tabs = [
            ("profile", "Profile Information"),
            ("keywords", "Matched Keywords"),
            ("content", "CV Content")
        ]
        
        for tab_id, tab_name in tabs:
            btn = ctk.CTkButton(
                tab_buttons_frame,
                text=tab_name,
                font=ctk.CTkFont(size=12, weight="bold"),
                height=32,
                corner_radius=8,
                command=lambda t=tab_id: self.switch_tab(t)
            )
            btn.pack(side="left", padx=(0, 10))
            self.tab_buttons[tab_id] = btn
        
        # Content area
        self.content_area = ctk.CTkFrame(
            tab_container,
            fg_color="transparent"
        )
        self.content_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Initialize with profile tab
        self.switch_tab("profile")
    
    def switch_tab(self, tab_id):
        """Switch between tabs"""
        # Update button states
        for btn_id, btn in self.tab_buttons.items():
            if btn_id == tab_id:
                btn.configure(
                    fg_color=self.colors['primary'],
                    hover_color=self.colors['accent']
                )
            else:
                btn.configure(
                    fg_color=self.colors['surface_light'],
                    hover_color=self.colors['border']
                )
        
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Show selected tab content
        self.active_tab = tab_id
        if tab_id == "profile":
            self.create_profile_tab()
        elif tab_id == "keywords":
            self.create_keywords_tab()
        elif tab_id == "content":
            self.create_content_tab()
    
    def create_profile_tab(self):
        """Create profile information tab"""
        profile_frame = ctk.CTkScrollableFrame(self.content_area)
        profile_frame.pack(fill="both", expand=True)
        
        profile = self.result.get('profile', {})
        detail = self.result.get('detail', {})
        
        # Personal Information Section
        personal_section = ctk.CTkFrame(
            profile_frame,
            fg_color=self.colors['surface_light'],
            corner_radius=8
        )
        personal_section.pack(fill="x", pady=(0, 15))
        
        self.create_info_section(
            personal_section,
            "Personal Information",
            [
                ("Full Name", f"{profile.get('first_name', 'N/A')} {profile.get('last_name', 'N/A')}"),
                ("Date of Birth", profile.get('date_of_birth', 'N/A')),
                ("Phone Number", profile.get('phone_number', 'N/A')),
                ("Email", profile.get('email', 'N/A')),
                ("Address", profile.get('address', 'N/A'))
            ]
        )
        
        # Application Information Section
        application_section = ctk.CTkFrame(
            profile_frame,
            fg_color=self.colors['surface_light'],
            corner_radius=8
        )
        application_section.pack(fill="x", pady=(0, 15))
        
        self.create_info_section(
            application_section,
            "Application Details",
            [
                ("Applied Role", detail.get('application_role', 'N/A')),
                ("CV File Path", detail.get('cv_path', 'N/A')),
                ("Application Date", detail.get('application_date', 'N/A')),
                ("Status", detail.get('status', 'N/A'))
            ]
        )
    
    def create_keywords_tab(self):
        """Create matched keywords tab"""
        keywords_frame = ctk.CTkScrollableFrame(self.content_area)
        keywords_frame.pack(fill="both", expand=True)
        
        # Get keyword data
        matched_keywords = self.get_matched_keywords()
        exact_matches = self.result.get('exact_matches', {})
        
        if not matched_keywords:
            # No keywords found
            no_keywords_frame = ctk.CTkFrame(
                keywords_frame,
                fg_color=self.colors['surface_light'],
                corner_radius=8
            )
            no_keywords_frame.pack(fill="x", pady=20)
            
            ctk.CTkLabel(
                no_keywords_frame,
                text="No matched keywords found",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['text_muted']
            ).pack(pady=40)
            return
        
        # Keywords overview
        overview_frame = ctk.CTkFrame(
            keywords_frame,
            fg_color=self.colors['surface_light'],
            corner_radius=8
        )
        overview_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            overview_frame,
            text="Keyword Matches Overview",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w", padx=20, pady=(15, 10))
        
        # Keywords list with counts
        for keyword in matched_keywords:
            keyword_frame = ctk.CTkFrame(
                overview_frame,
                fg_color=self.colors['surface'],
                corner_radius=6
            )
            keyword_frame.pack(fill="x", padx=15, pady=2)
            
            # Keyword info
            info_frame = ctk.CTkFrame(keyword_frame, fg_color="transparent")
            info_frame.pack(fill="x", padx=15, pady=10)
            
            # Keyword name
            keyword_label = ctk.CTkLabel(
                info_frame,
                text=keyword,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.colors['text_primary'],
                anchor="w"
            )
            keyword_label.pack(side="left")
            
            # Count badge
            count = exact_matches.get(keyword, 1) if isinstance(exact_matches, dict) else 1
            count_badge = ctk.CTkFrame(
                info_frame,
                fg_color=self.colors['primary'],
                corner_radius=12,
                width=50,
                height=24
            )
            count_badge.pack(side="right")
            count_badge.pack_propagate(False)
            
            ctk.CTkLabel(
                count_badge,
                text=str(count),
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="white"
            ).pack(expand=True)
    
    def create_content_tab(self):
        """Create CV content tab"""
        content_frame = ctk.CTkFrame(
            self.content_area,
            fg_color=self.colors['surface_light'],
            corner_radius=8
        )
        content_frame.pack(fill="both", expand=True)
        
        # Header
        header_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            header_frame,
            text="CV Content",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")
        
        # Word count
        cv_text = self.result.get('cv_text', '')
        word_count = len(cv_text.split()) if cv_text else 0
        
        ctk.CTkLabel(
            header_frame,
            text=f"{word_count} words",
            font=ctk.CTkFont(size=11),
            text_color=self.colors['text_muted']
        ).pack(side="right")
        
        # Content textbox
        cv_textbox = ctk.CTkTextbox(
            content_frame,
            font=ctk.CTkFont(size=11),
            wrap="word",
            corner_radius=8
        )
        cv_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        if cv_text:
            cv_textbox.insert("0.0", cv_text)
        else:
            cv_textbox.insert("0.0", "CV content not available in the system.")
        
        cv_textbox.configure(state="disabled")
    
    def create_info_section(self, parent, title, info_items):
        """Create an information section with key-value pairs"""
        # Section header
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 10))
        
        ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w")
        
        # Info items
        for label, value in info_items:
            item_frame = ctk.CTkFrame(
                parent,
                fg_color="transparent"
            )
            item_frame.pack(fill="x", padx=20, pady=2)
            
            # Label
            label_widget = ctk.CTkLabel(
                item_frame,
                text=f"{label}:",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=self.colors['text_secondary'],
                width=150,
                anchor="w"
            )
            label_widget.pack(side="left")
            
            # Value
            value_widget = ctk.CTkLabel(
                item_frame,
                text=str(value),
                font=ctk.CTkFont(size=11),
                text_color=self.colors['text_primary'],
                anchor="w"
            )
            value_widget.pack(side="left", fill="x", expand=True, padx=(10, 0))
        
        # Add bottom padding
        ctk.CTkFrame(parent, height=10, fg_color="transparent").pack()
    
    def create_footer_section(self, parent):
        """Create footer with action buttons"""
        footer_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            height=60
        )
        footer_frame.pack(fill="x")
        footer_frame.pack_propagate(False)
        
        # Action buttons
        buttons_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        buttons_frame.pack(side="right", pady=15)
        
        # # Export button (placeholder)
        # export_btn = ctk.CTkButton(
        #     buttons_frame,
        #     text="Export Details",
        #     font=ctk.CTkFont(size=12),
        #     height=36,
        #     width=120,
        #     corner_radius=8,
        #     fg_color=self.colors['accent'],
        #     hover_color=self.colors['primary'],
        #     command=self.export_details
        # )
        # export_btn.pack(side="left", padx=(0, 10))
        
        # Close button
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="Close",
            font=ctk.CTkFont(size=12),
            height=36,
            width=100,
            corner_radius=8,
            fg_color=self.colors['surface_light'],
            hover_color=self.colors['border'],
            border_width=1,
            border_color=self.colors['border'],
            command=self.on_closing
        )
        close_btn.pack(side="left")
    
    def get_matched_keywords(self):
        """Get matched keywords from result data"""
        matched_keywords = self.result.get('matched_keywords', [])
        
        if isinstance(matched_keywords, dict):
            # PatternMatcher format
            exact_keywords = matched_keywords.get('exact', [])
            fuzzy_keywords = matched_keywords.get('fuzzy', [])
            return exact_keywords + fuzzy_keywords
        elif isinstance(matched_keywords, list):
            # Simple format
            return matched_keywords
        else:
            return []
    
    def export_details(self):
        """Export CV details (placeholder functionality)"""
        # This could be implemented to export to PDF, JSON, etc.
        from tkinter import messagebox
        messagebox.showinfo(
            "Export", 
            "Export functionality would save CV details to a file.\n"
            "This feature can be implemented based on requirements."
        )
    
    def on_closing(self):
        """Handle window closing"""
        self.grab_release()
        self.destroy()