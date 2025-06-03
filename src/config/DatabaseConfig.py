import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConfig:
    """Database configuration settings"""
    
    HOST = os.getenv('DB_HOST', 'localhost')
    USER = os.getenv('DB_USER', 'root')
    PASSWORD = os.getenv('DB_PASSWORD', '')
    DATABASE = os.getenv('DB_NAME', 'cv_ats_system')
    PORT = int(os.getenv('DB_PORT', '3306'))
    
    # Connection pool settings
    POOL_NAME = 'ats_pool'
    POOL_SIZE = 5
    POOL_RESET_SESSION = True
    
    @classmethod
    def get_connection_config(cls):
        """Get database connection configuration as dictionary"""
        return {
            'host': cls.HOST,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'database': cls.DATABASE,
            'port': cls.PORT,
            'autocommit': False,
            'charset': 'utf8mb4',
            'use_unicode': True
        }
