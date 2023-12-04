extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	WorldGraph.tile_map = $TileMap
	var adjacency_list: Dictionary = {
		"0": [1, 2, 3],
		"1": [0, 4],
		"2": [0],
		"3": [0],
		"4": [1, 5],
		"5": [4, 6],
		"6": [5, 7, 8],
		"7": [6],
		"8": [],
	}
	WorldGraph.load_adjacency_list(%TileMap, adjacency_list)
	#Remote.fetch_map(%TileMap)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
