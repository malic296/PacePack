from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import os

load_dotenv("environment.env")

engine = create_engine(os.getenv("DATABASE_URL"))

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()")) 
        db_version = result.fetchone()[0]
        print(f"Connection successful! Database version: {db_version}")
except Exception as e:
    print(f"Connection failed: {e}")