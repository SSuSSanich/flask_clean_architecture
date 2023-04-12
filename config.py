from dotenv import load_dotenv
import os

load_dotenv()

# database configuration
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

# API keys
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
HASH_SECRET_KEY = os.environ.get("HASH_SECRET_KEY")

# Flags
DEBUG = os.environ.get("DEBUG")
TESTING = os.environ.get("TESTING")
LOG_LEVEL = os.environ.get("LOG_LEVEL")