from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from ..database import Base

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    goal_value = Column(Float, default=0)
    has_reached_goal = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship("User", back_populates="projects")
    contributions = relationship("Contribution", back_populates="project")


class Contribution(Base):
    __tablename__ = 'project_donations'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, default=0)
    donor_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'))

    donor = relationship("User", back_populates="my_contributions")
    project = relationship("Project", back_populates="contributions")