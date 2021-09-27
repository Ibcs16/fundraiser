from typing import List
from pydantic import BaseModel

# Project schemas
class ContributionBase(BaseModel):
    amount: float

class ContributionCreateDTO(ContributionBase):
    donor_id: int
    pass

class Contribution(ContributionBase):
    donor_id: int
    project_id: int

    class Config:
        orm_mode = True

class ProjectBase(BaseModel):
    goal_value: float
    title: str

class ProjectCreateDTO(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    author_id: int
    has_reached_goal: bool
    contributions: List[Contribution] = []

    class Config:
        orm_mode = True