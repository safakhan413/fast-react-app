# app/test_connection.py

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text  # Import the text function
from database import engine, SessionLocal, Base
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_db_connection():
    try:
        # Attempt to connect to the database
        with engine.connect() as connection:
            print("✅ Successfully connected to the database!")

        # Create a new session
        session = SessionLocal()

        # Get the current database name using the text function
        current_db = session.execute(text("SELECT DATABASE();")).fetchone()[0]
        print(f"🗄️ Current Database: {current_db}")

        # List all tables in the current database using the text function
        tables = session.execute(text("SHOW TABLES;")).fetchall()
        print("📋Tables in the current database:")
        for table in tables:
            print(f"- {table[0]}")

        session.close()

    except SQLAlchemyError as e:
        print("❌ Failed to connect to the database.")
        print(f"Error Details: {e}")

if __name__ == "__main__":
        test_db_connection()
