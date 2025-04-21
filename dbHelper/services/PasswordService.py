from dbHelper.DBModels import Password, User, Sponsor
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import hashlib

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

def generate_salt():
        return os.urandom(16).hex()
    
def generate_hash(password, salt):
    salted_password = bytes.fromhex(salt) + password.encode()
    return hashlib.sha256(salted_password).hexdigest()

class PasswordService:
    def __init__(self):
        self.session = SessionLocal()

    def add_password(self, password):
        passwordSalt = generate_salt()

        new_password = Password(
            passwordsalt=passwordSalt,
            passwordhash=generate_hash(password, passwordSalt)
        )
        self.session.add(new_password)
        self.session.commit()
        return new_password.id
    
    def validate_user_login(self, email, password):
        user = self.session.query(User).filter_by(email=email).first()

        if user is None:
            return False
        
        passwordInTable = self.session.query(Password).filter(Password.id == user.passwordid).first()

        if passwordInTable is None:
            return False
        
        passwordHashed = generate_hash(password, passwordInTable.passwordsalt)

        if passwordHashed == passwordInTable.passwordhash:
            return True

        return False
    
    def validate_sponsor_login(self, email, password):
        sponsor = self.session.query(Sponsor).filter_by(email=email).first()

        if sponsor is None:
            return False

        password_record = self.session.query(Password).filter(Password.id == sponsor.passwordid).first()

        if password_record is None:
            return False

        password_hashed = generate_hash(password, password_record.passwordsalt)

        if password_hashed == password_record.passwordhash:
            return True

        return False


    def close(self):
        self.session.close()
