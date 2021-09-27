from fastapi import Depends, Path
from fastapi.exceptions import HTTPException
from sqlalchemy.orm.session import Session
from fastapi import APIRouter
from .. import crud
from ..schemas.users import UserCreateDTO
from ..dependencies import get_db

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@router.post('/')
async def create_user(user: UserCreateDTO, db: Session = Depends(get_db)):
    new_user = crud.get_user_by_email(db, email=user.email)
    if new_user:
        raise HTTPException(status_code=400, detail='Email already exists')
    return crud.create_user(db, user=user)

@router.get('/{id}')
async def get_user(id: int = Path(...), db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=id)
    if user == None:
        raise HTTPException(status_code=400, detail='User not found')
    return user