from dbHelper.DBModels import Team
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv("environment.env")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

class TeamService:
    def __init__(self):
        self.session = SessionLocal()

    def add_team(self, name):
        new_team = Team(name=name)
        self.session.add(new_team)
        self.session.commit()
        return new_team.id

    def get_team_by_id(self, team_id):
        return self.session.query(Team).filter(Team.id == team_id).first()

    def get_all_teams(self):
        return self.session.query(Team).all()

    def delete_team(self, team_id):
        team = self.get_team_by_id(team_id)
        if team:
            self.session.delete(team)
            self.session.commit()
            return True
        return False

    def close(self):
        self.session.close()
