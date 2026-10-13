import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, sessionmaker

from db_password import get_password

load_dotenv()

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise RuntimeError(
        "DATABASE_URL is not set. Copy .env.example to .env and fill it in."
    )

# The password comes from the encrypted OS keyring (python db_password.py),
# so .env only holds user, host and database name.
password = get_password()
url = make_url(database_url)
if password:
    url = url.set(password=password)

# EXPANSION: production settings. When the app goes online, tune the pool
# (pool_size, max_overflow) and read extra settings (debug mode, allowed
# CORS origins, JWT secret) from .env via a pydantic-settings Settings class.
engine = create_engine(url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
