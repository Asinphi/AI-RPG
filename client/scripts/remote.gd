extends Node

const URL = "http://localhost:8000"
const USE_ADJACENCY_LIST = false  # Whether or not to use adjacency list or 2D array


func fetch_map(tile_map: TileMap) -> void:
	var request := HTTPRequest.new()
	request.request_completed.connect(_on_map_fetched.bind(tile_map))
	
	var error := request.request(URL + ("/adjacency-list" if USE_ADJACENCY_LIST else "/twod-array"))
	if error != OK:
		push_error("An error occurred in the map request: %s", error)


func enter_tile(tile_id: int) -> void:
	var request := HTTPRequest.new()
	

func _on_map_fetched(result: int, response_code: int, headers: PackedStringArray, 
body: PackedByteArray, tile_map: TileMap) -> void:
	var json := JSON.new()
	json.parse(body.get_string_from_utf8())
	if USE_ADJACENCY_LIST:
		WorldGraph.load_adjacency_list(tile_map, json.get_data())
	else:
		WorldGraph.load_2d_array(tile_map, json.get_data())
