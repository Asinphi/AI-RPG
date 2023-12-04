extends Camera2D

var target_offset := Vector2()

@onready var player: LocalPlayer = %LocalPlayer


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	position = player.position


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	position = position.lerp(player.position + target_offset, 1.0 * delta)
