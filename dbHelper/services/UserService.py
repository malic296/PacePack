from dbHelper.DBModels import User, Password, Address
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
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

    def add_user(self, name, surname, email, telephone, telephone_code, is_admin, can_create_runs, gender, password_id, address_id):
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
    
    # Returns user info with address included 
    def getUserInfo(self, email):
        return self.session.query(User).filter(User.email == email).options(joinedload(User.address)).first()
    
    def updateUser(self, email, name, surname, telephone, gender, country, streetname, postalcode):
        user = self.session.query(User).filter(User.email==email).options(joinedload(User.address)).first()

        if not user:
            return False

        # Check if user has an address
        if not user.address:
            return False
        
        user.name = name
        user.surname = surname
        user.telephone = telephone
        user.gender = gender
        user.address.country = country
        user.address.streetname = streetname
        user.address.postalcode = postalcode

        self.session.commit()
        return True


    def close(self):
        self.session.close()
