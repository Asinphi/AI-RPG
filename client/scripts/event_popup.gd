extends Control

@onready var overlay: Control = %Overlay
@onready var title_label: Label = %Title
@onready var desc_label: RichTextLabel = %Description
@onready var text_edit: TextEdit = %TextEdit
@onready var submit_btn: Button = %SubmitButton
@onready var panel: PanelContainer = %PanelContainer


var _is_event_finished: bool = false


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	Messenger.popup_toggled_on.connect(_on_popup_toggled)
	submit_btn.pressed.connect(_on_submitted)
	Messenger.ai_responded.connect(_on_ai_responded)
	overlay.gui_input.connect(_on_overlay_pressed)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_popup_toggled(title: String, desc: String):
	title_label.text = title
	desc_label.text = desc
	panel.anchor_left -= 0.5
	panel.anchor_right -= 0.5
	visible = true
	var tween := get_tree().create_tween().bind_node(self).set_parallel(true)
	tween.set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
	tween.tween_property(panel, "anchor_left", .05, 0.5)
	tween.tween_property(panel, "anchor_right", 0.45, 0.5)
	#get_tree().paused = true
	submit_btn.disabled = false
	text_edit.editable = true


func _on_submitted():
	var context := "Area:%s\n\nNarrator:\n%s"
	var user_input := "Player: %s" % text_edit.text
	Remote.interact(context % [title_label.text, desc_label.text], user_input,
		WorldGraph.coords_to_id[Common.local_player.tile_coords])
	submit_btn.disabled = true
	text_edit.editable = false
	text_edit.text = ""
	desc_label.text += "\n\n[color=orange]%s[/color]" % text_edit.text


func _on_ai_responded(response: String, delta_gold: int, delta_health: int):
	desc_label.text += "\n\n%s" % response
	Common.local_player.health += delta_health
	Common.local_player.gold += delta_gold
	_is_event_finished = true


func _on_overlay_pressed(event: InputEvent):
	if not _is_event_finished:
		return
	if (event is InputEventMouseButton or event is InputEventScreenTouch) and event.pressed:
		_is_event_finished = false
		var tween := get_tree().create_tween().bind_node(self).set_parallel(true)
		tween.set_trans(Tween.TRANS_BOUNCE).set_ease(Tween.EASE_IN)
		tween.tween_property(panel, "anchor_left", panel.anchor_left - 0.5, 0.5)
		tween.tween_property(panel, "anchor_right", panel.anchor_right - 0.5, 0.5)
		tween.chain().tween_callback(func() -> void:
			visible = false
		)
		get_tree().paused = false
		Messenger.popup_toggled_off.emit()
