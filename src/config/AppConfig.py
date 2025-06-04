# class AppConfig:
#     # Database Config
#     DB_HOST = "localhost"
#     DB_USER = "root"
#     DB_PASSWORD = "admin123"
#     DB_NAME = "ATS_SYSTEM"
    
#     # # App Settings
#     # APP_TITLE = "CV Analyzer App - ATS System"
#     # APP_GEOMETRY = "1200x800"
    
#     # # File Paths
#     # CV_DATA_PATH = "data/cv_files"
#     # EXTRACTED_TEXT_PATH = "data/extracted_texts"
    
#     # # Algorithm Settings
#     # LEVENSHTEIN_THRESHOLD = 0.7
#     # MAX_FUZZY_MATCHES = 10
    
#     # # GUI Settings
#     # FONT_FAMILY = "Arial"
#     # FONT_SIZE = 12

from dotenv import load_dotenv
import os

load_dotenv()

class AppConfig:
    BASE_DATA_PATH = os.getenv("BASE_DATA_PATH", "data/")
    CV_FILES_PATH = os.path.join(BASE_DATA_PATH, "cv_files/")
    EXTRACTED_TEXT_PATH = os.path.join(BASE_DATA_PATH, "extracted_texts/")
    
    # Application settings
    APP_TITLE = "CV Analyzer App - ATS System"
    APP_GEOMETRY = "1200x800"
    
    # Algorithm settings
    LEVENSHTEIN_THRESHOLD = 0.7
    MAX_FUZZY_MATCHES = 10
