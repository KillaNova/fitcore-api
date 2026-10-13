import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError(
        "DATABASE_URL is not set. Copy .env.example to .env and fill it in."
    )

# EXPANSION: production settings. When the app goes online, tune the pool
# (pool_size, max_overflow) and read extra settings (debug mode, allowed
# CORS origins, JWT secret) from .env via a pydantic-settings Settings class.
engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
