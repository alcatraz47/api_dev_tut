from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from sqlalchemy.orm import Session
from typing import List

from .models import Posts, User
from .schemas import PostCreate, PostUpdate, PostGet, UserCreate, UserGet
from . import models
from .database import engine, get_db
from .utils import hash
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

# the fastapi will try to find the first path so the path names need to be sequential
@app.get("/posts", response_model=List[PostGet])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(Posts).all()

    return posts
        
# @app.get("/posts/latest")
# def get_latest():
#     return {"data": my_posts[-1]}

@app.get("/posts/{id}", response_model=PostGet)
def get_post(id: int, db: Session = Depends(get_db)):
    # post = find_posts(id)
    # using first() just to return one post with that id as there is no point
    # searching for more posts with that id as the id is primary key
    post = db.query(Posts).filter(Posts.id==id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {id} not found!")
    
    return post

# use plurals for links/path names
@app.post("/posts", status_code = status.HTTP_201_CREATED, response_model=PostGet)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    single_post = Posts(**post.__dict__)
    db.add(single_post)
    db.commit()
    db.refresh(single_post)

    return single_post

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=PostGet)
def update_posts(id: int, post: PostUpdate, db: Session = Depends(get_db)) -> None:
    # post_idx = find_post_idx(id)
    post_query = db.query(Posts).filter(Posts.id == id)

    if not post_query.first():
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Index not found"
            )
    
    post_query.update(post.__dict__, synchronize_session=False)
    db.commit()
    # my_posts[post_idx] = post.__dict__
    # my_posts[post_idx]["id"] = id
    return post_query.first()

@app.delete("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_posts(id: int, db: Session = Depends(get_db)) -> dict:
    # post_idx = find_post_idx(id)
    post = db.query(Posts).filter(Posts.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post ID: {id} Not Found!"
        )
    
    # my_posts.pop(post_idx)
    post.delete(synchronize_session=False)
    db.commit()
    return {"message": f"post {id} deleted!"}

@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=UserGet)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    # hash the password - user.password
    hashed_pwd = hash(user.password)
    user.password = hashed_pwd

    new_user = User(**user.__dict__)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user