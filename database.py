"""
Database Connection and Query Helpers
=====================================
Connects Flask application to MySQL database (financial_risk_db) using
environment variables and parameterized SQL queries to prevent SQL injection.
Supports both PyMySQL and mysql-connector-python connectors.
"""

import os
import pymysql
from dotenv import load_dotenv

# Load environment configuration
load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'financial_risk_db')
DB_PORT = int(os.getenv('DB_PORT', 3306))


def get_db_connection(database=None):
    """
    Establishes and returns a connection to MySQL.
    Uses DictCursor so records can be accessed like dictionaries.
    """
    db_to_use = DB_NAME if database is None else database
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=db_to_use,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )


def test_connection():
    """
    Tests whether the MySQL server is reachable.
    Returns (status: bool, message: str).
    """
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        conn.close()
        return True, "Successfully reached MySQL server."
    except Exception as e:
        return False, str(e)
