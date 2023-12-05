extends Camera2D

var target_offset := Vector2()

@onready var player: LocalPlayer = %LocalPlayer


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	position = player.position
	Messenger.popup_toggled_on.connect(_on_popup_toggled_on)
	Messenger.popup_toggled_off.connect(_on_popup_toggled_off)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	position = position.lerp(player.position + target_offset, 1.0 * delta)


func _on_popup_toggled_on(title: String, desc: String) -> void:
	target_offset = Vector2(-150, 0)


func _on_popup_toggled_off() -> void:
	target_offset = Vector2(0, 0)
