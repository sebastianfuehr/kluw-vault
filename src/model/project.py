from types import NotImplementedType
from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .orm_base import Base


class Project(Base):
    """
    Initialise with id=None to handle as a new project which will be
    inserted into the database. If an id is given, an existing entry
    is searched for and is updated.
    """

    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    project_category_id = Column(Integer, ForeignKey("project_categories.id"))
    project_category = relationship("ProjectCategory")
    project_tags = relationship(
        "ProjectTag", secondary="rel_project_tags", back_populates="projects"
    )
    activities = relationship("Activity", back_populates="project")

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @staticmethod
    def get_column_names() -> List[str]:
        return [
            "id",
            "Name",
            "Description",
            "Project Category ID",
            "Project Tags",
        ]

    def to_string(self) -> str:
        return f"{self.name} ({self.project_category}): {self.description}"

    def __repr__(self) -> str:
        class_name = type(self).__name__
        return (
            f"{class_name}(id={self.id}, name={self.name},"
            f" category={self.project_category}, description={self.description})"
        )

    def __eq__(self, other: object) -> bool | NotImplementedType:
        if not isinstance(other, Project):
            return NotImplemented
        return (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
            and self.project_category == other.project_category
        )
