from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostGet(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserGet(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(UserBase):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]
    