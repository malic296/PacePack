from dbHelper.DBModels import UserRace
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class UserRaceService:
    def __init__(self):
        self.session = SessionLocal()

    def add_user_race(self, paymentid, userracenumber, time, raceid):
        new_user_race = UserRace(
            paymentid=paymentid,
            userracenumber=userracenumber,
            time=time,
            raceid=raceid
        )
        self.session.add(new_user_race)
        self.session.commit()
        return new_user_race.id

    def get_user_race_by_id(self, user_race_id):
        return self.session.query(UserRace).filter(UserRace.iduserrace == user_race_id).first()
    
    def get_users_by_race_id(self, race_id):
        return self.session.query(UserRace).filter_by(raceid=race_id).all()

    def get_user_races_by_race(self, race_id):
        return self.session.query(UserRace).filter(UserRace.raceid == race_id).all()

    def get_user_races_by_payment(self, payment_id):
        return self.session.query(UserRace).filter(UserRace.paymentid == payment_id).all()

    def get_all_user_races(self):
        return self.session.query(UserRace).all()

    def delete_user_race(self, user_race_id):
        user_race = self.get_user_race_by_id(user_race_id)
        if user_race:
            self.session.delete(user_race)
            self.session.commit()
            return True
        return False

    def close(self):
        self.session.close()
