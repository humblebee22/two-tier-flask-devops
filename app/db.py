import mysql.connector
from mysql.connector import Error
from app.config import Config


def get_db_connection():
    """
    Creates and returns a new connection to the MySQL database.
    Raises an exception if the connection fails, so callers can
    handle it (e.g. return a 500 error to the client) instead of
    the app crashing silently.
    """
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def init_db():
    """
    Creates the 'tasks' table if it doesn't already exist.
    Safe to call every time the app starts — CREATE TABLE IF NOT EXISTS
    is idempotent, so it won't wipe existing data or error out on
    repeated runs.
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(50) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()
