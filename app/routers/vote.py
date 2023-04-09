from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..models import Vote, Posts
from ..schemas.schemas import VoteBase, PostGet
# from ..schemas.vote_schema import VoteBase
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix = "/votes",
    tags = ["Votting on Post"]
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(
    vote: VoteBase,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    if not db.query(Posts).filter(Posts.id == vote.post_id).first():
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail=f"The post with id: {vote.post_id} not found."
        )
    vote_query = db.query(
            Vote).filter(
            Vote.post_id == vote.post_id,
            Vote.user_id == current_user.id)
    
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail = f"User {current_user.id} already voted on the post"
            )
        new_vote = Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "Vote does not exist"
            )
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted vote"}