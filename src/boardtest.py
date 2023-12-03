from board import Board

board = Board(5, 5)
adjlist = board.get_near_player()
print(adjlist)