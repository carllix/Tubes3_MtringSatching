from typing import List, Optional
from src.database.Connection import DatabaseManager
from src.database.Models import ApplicantProfile, ApplicationDetail
from src.utils.encryption.FeistelCipherAdv import FeistelCipherAdv
import mysql.connector

class ApplicantDAO:
    def __init__(self, dbManager: DatabaseManager):
        self.dbManager = dbManager
        self.master_key = "MTRING_SATCHING_KEY_CINTA_STIMA"
        self.cipher = FeistelCipherAdv(self.master_key, rounds=8)
        
    def insertApplicant(self, applicant: ApplicantProfile) -> int:
        """Insert new applicant dengan enkripsi data sensitif"""
        connection = self.dbManager.get_connection()
        cursor = connection.cursor()
        
        try:
            # Encrypt sensitive fields dengan Feistel
            encrypted_first_name = self.cipher.encrypt(applicant.first_name)
            encrypted_last_name = self.cipher.encrypt(applicant.last_name)
            encrypted_address = self.cipher.encrypt(applicant.address)
            encrypted_phone_number = self.cipher.encrypt(applicant.phone_number)

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
            
            return applicantId
            
        except Exception as e:
            connection.rollback()
            raise
        finally:
            cursor.close()
        
    def getApplicantById(self, applicantId: int) -> Optional[ApplicantProfile]:
        """Get applicant by ID dengan dekripsi otomatis"""
        connection = self.dbManager.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = "SELECT * FROM ApplicantProfile WHERE applicant_id = %s"
            cursor.execute(query, (applicantId,))
            
            result = cursor.fetchone()
            
            if result:
                
                # Decrypt sensitive fields
                result['first_name'] = self.cipher.decrypt(result['first_name'])
                result['last_name'] = self.cipher.decrypt(result['last_name'])
                result['address'] = self.cipher.decrypt(result['address'])
                result['phone_number'] = self.cipher.decrypt(result['phone_number'])
                
                return ApplicantProfile(**result)
            else:
                return None
                
        except Exception as e:
            raise
        finally:
            cursor.close()
    
    def getAllApplicants(self) -> List[ApplicantProfile]:
        """Get all applicants dengan dekripsi batch"""
        connection = self.dbManager.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = "SELECT * FROM ApplicantProfile"
            cursor.execute(query)
            
            results = cursor.fetchall()
            
            # Decrypt each result
            decrypted_results = []
            sensitive_fields = ['first_name', 'last_name', 'address', 'phone_number']
            
            for result in results:
                # Batch decrypt sensitive fields
                for field in sensitive_fields:
                    if result.get(field):  # Check if field exists and not None
                        result[field] = self.cipher.decrypt(result[field])
                
                decrypted_results.append(ApplicantProfile(**result))
            
            return decrypted_results
            
        except Exception as e:
            raise
        finally:
            cursor.close()


class ApplicationDAO:
    def __init__(self, dbManager: DatabaseManager):
        self.dbManager = dbManager
        # Initialize cipher dengan master key yang sama untuk konsistensi
        self.master_key = "MTRING_SATCHING_KEY_CINTA_STIMA"
        self.cipher = FeistelCipherAdv(self.master_key, rounds=8)
        
    def insertApplication(self, application: ApplicationDetail) -> int:
        """Insert new application and return ID"""
        connection = self.dbManager.get_connection()
        cursor = connection.cursor()
        
        try:
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
            
            return detailId
            
        except Exception as e:
            connection.rollback()
            raise
        finally:
            cursor.close()
        
    def getApplicationsWithProfiles(self) -> List[tuple]:
        """Get applications dengan profiles yang sudah didekripsi"""
        connection = self.dbManager.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT ap.*, ad.*
            FROM ApplicantProfile ap
            JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
            ORDER BY ad.detail_id DESC
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            applications = []
            sensitive_fields = ['first_name', 'last_name', 'address', 'phone_number']
            
            for result in results:
                # Extract profile data
                profileData = {k: v for k, v in result.items() 
                              if k in ['applicant_id', 'first_name', 'last_name', 
                                       'date_of_birth', 'address', 'phone_number']}
                
                # Decrypt profile data
                for field in sensitive_fields:
                    if profileData.get(field):
                        profileData[field] = self.cipher.decrypt(profileData[field])

                # Extract application detail data
                detailData = {k: v for k, v in result.items() 
                             if k in ['detail_id', 'applicant_id', 'application_role', 'cv_path']}
                
                # Create objects
                profile = ApplicantProfile(**profileData)
                detail = ApplicationDetail(**detailData)
                applications.append((profile, detail))

            return applications
            
        except Exception as e:
            raise
        finally:
            cursor.close()
    
    def getApplicationById(self, detailId: int) -> Optional[tuple]:
        """Get specific application dengan profile"""
        connection = self.dbManager.get_connection()
        cursor = connection.cursor(dictionary=True)
        
        try:
            query = """
            SELECT ap.*, ad.*
            FROM ApplicantProfile ap
            JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
            WHERE ad.detail_id = %s
            """
            
            cursor.execute(query, (detailId,))
            result = cursor.fetchone()
            
            if result:
                
                # Extract and decrypt profile data
                profileData = {k: v for k, v in result.items() 
                              if k in ['applicant_id', 'first_name', 'last_name', 
                                       'date_of_birth', 'address', 'phone_number']}
                
                sensitive_fields = ['first_name', 'last_name', 'address', 'phone_number']
                for field in sensitive_fields:
                    if profileData.get(field):
                        profileData[field] = self.cipher.decrypt(profileData[field])

                # Extract application detail data
                detailData = {k: v for k, v in result.items() 
                             if k in ['detail_id', 'applicant_id', 'application_role', 'cv_path']}
                
                profile = ApplicantProfile(**profileData)
                detail = ApplicationDetail(**detailData)
                
                return (profile, detail)
            else:
                return None
                
        except Exception as e:
            raise
        finally:
            cursor.close()