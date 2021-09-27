from typing import List

from pydantic import BaseModel
from .projects import Project

# User schemas

class UserBase(BaseModel):
    name: str
    email: str

class UserCreateDTO(UserBase):
    password: str

class User(UserBase):
    id: int
    projects: List[Project] = []

    class Config:
        orm_mode = True