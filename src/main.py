# src/main.py
import sys
import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.gui.App import App
from src.database.Connection import DatabaseManager
# from src.config.AppConfig import AppConfig
from src.database.Models import ApplicantProfile, ApplicationDetail
from src.database.DAO import ApplicantDAO, ApplicationDAO

def main():
    try:
        #  Inisilaisasi database connection
        db_manager = DatabaseManager()
        db_manager.connect()
        
        # # Cara Pakai DAO (Data Access Object)
        # # Create DAO instances
        # applicantDAO = ApplicantDAO(db_manager)
        # applicationDAO = ApplicationDAO(db_manager)

        # # 1. Insert an applicant
        # new_applicant = ApplicantProfile(
        #     first_name="John",
        #     last_name="Doe",
        #     date_of_birth="1995-05-15",
        #     address="123 Main St",
        #     phone_number="08123456789"
        # )
        # applicant_id = applicantDAO.insertApplicant(new_applicant)
        # print(f"Inserted applicant with ID: {applicant_id}")

        #  # 2. Get applicant by ID
        # fetched_applicant = applicantDAO.getApplicantById(applicant_id)
        # print("Fetched Applicant:", fetched_applicant)

        # # 3. Insert application for that applicant
        # new_application = ApplicationDetail(
        #     applicant_id=applicant_id,
        #     application_role="Software Engineer",
        #     cv_path="/path/to/john_doe_cv.pdf"
        # )
        # detail_id = applicationDAO.insertApplication(new_application)
        # print(f"Inserted application with ID: {detail_id}")

        # # 4. Fetch all applications with profiles
        # all_data = applicationDAO.getApplicationsWithProfiles()
        # print("\nAll Applications with Profiles:")
        # for profile, detail in all_data:
        #     print("Applicant:", profile)
        #     print("Application:", detail)
        #     print("-" * 30)


        # Initialize and run GUI
        app = App()
        app.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")
    finally:
        # Cleanup database connection
        if 'db_manager' in locals():
            db_manager.disconnect()

if __name__ == "__main__":
    main()
