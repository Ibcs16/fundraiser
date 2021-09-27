from sqlalchemy.orm import Session

from .schemas.users import UserCreateDTO
from .schemas.projects import ContributionCreateDTO, ProjectCreateDTO

from .models.users import User
from .models.projects import Contribution, Project

def get_user(db: Session, user_id: int):
    return db.query(User).filter_by(id = user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter_by(email = email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreateDTO):
    hashed_password = 'not so random'
    new_user = User(name=user.name, email=user.email,hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_project(db: Session, project_id: int):
    return db.query(Project).filter_by(id = project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: ProjectCreateDTO, user_id: int):
    new_project = Project(**project.dict(), author_id=user_id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_project_contributions(db: Session, project_id: int, skip: int = 0, limit: int = 100):
    return db.query(Contribution).filter_by(id=project_id).offset(skip).limit(limit).all()

def create_contribution(db: Session, contribution: ContributionCreateDTO, project_id: int):
    new_contribution = Contribution(**contribution.dict(), project_id=project_id)
    db.add(new_contribution)
    db.commit()
    db.refresh(new_contribution)
    return new_contribution