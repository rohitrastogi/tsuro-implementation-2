from player import Player
from board import Board
from tile import Tile
import copy

def legal_play(player, board, curr_tile):
	another_legal = False  # is there another legal tile that can be played?
	for tile in player.tiles_owned:
		for i in range(4):
			tile.rotate_tile()
			if legal_play_helper(player, board, tile):
				another_legal = True
	if another_legal:
		return legal_play_helper(player,board,curr_tile)
	else:
		return player.is_tile_owned(curr_tile)

def legal_play_helper(player, board, curr_tile):
	end_position, end_board_position, hit_a_wall = board.move_across_board(player, curr_tile)
	if hit_a_wall:
		return False
	return player.is_tile_owned(curr_tile)

def play_a_turn(draw_pile, players, eliminated, board, curr_tile):
	"""
	plays the turn for the first player in the list of players and curr_tile is the tile to be played
	"""
	# TODO modify board fields for alive and eliminated

	# TODO: if such a thing happens then you must boot the player and replace with random player
	# if not legal_play(players[0], board, curr_tile):
	# 	raise RuntimeError("This player is insisting on playing an incorrect tile.")
	# Remove later once whole game is implemented
	for p in eliminated:
		p.eliminated = True

	curr_player = players.pop(0)
	players.append(curr_player)
	curr_player_color = curr_player.color

	original_board_position = board.get_next_board_space(curr_player.position, curr_player.square)
	original_coordinates = board.get_coordinates(original_board_position)
	original_players = copy.deepcopy(players)

	board.place_tile(original_board_position, curr_tile)
	# board.tiles[original_board_position[0]][original_board_position[1]] = curr_tile
	board.num_tiles += 1

	# print ("Line 49")
	for player in players:
		if not player.eliminated:
			if player.position in original_coordinates:
				end_position, end_board_position, hit_a_wall = board.move_across_board(player, curr_tile)
				player.update_position(end_position, end_board_position)
				if hit_a_wall:
					player.eliminated = True
	# print ("Line 57")
	for i in range(len(players)):
		if players[i].dragon_held and players[i].eliminated:
			j = (i+1)%len(players)
			count = 1
			while count < len(players):
				if not players[j].eliminated:
					if len(players[j].tiles_owned) < 3:
						players[j].dragon_held = True
						break
					else:
						j = (j+1)%len(players)
				count += 1
			players[i].dragon_held = False
			break
	# print ("Line 72")
	for i in range(len(players)):
		if players[i].eliminated:
			eliminated.append(player)
			players[i].lose_tiles(draw_pile)
			players[i].dragon_held = False

	players = [x for x in players if not x.eliminated]

	dragon_already_held = False
	# print ("Line 82")
	for i in range(len(players)):
		if players[i].dragon_held:
			dragon_already_held = True
			break

	# print ("Line 88")
	while draw_pile and dragon_already_held:
		players[i].draw_tile(draw_pile)
		players[i].dragon_held = False
		if len(players[(i+1)%len(players)].tiles_owned) < 3:
			players[(i+1)%len(players)].dragon_held = True
		else:
			dragon_already_held = False

		i = (i+1)%len(players)

	# print ("Line 99")
	if not dragon_already_held:
		for j in range(len(players)):
			if players[j].color == curr_player_color:
				if not players[j].eliminated:
					if len(draw_pile) == 0:
						players[j].dragon_held = True
					else:
						players[j].draw_tile(draw_pile)

	# print ("Line 109")
	#  Game over scenarios!
	if len(players) == 1:
		game_over = players[0]
	elif not players:
		game_over = original_players
	elif board.num_tiles == 35:
		game_over = players
	else:
		game_over = False

	return draw_pile, players, eliminated, board, game_over

def create_draw_pile():
	draw_pile = []

	unique_tiles = [[[0, 1], [2, 3], [4, 5], [6, 7]], \
					[[0, 1], [2, 4], [3, 6], [5, 7]], \
					[[0, 6], [1, 5], [2, 4], [3, 7]], \
					[[0, 5], [1, 4], [2, 7], [3, 6]], \
					[[0, 2], [1, 4], [3, 7], [5, 6]], \
					[[0, 4], [1, 7], [2, 3], [5, 6]], \
					[[0, 1], [2, 6], [3, 7], [4, 5]], \
					[[0, 2], [1, 6], [3, 7], [4, 5]], \
					[[0, 4], [1, 5], [2, 6], [3, 7]], \
					[[0, 1], [2, 7], [3, 4], [5, 6]], \
					[[0, 2], [1, 7], [3, 4], [5, 6]], \
					[[0, 3], [1, 5], [2, 7], [4, 6]], \
					[[0, 4], [1, 3], [2, 7], [5, 6]], \
					[[0, 3], [1, 7], [2, 6], [4, 5]], \
					[[0, 1], [2, 5], [3, 6], [4, 7]], \
					[[0, 3], [1, 6], [2, 5], [4, 7]], \
					[[0, 1], [2, 7], [3, 5], [4, 6]], \
					[[0, 7], [1, 6], [2, 3], [4, 5]], \
					[[0, 7], [1, 2], [3, 4], [5, 6]], \
					[[0, 2], [1, 4], [3, 6], [5, 7]], \
					[[0, 7], [1, 3], [2, 5], [4, 6]], \
					[[0, 7], [1, 5], [2, 6], [3, 4]], \
					[[0, 4], [1, 5], [2, 7], [3, 6]], \
					[[0, 1], [2, 4], [3, 5], [6, 7]], \
					[[0, 2], [1, 7], [3, 5], [4, 6]], \
					[[0, 7], [1, 5], [2, 3], [4, 6]], \
					[[0, 4], [1, 3], [2, 6], [5, 7]], \
					[[0, 6], [1, 3], [2, 5], [4, 7]], \
					[[0, 1], [2, 7], [3, 6], [4, 5]], \
					[[0, 3], [1, 2], [4, 6], [5, 7]], \
					[[0, 3], [1, 5], [2, 6], [4, 7]], \
					[[0, 7], [1, 6], [2, 5], [3, 4]], \
					[[0, 2], [1, 3], [4, 6], [5, 7]], \
					[[0, 5], [1, 6], [2, 7], [3, 4]], \
					[[0, 5], [1, 3], [2, 6], [4, 7]]]

	for i, paths in enumerate(unique_tiles):
		draw_pile.append(Tile(i, paths))

	return draw_pile
