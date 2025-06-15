
import customtkinter as ctk
import re
from typing import Dict, Any, List, Tuple

class SummaryView(ctk.CTkToplevel):
    """Summary view window for displaying CV details"""
    
    def __init__(self, parent, result: Dict[str, Any]):
        super().__init__(parent)
        
        # Professional color scheme matching main app and components
        self.colors = {
            'primary': '#1f538d',
            'secondary': '#14375e',
            'accent': '#36719e',
            'surface': '#212121',
            'background': '#1a1a1a',
            'surface_variant': '#2b2b2b',      # Matching CVCard's card_bg
            'surface_light': '#404040',        # For borders and lighter surfaces
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'text_muted': '#808080',
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336',
            'fuzzy': '#9c27b0',
            'border': '#404040',
            'hover': '#3a3a3a',
            'skill_bg': '#1f538d',            # Using primary color for skill bubbles
            'skill_hover': '#36719e'          # Using accent color for hover
        }
        
        self.result = result
        self.parsed_cv_data = self.parse_cv_text(result.get('cv_text', ''))
        self.setup_theme()
        self.setup_window()
        self.setup_content()
    
    def setup_theme(self):
        """Configure the professional dark theme matching main app"""
        # Set the global appearance mode
        ctk.set_appearance_mode("dark")
        
        # Configure window background to match main app
        self.configure(fg_color=self.colors['background'])
    
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
        """Setup the content of the summary window with professional styling"""
        # Main container with professional styling matching main app
        main_frame = ctk.CTkFrame(
            self,
            fg_color=self.colors['surface'],
            corner_radius=0
        )
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Header section with gradient-like effect matching main app
        header_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors['primary'],
            corner_radius=0,
            height=100  # Increased height to prevent name truncation
        )
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Title with professional styling
        profile = self.result.get('profile', {})
        first_name = profile.get('first_name', 'Unknown').strip()
        last_name = profile.get('last_name', '').strip()
        name = f"{first_name} {last_name}".strip() if last_name else first_name
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"CV Summary",
            font=ctk.CTkFont(size=26, weight="bold"),  # Slightly smaller to fit better
            text_color=self.colors['text_primary']
        )
        title_label.pack(pady=(15, 5))  # Adjusted padding
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text=name,
            font=ctk.CTkFont(size=16),
            text_color=self.colors['text_primary'],
            wraplength=0  # Disable text wrapping to prevent truncation
        )
        subtitle_label.pack(pady=(0, 15))  # More bottom padding
        
        # Content area with padding matching main app layout
        content_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors['surface'],
            corner_radius=0
        )
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create scrollable frame with professional styling matching main app
        scrollable_frame = ctk.CTkScrollableFrame(
            content_frame,
            fg_color=self.colors['background'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['border'],
            scrollbar_button_color="gray40",
            scrollbar_button_hover_color="gray50"
        )
        scrollable_frame.pack(fill="both", expand=True)
        
        # Profile section
        self.create_profile_section(scrollable_frame)
        
        # Skills section with bubble design
        self.create_skills_section(scrollable_frame)
        
        # Job History section with numbered entries
        self.create_job_history_section(scrollable_frame)
        
        # Education section with numbered entries
        self.create_education_section(scrollable_frame)
        
        # Accomplishments section (if present)
        accomplishments = self.parsed_cv_data.get("accomplishments", [])
        if accomplishments and accomplishments[0] != "No accomplishments information found":
            self.create_accomplishments_section(scrollable_frame)
        
        # Action buttons frame matching main app styling
        button_frame = ctk.CTkFrame(
            main_frame,
            fg_color=self.colors['surface'],
            corner_radius=0
        )
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Close button with hover effect matching main app styling
        close_btn = ctk.CTkButton(
            button_frame,
            text="Close",
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['accent'],
            text_color=self.colors['text_primary'],
            corner_radius=8,
            command=self.destroy
        )
        close_btn.pack(pady=15)
    
    def create_profile_section(self, parent):
        """Create the profile information section with professional styling"""
        profile_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_variant'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['border']
        )
        profile_frame.pack(fill="x", pady=(15, 20), padx=15)
        
        # Section header
        header_frame = ctk.CTkFrame(
            profile_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(
            header_frame,
            text="Profile Information",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w")
        
        # Profile content in grid-like layout
        content_frame = ctk.CTkFrame(
            profile_frame,
            fg_color="transparent"
        )
        content_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        profile = self.result.get('profile', {})
        detail = self.result.get('detail', {})
        
        # Create professional info cards with proper name handling
        first_name = profile.get('first_name', 'N/A').strip()
        last_name = profile.get('last_name', '').strip()
        full_name = f"{first_name} {last_name}".strip() if last_name and last_name != 'N/A' else first_name
        
        info_items = [
            ("Name", full_name),
            ("Date of Birth", profile.get('date_of_birth', 'N/A')),
            ("Phone", profile.get('phone_number', 'N/A')),
            ("Address", profile.get('address', 'N/A')),
            ("Applied Role", detail.get('application_role', 'Position not specified')),
            ("CV File", detail.get('cv_path', 'N/A').split('/')[-1] if detail.get('cv_path') else 'N/A')
        ]
        
        for i, (label, value) in enumerate(info_items):
            row = i // 2
            col = i % 2
            
            info_frame = ctk.CTkFrame(
                content_frame,
                fg_color=self.colors['surface'],
                corner_radius=8,
                border_width=1,
                border_color=self.colors['border']
            )
            info_frame.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            ctk.CTkLabel(
                info_frame,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=self.colors['primary']
            ).pack(anchor="w", padx=15, pady=(10, 2))
            
            ctk.CTkLabel(
                info_frame,
                text=value,
                font=ctk.CTkFont(size=12),
                text_color=self.colors['text_secondary'],
                wraplength=200
            ).pack(anchor="w", padx=15, pady=(0, 10))
        
        # Configure grid weights
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
    
    def parse_cv_text(self, cv_text: str) -> Dict[str, List[str]]:
        """Parse CV text to extract structured information using regex"""
        if not cv_text:
            return {"job_history": [], "education": [], "skills": [], "accomplishments": []}
        
        # Minimal cleaning to preserve structure
        # Remove excessive whitespace but keep line breaks
        text = re.sub(r'[ \t]+', ' ', cv_text)
        # Normalize line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = text.strip()
        
        parsed_data = {
            "job_history": self.extract_job_history(text),
            "education": self.extract_education(text),
            "skills": self.extract_skills(text),
            "accomplishments": self.extract_accomplishments(text)
        }
        
        return parsed_data
    
    def extract_accomplishments(self, text: str) -> List[str]:
        """Extract accomplishments information by finding text between section headers"""
        # Patterns for accomplishments sections - only look for main sections
        accomplishments_patterns = [
            r'(?i)\n\s*(?:Accomplishments|Accomplishment|Achievements|Achievement)\s*\n(.*?)(?=(?:\n\s*(?:Work\s+History|Education|Experience|Skills)\s*\n|$))',
            r'(?i)\n\s*(?:Awards|Award|Honors|Honor|Recognition)\s*\n(.*?)(?=(?:\n\s*(?:Work\s+History|Education|Experience|Skills)\s*\n|$))',
            r'(?i)\n\s*(?:Certifications|Certification|Certificates|Certificate)\s*\n(.*?)(?=(?:\n\s*(?:Work\s+History|Education|Experience|Skills)\s*\n|$))',
        ]
        
        for pattern in accomplishments_patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                accomplishments_text = match.group(1).strip()
                
                if accomplishments_text:
                    # Clean up the text and preserve formatting
                    cleaned_text = re.sub(r'\n{3,}', '\n\n', accomplishments_text)
                    cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)
                    return [cleaned_text.strip()]
        
        return ["No accomplishments information found"]
    
    def extract_job_history(self, text: str) -> List[str]:
        """Extract job history/experience information by finding text between section headers"""
        # Patterns for work experience sections - only look for main sections
        work_history_patterns = [
            r'(?i)\n\s*(?:Work\s+History|Work\s+Experience|Work\s+Experiences)\s*\n(.*?)(?=(?:\n\s*(?:Education|Skills|Accomplishments|Accomplishment)\s*\n|$))',
            r'(?i)\n\s*(?:Experience|Experiences|Professional\s+Experience|Professional\s+Experiences)\s*\n(.*?)(?=(?:\n\s*(?:Education|Skills|Accomplishments|Accomplishment)\s*\n|$))',
            r'(?i)\n\s*(?:Employment\s+History|Career\s+History|Career\s+Experience)\s*\n(.*?)(?=(?:\n\s*(?:Education|Skills|Accomplishments|Accomplishment)\s*\n|$))',
            r'(?i)\n\s*(?:Job\s+History|Professional\s+Background|Career\s+Summary)\s*\n(.*?)(?=(?:\n\s*(?:Education|Skills|Accomplishments|Accomplishment)\s*\n|$))',
        ]
        
        for pattern in work_history_patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                work_history_text = match.group(1).strip()
                
                if work_history_text:
                    # Clean up the text and preserve formatting
                    cleaned_text = re.sub(r'\n{3,}', '\n\n', work_history_text)
                    cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)
                    return [cleaned_text.strip()]
        
        return ["No work history information found"]
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education information by finding text between section headers"""
        # Patterns for education sections - only look for main sections
        education_patterns = [
            r'(?i)\n\s*(?:Education|Educational\s+Background|Academic\s+Background)\s*\n(.*?)(?=(?:\n\s*(?:Work\s+History|Skills|Experience|Accomplishments|Accomplishment)\s*\n|$))',
            r'(?i)\n\s*(?:Past\s+Education|Past\s+Educations|Academic\s+Qualification|Academic\s+Qualifications)\s*\n(.*?)(?=(?:\n\s*(?:Work\s+History|Skills|Experience|Accomplishments|Accomplishment)\s*\n|$))',
            r'(?i)\n\s*(?:Learning|Studies|Academic\s+History|Educational\s+History)\s*\n(.*?)(?=(?:\n\s*(?:Work\s+History|Skills|Experience|Accomplishments|Accomplishment)\s*\n|$))',
        ]
        
        for pattern in education_patterns:
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                education_text = match.group(1).strip()
                
                if education_text:
                    # Clean up the text and preserve formatting
                    cleaned_text = re.sub(r'\n{3,}', '\n\n', education_text)
                    cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)
                    return [cleaned_text.strip()]
        
        return ["No education information found"]
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills information by finding text between section headers"""
        # Patterns for skills sections - only look for main sections
        skills_patterns = [
            r'(?i)\n\s*(?:Skills|Skill)\s*\n(.*?)(?=(?:\n\s*(?:Work\s+History|Education|Experience|Accomplishments|Accomplishment)\s*\n|$))',
            r'(?i)\n\s*(?:Hard\s+Skills|Soft\s+Skills|Technical\s+Skills|Core\s+Competencies)\s*\n(.*?)(?=(?:\n\s*(?:Work\s+History|Education|Experience|Accomplishments|Accomplishment)\s*\n|$))',
            r'(?i)\n\s*(?:Key\s+Skills|Competencies|Abilities|Proficiencies|Expertise)\s*\n(.*?)(?=(?:\n\s*(?:Work\s+History|Education|Experience|Accomplishments|Accomplishment)\s*\n|$))',
            r'(?i)\n\s*(?:Tools|Software|Technologies|Programming\s+Languages)\s*\n(.*?)(?=(?:\n\s*(?:Work\s+History|Education|Experience|Accomplishments|Accomplishment)\s*\n|$))',
        ]
        
        all_skills = []
        
        # Try to find all skills sections (might have multiple like "Hard Skills" and "Soft Skills")
        for pattern in skills_patterns:
            matches = re.finditer(pattern, text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                skills_text = match.group(1).strip()
                
                if skills_text:
                    # Clean up the text and preserve formatting
                    cleaned_text = re.sub(r'\n{3,}', '\n\n', skills_text)
                    cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)
                    
                    # Parse individual skills from the text
                    skills_list = []
                    
                    # Split by newlines first (each line is likely a skill or group of skills)
                    lines = cleaned_text.split('\n')
                    
                    for line in lines:
                        line = line.strip()
                        if line and len(line) > 1:
                            # If the line contains commas, split by commas
                            if ',' in line:
                                parts = line.split(',')
                                for part in parts:
                                    part = part.strip()
                                    if part and len(part) > 1:
                                        skills_list.append(part)
                            else:
                                # Otherwise, treat the whole line as a skill
                                skills_list.append(line)
                    
                    # Add found skills to the overall list
                    all_skills.extend(skills_list)
        
        # Remove duplicates while preserving order and filter out invalid skills
        seen = set()
        unique_skills = []
        for skill in all_skills:
            skill_cleaned = skill.strip()
            # Remove "and" if it's at the beginning of the skill (case insensitive)
            if skill_cleaned.lower().startswith('and '):
                skill_cleaned = skill_cleaned[4:].strip()
            
            skill_lower = skill_cleaned.lower().strip()
            # Filter out empty skills, very short skills, and skills that are just "and"
            if skill_lower and skill_lower not in seen and len(skill_lower) > 1 and skill_lower != 'and':
                seen.add(skill_lower)
                unique_skills.append(skill_cleaned)
        
        if unique_skills:
            return unique_skills
        
        # Fallback: If no skills section found, try to find common skill-related terms throughout the document
        common_skills = []
        skill_keywords = [
            'Microsoft Office', 'Excel', 'PowerPoint', 'Word', 'Outlook', 'Microsoft Project',
            'Project Management', 'Leadership', 'Communication', 'Analysis', 'Six Sigma',
            'Problem Solving', 'Time Management', 'Team Management', 'SolidWorks', 'Solid Works',
            'Quality Assurance', 'Training', 'Documentation', 'Product Development',
            'Cost Analysis', 'Critical Thinking', 'Research', 'Visio', 'Personnel Management',
            'Quality', 'Six Sigma Green Belt', 'Prioritization', 'Critical thinking skills',
            'Analyst', 'Agency', 'Consulting', 'Designing', 'Dialysis', 'Direction',
            'Develop drug', 'Functional', 'IIa', 'ISO', 'Market and development',
            'Design process', 'Product management', 'Researching', 'Sales', 'Validation'
        ]
        
        for skill in skill_keywords:
            if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE):
                common_skills.append(skill)
        
        return common_skills if common_skills else ["No skills information found"]
    
    def create_job_history_section(self, parent):
        """Create the job history section with numbered entries"""
        job_history = self.parsed_cv_data.get("job_history", [])
        
        job_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_variant'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['border']
        )
        job_frame.pack(fill="x", pady=(0, 20), padx=15)
        
        # Section header
        header_frame = ctk.CTkFrame(
            job_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(
            header_frame,
            text="Work Experience",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w")
        
        # Job content
        content_frame = ctk.CTkFrame(
            job_frame,
            fg_color="transparent"
        )
        content_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        if job_history and job_history[0] != "No work history information found":
            # Split job history into potential entries
            job_entries = self.parse_job_entries(job_history[0])
            
            if len(job_entries) > 1:
                # Multiple job entries found
                for i, entry in enumerate(job_entries, 1):
                    self.create_job_entry(content_frame, f"Position {i}", entry, i)
            else:
                # Single job entry or unstructured text
                job_textbox = ctk.CTkTextbox(
                    content_frame,
                    height=200,
                    font=ctk.CTkFont(size=12),
                    fg_color=self.colors['surface'],
                    border_width=1,
                    border_color=self.colors['border'],
                    text_color=self.colors['text_secondary']
                )
                job_textbox.pack(fill="x")
                job_textbox.insert("0.0", job_history[0])
                job_textbox.configure(state="disabled")
        else:
            # No job history message
            no_job_label = ctk.CTkLabel(
                content_frame,
                text="No work history information found",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['text_muted']
            )
            no_job_label.pack(pady=20)
    
    def parse_job_entries(self, job_text):
        """Parse job history text into separate job entries"""
        # Try to split by common patterns that indicate new job entries
        patterns = [
            r'\n(?=\w+\s+\d{4})',  # Year patterns
            r'\n(?=[A-Z][a-z]+\s+\d{4})',  # Month Year patterns
            r'\n(?=\d{1,2}/\d{4})',  # Date patterns
            r'\n(?=Job\s+\d+)',  # Explicit job numbering
            r'\n(?=Position\s+\d+)',  # Position numbering
        ]
        
        for pattern in patterns:
            entries = re.split(pattern, job_text)
            if len(entries) > 1:
                return [entry.strip() for entry in entries if entry.strip()]
        
        # If no clear separation found, return as single entry
        return [job_text.strip()]
    
    def create_job_entry(self, parent, title, content, index):
        """Create a single job entry with professional styling"""
        entry_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['border']
        )
        entry_frame.pack(fill="x", pady=5)
        
        # Entry header
        header_label = ctk.CTkLabel(
            entry_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['primary']
        )
        header_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Entry content
        content_textbox = ctk.CTkTextbox(
            entry_frame,
            height=120,
            font=ctk.CTkFont(size=11),
            fg_color=self.colors['background'],
            border_width=0,
            text_color=self.colors['text_secondary']
        )
        content_textbox.pack(fill="x", padx=15, pady=(0, 15))
        content_textbox.insert("0.0", content)
        content_textbox.configure(state="disabled")
    
    def create_education_section(self, parent):
        """Create the education section with numbered entries"""
        education = self.parsed_cv_data.get("education", [])
        
        edu_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_variant'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['border']
        )
        edu_frame.pack(fill="x", pady=(0, 20), padx=15)
        
        # Section header
        header_frame = ctk.CTkFrame(
            edu_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(
            header_frame,
            text="Education",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w")
        
        # Education content
        content_frame = ctk.CTkFrame(
            edu_frame,
            fg_color="transparent"
        )
        content_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        if education and education[0] != "No education information found":
            # Split education into potential entries
            edu_entries = self.parse_education_entries(education[0])
            
            if len(edu_entries) > 1:
                # Multiple education entries found
                for i, entry in enumerate(edu_entries, 1):
                    self.create_education_entry(content_frame, f"Education {i}", entry, i)
            else:
                # Single education entry or unstructured text
                edu_textbox = ctk.CTkTextbox(
                    content_frame,
                    height=150,
                    font=ctk.CTkFont(size=12),
                    fg_color=self.colors['surface'],
                    border_width=1,
                    border_color=self.colors['border'],
                    text_color=self.colors['text_secondary']
                )
                edu_textbox.pack(fill="x")
                edu_textbox.insert("0.0", education[0])
                edu_textbox.configure(state="disabled")
        else:
            # No education message
            no_edu_label = ctk.CTkLabel(
                content_frame,
                text="No education information found",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['text_muted']
            )
            no_edu_label.pack(pady=20)
    
    def parse_education_entries(self, edu_text):
        """Parse education text into separate education entries"""
        # Try to split by common patterns that indicate new education entries
        patterns = [
            r'\n(?=\w+\s+\d{4})',  # Year patterns
            r'\n(?=[A-Z][a-z]+\s+\d{4})',  # Month Year patterns
            r'\n(?=\d{1,2}/\d{4})',  # Date patterns
            r'\n(?=Bachelor|Master|PhD|Diploma|Certificate)',  # Degree types
            r'\n(?=University|College|Institute|School)',  # Institution types
        ]
        
        for pattern in patterns:
            entries = re.split(pattern, edu_text)
            if len(entries) > 1:
                return [entry.strip() for entry in entries if entry.strip()]
        
        # If no clear separation found, return as single entry
        return [edu_text.strip()]
    
    def create_education_entry(self, parent, title, content, index):
        """Create a single education entry with professional styling"""
        entry_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['border']
        )
        entry_frame.pack(fill="x", pady=5)
        
        # Entry header
        header_label = ctk.CTkLabel(
            entry_frame,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors['primary']
        )
        header_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # Entry content
        content_textbox = ctk.CTkTextbox(
            entry_frame,
            height=100,
            font=ctk.CTkFont(size=11),
            fg_color=self.colors['background'],
            border_width=0,
            text_color=self.colors['text_secondary']
        )
        content_textbox.pack(fill="x", padx=15, pady=(0, 15))
        content_textbox.insert("0.0", content)
        content_textbox.configure(state="disabled")
    
    def create_skills_section(self, parent):
        """Create the skills section with interactive bubbles"""
        skills = self.parsed_cv_data.get("skills", [])
        
        skills_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_variant'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['border']
        )
        skills_frame.pack(fill="x", pady=(0, 20), padx=15)
        
        # Section header
        header_frame = ctk.CTkFrame(
            skills_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(
            header_frame,
            text="Skills & Competencies",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w")
        
        # Skills container with horizontal scrollable content
        skills_container = ctk.CTkFrame(
            skills_frame,
            fg_color="transparent"
        )
        skills_container.pack(fill="x", padx=20, pady=(0, 20))
        
        if skills and skills[0] != "No skills information found":
            # Create horizontally scrollable skill bubbles
            self.create_skill_bubbles(skills_container, skills)
        else:
            # No skills message
            no_skills_label = ctk.CTkLabel(
                skills_container,
                text="No skills information found",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['text_muted']
            )
            no_skills_label.pack(pady=20)
    
    def create_skill_bubbles(self, parent, skills):
        """Create horizontally scrollable skill bubbles with smaller font in 2 rows"""
        # Create a frame with canvas for horizontal scrolling
        canvas_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface'],
            corner_radius=8,
            border_width=1,
            border_color=self.colors['border'],
            height=120  # Increased height to accommodate 2 rows + scrollbar
        )
        canvas_frame.pack(fill="x", pady=5)
        canvas_frame.pack_propagate(False)
        
        # Create a canvas for scrolling
        canvas = ctk.CTkCanvas(
            canvas_frame,
            bg=self.colors['surface'],
            highlightthickness=0,
            height=90  # Increased height for 2 rows
        )
        canvas.pack(side="top", fill="x", expand=False, padx=5, pady=(5, 0))
        
        # Create horizontal scrollbar below the canvas
        scrollbar = ctk.CTkScrollbar(
            canvas_frame,
            orientation="horizontal",
            command=canvas.xview
        )
        scrollbar.pack(side="bottom", fill="x", padx=5, pady=(2, 5))
        canvas.configure(xscrollcommand=scrollbar.set)
        
        # Create a frame inside the canvas to hold all skill bubbles
        bubbles_frame = ctk.CTkFrame(canvas, fg_color="transparent")
        canvas_window = canvas.create_window(0, 0, anchor="nw", window=bubbles_frame)
        
        # Create skill bubbles in 2 rows
        row1_frame = ctk.CTkFrame(bubbles_frame, fg_color="transparent")
        row1_frame.pack(fill="x", pady=(5, 2))
        
        row2_frame = ctk.CTkFrame(bubbles_frame, fg_color="transparent")
        row2_frame.pack(fill="x", pady=(2, 5))
        
        # Distribute skills between 2 rows
        for i, skill in enumerate(skills):  # Show all skills, no limit
            skill_text = skill.strip()
            if not skill_text:
                continue
            
            # Determine which row to use (alternate between rows)
            target_frame = row1_frame if i % 2 == 0 else row2_frame
            
            # Create skill bubble with smaller font
            skill_button = ctk.CTkButton(
                target_frame,
                text=skill_text,
                font=ctk.CTkFont(size=10, weight="bold"),  # Small font size
                fg_color=self.colors['skill_bg'],
                hover_color=self.colors['skill_hover'],
                text_color=self.colors['text_primary'],
                corner_radius=16,  # Smaller corner radius
                height=28,  # Smaller height
                command=lambda s=skill_text: self.on_skill_click(s)
            )
            skill_button.pack(side="left", padx=3, pady=2)  # Horizontal layout with small padding
        
        # Update scroll region when frame changes size
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Make the canvas window height match the canvas height
            canvas.itemconfig(canvas_window, height=canvas.winfo_height())
        
        bubbles_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)
        
        # Bind mouse wheel to horizontal scrolling
        def on_mousewheel(event):
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind("<MouseWheel>", on_mousewheel)  # Windows
        canvas.bind("<Button-4>", lambda e: canvas.xview_scroll(-1, "units"))  # Linux
        canvas.bind("<Button-5>", lambda e: canvas.xview_scroll(1, "units"))   # Linux
        
        # Update the scroll region after all widgets are packed
        canvas_frame.after(100, configure_scroll_region)
    
    def create_accomplishments_section(self, parent):
        """Create the accomplishments section with professional bullet points"""
        accomplishments = self.parsed_cv_data.get("accomplishments", [])
        
        acc_frame = ctk.CTkFrame(
            parent,
            fg_color=self.colors['surface_variant'],
            corner_radius=12,
            border_width=1,
            border_color=self.colors['border']
        )
        acc_frame.pack(fill="x", pady=(0, 20), padx=15)
        
        # Section header
        header_frame = ctk.CTkFrame(
            acc_frame,
            fg_color="transparent"
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 15))
        
        ctk.CTkLabel(
            header_frame,
            text="Accomplishments & Certifications",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w")
        
        # Accomplishments content
        content_frame = ctk.CTkFrame(
            acc_frame,
            fg_color="transparent"
        )
        content_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        if accomplishments and accomplishments[0] != "No accomplishments information found":
            # Format accomplishments as professional bullet points
            formatted_content = self.format_accomplishments(accomplishments[0])
            
            acc_textbox = ctk.CTkTextbox(
                content_frame,
                height=150,
                font=ctk.CTkFont(size=12),
                fg_color=self.colors['surface'],
                border_width=1,
                border_color=self.colors['border'],
                text_color=self.colors['text_secondary']
            )
            acc_textbox.pack(fill="x")
            acc_textbox.insert("0.0", formatted_content)
            acc_textbox.configure(state="disabled")
        else:
            # No accomplishments message
            no_acc_label = ctk.CTkLabel(
                content_frame,
                text="No accomplishments information found",
                font=ctk.CTkFont(size=14),
                text_color=self.colors['text_muted']
            )
            no_acc_label.pack(pady=20)
    
    def format_accomplishments(self, acc_text):
        """Format accomplishments text as professional bullet points"""
        lines = acc_text.split('\n')
        formatted_lines = []
        
        for line in lines:
            line = line.strip()
            if line and len(line) > 3:
                # Add bullet point if not already present
                if not line.startswith('•') and not line.startswith('-') and not line.startswith('*'):
                    line = f"• {line}"
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)