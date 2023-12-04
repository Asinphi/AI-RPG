from fastapi import FastAPI, Request, Query, Body
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()

app.mount("/dist", StaticFiles(directory="dist"), name="dist")

# templates = Jinja2Templates(directory="src/templates")
# Use the Vite-generated templates; the dev server view won't be parsed
templates = Jinja2Templates(directory="dist/src/templates")


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
@app.post("/enter-node", response_model="") #Make an object with event + node name?
def get_node_data():
    #Get players location, generate a node name, and an event
    return
@app.post("/interact/?node=node-id", response_model= "")
def get_player_response():
    #Get player's response to action, return node response
    return
