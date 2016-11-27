# Configuration start
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Classes and Mapping
class Shelter(Base):
    __tablename__ = 'shelter'


class Puppy(Base):
    __tablename__ = 'puppy'


# Configuration end
engine = create_engine('sqlite:///puppyshelters.db')

Base.metadata.create_all(engine)
