import os
import psycopg2
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Get DATABASE_URL
dsn = os.getenv("DATABASE_URL")
print("Connecting to:", dsn)  # just to confirm it's loaded

try:
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Postgres version:", version)
    cur.close()
    conn.close()
except Exception as e:
    print("Connection failed:", e)



'''
Start Postgres

Open your terminal in the project folder and run:

docker compose up -d


-d → detached mode (runs in background)

To check running containers:

docker ps


To see logs:

docker compose logs -f db
'''
''' Explanation:

image: postgres:15 → latest Postgres 15 image

POSTGRES_USER / POSTGRES_PASSWORD → credentials for your app

POSTGRES_DB → database your app will use

ports → expose 5432 so Flask can connect

volumes → persist data even if container stops'''

'''
docker compose exec db psql -U ums_user -d ums_dev
\dt → list tables

\q → quit
'''