#fetch profile

from app.db import get_connection
import psycopg2
from passlib.context import CryptContext
from psycopg2.extras import RealDictCursor


# Reuse password hashing and verification from auth.py
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_ctx.hash(password)

def verify_password(password, hashed):
    return pwd_ctx.verify(password, hashed)

def get_user_by_id(user_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT id, email, username, role
                    FROM users where id = %s
                """
                cur.execute(query, (user_id,))
                row = cur.fetchone()
                if not row:
                    return None
                return dict(row)
    except Exception as e:
        print("Error in get_user_by_id:", e)  # debug
        raise e
    finally:
        conn.close()
        
# def get_user_by_email(email):
#     with get_connection() as conn:
#         with conn.cursor() as cur:
#             query= """
#                 SELECT * FROM users WHERE email = %s
#             """
#             cur.execute(query, (email))
#             user = cur.fetchone()
#             return user

def update_user(email, username, user_id):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Check duplicate email
                cur.execute("SELECT id FROM users WHERE email=%s AND id != %s", (email, user_id))
                if cur.fetchone():
                    raise ValueError(f"Email {email} already exists.")

                # Update user
                cur.execute(
                    "UPDATE users SET email=%s, username=%s WHERE id=%s RETURNING id, email, username",
                    (email, username, user_id)
                )
                user = cur.fetchone()  # now this is a dict
                conn.commit()
                return user
    except Exception as e:
        raise e

# Exceptions for clarity
class UserNotFound(Exception):
    pass

class InvalidPassword(Exception):
    pass
        
def change_password(user_id, old_pass, new_pass):
    """
    Change a user's password after verifying the old password.

    Args:
        user_id (int): ID of the user whose password will change
        old_password (str): Current password for verification
        new_password (str): New password to be saved

    Returns:
        bool: True if password updated successfully

    Raises:
        UserNotFound: if user does not exist
        InvalidPassword: if old_password is incorrect
        RuntimeError: for general DB errors
        """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT password_hash FROM users WHERE id=%s
                """
                cur.execute(query,(user_id,))
                row = cur.fetchone()
                if not row:
                    raise UserNotFound(f"user with id {user_id} not found")
                
                current_hash = row['password_hash']
                
                #verify old password
                if not verify_password(old_pass, current_hash):
                    raise InvalidPassword("Old password is incorrect.")
                
                #hash new password
                new_hash = hash_password(new_pass)
                
                # update the password
                
                query = """
                    UPDATE users SET password_hash=%s WHERE id=%s
                """
                cur.execute(query, (new_hash, user_id))
                conn.commit()
    except (UserNotFound, InvalidPassword):
        # propagate known exceptions
        raise
    except Exception as e:
        # catch all other DB errors
        raise RuntimeError(f"Database error: {e}")
                    

def delete_user(user_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    DELETE FROM users WHERE id=%s RETURNING id
                """
                cur.execute(query,(user_id,))
                deleted = cur.fetchone()
                if not deleted:
                    raise ValueError("User not found")
                conn.commit()
                return True
    except Exception as e:
        raise RuntimeError(f"Database error: {e}")
# def delete_user(user_id, soft=True):
    """
    Delete a user from the database.

    Args:
        user_id (int): ID of the user to delete
        soft (bool): If True, perform a soft delete; else hard delete

    Returns:
        bool: True if deletion was successful

    Raises:
        UserNotFound: if the user does not exist
        RuntimeError: for other database errors
    """
    """try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                if soft:
                    # Soft delete: mark as inactive and set deleted_at timestamp
                    query = """
                        # UPDATE users
                        # SET is_active = FALSE,
                        #     deleted_at = NOW(),
                        #     updated_at = NOW()
                        # WHERE id = %s;
"""
                    cur.execute(query, (user_id,))
                else:
                    # Hard delete: remove the row permanently
                    query = "DELETE FROM users WHERE id = %s;"
                    cur.execute(query, (user_id,))

                # Check if any row was affected
                if cur.rowcount == 0:
                    raise UserNotFound(f"User with id {user_id} not found.")

                # Commit the transaction
                conn.commit()
                return True

    except UserNotFound:
        # propagate known exception
        raise
    except Exception as e:
        # catch all other DB errors
        raise RuntimeError(f"Database error: {e}")
    """
    