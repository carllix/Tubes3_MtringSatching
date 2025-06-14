from typing import List, Optional
from src.database.Connection import DatabaseManager
from src.database.Models import ApplicantProfile, ApplicationDetail
from src.utils.encryption.Encryption import encrypt, decrypt
import mysql.connector

ENCRYPTION_KEY = "kucing" 

class ApplicantDAO:
    def __init__(self, dbManager: DatabaseManager):
        self.dbManager = dbManager
        
    def insertApplicant(self, applicant: ApplicantProfile) -> int:
        connection = self.dbManager.get_connection()
        cursor = connection.cursor()
        
        encrypted_first_name = encrypt(applicant.first_name, ENCRYPTION_KEY)
        encrypted_last_name = encrypt(applicant.last_name, ENCRYPTION_KEY)
        encrypted_address = encrypt(applicant.address, ENCRYPTION_KEY)
        encrypted_phone_number = encrypt(applicant.phone_number, ENCRYPTION_KEY)

        query = """
        INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        values = (
            encrypted_first_name,
            encrypted_last_name,
            applicant.date_of_birth,
            encrypted_address,
            encrypted_phone_number
        )
        
        cursor.execute(query, values)
        connection.commit()
        
        applicantId = cursor.lastrowid
        cursor.close()
        return applicantId
        
    def getApplicantById(self, applicantId: int) -> Optional[ApplicantProfile]:
        connection = self.dbManager.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT * FROM ApplicantProfile WHERE applicant_id = %s"
        cursor.execute(query, (applicantId,))
        
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            result['first_name'] = decrypt(result['first_name'], ENCRYPTION_KEY)
            result['last_name'] = decrypt(result['last_name'], ENCRYPTION_KEY)
            result['address'] = decrypt(result['address'], ENCRYPTION_KEY)
            result['phone_number'] = decrypt(result['phone_number'], ENCRYPTION_KEY)
            return ApplicantProfile(**result)
        return None
    
    # TODO: belum encrypt
    def getAllApplicants(self) -> List[ApplicantProfile]:
        connection = self.dbManager.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT * FROM ApplicantProfile"
        cursor.execute(query)
        
        results = cursor.fetchall()
        cursor.close()
        
        return [ApplicantProfile(**result) for result in results]

class ApplicationDAO:
    def __init__(self, dbManager: DatabaseManager):
        self.dbManager = dbManager
        
    def insertApplication(self, application: ApplicationDetail) -> int:
        """Insert new application and return ID"""
        connection = self.dbManager.get_connection()
        cursor = connection.cursor()
        
        query = """
        INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
        VALUES (%s, %s, %s)
        """
        
        values = (
            application.applicant_id,
            application.application_role,
            application.cv_path
        )
        
        cursor.execute(query, values)
        connection.commit()
        
        detailId = cursor.lastrowid
        cursor.close()
        return detailId
        
    def getApplicationsWithProfiles(self) -> List[tuple]:
        connection = self.dbManager.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        query = """
        SELECT ap.*, ad.*
        FROM ApplicantProfile ap
        JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        applications = []
        for result in results:
            profileData = {k: v for k, v in result.items() 
                          if k in ['applicant_id', 'first_name', 'last_name', 
                                   'date_of_birth', 'address', 'phone_number']}
            
            profileData['first_name'] = decrypt(profileData['first_name'], ENCRYPTION_KEY)
            profileData['last_name'] = decrypt(profileData['last_name'], ENCRYPTION_KEY)
            profileData['address'] = decrypt(profileData['address'], ENCRYPTION_KEY)
            profileData['phone_number'] = decrypt(profileData['phone_number'], ENCRYPTION_KEY)

            detailData = {k: v for k, v in result.items() 
                         if k in ['detail_id', 'applicant_id', 'application_role', 'cv_path']}
            
            profile = ApplicantProfile(**profileData)
            detail = ApplicationDetail(**detailData)
            applications.append((profile, detail))
            
        return applications
