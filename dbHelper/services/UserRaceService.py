from dbHelper.DBModels import UserRace, Payment
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class UserRaceService:
    def __init__(self):
        self.session = SessionLocal()

    def add_user_race(self, paymentid, userracenumber, time, raceid, userid):
        new_user_race = UserRace(
            paymentid=paymentid,
            userracenumber=userracenumber,
            time=time,
            raceid=raceid,
            userid=userid
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
    
    def register_user_to_race(self, userId, raceId):
        # Create payment (example: hardcoded values just to make it work)
        payment = Payment(
            price=20,                 # you can later change this to dynamic pricing
            state='D',               # D = done
            date=date.today(),
            userid=userId
        )
        self.session.add(payment)
        self.session.commit()  # commit so payment.id gets assigned

        # Create user-race relation with the new payment
        new_registration = UserRace(
            userid=userId,
            raceid=raceId,
            paymentid=payment.id,
            userracenumber=0  # you can later add logic for assigning race numbers
        )
        self.session.add(new_registration)
        self.session.commit()

        return True

        
    def unregister_user_from_race(self, userId, raceId):
        user_race = self.session.query(UserRace).filter_by(userid=userId, raceid=raceId).first()

        if user_race:
            # Also remove the associated payment
            payment = self.session.query(Payment).filter_by(id=user_race.paymentid).first()
            if payment:
                self.session.delete(payment)

            self.session.delete(user_race)
            self.session.commit()
            return True

        return False
    
    def get_user_races(self, userid):
        """
        Returns all runs a user is registered for.
        """
        user_runs = self.session.query(UserRace).filter_by(userid=userid).options(joinedload(UserRace.race)).all()
        return user_runs

    def close(self):
        self.session.close()
