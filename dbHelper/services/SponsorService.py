from dbHelper.DBModels import Sponsor
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class SponsorService:
    def __init__(self):
        self.session = SessionLocal()

    def add_sponsor(self, name, email, passwordid):
        new_sponsor = Sponsor(name=name, email=email, passwordid=passwordid)
        self.session.add(new_sponsor)
        self.session.commit()
        return new_sponsor.id

    def get_sponsor_by_id(self, sponsor_id):
        return self.session.query(Sponsor).filter(Sponsor.id == sponsor_id).first()

    def get_all_sponsors(self):
        return self.session.query(Sponsor).all()

    def update_sponsor(self, sponsor_id, name=None, email=None, passwordid=None):
        sponsor = self.get_sponsor_by_id(sponsor_id)
        if sponsor:
            if name is not None:
                sponsor.name = name
            if email is not None:
                sponsor.email = email
            if passwordid is not None:
                sponsor.passwordid = passwordid
            self.session.commit()
            return True
        return False

    def delete_sponsor(self, sponsor_id):
        sponsor = self.get_sponsor_by_id(sponsor_id)
        if sponsor:
            self.session.delete(sponsor)
            self.session.commit()
            return True
        return False

    def get_sponsor_by_email(self, email):
        return self.session.query(Sponsor).filter(Sponsor.email == email).first()

    def close(self):
        self.session.close()
