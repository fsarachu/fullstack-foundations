# Configuration start
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Enum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Classes and Mapping
class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zipcode = Column(String(10), nullable=False)
    website = Column(String(255))


class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(Enum('male', 'female'), nullable=False)
    weight = Column(Numeric(precision=10, scale=2), nullable=False)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)


# Configuration end
engine = create_engine('sqlite:///puppyshelters.db')

Base.metadata.create_all(engine)
