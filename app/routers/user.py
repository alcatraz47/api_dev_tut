from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session

from ..models import User
from ..schemas import UserCreate, UserGet
from .. import models
from ..database import engine, get_db
from ..utils import hash
router = APIRouter(
    prefix = "/users",
    tags = ["Users"]
)

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=UserGet)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    # hash the password - user.password
    hashed_pwd = hash(user.password)
    user.password = hashed_pwd

    new_user = User(**user.__dict__)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", status_code = status.HTTP_201_CREATED, response_model=UserGet)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"User with {id} NOT FOUND"
        )
    return user.__dict__