1️⃣ from app.db import get_connection

Why we need it:

All database operations need a connection to Postgres.

You already wrote db.py to handle connections safely.

Instead of creating a new connection every time inside auth.py, we reuse the helper.

This keeps code DRY (Don’t Repeat Yourself) and centralized — if DB connection logic changes, you change it in one place.

How you know to use it:

Any time you need to run a query against your database.

This is standard in layered apps: services use a DB helper or ORM, not raw connections everywhere.

2️⃣ from passlib.context import CryptContext

Why we need it:

User passwords must never be stored in plain text.

We need a secure hash (bcrypt) that includes salt automatically.

passlib is the standard Python library for password hashing.

How you know to use it:

Whenever you store or verify passwords.

You could use other libraries (bcrypt directly, werkzeug.security) but passlib is easier and secure by default.

Example usage logic:

hash_password("mypassword") → store in DB

verify_password("mypassword", hashed_from_db) → login check

3️⃣ import psycopg2

Why we need it:

psycopg2 is the official Postgres adapter for Python.

get_connection() returns a psycopg2 connection object.

We need the module to handle exceptions, e.g., psycopg2.errors.UniqueViolation when inserting duplicate emails.

How you know to use it:

Any time you want to catch DB-specific errors.

Any time you want to run parameterized queries safely.

✅ How you “know” what libraries to import in general

Ask yourself: “What do I need to do here?”

Connect to DB → need get_connection (or ORM)

Hash passwords → need a password library

Catch DB errors → need psycopg2 exceptions

Check existing modules in your project

We already wrote db.py → use it

You installed passlib → use it

Python docs or common patterns

Security → always hash passwords

DB → parameterized queries, proper exception handling

💡 Quick analogy:

get_connection → “phone line” to talk to DB

CryptContext → “lockbox” for storing passwords safely

psycopg2 → “manuals” to understand DB errors and do queries safely