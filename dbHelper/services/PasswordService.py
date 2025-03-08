from dbHelper.DBModels import Password
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class PasswordService:
    def __init__(self):
        self.session = SessionLocal()

    def add_password(self, passwordhash, passwordsalt):
        new_password = Password(
            passwordhash=passwordhash,
            passwordsalt=passwordsalt
        )
        self.session.add(new_password)
        self.session.commit()
        print(f"✅ New password inserted with ID: {new_password.id}")
        return new_password.id

    def close(self):
        self.session.close()
