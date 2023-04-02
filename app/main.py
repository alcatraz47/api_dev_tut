from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from app.model import Post
from random import randrange

app = FastAPI()

# temporarily saving the posts in an array
my_posts = [
        {"title": "title of post 1", "content": "contents of post 1", "id": 1},
        {"title": "favourite foods", "content": "I like pizza", "id": 544192463}
    ]

def find_posts(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_post_idx(id: int) -> int:
    for i, posts in enumerate(my_posts):
        if id == posts["id"]:
            return i

#path operation [according to fastapi] or route
# http methods will be maintained via decorator's function(get, post, update, delete). path is the specific domain name fo the api.
# the line below is the decoretor. this will convert the function into an actual path operation.
@app.get("/")
# this is a function for asynchronization, async is used.
async def root():
    return {"message": "Hello World"}

# the fastapi will try to find the first path so the path names need to be sequential
@app.get("/posts")
def get_posts():
    return {"data": my_posts}
        
@app.get("/posts/latest")
def get_latest():
    return {"data": my_posts[-1]}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_posts(id)
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{id} not found!")
    
    return {"data": post}
# use plurals for links/path names
@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.__dict__
    post_dict["id"] = randrange(0, 10000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_posts(id: int, post: Post) -> None:
    post_idx = find_post_idx(id)
    
    if not post_idx:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Index not found"
            )
    
    my_posts[post_idx] = post.__dict__
    my_posts[post_idx]["id"] = id

@app.delete("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def delete_posts(id: int) -> dict:
    post_idx = find_post_idx(id)

    if not post_idx:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{id} Not Found!"
        )
    
    my_posts.pop(post_idx)
    return {"message": f"post {id} deleted!"}