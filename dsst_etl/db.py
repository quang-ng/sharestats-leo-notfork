import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base


def get_db_engine():
    database_url = (
        "postgresql://"
        f"{os.environ['POSTGRES_USER']}"
        f":{os.environ['POSTGRES_PASSWORD']}"
        f"@{os.environ['POSTGRES_HOST']}:"
        f"{os.environ['POSTGRES_PORT']}"
    )
    return create_engine(database_url)


def get_db_session():
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    return Session()


def init_db():
    engine = get_db_engine()
    Base.metadata.create_all(engine)
