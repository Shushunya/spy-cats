import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./cats.db")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
