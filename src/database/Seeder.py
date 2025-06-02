# src/database/seeder.py
from datetime import date
from database.connection import DatabaseManager
from database.dao import ApplicantDAO, ApplicationDAO
from database.models import ApplicantProfile, ApplicationDetail

class DatabaseSeeder:
    """Seed database with sample data"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.applicant_dao = ApplicantDAO(db_manager)
        self.application_dao = ApplicationDAO(db_manager)
        
    def seed_sample_data(self):
        """Seed database with sample applicant and application data"""
        sample_applicants = [
            ApplicantProfile(
                first_name="Farhan",
                last_name="Developer",
                date_of_birth=date(1995, 1, 15),
                address="Jl. Ganesha No. 10, Bandung",
                phone_number="0812-3456-7890"
            ),
            ApplicantProfile(
                first_name="Aland",
                last_name="Designer",
                date_of_birth=date(1996, 3, 22),
                address="Jl. Dipatiukur No. 35, Bandung",
                phone_number="0813-4567-8901"
            ),
            ApplicantProfile(
                first_name="Ariel",
                last_name="DataScientist",
                date_of_birth=date(1994, 7, 8),
                address="Jl. Sumbersari No. 21, Bandung",
                phone_number="0814-5678-9012"
            )
        ]
        
        # Insert applicants and get their IDs
        applicant_ids = []
        for applicant in sample_applicants:
            applicant_id = self.applicant_dao.insert_applicant(applicant)
            applicant_ids.append(applicant_id)
            print(f"Inserted applicant: {applicant.first_name} {applicant.last_name} (ID: {applicant_id})")
        
        # Create sample applications
        sample_applications = [
            ApplicationDetail(
                applicant_id=applicant_ids[0],
                application_role="Full Stack Developer",
                cv_path="data/cv_files/Developer/farhan_cv.pdf"
            ),
            ApplicationDetail(
                applicant_id=applicant_ids[1],
                application_role="UI/UX Designer",
                cv_path="data/cv_files/Designer/aland_cv.pdf"
            ),
            ApplicationDetail(
                applicant_id=applicant_ids[2],
                application_role="Data Scientist",
                cv_path="data/cv_files/DataScientist/ariel_cv.pdf"
            )
        ]
        
        # Insert applications
        for application in sample_applications:
            detail_id = self.application_dao.insert_application(application)
            print(f"Inserted application: {application.application_role} (ID: {detail_id})")
            
        print("Database seeding completed!")