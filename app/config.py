#config class, loads .env

import os
from dotenv import load_dotenv
from datetime import timedelta

# load_dotenv()

class Config:
    DATABASE_URL=os.environ.get("DATABASE_URL")
    
    SECRET_KEY= os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY= os.environ.get("JWT_SECRET")
    
     # JWT config
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # token expires in 1 hour
    JWT_COOKIE_CSRF_PROTECT = False  # disable CSRF for header tokens
