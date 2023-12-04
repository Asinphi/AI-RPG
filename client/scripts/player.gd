class_name Player
extends Sprite2D


signal tile_reached(tile_id: int)


const SPEED := 2.0  # In tiles per second


var username: String
var tile_coords: Vector2i  = Vector2i(0, 0) # Map coordinates of current tile
var tile_id := 0  # id of current tile

var _last_move_queued: float


@onready var position_tween: Tween
@onready var animation_player: AnimationPlayer = $AnimationPlayer


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	position = tile_coords * 96


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func move_to(destination_coords: Vector2i) -> void:
	var path: Array[Vector2i] = WorldGraph.astar.get_id_path(tile_coords, destination_coords)
	if position_tween and position_tween.is_running():
		var now := Time.get_ticks_msec()
		_last_move_queued = now
		await tile_reached
		if now != _last_move_queued:
			return
		position_tween.kill()
	position_tween = get_tree().create_tween().bind_node(self)
	for point: Vector2i in path.slice(1):
		var waypoint_pos := point * 96.0 + Vector2(48, 48)
		position_tween.tween_callback(func() -> void:
			var direction := (point - tile_coords).sign()
			tile_coords = point
			match direction:
				Vector2i(1, 0):  # right
					flip_h = false
					animation_player.play("walk_side")
					animation_player.advance(0)
				Vector2i(-1, 0):  # left
					flip_h = true
					animation_player.play("walk_side")
					animation_player.advance(0)
				Vector2i(0, 1):  # down
					animation_player.play("walk_down")
				Vector2i(0, -1):  # up
					animation_player.play("walk_up")
		)
		position_tween.tween_property(self, "position", waypoint_pos,
			1 / SPEED)
		position_tween.tween_callback(func() -> void:
			tile_reached.emit(WorldGraph.coords_to_id[point])
		)
	position_tween.tween_callback(func() -> void:
		animation_player.stop()
		animation_player.play("RESET")
	)
