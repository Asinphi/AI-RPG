extends Node

const URL = "http://localhost:8000"


func fetch_map(tile_map: TileMap) -> void:
	var request := HTTPRequest.new()
	add_child(request)
	request.request_completed.connect(_on_map_fetched.bind(tile_map))
	
	var error := request.request(URL + "/adjacency-list")
	if error != OK:
		push_error("An error occurred in the map request: %s", error)


func enter_tile() -> void:
	pass
	

func _on_map_fetched(result: int, response_code: int, headers: PackedStringArray, 
body: PackedByteArray, tile_map: TileMap) -> void:
	var json := JSON.new()
	json.parse(body.get_string_from_utf8())
	WorldGraph.load_adjacency_list(tile_map, json.get_data())
