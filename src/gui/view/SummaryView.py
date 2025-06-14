
import customtkinter as ctk
from typing import Dict, Any

class SummaryView(ctk.CTkToplevel):
    """Summary view window for displaying CV details"""
    
    def __init__(self, parent, result: Dict[str, Any]):
        super().__init__(parent)
        
        self.result = result
        self.setup_window()
        self.setup_content()
    
    def setup_window(self):
        """Setup the summary window"""
        self.title("CV Summary")
        self.geometry("900x700")
        self.grab_set()  # Make window modal
        
        # Center the window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"900x700+{x}+{y}")
    
    def setup_content(self):
        """Setup the content of the summary window"""
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        profile = self.result.get('profile', {})
        name = f"{profile.get('first_name', 'Unknown')} {profile.get('last_name', '')}"
        
        title_label = ctk.CTkLabel(
            main_frame,
            text=f"CV Summary - {name}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Create scrollable frame
        scrollable_frame = ctk.CTkScrollableFrame(main_frame)
        scrollable_frame.pack(fill="both", expand=True)
        
        # Profile section
        self.create_profile_section(scrollable_frame)
        
        # CV content section
        self.create_cv_content_section(scrollable_frame)
        
        # Close button
        close_btn = ctk.CTkButton(
            main_frame,
            text="Close",
            width=100,
            command=self.destroy
        )
        close_btn.pack(pady=(20, 0))
    
    def create_profile_section(self, parent):
        """Create the profile information section"""
        profile_frame = ctk.CTkFrame(parent)
        profile_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            profile_frame,
            text="Profile Information",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        profile = self.result.get('profile', {})
        detail = self.result.get('detail', {})
        
        profile_info = f"""Name: {profile.get('first_name', 'N/A')} {profile.get('last_name', 'N/A')}
Date of Birth: {profile.get('date_of_birth', 'N/A')}
Phone: {profile.get('phone_number', 'N/A')}
Address: {profile.get('address', 'N/A')}
Applied Role: {detail.get('application_role', 'N/A')}
CV File: {detail.get('cv_path', 'N/A')}"""
        
        profile_textbox = ctk.CTkTextbox(
            profile_frame,
            height=150,
            font=ctk.CTkFont(size=12)
        )
        profile_textbox.pack(fill="x", padx=15, pady=(0, 15))
        profile_textbox.insert("0.0", profile_info)
        profile_textbox.configure(state="disabled")
    
    def create_match_stats_section(self, parent):
        """Create the match statistics section"""
        stats_frame = ctk.CTkFrame(parent)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            stats_frame,
            text="📊 Match Statistics",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        # Exact matches
        exact_matches = self.result.get('exact_matches', {})
        total_exact = self.result.get('total_exact_matches', 0)
        
        exact_info = f"Total Exact Matches: {total_exact}\\n"
        exact_info += "Breakdown:\\n"
        for keyword, count in exact_matches.items():
            if count > 0:
                exact_info += f"  • {keyword}: {count} occurrences\\n"
        
        if not any(count > 0 for count in exact_matches.values()):
            exact_info += "  No exact matches found\\n"
        
        # Fuzzy matches
        fuzzy_matches = self.result.get('fuzzy_matches', {})
        total_fuzzy = self.result.get('total_fuzzy_matches', 0)
        
        fuzzy_info = f"\\nTotal Fuzzy Matches: {total_fuzzy}\\n"
        fuzzy_info += "Breakdown:\\n"
        for keyword, score in fuzzy_matches.items():
            if score > 0:
                fuzzy_info += f"  • {keyword}: {score:.3f} similarity\\n"
        
        if not any(score > 0 for score in fuzzy_matches.values()):
            fuzzy_info += "  No fuzzy matches found\\n"
        
        stats_textbox = ctk.CTkTextbox(
            stats_frame,
            height=200,
            font=ctk.CTkFont(size=12)
        )
        stats_textbox.pack(fill="x", padx=15, pady=(0, 15))
        stats_textbox.insert("0.0", exact_info + fuzzy_info)
        stats_textbox.configure(state="disabled")
    
    def create_cv_content_section(self, parent):
        """Create the CV content section"""
        cv_frame = ctk.CTkFrame(parent)
        cv_frame.pack(fill="both", expand=True)
        
        ctk.CTkLabel(
            cv_frame,
            text="CV Content",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))
        
        cv_text = self.result.get('cv_text', '')
        
        cv_textbox = ctk.CTkTextbox(
            cv_frame,
            font=ctk.CTkFont(size=11)
        )
        cv_textbox.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        if cv_text:
            cv_textbox.insert("0.0", cv_text)
        else:
            cv_textbox.insert("0.0", "CV content not available")
        
        cv_textbox.configure(state="disabled")