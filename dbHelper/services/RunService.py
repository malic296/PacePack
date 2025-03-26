from dbHelper.DBModels import User, Password, Address, Run
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
from sqlalchemy import create_engine
from dotenv import load_dotenv

import os

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class RunService:
    def __init__(self):
        self.session = SessionLocal()

    def create_run(self, address_id, date, name, description):
        """Creates a new run and saves it to the database."""
        new_run = Run(
            addressid=address_id,
            date=date,
            name=name,
            description=description
        )
        self.session.add(new_run)
        self.session.commit()
        self.session.refresh(new_run)
        return new_run

    def get_run_by_id(self, run_id: int) -> Run:
        """Fetches a run by its ID."""
        return self.session.query(Run).filter(Run.id == run_id).first()

    def get_all_runs(self):
        """Returns all runs from the database."""
        return self.session.query(Run).options(joinedload(Run.address)).all()

    def update_run(self, run_id, address_id, date, name, description):
        """Updates a run's details."""
        run = self.get_run_by_id(run_id)
        if not run:
            raise ValueError(f"Run with ID {run_id} not found.")
        if address_id:
            run.addressid = address_id
        if date:
            run.date = date
        if name:
            run.name = name
        if description:
            run.description = description
        self.session.commit()
        return run

    def deleteRun(self, run_id: int) -> bool:
        """Deletes a run by ID."""
        run = self.get_run_by_id(run_id)
        if not run:
            raise ValueError(f"Run with ID {run_id} not found.")
        self.session.delete(run)
        self.session.commit()
        return True
    
    def close(self):
        self.session.close()
