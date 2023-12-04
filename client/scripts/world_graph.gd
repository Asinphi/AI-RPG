extends Node

enum TileType {MYSTERY, EVENT, MERCHANT, MONSTER, TREASURE, BLANK}

const DIRECTIONS: Array[Vector2i] = [Vector2i(1, 0), Vector2i(-1, 0), Vector2i(0, 1), Vector2i(0, -1)]
const MAX_TILES := 1000
const TILE_POOL: Dictionary = {
	TileType.MYSTERY: 15,
	TileType.EVENT: 40,
	#TileType.MERCHANT: 10,
	TileType.MONSTER: 30,
	TileType.TREASURE: 5,
	TileType.BLANK: 100,
}
const TILE_ICONS: Dictionary = {
	TileType.MYSTERY: 0,
	TileType.EVENT: 1,
	TileType.MERCHANT: 0,
	TileType.MONSTER: 2,
	TileType.TREASURE: 3,
}

var astar: AStarGrid2D = AStarGrid2D.new()
var num_tiles: int = 0
var id_to_coords: Dictionary = {}  # Maps tile IDs to positions
var coords_to_id: Dictionary = {}
var visited_tiles: Dictionary = {}  # Tile IDs to bools, whether player has visited
var tile_types: Dictionary = {}  # Tile IDs to TileTypes


func _ready() -> void:
	await Common.local_player_set
	Common.local_player.tile_reached.connect(_on_tile_reached)


func load_adjacency_list(tile_map: TileMap, adj_list: Dictionary, origin_id := 0, 
origin_coords := Vector2i()) -> void:
	var region_size := Vector2i(MAX_TILES / 2, MAX_TILES / 2)
	astar.diagonal_mode = AStarGrid2D.DIAGONAL_MODE_NEVER
	astar.default_compute_heuristic = AStarGrid2D.HEURISTIC_MANHATTAN
	astar.default_estimate_heuristic = AStarGrid2D.HEURISTIC_MANHATTAN
	astar.region = Rect2i(-region_size / 2, region_size)
	astar.update()
	astar.fill_solid_region(astar.region, true)
	
	var q := [origin_id]
	_load_tile(tile_map, origin_id, origin_coords)
	num_tiles = 1
	while not q.is_empty() and num_tiles < MAX_TILES:
		var tile_id: int = q.pop_front()
		var coords: Vector2i = id_to_coords[tile_id]
		var neighbors: Array = adj_list[str(tile_id)]
		for i in range(neighbors.size()):
			var neighbor_id: int = int(neighbors[i])
			if not id_to_coords.get(neighbor_id):
				var neighbor_coords: Vector2i = coords + DIRECTIONS[i]
				_load_tile(tile_map, neighbor_id, neighbor_coords)
				q.append(neighbor_id)
			


func load_adjacency_matrix(tile_map: TileMap, adj_matrix: Array[Array]) -> void:
	pass


func _load_tile(tile_map: TileMap, id: int, coords: Vector2i) -> void:
	num_tiles += 1
	id_to_coords[id] = coords
	coords_to_id[coords] = id
	astar.set_point_solid(coords, false)
	tile_map.set_cell(0, coords, 0, Vector2i(randi_range(12, 18), 22))
	# Set tile map symbols layer, too
	var tile_type: TileType
	var sum: float = 0.0
	for weight: float in TILE_POOL.values():
		sum += weight
	seed(id)
	var p := randf() * sum
	sum = 0
	for possible_tile_type: TileType in TILE_POOL.keys():
		sum += TILE_POOL[possible_tile_type]
		if sum > p:
			tile_type = possible_tile_type
			break
	tile_types[id] = tile_type
	if tile_type != TileType.BLANK:
		tile_map.set_cell(1, coords, 1, Vector2i(TILE_ICONS[tile_type], 0))
		astar.set_point_weight_scale(coords, 10.0)


func _on_tile_reached(tile_id: int):
	visited_tiles[tile_id] = true
