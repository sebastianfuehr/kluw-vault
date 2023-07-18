from sqlalchemy import Column, Integer, ForeignKey
from .orm_base import Base


class RelProjectTag(Base):
    __tablename__ = "rel_project_tags"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    project_tag_id = Column(
        Integer, ForeignKey("project_tags.id"), primary_key=True
    )

    def __init__(self):
        print("Test")
