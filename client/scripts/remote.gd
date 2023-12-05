extends Node

const URL = "http://127.0.0.1:8000"
const USE_ADJACENCY_LIST = false  # Whether or not to use adjacency list or 2D array


func fetch_map(tile_map: TileMap) -> void:
	var request: HTTPRequest = HTTPRequest.new()
	add_child(request)
	request.request_completed.connect(_on_map_fetched.bind(tile_map))
	
	var error := request.request(URL + ("/adjacency-list" if USE_ADJACENCY_LIST else "/twod-array"))
	if error != OK:
		push_error("An error occurred in the map request: %s" % error)


func enter_tile(tile_id: int) -> void:
	var request: HTTPRequest = HTTPRequest.new()
	add_child(request)
	request.request_completed.connect(_on_tile_entered.bind(tile_id))
	
	var error = request.request("%s/enter-node?node_id=%s&player_id=%s" % [URL, tile_id, 0], [],
		HTTPClient.METHOD_POST)
	if error != OK:
		push_error("Error in entering node: %s" % error)
	print("Request sent: enter tile")


func interact(context: String, user_input: String, tile_id: int) -> void:
	var request: HTTPRequest = HTTPRequest.new()
	add_child(request)
	request.request_completed.connect(_on_interacted)
	
	var body = JSON.new().stringify({"context": context, "user_input": user_input, "player_id": 0,
		"node_id": tile_id})
	var error = request.request("%s/interact" % URL, [
		"accept: application/json",
		"Content-Type: application/json",
	], HTTPClient.METHOD_POST, body)
	if error != OK:
		push_error("Error with interacting: %s" % error)
	print("Request sent: interact")
	

func _on_map_fetched(result: int, code: int, headers: PackedStringArray, 
body: PackedByteArray, tile_map: TileMap) -> void:
	var json := JSON.new()
	json.parse(body.get_string_from_utf8())
	if USE_ADJACENCY_LIST:
		WorldGraph.load_adjacency_list(tile_map, json.get_data())
	else:
		WorldGraph.load_2d_array(tile_map, json.get_data())


func _on_tile_entered(result: int, code: int, headers: PackedStringArray, body: PackedByteArray,
tile_id: int) -> void:
	var json := JSON.new()
	json.parse(body.get_string_from_utf8())
	var data: Dictionary = json.get_data()
	print("Response received: tile entered")
	print(body.get_string_from_utf8())
	Messenger.popup_toggled_on.emit(data["node_name"], data["event"])
	

func _on_interacted(result: int, code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	var json := JSON.new()
	json.parse(body.get_string_from_utf8())
	var data: Dictionary = json.get_data()
	Messenger.ai_responded.emit(data["response"], data["gold_change"], data["health_change"])
	print("Response received, interact: %s" % result)
