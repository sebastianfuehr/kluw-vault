from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


class Base(DeclarativeBase):
    """Preferred over declarative_base() method to support typing.

    Source:
    https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html#migrating-an-existing-mapping # noqa: E501
    """

    pass


class DBConnection:
    def __init__(self, db_path: str):
        self.db_engine = create_engine(f"sqlite://{db_path}", echo=False)
        self.Session = sessionmaker(bind=self.db_engine)
