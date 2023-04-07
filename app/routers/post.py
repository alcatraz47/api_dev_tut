from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
from typing import List

from ..models import Posts, User
from ..schemas.post_schema import PostCreate, PostUpdate, PostGet
from ..schemas.user_schema import UserCreate, UserGet
from .. import models
from ..database import engine, get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

# the fastapi will try to find the first path so the path names need to be sequential
@router.get(
        "/",
        response_model=List[PostGet])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)):
    # posts = db.query(Posts).filter(Posts.owner_id == current_user.id).all()
    posts = db.query(Posts).all()

    return posts
        
# @app.get("/posts/latest")
# def get_latest():
#     return {"data": my_posts[-1]}

@router.get(
        "/{id}",
        response_model=PostGet)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)):
    # post = find_posts(id)
    # using first() just to return one post with that id as there is no point
    # searching for more posts with that id as the id is primary key
    post = db.query(Posts).filter(Posts.id==id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID: {id} not found!")
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail=f"{current_user.email} is not authorized to see this post"
    #     )
    
    return post

# use plurals for links/path names
@router.post(
        "/",
        status_code = status.HTTP_201_CREATED,
        response_model=PostGet)
def create_posts(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)):
    print(current_user.id)
    
    single_post = Posts(owner_id = current_user.id, **post.__dict__)
    db.add(single_post)
    db.commit()
    db.refresh(single_post)

    return single_post

@router.put(
        "/{id}", 
        status_code=status.HTTP_202_ACCEPTED, 
        response_model=PostGet)
def update_posts(
    id: int, post: PostUpdate, 
    db: Session = Depends(get_db), 
    current_user: int = Depends(get_current_user)) -> None:
    
    # post_idx = find_post_idx(id)
    post_query = db.query(Posts).filter(Posts.id == id)

    if not post_query.first():
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Index not found"
            )
    
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{current_user.email} is not authorized to update this post"
        )
    
    post_query.update(post.__dict__, synchronize_session=False)
    db.commit()
    # my_posts[post_idx] = post.__dict__
    # my_posts[post_idx]["id"] = id
    return post_query.first()

@router.delete(
        "/{id}",
        status_code=status.HTTP_202_ACCEPTED)
def delete_posts(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)) -> dict:
    
    # post_idx = find_post_idx(id)
    post = db.query(Posts).filter(Posts.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post ID: {id} Not Found!"
        )
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"{current_user.email} is not authorized to delete this post"
        )
    
    # my_posts.pop(post_idx)
    post.delete(synchronize_session=False)
    db.commit()
    return {"message": f"post {id} deleted!"}