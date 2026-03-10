import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker

from db.models import Base


load_dotenv()

DB_PATH = os.getenv("DB_PATH", "ships.db")


def get_engine(db_path: str = DB_PATH):
    return create_engine(f"sqlite:///{db_path}")


@contextmanager
def open_session(db_path: str = DB_PATH):
    engine = get_engine(db_path)
    session: Session = sessionmaker(bind=engine)()
    try:
        yield session
        session.commit()
    except SQLAlchemyError as err:
        print(f"Error: {err}")
        session.rollback()
        raise
    finally:
        session.close()


def create_tables(db_path: str = DB_PATH) -> None:
    Base.metadata.create_all(get_engine(db_path))
