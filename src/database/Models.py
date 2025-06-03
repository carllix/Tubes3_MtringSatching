from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class ApplicantProfile:
    # Model untuk table ApplicantProfile
    applicant_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None

@dataclass
class ApplicationDetail:
    # Model untuk table ApplicationDetail
    detail_id: Optional[int] = None
    applicant_id: int = None
    application_role: Optional[str] = None
    cv_path: Optional[str] = None

@dataclass
class SearchResult:
    # Model untuk hasil pencarian
    applicant_profile: ApplicantProfile
    application_detail: ApplicationDetail
    match_count: int
    matched_keywords: list
    similarity_score: float = 0.0