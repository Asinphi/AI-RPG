extends Control

@onready var hearts_container: HBoxContainer = $HeartsContainer

var _empty_heart: Texture2D = preload("res://sprites/empty_heart.png")
var _filled_heart: Texture2D = preload("res://sprites/filled_heart.png")


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	Common.local_player.health_changed.connect(_on_health_changed)
	_on_health_changed(Common.local_player.health)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_health_changed(health: int):
	var max_health := Common.local_player.max_health
	while hearts_container.get_child_count() < max_health:
		hearts_container.add_child(hearts_container.get_child(0).duplicate())
	while hearts_container.get_child_count() > max_health:
		hearts_container.remove_child(hearts_container.get_child(0))
	for i in range(hearts_container.get_child_count()):
		hearts_container.get_child(i).texture = _filled_heart if i <= health else _empty_heart
