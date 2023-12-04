from openai import OpenAI
from fastapi.responses import JSONResponse
import random
import math


client = OpenAI(
    api_key=""
)

def choose_event_type(node_id):
    TILE_POOL = {
            'mystery': 15,
            'event': 40,
            # 'merchant': 10,
            'monster': 30,
            'treasure': 5,
            'blank': 100
        }

    tile_type = ''
    # Then do basic algorithm for weighted probability
    weight_sum = 0
    for weight in TILE_POOL.values():
        weight_sum += weight
    random.seed(node_id)
    p = random.random() * weight_sum
    weight_sum = 0
    for possible_tile_type, weight in TILE_POOL.items():
        weight_sum += weight
        if weight_sum > p:
            tile_type = possible_tile_type
            break
    return possible_tile_type



def openai_response_call(prompt):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are generating things for a fantasy RPG"},
            {"role": "assistant", "content": prompt}
        ],
        model="gpt-3.5-turbo-1106",
    )
    data = response.choices[0].message.content
    return data

#Generate a setting for the RPG
def generate_setting():
    fullprompt=f"Give a short description of a fantasy setting for a role-playing game, " \
            f"wherein a character has just entered an area"
    return openai_response_call(fullprompt)

#Generate an event for the player to respond to given a setting, location, and maybe context
def generate_node_events(seed ,context="", setting="", place_name = ""):
    if context:
        fullprompt = f"Describe an event for a player to respond to in a fantasy role-playing game " \
                     f"with the context that {context} and in the following setting, {setting}, using the seed" \
                     f"{seed}, with the event location being called {place_name}"
    else:
        fullprompt = f"Describe an event for a player to respond to in a fantasy role-playing game " \
                     f"in the following setting, {setting}, using the seed" \
                     f"{seed}, with the event location being called {place_name}"

    return openai_response_call(fullprompt)


#Generate an NPC for the player to interact with
def generate_npc(seed, context="", setting=""):
    if context:
        fullprompt = f"Briefly describe a NPC in a fantasy role-playing game for the player to meet " \
                     f"and interact with, using the context that {context} and in the following setting, {setting}," \
                     f"using the following seed, {seed}"
    else:
        fullprompt = f"Briefly describe a NPC in a fantasy role-playing game for the player to meet " \
                     f"and interact with in the following setting, {setting}, using the following seed, {seed}"
    return openai_response_call(fullprompt)

#Generate a monster for the player to encounter given a seed and setting
def generate_monster(seed, place_name, setting = ""):
    fullprompt = f"Give a short description of a hostile monster in a fantasy role-playing game for the player " \
                 f"to fight and interact with in the following setting, {setting}, using the following seed," \
                 f"{seed}, at the following location {place_name}"
    return openai_response_call(fullprompt)

def generate_NPC_response(seed,context = "", setting = "", action = ""):
    fullprompt = f"Generate the NPC's response to the player's action of {action}, using the context " \
                 f"that {context} and in the following setting, {setting}, using the following seed, {seed}"
    return openai_response_call(fullprompt)


def generate_monster_response(context = "", setting = "", action = ""):
    fullprompt = f"Generate the monster's response to the player's action of {action}, using " \
                 f"the context that {context} and in the following setting, {setting}. If the monster's response is" \
                f"an attack, generate a value between -2 and 2 to represent health lost by the player"
    return openai_response_call(fullprompt)

#Generate the name of a fantaasy location given an integer to be used as the seed
def generate_node_name(seed, setting = ""):
    fullprompt = f"Generate a short name for a fantasy location using the following setting, {setting}" \
                 f"and the seed, {seed}"
    return openai_response_call(fullprompt)

def generate_value(item_name = ""):
    fullprompt = f"Generate a price for the following item, {item_name}"
    return openai_response_call(fullprompt)

def gpt_call(tile, seed, setting, node_name, context=""):
    if(tile == "mystery"):
        tile = ("event", "monster", "treasure")[math.floor(random.random() * 3)]
    if(tile == "event"):
        return generate_node_events(seed,context, setting, node_name)
    elif(tile == "monster"):
        return generate_monster(seed, node_name, setting)
    elif(tile == "treasure"):
        #generate a treasure item?
        return