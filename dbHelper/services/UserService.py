from dbHelper.DBModels import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class UserService:
    def __init__(self):
        self.session = SessionLocal()

    def add_user(self, name, surname, address_id, email, telephone, telephone_code, is_admin, can_create_runs, gender, password_id):
        new_user = User(
            name=name,
            surname=surname,
            addressid=address_id,
            email=email,
            telephone=telephone,
            telephonecode=telephone_code,
            isadmin=is_admin,
            cancreateruns=can_create_runs,
            gender=gender,
            passwordid=password_id
        )
        self.session.add(new_user)
        self.session.commit()
        print(f"✅ New user inserted with ID: {new_user.id}")

    def isUserEmailInUse(self, email):
        existing_user = self.session.query(User).filter_by(email=email).first()
        return existing_user is not None

    def close(self):
        self.session.close()
