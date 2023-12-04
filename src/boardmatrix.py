from tile import Tile

class BoardMatrix:
    def __init__(self, width = 320, height = 320):
        self.width = width
        self.height = height
        self.tiles = {}
        self.graph = []
        self.playertile = 0
        row = []
        # generates graph with no edges along with tiles
        for i in range(width * height):
            row.append(0)
            self.tiles[i] = Tile(i)
        for j in range(width * height):
            self.graph.append(row.copy())

        # adds edges to graph
        for tilenum in range(width * height):
            above = tilenum - width
            below = tilenum + width
            left = tilenum % width != 0
            right = (tilenum + 1) % width != 0 and tilenum < width * height - 1

            if above > -1:
                self.graph[tilenum][above] = 1
                self.graph[above][tilenum] = 1
            if below < height:
                self.graph[tilenum][below] = 1
                self.graph[below][tilenum] = 1
            if left:
                self.graph[tilenum][tilenum - 1] = 1
                self.graph[tilenum - 1][tilenum] = 1
            if right:
                self.graph[tilenum][tilenum + 1] = 1
                self.graph[tilenum + 1][tilenum] = 1
    
    # returns entire adjacency matrix
    def get_matrix(self):
        return self.graph
            

