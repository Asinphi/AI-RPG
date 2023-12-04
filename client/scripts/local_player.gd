class_name LocalPlayer
extends Player

signal health_changed(new_health: int)

@export var health: int = 7:
	get:
		return health
	set(value):
		health = clamp(value, 0, max_health)
		health_changed.emit(value)
		
@export var max_health: int = 7:
	get:
		return max_health
	set(value):
		max_health = value
		health = min(health, max_health)


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	Common.local_player = self
	Messenger.tile_clicked.connect(_on_cell_clicked)
	tile_reached.connect(_on_tile_reached)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_cell_clicked(coords: Vector2i) -> void:
	move_to(coords)


func _on_tile_reached(tile_id: int) -> void:
	if not WorldGraph.visited_tiles.get(tile_id) \
	and WorldGraph.tile_types[tile_id] != WorldGraph.TileType.BLANK:
		position_tween.kill()
		animation_player.stop()
		animation_player.play("RESET")
		WorldGraph.set_tile_visited(tile_id)
		Remote.enter_tile(tile_id)
