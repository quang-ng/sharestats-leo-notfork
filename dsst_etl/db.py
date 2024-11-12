from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import get_database_url

def get_db_engine():
    database_url = get_database_url()
    return create_engine(database_url)

def get_db_session():
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    return Session() 