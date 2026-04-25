import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load local .env if it exists (Railway ignores this, which is fine)
load_dotenv()

# Fetch the variable
DATABASE_URL = os.getenv("DATABASE_URL")

# --- BULLETPROOFING CHECKS ---
# 1. Fail loudly if the variable is still missing
if not DATABASE_URL:
    raise ValueError("🚨 CRITICAL ERROR: DATABASE_URL is None. Railway is not passing the variable to Python.")

# 2. Fix the classic SQLAlchemy Postgres trap
# SQLAlchemy 1.4+ requires 'postgresql://', but Neon sometimes gives 'postgres://'
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Connection to database
engine = create_engine(DATABASE_URL)

# Each instance of the SessionLocal class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Class to create each of the database models
Base = declarative_base()