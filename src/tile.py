from gpt import generate_node_events

class Tile:
    def __init__(self, identifier):
        self.identifier = identifier
        self.npcs = []
        self.hasplayer = False
    
    # placeholder until events are more fleshed out
    def gen_event(self):
        self.event = generate_node_events()
