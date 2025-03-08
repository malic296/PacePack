from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
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

    # Establish relationships
    address = relationship("Address")
    password = relationship("Password")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}')>"
