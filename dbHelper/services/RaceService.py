from dbHelper.DBModels import Race
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class RaceService:
    def __init__(self):
        self.session = SessionLocal()

    def add_race(self, date, time, capacity, state, name, description, sponsorid, categoryid, addressid):
        new_race = Race(
            date=date,
            time=time,
            capacity=capacity,
            state=state,
            name=name,
            description=description,
            sponsorid=sponsorid,
            categoryid=categoryid,
            addressid=addressid
        )
        self.session.add(new_race)
        self.session.commit()
        return new_race.id

    def get_race_by_id(self, race_id):
        return self.session.query(Race).filter(Race.id == race_id).first()

    def get_all_races(self):
        return self.session.query(Race).all()

    def get_races_by_category(self, category_id):
        return self.session.query(Race).filter(Race.categoryid == category_id).all()

    def get_races_by_sponsor(self, sponsor_id):
        return self.session.query(Race).filter(Race.sponsorid == sponsor_id).all()

    def get_races_by_address(self, address_id):
        return self.session.query(Race).filter(Race.addressid == address_id).all()

    def update_race(self, race_id, date=None, time=None, capacity=None, state=None, name=None, description=None, sponsorid=None, categoryid=None, addressid=None):
        race = self.get_race_by_id(race_id)
        if race:
            if date: race.date = date
            if time: race.time = time
            if capacity: race.capacity = capacity
            if state: race.state = state
            if name: race.name = name
            if description: race.description = description
            if sponsorid: race.sponsorid = sponsorid
            if categoryid: race.categoryid = categoryid
            if addressid: race.addressid = addressid

            self.session.commit()
            return race
        return None

    def delete_race(self, race_id):
        race = self.get_race_by_id(race_id)
        if race:
            self.session.delete(race)
            self.session.commit()
            return True
        return False

    def close(self):
        self.session.close()
