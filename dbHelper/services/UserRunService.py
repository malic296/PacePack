from dbHelper.DBModels import User, Run, UserRun
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import joinedload
from sqlalchemy import create_engine
from dotenv import load_dotenv

import os

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class UserRunService:
    def __init__(self):
        self.session = SessionLocal()

    def add_user_to_run(self, userid, runid, iscreator=False):
        """
        Adds a user to a run with an option to set them as the creator of the run.
        """
        user_run = UserRun(userid=userid, runid=runid, iscreator=iscreator)
        self.session.add(user_run)
        self.session.commit()
        print(f"✅ User with ID {userid} added to run with ID {runid}. Creator: {iscreator}")

    def create_run_and_add_creator(self, userid, runid):
        """
        Creates a run and adds the user as the first participant (creator).
        """
        self.add_user_to_run(userid, runid, iscreator=True)

    def is_user_creator(self, userid, runid):
        """
        Checks if the user is the creator of the run.
        """
        user_run = self.session.query(UserRun).filter_by(userid=userid, runid=runid, iscreator=True).first()
        return user_run is not None

    def get_user_runs(self, userid):
        """
        Returns all runs a user is registered for.
        """
        user_runs = self.session.query(UserRun).filter_by(userid=userid).options(joinedload(UserRun.run)).all()
        return user_runs
    
    def get_user_run_by_run_id(self, run_id):
        """
        Returns the user who is the creator for the given run ID.
        """
        # Query the user_run table for the run_id where is_creator is True
        user_run = self.session.query(UserRun).filter(UserRun.runid == run_id).first()
        
        # If no user is found, return None
        if user_run is None:
            return None
        
        # If a user is found, return the user_run or user details
        return user_run
    
    def get_user_run_by_run_id_and_user_id(self, run_id, user_id):
        """
        Returns the user who is the creator for the given run ID.
        """
        # Query the user_run table for the run_id where is_creator is True
        user_run = self.session.query(UserRun).filter(UserRun.runid == run_id, UserRun.userid == user_id).first()
        
        # If no user is found, return None
        if user_run is None:
            return None
        
        # If a user is found, return the user_run or user details
        return user_run
    
    def get_users_by_run_id(self, run_id):
        return self.session.query(UserRun).filter_by(runid=run_id).all()
    
    # In your UserService class

    def get_user_by_id(self, user_id):
        try:
            return self.session.query(User).filter_by(id=user_id).first()
        except Exception as e:
            print(f"Error fetching user by ID: {e}")
            return None
        
    def register_user_to_run(self, userId, runId):
        new_registration = UserRun(userid=userId, runid=runId, iscreator=False)
        self.session.add(new_registration)
        self.session.commit()
        return True

        
    def unregister_user_from_run(self, userId, runId):
        user_run = self.session.query(UserRun).filter_by(userid=userId, runid=runId).first()
        if user_run:
            self.session.delete(user_run)
            self.session.commit()
            return True
        return False


    def close(self):
        self.session.close()
