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



def openai_response_call(prompt, seed_num=0):
    response = client.chat.completions.create(
        temperature = 0.7,
        n = 1,
        stop=None,
        seed = seed_num,
        max_tokens=300,
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
    fullprompt=f"In 100 words or less, give a short description of a fantasy setting for a role-playing game, " \
               f"wherein a character has just entered an area"
    return openai_response_call(fullprompt)

#Generate an event for the player to respond to given a setting, location, and maybe context
def generate_node_events(seed ,context="", setting="", place_name = ""):
    if context:
        fullprompt = f"In 100 words or less, describe an event for a player to respond to in a fantasy role-playing game " \
                     f"with the context that {context} and in the following setting, {setting}," \
                     f" with the event location being called {place_name}. Do this in 100 words or less"
    else:
        fullprompt = f"In 100 words or less, describe an event for a player to respond to in a fantasy role-playing game " \
                     f"in the following setting, {setting}," \
                     f" with the event location being called {place_name}. Do this in 100 words or less"

    return openai_response_call(fullprompt, seed)


#Generate an NPC for the player to interact with
def generate_npc(seed, context="", setting=""):
    if context:
        fullprompt = f"Briefly describe a NPC in a fantasy role-playing game for the player to meet " \
                     f"and interact with, using the context that {context} and in the following setting, {setting}"
    else:
        fullprompt = f"Briefly describe a NPC in a fantasy role-playing game for the player to meet " \
                     f"and interact with in the following setting, {setting}"
    return openai_response_call(fullprompt, seed)

#Generate a monster for the player to encounter given a seed and setting
def generate_monster(seed, place_name, setting = ""):
    fullprompt = f"In 100 words or less, give a short description of a hostile monster in a fantasy role-playing game for the player " \
                 f"to fight and interact with in the following setting, {setting}," \
                 f" at the following location {place_name}. Do this in 100 words or less"
    return openai_response_call(fullprompt, seed)

def generate_NPC_response(seed,context = "", setting = "", action = ""):
    fullprompt = f"In 100 words or less, generate the NPC's response to the player's action of {action}, using the context " \
                 f"that {context} and in the following setting, {setting}."
    return openai_response_call(fullprompt, seed)


def generate_monster_response(context = "", setting = "", action = ""):
    fullprompt = f"In 100 words or less, generate the monster's response to the player's action of {action}, using " \
                 f"the context that {context} and in the following setting, {setting}. Do this in 100 words or less"
    return openai_response_call(fullprompt)

#Generate the name of a fantaasy location given an integer to be used as the seed
def generate_node_name(seed, setting = ""):
    fullprompt = f"Generate a short two word name for a fantasy location using the following setting, {setting}"
    return openai_response_call(fullprompt, seed)

def generate_treasure(setting):
    fullprompt = f"In 100 words or less, generate and describe a rare treasure for the player of a fantasy rpg to find using the following"\
                 f" setting, {setting}. Do this in 100 words or less"
    return openai_response_call(fullprompt)

def generate_node_response(seed, context="", setting="", action=""):
    fullprompt = f"In 100 words or less, generate a response to the player's action of {action}, with the context that {context}, and"\
                 f"in the following setting, {setting}. Do this in 100 words or less"
    return openai_response_call(fullprompt, seed)

def gpt_event_call(tile, seed, setting, node_name, context=""):
    if(tile == "mystery"):
        tile = ("event", "monster", "treasure")[math.floor(random.random() * 3)]
    if(tile == "event"):
        return generate_node_events(seed, context, setting, node_name)
    elif(tile == "monster"):
        return generate_monster(seed, node_name, setting)
    elif(tile == "treasure"):
        return generate_treasure(setting)

def gpt_response_call(tile, seed, setting, user_response, node_context=""):
    if(tile == "event"):
        return generate_node_response(seed, context=node_context, setting=setting, action = user_response)
    elif(tile == "monster"):
        return generate_monster_response(context=node_context, setting=setting, action=user_response)

def hp_gained_or_lost(gpt_response):
    fullprompt = f"Using the context of {gpt_response}, generate an integer number between -2 and 2" \
                 f"to represent the amount of health lost or gained by a player, if applicable, meaning there was an"\
                 f" event such as a successful attack or healing. If the player is not harmed, such as when simply traversing" \
                 f" or successfully dodges a monster's attack, generate 0. If the player is harmed, such as being successfully" \
                 f" harmed by another being or falling, generate a negative number. If the player is helped, such as by eating" \
                 f", healing themselves, or resting, generate a positive number. Only generate an integer, nothing else"
    return openai_response_call(fullprompt)

def gold_gained_or_lost(gpt_response):
    fullprompt = f"Using the context of {gpt_response}, generate an integer number to represent an amount of gold" \
                 f" lost or gained by the player, if applicable, meaning there was an event similar to events such as"\
                 f" as thieves attacking, or finding a bag of gold or treasure. If the player is not robbed, or does" \
                 f" does not find anything, generate 0. If the player is robbed, such as being attacked by bandits or" \
                 f"loses some items, generate a negative number. If the player finds treasure or picks up various items," \
                 f"generate a positive number. Only generate an integer, nothing else such as units"
    return openai_response_call(fullprompt)