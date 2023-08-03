from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class DBConnection:
    def __init__(self, db_path):
        self.db_engine = create_engine(f"sqlite://{db_path}", echo=False)
        self.Session = sessionmaker(bind=self.db_engine)
