from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = "postgresql://postgres:2u8d6ay3@localhost/Fitcore"

engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
