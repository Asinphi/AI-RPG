import openai

openai.api_key = 'KEY'

#Generate a setting for the RPG
def generate_setting():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Give a short description of a fantasy setting for a role-playing game, "
               f"wherein a character has just entered an area",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    setting = response.choices[0].text.strip()
    return setting

#Generate an event for the player to respond to
def generate_node_events(context="", setting=""):
    if context:
        fullprompt = f"Describe an event for a player to respond to in a fantasy role-playing game " \
                     f"with the context that {context} and in the following setting, {setting}"
    else:
        fullprompt = f"Describe an event for a player to respond to in a fantasy role-playing game " \
                     f"in the following setting, {setting}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= fullprompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].text.strip()


#Generate an NPC for the player to interact with
def generate_npc(context = "", setting = ""):
    if context:
        fullprompt = f"Briefly describe a NPC in a fantasy role-playing game for the player to meet " \
                     f"and interact with, using the context that {context} and in the following setting, {setting}"
    else:
        fullprompt = f"Briefly describe a NPC in a fantasy role-playing game for the player to meet " \
                     f"and interact with in the following setting, {setting}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=fullprompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

#Generate a monster for the player to encounter
def generate_monster(setting = ""):
    fullprompt = f"Give a short description of a hostile monster in a fantasy role-playing game for the player " \
                 f"to fight and interact with in the following setting, {setting}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= fullprompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def generate_NPC_response(context = "", setting = "", action = ""):
    fullprompt = f"Generate the NPC's response to the player's action of {action}, using the context " \
                 f"that {context} and in the following setting, {setting}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=fullprompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


def generate_monster_response(context = "", setting = "", action = ""):
    fullprompt = f"Generate the monster's response to the player's action of {action}, using " \
                 f"the context that {context} and in the following setting, {setting}"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=fullprompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def generate_node_name(setting = ""):
    fullprompt = f"Generate a short name for a fantasy place using the following setting, {setting}",
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=fullprompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def generate_value(item_name = ""):
    fullprompt = f"Generate a price, in terms of gold, for the following item, {item_name}",
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=fullprompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()
