extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	#var adjacency_list: Array[Array] = [
		#[1, 2, 3],
		#[0, 4],
		#[0],
		#[0],
		#[1, 5],
		#[4, 6],
		#[5, 7, 8],
		#[6],
		#[],
	#]
	#WorldGraph.load_adjacency_list(%TileMap, adjacency_list)
	Remote.fetch_map(%TileMap)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
