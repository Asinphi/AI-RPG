extends Sprite2D
## Handles tile hover effects and detects click signal


@onready var tile_map: TileMap = %TileMap

var tile_coords: Vector2i  # Map coordinates of current hovered cell


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	#position = (get_global_mouse_position() / 96.0).floor() * 96 + Vector2(48, 48)
	tile_coords = tile_map.local_to_map(tile_map.get_local_mouse_position())
	position = tile_coords * 96 + Vector2i(48, 48)
	visible = tile_map.get_cell_tile_data(0, tile_coords) != null


func _unhandled_input(event: InputEvent) -> void:
	if visible and (event is InputEventMouseButton or event is InputEventScreenTouch):
		if event.pressed:
			Messenger.tile_clicked.emit(tile_coords)
