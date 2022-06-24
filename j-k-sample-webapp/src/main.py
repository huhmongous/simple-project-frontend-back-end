from typing import Union
import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):

    # Get request from user
    # Determine what to do from their request parameters
    # Make your DB query
    # Process DB results
    # Return the processed results to the user


    return {"item_id": item_id, "q": q}


@app.get("/server")
def read_server():
    server_id = os.getenv('SERVER_ID')
    return {"id": server_id}
