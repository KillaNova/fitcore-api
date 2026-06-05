from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

database_url = "*************************"

engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
