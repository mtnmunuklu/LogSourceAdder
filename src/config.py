import os
from dotenv import load_dotenv
from pathlib import Path  # python3 only

# load enviorment variables
env_path = 'src/.env'
load_dotenv(dotenv_path=env_path)


class Config:
    """
    Set configuration vars from .env file
    """

    # Load in environment variables
    # These fields are associated with logger
    LOG_DIR = os.getenv('LOG_DIR')
    LOG_FILE = os.getenv('LOG_FILE')
    LOG_FORMAT = os.getenv('LOG_FORMAT')
    # These fields are associated with ssh and database connection
    DATABASE_SERVER_IP = os.getenv('DATABASE_SERVER_IP')
    DATABASE_NAME = os.getenv('DATABASE_NAME')
    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
    # These fields are associated with logsources
    LOG_SOURCES = os.getenv('LOG_SOURCES')