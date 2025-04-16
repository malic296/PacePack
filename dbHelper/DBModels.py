from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, CHAR, CheckConstraint, Interval, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Address(Base):
    __tablename__ = "address"
    
    id = Column(Integer, primary_key=True)
    streetname = Column(String(50), nullable=False)
    postalcode = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Address(id={self.id}, street='{self.streetname}', country='{self.country}')>"

class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True)
    passwordhash = Column(String(100), nullable=False)
    passwordsalt = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Password(id={self.id})>"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    surname = Column(String(20), nullable=False)
    addressid = Column(Integer, ForeignKey("address.id"), nullable=False)
    email = Column(String(30), nullable=False)
    telephone = Column(String(15))
    telephonecode = Column(String(5))
    isadmin = Column(Boolean, nullable=False)
    cancreateruns = Column(Boolean, nullable=False)
    gender = Column(String(1), nullable=False)
    passwordid = Column(Integer, ForeignKey("passwords.id"), nullable=False)
    teamid = Column(Integer, ForeignKey("team.id"), nullable=False)

    # Establish relationships
    address = relationship("Address")
    password = relationship("Password")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
    
class Run(Base):
    __tablename__ = 'run'

    id = Column(Integer, primary_key=True)
    addressid = Column(Integer, ForeignKey('address.id'), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(DateTime, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)

    address = relationship("Address", backref="runs")

    def __repr__(self):
        return f"<Run(name={self.name}, date={self.date})>"
    
class UserRun(Base):
    __tablename__ = 'user_run'

    id = Column(Integer, primary_key=True)
    userid = Column(Integer, ForeignKey('users.id'), nullable=False)
    runid = Column(Integer, ForeignKey('run.id'), nullable=False)
    iscreator = Column(Boolean, default=False)  # True if the user is the creator

    user = relationship("User", backref="user_runs")
    run = relationship("Run", backref="user_runs")

    def __repr__(self):
        return f"<UserRun(user_id={self.user_id}, run_id={self.run_id}, is_creator={self.is_creator})>"
    
class Sponsor(Base):
    __tablename__ = 'sponsor'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False)
    passwordid = Column(Integer, ForeignKey('passwords.id'), nullable=False)

    password = relationship("Password")

    def __repr__(self):
        return f"<Sponsor(name={self.name}, email={self.email})>"
    
class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    category = Column(String(50), nullable=False)
    gender = Column(CHAR(1), CheckConstraint("gender IN ('M', 'F', 'O')"), nullable=False)

    def __repr__(self):
        return f"<Category(category={self.category}, gender={self.gender})>"
    
class Race(Base):
    __tablename__ = 'race'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    time = Column(DateTime, nullable=False)
    capacity = Column(Integer, nullable=False)
    state = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(100), nullable=True)
    sponsorid = Column(Integer, ForeignKey('sponsor.id'), nullable=False)
    categoryid = Column(Integer, ForeignKey('category.id'), nullable=False)
    addressid = Column(Integer, ForeignKey('address.id'), nullable=False)

    sponsor = relationship("Sponsor")
    category = relationship("Category")
    address = relationship("Address")

    def __repr__(self):
        return f"<Race(date={self.date}, capacity={self.capacity}, state={self.state}, name={self.name}, sponsor_id={self.sponsorid}, category_id={self.categoryid})>"
    
class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Team(id={self.id}, name={self.name})>"

class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    state = Column(CHAR(1), CheckConstraint("state IN ('P', 'U', 'C')"), nullable=False)  # Example: P=Paid, U=Unpaid, C=Cancelled
    date = Column(Date, nullable=False)
    userid = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("User")

    def __repr__(self):
        return f"<Payment(id={self.id}, price={self.price}, state={self.state}, date={self.date}, userid={self.userid})>"

class UserRace(Base):
    __tablename__ = 'user_race'

    iduserrace = Column(Integer, primary_key=True)
    paymentid = Column(Integer, ForeignKey('payment.id'), nullable=False)
    userracenumber = Column(Integer, nullable=False)
    time = Column(Interval, nullable=True)
    raceid = Column(Integer, ForeignKey('race.id'), nullable=False)
    userid = Column(Integer, ForeignKey('users.id'), nullable=False)

    payment = relationship("Payment")
    race = relationship("Race")
    user = relationship("User", backref="user_races")

    def __repr__(self):
        return f"<UserRace(iduserrace={self.iduserrace}, number={self.userracenumber}, time={self.time}, raceid={self.raceid}, userid={self.userid})>"