from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from .user_schema import UserGet

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
    owner_id: int
    # owner: UserGet

    class Config:
        orm_mode = True