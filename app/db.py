#Db connection/helper functions

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Step 1: Load environment variables from .env
load_dotenv()

# Step 2: Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Step 3: Function to create a new connection to Postgres
def get_connection():
    """
    Returns a psycopg2 connection object with RealDictCursor.
    Each call returns a new connection. Remember to close it after use.
    
    Returns a new psycopg2 connection object with RealDictCursor
    so that query results are returned as dictionaries.
    Usage:
        with get_connection() as conn:
            with conn.cursor() as cur:
                ...
    
    """
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# Step 4: Optional test function to verify connection
def test_connection():
    """
    Simple test to check if the database is reachable.
    """
    try:
        # Get a connection
        conn = get_connection()
        # Create a cursor
        cur = conn.cursor()
        # Execute a simple query
        cur.execute("SELECT version();")
        # Fetch result
        version = cur.fetchone()
        print("Postgres version:", version)
        # Close cursor and connection
        cur.close()
        conn.close()
    except Exception as e:
        print("Database connection failed:", e)

# Step 5: If you run this file directly, test the DB connection
if __name__ == "__main__":
    test_connection()
    
'''
# Step 4: Optional test function to check DB connection
if __name__ == "__main__":
    try:
        # Use the helper function to get connection
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Execute a simple query
                cur.execute("SELECT version();")
                row = cur.fetchone()
                print("Postgres version:", row)
    except Exception as e:
        print("DB connection failed:", e)
'''
