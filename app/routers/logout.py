from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

from ..database import get_db
from ..schemas.schemas import UserLogin, Token
from ..utils import verify
from ..models import User
from ..oauth2 import generate_access_token, get_current_user

router = APIRouter(
    prefix = "/logout",
    tags = ['Revoke Access']
)
@router.get("/")
def logout(current_user: int = Depends(get_current_user)):
    print(current_user.__dict__)
    # OAuth2PasswordBearer(tokenUrl=None)
