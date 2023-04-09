from typing import Optional
from pydantic import BaseModel, EmailStr, conint
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
    id: int
    created_at: datetime
    owner_id: int

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

class VoteBase(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostsWithVote(BaseModel):
    Posts: PostGet
    votes: int

    class Config:
        orm_mode = True