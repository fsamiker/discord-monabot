from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import os

from dotenv import load_dotenv
load_dotenv()


DATABASE_URI = os.getenv('DATABSE_URI')
engine = create_engine(
    DATABASE_URI,
    pool_size=20,
    max_overflow=2,
    pool_recycle=300,
    pool_pre_ping=True,
    pool_use_lifo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()