from dbHelper.DBModels import Team, User, UserRun, Race, UserRace, Run
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_
from dotenv import load_dotenv
import os

from sqlalchemy import func, select, and_, cast, DateTime
from sqlalchemy.orm import aliased
from datetime import datetime

from sqlalchemy.sql import literal_column

from sqlalchemy import case

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

    def get_team_activity_counts(self):
        from datetime import datetime
        now = datetime.now()

        try:
            run_counts = (
                self.session.query(
                    Team.id.label("team_id"),
                    func.count(UserRun.id).label("count")
                )
                .join(User, User.teamid == Team.id)
                .join(UserRun, UserRun.userid == User.id)
                .join(Run, Run.id == UserRun.runid)
                .filter(Run.date + Run.time < now)
                .group_by(Team.id)
                .all()
            )

            race_counts = (
                self.session.query(
                    Team.id.label("team_id"),
                    func.count(UserRace.iduserrace).label("count")
                )
                .join(User, User.teamid == Team.id)
                .join(UserRace, UserRace.userid == User.id)
                .join(Race, Race.id == UserRace.raceid)
                .filter(Race.date + Race.time < now)
                .group_by(Team.id)
                .all()
            )

            combined = {}
            for team_id, count in run_counts:
                combined[team_id] = combined.get(team_id, 0) + count
            for team_id, count in race_counts:
                combined[team_id] = combined.get(team_id, 0) + count

            return list(combined.items())

        except Exception as e:
            print(f"Error: {str(e)}")
            return []


    def close(self):
        self.session.close()
