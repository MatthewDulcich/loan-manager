import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Database configuration
DB_NAME = "loans.db"
DB_PATH = BASE_DIR / "database" / DB_NAME
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

# GUI settings
WINDOW_TITLE = "Loan Manager"
WINDOW_SIZE = "800x600"

# Default strategy ID
DEFAULT_STRATEGY_ID = 1

# Logging configuration
LOG_FILE = BASE_DIR / "logs" / "app.log"
LOG_LEVEL = "INFO"

# Other constants
DATE_FORMAT = "%Y-%m-%d"