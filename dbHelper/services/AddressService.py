from dbHelper.DBModels import Address
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class AddressService:
    def __init__(self):
        self.session = SessionLocal()

    def add_address(self, streetname, postalcode, country):
        new_address = Address(
            streetname=streetname,
            postalcode=postalcode,
            country=country
        )
        self.session.add(new_address)
        self.session.commit()
        return new_address.id
    
    def get_all_addresses(self):
        return self.session.query(Address).all()

    def close(self):
        self.session.close()
