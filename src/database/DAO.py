# from typing import List, Optional
# from database.connection import DatabaseManager
# from database.models import ApplicantProfile, ApplicationDetail
# import mysql.connector

# class ApplicantDAO:
#     """Data Access Object for Applicant operations"""
    
#     def __init__(self, db_manager: DatabaseManager):
#         self.db_manager = db_manager
        
#     def insert_applicant(self, applicant: ApplicantProfile) -> int:
#         """Insert new applicant and return ID"""
#         connection = self.db_manager.get_connection()
#         cursor = connection.cursor()
        
#         query = """
#         INSERT INTO ApplicantProfile (first_name, last_name, date_of_birth, address, phone_number)
#         VALUES (%s, %s, %s, %s, %s)
#         """
        
#         values = (
#             applicant.first_name,
#             applicant.last_name,
#             applicant.date_of_birth,
#             applicant.address,
#             applicant.phone_number
#         )
        
#         cursor.execute(query, values)
#         connection.commit()
        
#         applicant_id = cursor.lastrowid
#         cursor.close()
#         return applicant_id
        
#     def get_applicant_by_id(self, applicant_id: int) -> Optional[ApplicantProfile]:
#         """Get applicant by ID"""
#         connection = self.db_manager.get_connection()
#         cursor = connection.cursor(dictionary=True)
        
#         query = "SELECT * FROM ApplicantProfile WHERE applicant_id = %s"
#         cursor.execute(query, (applicant_id,))
        
#         result = cursor.fetchone()
#         cursor.close()
        
#         if result:
#             return ApplicantProfile(**result)
#         return None
        
#     def get_all_applicants(self) -> List[ApplicantProfile]:
#         """Get all applicants"""
#         connection = self.db_manager.get_connection()
#         cursor = connection.cursor(dictionary=True)
        
#         query = "SELECT * FROM ApplicantProfile"
#         cursor.execute(query)
        
#         results = cursor.fetchall()
#         cursor.close()
        
#         return [ApplicantProfile(**result) for result in results]

# class ApplicationDAO:
#     """Data Access Object for Application operations"""
    
#     def __init__(self, db_manager: DatabaseManager):
#         self.db_manager = db_manager
        
#     def insert_application(self, application: ApplicationDetail) -> int:
#         """Insert new application and return ID"""
#         connection = self.db_manager.get_connection()
#         cursor = connection.cursor()
        
#         query = """
#         INSERT INTO ApplicationDetail (applicant_id, application_role, cv_path)
#         VALUES (%s, %s, %s)
#         """
        
#         values = (
#             application.applicant_id,
#             application.application_role,
#             application.cv_path
#         )
        
#         cursor.execute(query, values)
#         connection.commit()
        
#         detail_id = cursor.lastrowid
#         cursor.close()
#         return detail_id
        
#     def get_applications_with_profiles(self) -> List[tuple]:
#         """Get all applications with applicant profiles"""
#         connection = self.db_manager.get_connection()
#         cursor = connection.cursor(dictionary=True)
        
#         query = """
#         SELECT ap.*, ad.*
#         FROM ApplicantProfile ap
#         JOIN ApplicationDetail ad ON ap.applicant_id = ad.applicant_id
#         """
        
#         cursor.execute(query)
#         results = cursor.fetchall()
#         cursor.close()
        
#         applications = []
#         for result in results:
#             # Split the result into profile and detail
#             profile_data = {k: v for k, v in result.items() 
#                           if k in ['applicant_id', 'first_name', 'last_name', 
#                                   'date_of_birth', 'address', 'phone_number']}
#             detail_data = {k: v for k, v in result.items() 
#                          if k in ['detail_id', 'applicant_id', 'application_role', 'cv_path']}
            
#             profile = ApplicantProfile(**profile_data)
#             detail = ApplicationDetail(**detail_data)
#             applications.append((profile, detail))
            
#         return applications
