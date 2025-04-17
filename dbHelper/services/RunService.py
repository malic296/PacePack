from dbHelper.DBModels import User, Password, Address, Run, UserRun
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
from sqlalchemy import create_engine
from dotenv import load_dotenv
from datetime import datetime

import os

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class RunService:
    def __init__(self):
        self.session = SessionLocal()

    def create_run(self, streetname, postalcode, country, date, time, name, description):
        # Check if the address already exists
        existing_address = self.session.query(Address).filter_by(streetname=streetname, postalcode=postalcode, country=country).first()

        if not existing_address:
            new_address = Address(streetname=streetname, postalcode=postalcode, country=country)
            self.session.add(new_address)
            self.session.commit()
        else:
            new_address = existing_address

        new_run = Run(addressid=new_address.id, date=date, time=time, name=name, description=description)
        self.session.add(new_run)
        self.session.commit()
        return new_run

    def get_run_by_id(self, run_id):
        """Fetches a run by its ID."""
        return self.session.query(Run).filter(Run.id == run_id).options(joinedload(Run.address)).first()

    def get_all_runs(self):
        """Returns all runs from the database that are newer than the current date."""
        current_date = datetime.now()
        print(current_date)  
        #return self.session.query(Run).filter(Run.date + Run.time >= current_date).options(joinedload(Run.address)).all()
        return self.session.query(Run).options(joinedload(Run.address)).all()

    def update_run(self, run_id, streetname, postalcode, country, date, time, name, description):
        run = self.session.query(Run).filter_by(id=run_id).first()
        if not run:
            raise Exception("Run not found")

        existing_address = self.session.query(Address).filter_by(streetname=streetname, postalcode=postalcode, country=country).first()
        
        if not existing_address:
            new_address = Address(streetname=streetname, postalcode=postalcode, country=country)
            self.session.add(new_address)
            self.session.commit()
        else:
            new_address = existing_address

        run.addressid = new_address.id
        run.date = date
        run.time = time
        run.name = name
        run.description = description

        self.session.commit()
        return run

    def delete_run(self, run_id):
        """Deletes a run by ID."""
        try:
            run = self.get_run_by_id(run_id)
            if not run:
                raise ValueError(f"Run with ID {run_id} not found.")
            
            address_id = run.addressid

            self.session.query(UserRun).filter_by(runid=run_id).delete()

            self.session.delete(run)
            self.session.commit()

            address_in_use = self.session.query(Run).filter_by(addressid=address_id).first()
            if not address_in_use:
                address = self.session.query(Address).filter_by(id=address_id).first()
                if address:
                    self.session.delete(address)
                    self.session.commit()

            return True

        except Exception as e:
            self.session.rollback()
            return False

    
    def close(self):
        self.session.close()
