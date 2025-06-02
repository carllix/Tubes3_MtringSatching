# src/main.py
import sys
import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.App import App
from database.Connection import DatabaseManager
from config.AppConfig import AppConfig

def main():
    try:
        #  Inisilaisasi database connection
        db_manager = DatabaseManager()
        db_manager.connect()
        
        # # Initialize and run GUI
        app = App()
        app.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")
    finally:
        # Cleanup database connection
        if 'db_manager' in locals():
            db_manager.disconnect()

if __name__ == "__main__":
    main()
