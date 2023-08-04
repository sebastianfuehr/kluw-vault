from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .orm_base import Base


class ProjectCategory(Base):
    __tablename__ = "project_categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)

    def __init__(self, id=None, name=None) -> None:
        self.id = id
        self.name = name
