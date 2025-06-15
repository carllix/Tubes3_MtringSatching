from src.database.Connection import DatabaseManager
from src.database.DAO import ApplicantDAO

def encrypt_all_applicants():
    db = DatabaseManager()
    if not db.connect():
        print("Failed to connect to DB")
        return

    applicant_dao = ApplicantDAO(db)
    connection = db.get_connection()
    cursor = connection.cursor()

    try:
        raw_applicants = applicant_dao.getAllRawApplicants()
        print(f"{len(raw_applicants)} raw applicants fetched.")

        for applicant in raw_applicants:
            encrypted_first_name = applicant_dao.cipher.encrypt(applicant['first_name'])
            encrypted_last_name = applicant_dao.cipher.encrypt(applicant['last_name'])
            encrypted_address = applicant_dao.cipher.encrypt(applicant['address'])
            encrypted_phone = applicant_dao.cipher.encrypt(applicant['phone_number'])

            update_query = """
                UPDATE ApplicantProfile
                SET first_name = %s,
                    last_name = %s,
                    address = %s,
                    phone_number = %s
                WHERE applicant_id = %s
            """
            cursor.execute(update_query, (
                encrypted_first_name,
                encrypted_last_name,
                encrypted_address,
                encrypted_phone,
                applicant['applicant_id']
            ))

        connection.commit()
        print("Encryption & update completed successfully.")

    except Exception as e:
        connection.rollback()
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.disconnect()

if __name__ == "__main__":
    encrypt_all_applicants()
