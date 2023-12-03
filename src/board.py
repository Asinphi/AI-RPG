from tile import Tile

class Board:
    # graph implementation using an adjacency list
    def __init__(self, width, height):
        self.width = width
        self.heigh = height
        self.tiles = {}
        self.graph = {}
        self.playertile = str(height // 2) + "0" + str(width // 2)
        identifier = ""
        for i in range(height):
            for j in range(width):
                identifier = str(i) + "0" + str(j)
                self.tiles[identifier] = Tile(identifier)
                self.graph[identifier] = []

                for m in range(max(0, i - 1), min(i + 2, height)):
                    for n in range(max(0, j - 1), min(j + 2, width)):
                        self.graph[identifier].append(str(m) + "0" + str(n))
                self.graph[identifier].remove(identifier)

    # print adjacency list (for testing)
    def printadjlist(self):
        for tile in self.graph:
            print(tile + ": ")
            print(self.graph[tile])
            print()
    
    def move_player(self, identifier):
        self.tiles[self.playertile].hasplayer = False
        self.playertile = identifier
        self.tiles[identifier].hasplayer = True

    # returns an adjacency list of all the tiles within a set radius of the player
    def get_near_player(self, range = 30):
        adjlist = {}
        added = set()
        self.get_tiles(self.playertile, range, 0, adjlist, added)
        return adjlist

    def get_tiles(self, identifier, range, level, adjlist, added):
        if identifier not in added:
            adjlist[identifier] = self.graph[identifier]
            added.add(identifier)
            if (level < range):
                for tile in self.graph[identifier]:
                    self.get_tiles(tile, range, level + 1, adjlist, added)
    
