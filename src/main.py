from fastapi import FastAPI, Request, Query, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from src.board import Board
from src.boardmatrix import BoardMatrix
from src.twodarray import TwoDArray
from src.gpt import *
import random

app = FastAPI()

app.mount("/dist", StaticFiles(directory="dist"), name="dist")

# templates = Jinja2Templates(directory="src/templates")
# Use the Vite-generated templates; the dev server view won't be parsed
templates = Jinja2Templates(directory="dist/src/templates")

setting = generate_setting()

def render_template(path: str, request: Request, **kwargs):
    return templates.TemplateResponse(path, {"request": request, **kwargs})


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return render_template("index.html", request)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/create-character")
def create_character():
    return

@app.get("/map", response_model=List[int])
def get_map():
    #BFS, variable for depth, player_location, and graph itself
    return
@app.post("/enter-node")
def get_node_data(node_id: int = Query(..., title="Node ID"), player_id: int = Query(..., title="Player ID")):
    tile = choose_event_type(node_id)
    seed = node_id
    node_name = generate_node_name(seed)
    if(tile != "blank"):
        event = gpt_call(tile, seed, setting, node_name,)
    else:
        event = ""
    response_data = {"node_name": node_name, "event": event, "player-id": player_id}
    return JSONResponse(content=response_data)
@app.post("/interact")
def get_player_response():
    #Get player's response to action, return node response
    return

@app.get("/adjacency-list")
def get_adjlist():
    board = Board()
    return JSONResponse(content=board.get_adj_list())

@app.get("/twod-array")
def get_twod_arr():
    board = TwoDArray()
    return JSONResponse(content=board.get_array())
