import mysql.connector
from mysql.connector import Error
from src.config.AppConfig import AppConfig

class DatabaseManager:
    """Database connection and management"""
    
    def __init__(self):
        self.connection = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=AppConfig.DB_HOST,
                user=AppConfig.DB_USER,
                password=AppConfig.DB_PASSWORD,
                database=AppConfig.DB_NAME
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
                return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
    
    def get_connection(self):
        """Get current database connection"""
        return self.connection