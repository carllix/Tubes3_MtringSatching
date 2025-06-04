import re
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ExtractedInfo:
    """Data class for extracted CV information"""
    skills: List[str] = None
    education: List[str] = None
    experience: List[str] = None
    summary: Optional[str] = None

class RegexExtractor:
    """Extract structured information from CV text using regular expressions"""
    
    def __init__(self):
        self.setup_patterns()
    
    def setup_patterns(self):
        """Setup regex patterns for information extraction"""
        
        # Skills patterns (common programming and technical skills)
        self.skills_keywords = [
            # 'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'express',
            # 'django', 'flask', 'spring', 'hibernate', 'mysql', 'postgresql', 'mongodb',
            # 'html', 'css', 'bootstrap', 'tailwind', 'sass', 'less', 'typescript',
            # 'git', 'github', 'gitlab', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
            # 'linux', 'ubuntu', 'centos', 'nginx', 'apache', 'redis', 'elasticsearch',
            # 'machine learning', 'data science', 'tensorflow', 'pytorch', 'pandas', 'numpy',
            # 'sql', 'nosql', 'rest api', 'graphql', 'microservices', 'agile', 'scrum',
            # 'ci/cd', 'jenkins', 'maven', 'gradle', 'webpack', 'babel', 'jest', 'junit',
            # 'php', 'laravel', 'symfony', 'codeigniter', 'wordpress', 'drupal',
            # 'c++', 'c#', '.net', 'asp.net', 'unity', 'xamarin',
            # 'go', 'rust', 'kotlin', 'swift', 'dart', 'flutter',
            # 'photoshop', 'illustrator', 'figma', 'sketch', 'adobe xd',
            # 'tableau', 'power bi', 'excel', 'powerpoint', 'word'
        ]
        
        # Education patterns
        self.education_patterns = [
            re.compile(r'(bachelor|master|phd|diploma|degree).*?(?:in|of)\s+([^\n\.]+)', re.IGNORECASE),
            re.compile(r'(university|institut|college|school).*?([^\n\.]+)', re.IGNORECASE),
            re.compile(r'(S1|S2|S3|D3|D4)\s+([^\n\.]+)', re.IGNORECASE),
            re.compile(r'(sarjana|magister|doktor)\s+([^\n\.]+)', re.IGNORECASE),
        ]
        
        # Experience patterns - improved to capture job titles and companies
        self.experience_patterns = [
            re.compile(r'(software engineer|developer|programmer|analyst|manager|intern|consultant|architect|lead|senior|junior)\s+.*?(?:at|@)\s+([^\n\.]+)', re.IGNORECASE),
            re.compile(r'(\d{4})\s*[-–]\s*(\d{4}|\w+).*?([^\n\.]+)', re.IGNORECASE),
            re.compile(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+(\d{4})\s*[-–]\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|\w+)\s+(\d{4})?.*?([^\n\.]+)', re.IGNORECASE),
            re.compile(r'(work experience|professional experience|employment history).*?([^\n]{50,200})', re.IGNORECASE | re.DOTALL),
        ]
        
        # Summary patterns
        self.summary_patterns = [
            re.compile(r'(summary|profile|objective|about)\s*:?\s*([^\n\.]{50,200})', re.IGNORECASE),
            re.compile(r'^([^\n\.]{100,300})', re.MULTILINE),  # First long paragraph
        ]
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        found_skills = []
        text_lower = text.lower()
        
        for skill in self.skills_keywords:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(found_skills))
    
    def extract_education(self, text: str) -> List[str]:
        """Extract education information from text"""
        education = []
        
        for pattern in self.education_patterns:
            matches = pattern.findall(text)
            for match in matches:
                if isinstance(match, tuple):
                    edu_info = ' '.join(match).strip()
                else:
                    edu_info = match.strip()
                
                if edu_info and len(edu_info) > 5:  # Filter out very short matches
                    education.append(edu_info)
        
        # Remove duplicates while preserving order
        unique_education = []
        for edu in education:
            if edu not in unique_education:
                unique_education.append(edu)
        
        return unique_education[:5]  # Limit to 5 entries
    
    def extract_experience(self, text: str) -> List[str]:
        """Extract work experience from text"""
        experience = []
        
        for pattern in self.experience_patterns:
            matches = pattern.findall(text)
            for match in matches:
                if isinstance(match, tuple):
                    exp_info = ' '.join(str(item) for item in match).strip()
                else:
                    exp_info = match.strip()
                
                if exp_info and len(exp_info) > 10:  # Filter out very short matches
                    experience.append(exp_info)
        
        # Remove duplicates while preserving order
        unique_experience = []
        for exp in experience:
            if exp not in unique_experience:
                unique_experience.append(exp)
        
        return unique_experience[:5]  # Limit to 5 entries
    
    def extract_summary(self, text: str) -> Optional[str]:
        """Extract summary or objective from text"""
        for pattern in self.summary_patterns:
            match = pattern.search(text)
            if match:
                summary = match.group(2) if len(match.groups()) > 1 else match.group(1)
                summary = summary.strip()
                if len(summary) > 20:  # Ensure meaningful summary
                    return summary
        
        return None
    
    def extract_information(self, text: str) -> ExtractedInfo:
        """Extract all information from CV text
        
        Args:
            text: CV text content
            
        Returns:
            ExtractedInfo object containing all extracted information
        """
        if not text:
            return ExtractedInfo()
        
        return ExtractedInfo(
            skills=self.extract_skills(text),
            education=self.extract_education(text),
            experience=self.extract_experience(text),
            summary=self.extract_summary(text)
        )
    
    def format_summary(self, extracted_info: ExtractedInfo, applicant_profile=None) -> str:
        """Format extracted information into a readable summary
        
        Args:
            extracted_info: ExtractedInfo object
            applicant_profile: ApplicantProfile object for personal information
            
        Returns:
            Formatted summary string
        """
        summary_parts = []
        
        # Personal Information from database
        if applicant_profile:
            summary_parts.append("=== PERSONAL INFORMATION ===")
            summary_parts.append(f"Name: {applicant_profile.first_name} {applicant_profile.last_name}")
            if applicant_profile.phone_number:
                summary_parts.append(f"Phone: {applicant_profile.phone_number}")
            if applicant_profile.address:
                summary_parts.append(f"Address: {applicant_profile.address}")
            if applicant_profile.date_of_birth:
                summary_parts.append(f"Date of Birth: {applicant_profile.date_of_birth}")
        
        # Summary/Objective from CV
        if extracted_info.summary:
            summary_parts.append("\n=== PROFESSIONAL SUMMARY ===")
            summary_parts.append(extracted_info.summary)
        
        # Skills from CV
        if extracted_info.skills:
            summary_parts.append("\n=== TECHNICAL SKILLS ===")
            skills_text = ", ".join(extracted_info.skills)
            summary_parts.append(skills_text)
        
        # Education from CV
        if extracted_info.education:
            summary_parts.append("\n=== EDUCATION ===")
            education_text = "\n".join(f"• {edu}" for edu in extracted_info.education)
            summary_parts.append(education_text)
        
        # Experience from CV
        if extracted_info.experience:
            summary_parts.append("\n=== WORK EXPERIENCE ===")
            experience_text = "\n".join(f"• {exp}" for exp in extracted_info.experience)
            summary_parts.append(experience_text)
        
        return "\n\n".join(summary_parts) if summary_parts else "No structured information found."
