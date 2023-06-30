from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_engine = create_engine('sqlite:///time-journal.db', echo=False)
Session = sessionmaker(bind=db_engine)

Base = declarative_base()
