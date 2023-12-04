extends Node


signal local_player_set(value: LocalPlayer)


var local_player: LocalPlayer:
	get:
		return local_player
	set(value):
		local_player = value
		local_player_set.emit(value) 
