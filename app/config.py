#config class, loads .env

import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    DATABASE_URL=os.getenv("DATABASE_URL")
    
    SECRET_KEY= os.getenv("SECRET_KEY")
    JWT_SECRET_KEY= os.getenv("JWT_SECRET")
    
     # JWT config
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # token expires in 1 hour
    JWT_COOKIE_CSRF_PROTECT = False  # disable CSRF for header tokens