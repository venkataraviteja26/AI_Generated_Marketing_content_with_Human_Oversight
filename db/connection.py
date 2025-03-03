from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import config

# Use the DATABASE_URL from config; if using SQLite, set additional connect args.
DATABASE_URL = config["development"].SQLALCHEMY_DATABASE_URI
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Session factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

def init_db():
    """
    Initialize the database by importing models and creating tables.
    This function should be called at application startup.
    """
    # Import models so that they are registered on the Base
    from db import models  # Ensure models.py exists with your ORM models
    Base.metadata.create_all(bind=engine)
