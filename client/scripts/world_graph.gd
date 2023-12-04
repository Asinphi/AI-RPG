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
var tile_map: TileMap


func set_tile_visited(tile_id: int, was_visited: bool = true) -> void:
	WorldGraph.visited_tiles[tile_id] = true
	tile_map.set_cell(1, id_to_coords[tile_id], 1, Vector2i(TILE_ICONS[get_tile_type(tile_id)], 0), 1)
	


func get_tile_type(id: int) -> TileType:
	if id == 0:
		return TileType.BLANK
	var sum: float = 0.0
	for weight: float in TILE_POOL.values():
		sum += weight
	seed(id)
	var p := randf() * sum
	sum = 0
	for possible_tile_type: TileType in TILE_POOL.keys():
		sum += TILE_POOL[possible_tile_type]
		if sum > p:
			return possible_tile_type
	return TileType.BLANK  # Unreachable


func load_adjacency_list(tile_map: TileMap, adj_list: Dictionary, origin_id := 0, 
origin_coords := Vector2i()) -> void:
	init_astar()
	
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
			


func load_2d_array(tile_map: TileMap, grid: Array, origin_id := 0,
origin_coords := Vector2i()) -> void:
	init_astar()
	var origin_r: int = origin_id / grid[0].size()
	var origin_c: int = origin_id - origin_r * grid[0].size()
	var offset := -Vector2i(origin_r, origin_c) + origin_coords
	
	for r: int in range(grid.size()):
		for c: int in range(grid[0].size()):
			var tile_id: int = int(grid[r][c])
			var coords = Vector2i(r, c) + offset
			_load_tile(tile_map, tile_id, coords)


func init_astar() -> void:
	var region_size := Vector2i(MAX_TILES / 2, MAX_TILES / 2)
	astar.diagonal_mode = AStarGrid2D.DIAGONAL_MODE_NEVER
	astar.default_compute_heuristic = AStarGrid2D.HEURISTIC_MANHATTAN
	astar.default_estimate_heuristic = AStarGrid2D.HEURISTIC_MANHATTAN
	astar.region = Rect2i(-region_size / 2, region_size)
	astar.update()
	astar.fill_solid_region(astar.region, true)


func _load_tile(tile_map: TileMap, id: int, coords: Vector2i) -> void:
	if not astar.is_in_boundsv(coords):
		return
	num_tiles += 1
	id_to_coords[id] = coords
	coords_to_id[coords] = id
	astar.set_point_solid(coords, false)
	tile_map.set_cell(0, coords, 0, Vector2i(randi_range(12, 18), 22))
	# Set tile map symbols layer, too
	var tile_type: TileType = get_tile_type(id)
	tile_types[id] = tile_type
	if tile_type != TileType.BLANK:
		tile_map.set_cell(1, coords, 1, Vector2i(TILE_ICONS[tile_type], 0))
		astar.set_point_weight_scale(coords, 15.0)

