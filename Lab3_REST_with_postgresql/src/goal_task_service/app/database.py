from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DB_NAME = os.getenv('DATABASE_NAME', 'goal_task_service_db')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'toor')
CONTAINER_NAME = os.getenv('CONTAINER_NAME', 'goal_task_db')
PORT = os.getenv('PORT', '5432')

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{CONTAINER_NAME}:{PORT}/{DB_NAME}'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()