import openai

openai.api_key = 'KEY'

def openai_response_call(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

#Generate a setting for the RPG
def generate_setting():
    fullprompt=f"Give a short description of a fantasy setting for a role-playing game, " \
            f"wherein a character has just entered an area",
    return openai_response_call(fullprompt)

#Generate an event for the player to respond to
def generate_node_events(context="", setting=""):
    if context:
        fullprompt = f"Describe an event for a player to respond to in a fantasy role-playing game " \
                     f"with the context that {context} and in the following setting, {setting}"
    else:
        fullprompt = f"Describe an event for a player to respond to in a fantasy role-playing game " \
                     f"in the following setting, {setting}"

        return openai_response_call(fullprompt)


#Generate an NPC for the player to interact with
def generate_npc(context = "", setting = ""):
    if context:
        fullprompt = f"Briefly describe a NPC in a fantasy role-playing game for the player to meet " \
                     f"and interact with, using the context that {context} and in the following setting, {setting}"
    else:
        fullprompt = f"Briefly describe a NPC in a fantasy role-playing game for the player to meet " \
                     f"and interact with in the following setting, {setting}"
    return openai_response_call(fullprompt)

#Generate a monster for the player to encounter
def generate_monster(setting = ""):
    fullprompt = f"Give a short description of a hostile monster in a fantasy role-playing game for the player " \
                 f"to fight and interact with in the following setting, {setting}"
    return openai_response_call(fullprompt)

def generate_NPC_response(context = "", setting = "", action = ""):
    fullprompt = f"Generate the NPC's response to the player's action of {action}, using the context " \
                 f"that {context} and in the following setting, {setting}"
    return openai_response_call(fullprompt)


def generate_monster_response(context = "", setting = "", action = ""):
    fullprompt = f"Generate the monster's response to the player's action of {action}, using " \
                 f"the context that {context} and in the following setting, {setting}. If the monster's response is" \
                f"an attack, generate a value between -2 and 2 to represent health lost by the player"
    return openai_response_call(fullprompt)

def generate_node_name(setting = ""):
    fullprompt = f"Generate a short name for a fantasy location using the following setting, {setting}",
    return openai_response_call(fullprompt)

def generate_value(item_name = ""):
    fullprompt = f"Generate a price for the following item, {item_name}",
    return openai_response_call(fullprompt)
