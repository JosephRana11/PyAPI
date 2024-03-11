from fastapi import FastAPI , Body
from fastapi.params import Body

app = FastAPI()

#test file only

@app.get("/")
async def root():
    return {"hello":"world "}

@app.get("/posts")
async def get_posts():
    return {"posts": ["post01", "post02"]}


@app.post("/create")
async def create_post()   :
    return {"Status" : "Post Recieved Successfully"}