from fastapi import APIRouter, Depends, HTTPException, Form, Path
from sqlalchemy.orm.session import Session
from .. import crud
from ..schemas.projects import ContributionCreateDTO, ProjectCreateDTO
from ..dependencies import get_db

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)


@router.post('/')
async def create_project(title:str = Form(...), goal_value:str = Form(...), user_id: int = Form(..., min=1), db: Session = Depends(get_db)):
    author = crud.get_user(db=db,user_id=user_id)
    if author == None:
        raise HTTPException(status_code=400, detail='User not found')
    new_project = ProjectCreateDTO(title=title,goal_value=goal_value)
    return crud.create_project(user_id=user_id, db=db,project=new_project)


@router.get('/')
async def list_projects(skip:int = 0, limit:int = 100, db: Session = Depends(get_db)):
    return crud.get_projects(db=db,skip=skip, limit=limit)


@router.post('/{id}/contributions')
async def make_contribution(contribution: ContributionCreateDTO, id:int = Path(...), db: Session = Depends(get_db)):
    project = crud.get_project(db=db,project_id=id)
    donor = crud.get_user(db=db, user_id = contribution.donor_id)
    if project == None:
        raise HTTPException(status_code=400, detail='Project not found')
    elif donor == None:
        raise HTTPException(status_code=400, detail='User not found')
    return crud.create_contribution(project_id=id, db=db,contribution=contribution)

@router.get('/{id}/contributions')
async def make_contribution(id:int = Path(...), db: Session = Depends(get_db), skip:int=0, limit:int=100):
    project = crud.get_project(db=db,project_id=id)
    if project == None:
        raise HTTPException(status_code=400, detail='Project not found')
    return crud.get_project_contributions(project_id=id, db=db, skip=skip, limit=limit)