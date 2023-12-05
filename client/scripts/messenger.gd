extends Node

signal tile_clicked(coords: Vector2i)
signal popup_toggled_on(title: String, desc: String)
signal popup_toggled_off
signal ai_responded(response: String, delta_gold: int, delta_health: int)
