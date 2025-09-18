# services/auth.py — Register & Login logic

from app.db import get_connection
from passlib.context import CryptContext
import psycopg2

'''
get_connection → connects to the database
CryptContext → securely hashes and verifies passwords
psycopg2 → database driver to run queries safely
'''

# Step 1: Set up password hashing
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    """Hash a plaintext password"""
    return pwd_ctx.hash(password)

def verify_password(password, hashed):
    """Verify a plaintext password against a hashed password"""
    return pwd_ctx.verify(password, hashed)

# Step 2: Create a new user
def create_user(username, email, password):
    """
    Inserts a new user into the database with a hashed password.
    Returns a dictionary with user info on success.
    Raises ValueError on duplicate email.
    """
    hashed_password = hash_password(password)

    try:
        # Step 1: Get a connection (RealDictCursor ensures dict rows)
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Step 2: Execute INSERT query safely using parameters
                query = """
                    INSERT INTO users (username, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING id;
                """
                cur.execute(query, (username, email, hashed_password))
                
                # Step 3: Fetch the inserted user ID
                result = cur.fetchone()   # This is a dictionary because of RealDictCursor
                print("Insert result:", result)  # Optional debug
                
                user_id = result['id']

                # Step 4: Commit transaction
                conn.commit()

                # Step 5: Return sanitized user info
                return {"id": user_id, "username": username, "email": email}

    except psycopg2.errors.UniqueViolation:
        # Duplicate email
        raise ValueError(f"Email {email} already exists.")

    except Exception as e:
        # Catch other DB errors
        raise RuntimeError(f"Database error: {e}")

# Step 3: Get user by email (for login)
def get_user_by_email(email):
    """
    Fetches a user by email.
    Returns dictionary with user data including password_hash for verification.
    Returns None if not found.
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM users WHERE email = %s;"
                cur.execute(query, (email,))
                user = cur.fetchone()
                return user  # None if not found
    except Exception as e:
        raise RuntimeError(f"Database error: {e}")
