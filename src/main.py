from fastapi import FastAPI, Request, Query, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List

from src import board
from src.board import Board
from src.boardmatrix import BoardMatrix
from src.twodarray import TwoDArray
from src.gpt import *
import random
from pydantic import BaseModel

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
def create_character(player_name: str = Query(..., title="player-name")):
    return JSONResponse(content = player_name)

@app.get("/adjacency-list")
def get_adjlist():
    board = Board()
    return JSONResponse(content=board.get_adj_list())

@app.get("/twod-array")
def get_twod_arr():
    board = TwoDArray()
    return JSONResponse(content=board.get_array())

@app.post("/enter-node")
def get_node_data(node_id: int = Query(..., title="node-id"), player_id: int = Query(..., title="player-id")):
    tile = choose_event_type(node_id)
    seed = node_id
    node_name = generate_node_name(seed)
    if(tile != "blank"):
        event = gpt_event_call(tile, seed, setting, node_name)
    else:
        event = ""
    if(tile == "treasure"):
        treasure_worth = int(gold_gained_or_lost(event))
    else:
        treasure_worth = 0
    response_data = {"node_name": node_name, "event": event, "player-id": player_id, "treasure": treasure_worth}
    return JSONResponse(content=response_data)

class Context(BaseModel):
    node_id: int = Query(..., title="node-id")
    player_id: int = Query(..., title="player-id")
    context: str

def extract_context_and_usertext(context: str):
    lines = context.split("\n")
    area = ""
    context = ""
    user_resp = ""
    for line in lines:
        if line.startswith("Area:"):
            area = line[len("Area:"):]
        elif line.startswith("Narrator:"):
            context = line[len("Narrator:"):]
        elif line.startswith("Player:"):
            user_resp = line[len("Player:"):]
    return context.strip(), user_resp.strip()


@app.post("/interact")
async def get_player_response(request: Context):
    node_context, user_response = extract_context_and_usertext(request.context)
    node_id = request.node_id
    player_id = request.player_id
    board.playertile = node_id
    tile = choose_event_type(node_id)
    seed = node_id
    if(tile != "blank"):
        response = gpt_response_call(tile, seed, setting, user_response, node_context)
    else:
        response = ""
    gold_change = int(gold_gained_or_lost(response))
    health_change = int(hp_gained_or_lost(response))
    response_data = {"player-id": player_id, "response": response, "gold_change": gold_change, "health_change": health_change}
    return JSONResponse(content=response_data)


