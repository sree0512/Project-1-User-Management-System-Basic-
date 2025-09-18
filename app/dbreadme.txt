1️⃣ Enter the Postgres container
docker compose exec db psql -U ums_user -d ums_dev


This opens the psql prompt.

2️⃣ List all tables (optional)
\dt


Confirms the tables exist; you should see users.

3️⃣ View columns of the users table (optional)
\d users


Shows all columns, types, default values, and constraints.

4️⃣ Select all users
SELECT * FROM users;


Returns all rows in the table.

You’ll see columns like id, username, email, password_hash, role, created_at.

5️⃣ Filter by email or username (optional)
SELECT * FROM users WHERE email = 'john@example.com';


Returns only the user with that email.

6️⃣ Exit psql
\q

ums_dev=# SELECT * FROM users;
ums_dev=# SELECT * FROM users WHERE email = 'john1@example.com'; 

