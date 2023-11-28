import openai


#TODO: Re-do the below function to make more sense in the game (i.e, make sure events/NPCs tie back to each other)


def generate_node_events():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Describe an event for a player to respond to in a fantasy role-playing game",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()


def generate_npc():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Describe a NPC in a fantasy role-playing game for the player to meet and interact with",
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()