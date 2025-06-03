from datetime import date
from faker import Faker
import random

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

        for _ in range(count):
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
            for i in range(num_applications):
                role = random.choice(roles)
                cv_path = f"data/cv_files/{profile.last_name.lower()}_{applicant_id}_{i+1}.pdf"
                application = ApplicationDetail(
                    applicant_id=applicant_id,
                    application_role=role,
                    cv_path=cv_path
                )
                detail_id = self.application_dao.insertApplication(application)
                print(f"  ↳ Application: {role} (Detail ID: {detail_id})")

        print("✅ Database seeding completed with 1–3 applications per applicant!")

# Run as script
if __name__ == "__main__":
    db_manager = DatabaseManager()
    if db_manager.connect():
        seeder = Seeder(db_manager)
        seeder.seedSampleData(count=50)
        db_manager.disconnect()
