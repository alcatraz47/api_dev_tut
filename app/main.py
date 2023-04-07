from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from typing import List

from .models import Posts, User
from .schemas.schemas import PostCreate, PostUpdate, PostGet, UserCreate, UserGet
from . import models
from .database import engine, get_db
from .utils import hash

from .routers import post, user, auth, logout
# from .crud import create_post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#path operation [according to fastapi] or route
# http methods will be maintained via decorator's function(get, post, update, delete). path is the specific domain name fo the api.
# the line below is the decoretor. this will convert the function into an actual path operation.
@app.get("/")
# this is a function for asynchronization, async is used.
async def root():
    return {"message": "Hello World"}

app.include_router(auth.router)
app.include_router(logout.router)
app.include_router(user.router)
app.include_router(post.router)