from datetime import date
from faker import Faker
import random
import os

from src.database.Connection import DatabaseManager
from src.database.DAO import ApplicantDAO, ApplicationDAO
from src.database.Models import ApplicantProfile, ApplicationDetail

class Seeder:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.applicant_dao = ApplicantDAO(db_manager)
        self.application_dao = ApplicationDAO(db_manager)
        self.faker = Faker("en_US")

    def generateIndonesianPhone(self) -> str:
        """Generate realistic Indonesian mobile phone number"""
        prefix = random.choice(["0812", "0813", "0856", "0896", "0821", "0878"])
        suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return prefix + suffix

    def clearTables(self):
        """Delete all data from tables before seeding"""
        connection = self.db_manager.get_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM ApplicationDetail")
        cursor.execute("DELETE FROM ApplicantProfile")
        connection.commit()
        cursor.close()
        print("🧹 Cleared existing data in ApplicantProfile and ApplicationDetail.")

    def seedSampleData(self, count: int = 50):
        """Seed the database with `count` applicants and 1–3 applications each"""
        self.clearTables()

        roles = [
            "Software Engineer", "Data Analyst", "DevOps Engineer", "UI/UX Designer",
            "Backend Developer", "Project Manager", "System Administrator", "QA Tester"
        ]

        # Check if cv_files directory exists, if not create some sample entries anyway
        cv_files_dir = "data/cv_files"
        actual_pdf_files = []
        
        if os.path.exists(cv_files_dir):
            actual_pdf_files = [f for f in os.listdir(cv_files_dir) if f.endswith('.pdf')]
            print(f"Found {len(actual_pdf_files)} PDF files in {cv_files_dir}")
        else:
            print(f"Directory {cv_files_dir} does not exist. Creating sample CV paths anyway.")

        for i in range(count):
            profile = ApplicantProfile(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                date_of_birth=self.faker.date_of_birth(minimum_age=21, maximum_age=40),
                address=self.faker.address().replace('\n', ', '),
                phone_number=self.generateIndonesianPhone()
            )

            applicant_id = self.applicant_dao.insertApplicant(profile)
            print(f"Inserted applicant {profile.first_name} {profile.last_name} (ID: {applicant_id})")

            # 1 to 3 applications per applicant
            num_applications = random.randint(1, 3)
            for j in range(num_applications):
                role = random.choice(roles)
                
                # Use actual PDF files if available, otherwise create sample paths
                if actual_pdf_files:
                    # Use random PDF file from actual files
                    pdf_filename = random.choice(actual_pdf_files)
                    cv_path = f"cv_files/{pdf_filename}"  # Relative path from BASE_DATA_PATH
                else:
                    # Create sample path (for testing without actual files)
                    cv_path = f"cv_files/{profile.last_name.lower()}_{applicant_id}_{j+1}.pdf"
                
                application = ApplicationDetail(
                    applicant_id=applicant_id,
                    application_role=role,
                    cv_path=cv_path
                )
                detail_id = self.application_dao.insertApplication(application)
                print(f"  ↳ Application: {role} (Detail ID: {detail_id}, CV: {cv_path})")

        print("✅ Database seeding completed with 1–3 applications per applicant!")

    def seedWithActualPDFs(self, cv_files_dir: str = "data/cv_files"):
        """Seed database using actual PDF files in the directory"""
        self.clearTables()
        
        if not os.path.exists(cv_files_dir):
            print(f"❌ Directory {cv_files_dir} does not exist!")
            return
            
        pdf_files = [f for f in os.listdir(cv_files_dir) if f.endswith('.pdf')]
        
        if not pdf_files:
            print(f"❌ No PDF files found in {cv_files_dir}")
            return
            
        print(f"📄 Found {len(pdf_files)} PDF files. Creating applicants...")
        
        roles = [
            "Software Engineer", "Data Analyst", "DevOps Engineer", "UI/UX Designer",
            "Backend Developer", "Project Manager", "System Administrator", "QA Tester"
        ]
        
        for pdf_file in pdf_files:
            # Create applicant profile
            profile = ApplicantProfile(
                first_name=self.faker.first_name(),
                last_name=self.faker.last_name(),
                date_of_birth=self.faker.date_of_birth(minimum_age=21, maximum_age=40),
                address=self.faker.address().replace('\n', ', '),
                phone_number=self.generateIndonesianPhone()
            )
            
            applicant_id = self.applicant_dao.insertApplicant(profile)
            print(f"Created applicant {profile.first_name} {profile.last_name} (ID: {applicant_id})")
            
            # Create application with actual PDF file
            application = ApplicationDetail(
                applicant_id=applicant_id,
                application_role=random.choice(roles),
                cv_path=f"cv_files/{pdf_file}"  # Relative path from BASE_DATA_PATH
            )
            
            detail_id = self.application_dao.insertApplication(application)
            print(f"  ↳ Created application (Detail ID: {detail_id}) with CV: {pdf_file}")
        
        print("✅ Database seeded with actual PDF files!")

# Run as script
if __name__ == "__main__":
    db_manager = DatabaseManager()
    if db_manager.connect():
        seeder = Seeder(db_manager)
        
        # Check whether contains actual PDF files
        cv_dir = "data/cv_files"
        if os.path.exists(cv_dir) and any(f.endswith('.pdf') for f in os.listdir(cv_dir)):
            print("Using actual PDF files for seeding...")
            seeder.seedWithActualPDFs(cv_dir)
        else:
            print("No PDF files found. Using sample data...")
            seeder.seedSampleData(count=20)  # Reduced count for testing
            
        db_manager.disconnect()
