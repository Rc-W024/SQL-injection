from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# create a database engine
engine=create_engine('postgresql://postgres:XXXXX@localhost:5432/postgres')

# create a session factory
Session=sessionmaker(bind=engine)

# create base class
Base=declarative_base()

# define the model class
class Data(Base):
    __tablename__='data'

    id=Column(Integer,primary_key=True)
    username=Column(String)
    password=Column(String)
    geom=Column(String)

