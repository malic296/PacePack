from dbHelper.DBModels import Category
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class CategoryService:
    def __init__(self):
        self.session = SessionLocal()

    def get_categories(self):
        print("test")
        return self.session.query(Category).all()

    def close(self):
        self.session.close()
