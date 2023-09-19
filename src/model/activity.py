from types import NotImplementedType

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.project import Project

from .orm_base import Base


class Activity(Base):
    __tablename__ = "activities"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    project: Mapped["Project"] = relationship("Project", back_populates="activities")

    def __init__(self, id=None, name=None) -> None:
        self.id = id
        self.name = name

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Activity):
            return NotImplemented
        return (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
            and self.project == other.project
        )
