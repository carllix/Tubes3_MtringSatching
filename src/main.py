#!/usr/bin/env python3
"""
ATS CV Checker GUI Launcher
Launch the GUI application for the ATS CV checker
"""

import sys
import os

# Add the parent directory (project root) to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import and run the GUI
from src.gui.App import App

if __name__ == "__main__":
    app = App()
    app.run()
