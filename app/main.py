from fastapi import FastAPI

from .routers import post, user, auth, logout, vote

app = FastAPI()

# path operation [according to fastapi] or route
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
app.include_router(vote.router)
