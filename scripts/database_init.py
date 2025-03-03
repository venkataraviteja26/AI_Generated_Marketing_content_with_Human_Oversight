from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db  import User, Prompt, GeneratedContent, Review, Base
from config import config

# Define the database URL
DATABASE_URL = config["development"].SQLALCHEMY_DATABASE_URI

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to reset and initialize the database
def reset_and_init_db():
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    print("Creating new tables...")
    Base.metadata.create_all(bind=engine)  # Create new tables
    print("Database initialized successfully!")

if __name__ == "__main__":
    reset_and_init_db()
