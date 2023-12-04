class_name LocalPlayer
extends Player


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	Messenger.tile_clicked.connect(_on_cell_clicked)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_cell_clicked(coords: Vector2i) -> void:
	move_to(coords)
