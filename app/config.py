import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "taskdb")
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-only-insecure-key")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
