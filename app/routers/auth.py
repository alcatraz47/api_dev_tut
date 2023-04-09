from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..database import get_db
from ..schemas.schemas import UserLogin, Token
from ..utils import verify
from ..models import User
from ..oauth2 import generate_access_token, get_current_user

router = APIRouter(
    prefix = "/login",
    tags = ['Authentication']
)

@router.post(
        "/",
        status_code=status.HTTP_200_OK,
        response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # the user_credential will follow the schema below
    """
        {
            "username": "demo_user",
            "password": "demo_pass"
        }
    """
    
    user = db.query(User).filter(
        User.email == user_credentials.username
    ).first()
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Attempted Unauthorized Access! Check the Email or Password!"
        )
    elif (
        user.email != user_credentials.username
        or not verify(user_credentials.password, user.password)
    ):
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Attempted Unauthorized Access! Check the Email or Password!"
        )

    access_token = generate_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}