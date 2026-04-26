import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. Setup
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ Error: DATABASE_URL not found in environment.")
    exit(1)

# Fix for Neon/Postgres prefix if necessary
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()
metadata.reflect(bind=engine)

def clear_database():
    session = SessionLocal()
    print(f"🔗 Connected to: {DATABASE_URL.split('@')[-1]}") # Print host only for safety
    
    confirm = input("⚠️  Are you sure you want to DELETE ALL meetings and logs? (y/n): ")
    if confirm.lower() != 'y':
        print("Aborted.")
        return

    try:
        # We delete in reverse order of dependencies to avoid Foreign Key errors
        # Tables are deleted from bottom up
        tables = ['processing_logs', 'action_items', 'decisions', 'meetings']
        
        for table_name in tables:
            if table_name in metadata.tables:
                print(f"🗑️  Clearing table: {table_name}...")
                session.execute(metadata.tables[table_name].delete())
            else:
                print(f"❓ Table {table_name} not found, skipping...")

        session.commit()
        print("✅ Database cleared successfully! You have a clean slate.")
    except Exception as e:
        session.rollback()
        print(f"❌ Failed to clear database: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    clear_database()