from typing import List, Optional
from src.database.Connection import DatabaseManager
from src.database.Models import ApplicantProfile, ApplicationDetail
import mysql.connector

class ApplicantDAO:
    def __init__(self, dbManager: DatabaseManager):
        self.dbManager = dbManager
        
    def insertApplicant(self, applicant: ApplicantProfile) -> int:
        connection = self.dbManager.get_connection()
        cursor = connection.cursor()
        
        query = """
        INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        values = (
            applicant.first_name,
            applicant.last_name,
            applicant.date_of_birth,
            applicant.address,
            applicant.phone_number
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
            return ApplicantProfile(**result)
        return None
        
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
            detailData = {k: v for k, v in result.items() 
                         if k in ['detail_id', 'applicant_id', 'application_role', 'cv_path']}
            
            profile = ApplicantProfile(**profileData)
            detail = ApplicationDetail(**detailData)
            applications.append((profile, detail))
            
        return applications
