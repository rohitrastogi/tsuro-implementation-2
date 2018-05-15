from player import Player
from board import Board
from tile import Tile
import copy

def legal_play(player, board, tile):
	"""
	Returns whether the tile the player wants to play is a legal move or not, considering all the tiles the player has.

	Args:
		player: instance of Player class, the player whose turn it is
		board: instance of Board class, current state of the board
		tile: instance of Tile class, the tile the player wants to play

	Returns:
		boolean. True, if the tile is a legal move. False, otherwise.
	"""

	# First, check if there is another legal move that can be played.
	another_legal = False
	for a_tile in player.tiles_owned:
		for i in range(4):
			a_tile.rotate_tile()
			if legal_play_helper(player, board, a_tile):
				another_legal = True

	# If there is another legal move, just check whether this tile causes elimination or not
	# If there is not another legal move, then this tile can be played provided it belongs to the player
	if another_legal:
		return legal_play_helper(player, board, tile)
	else:
		return player.is_tile_owned(tile)

def legal_play_helper(player, board, tile):
	"""
	Returns whether the tile the player wants to play is a legal move or not, regardless of other tiles in the player's hand.

	Args:
		player: instance of Player class, the player whose turn it is
		board: instance of Board class, current state of the board
		tile: instance of Tile class, the tile the player wants to play

	Returns:
		boolean. True, if the tile is a legal move. False, otherwise.
	"""

	# Player position is returned by the move_across_board function, but is not updated.
	player_final_position, player_final_square, hit_a_wall = board.move_across_board(player, tile)

	# If player hits a wall, this tile causes elimination and is therefore, not legal.
	if hit_a_wall:
		return False
	return player.is_tile_owned(tile)

def play_a_turn(draw_pile, players, eliminated, board, curr_tile):
	"""
	Plays the turn for the first player in the list. Following the rules of the game, the tile is placed,
	all players affected by the tile are moved across the board. Players that are eliminated lose their tiles to the deck.
	Player(s) draw(s) tiles depending on whether there are any left and whether the dragon tile is held.

	Args:
		draw_pile: a list of all tiles in the draw pile
		players: a list of Player objects, players that are still in the game
		eliminated: a list of Player objects, players that have been eliminated from the game
		board: an instance of the Board class, current state of the board
		curr_tile: an instance of the Tile class, the current tile to be placed on the board

	Returns:
		draw_pile: a list of all tiles in the draw pile after the tile has been placed
		players: an updated list of Player objects, players that are still in the game after this turn
		eliminated: an updated list of Player objects, players that have been eliminated from the game
		board: an instance of the Board class, current state of the board
		game_over: boolean. False, if the game is not over. Player object if there is a single winner.
				   A list of players if there are multiple winners, in the case that all tiles are played or all remaining
				   players get eliminated in the same turn.
	"""

	# TODO: if such a thing happens then you must boot the player and replace with random player
	# if not legal_play(players[0], board, curr_tile):
	# 	raise RuntimeError("This player is insisting on playing an incorrect tile.")

	curr_player = players.pop(0)
	players.append(curr_player)
	curr_player_color = curr_player.color

	original_square = board.get_next_board_square(curr_player.position, curr_player.square)
	original_coordinates = board.get_coordinates(original_square)
	original_players = copy.deepcopy(players)

	board.place_tile(original_square, curr_tile)
	board.move_players(players, original_coordinates, curr_tile)
	eliminated_player_pass_dragon_tile(players)
	players = eliminated_players_cleanup(players, eliminated, draw_pile)
	players_draw_tiles(players, draw_pile, curr_player_color)

	game_over = check_game_state(players, original_players, board)

	return draw_pile, players, eliminated, board, game_over

def check_game_state(players, original_players, board):
	"""
	Function that checks if the game is over or not.

	Args:
		players: a list of Player objects, players that are still in the game at this point
		original_players: a list of Player objects, players that were in the game at the start of the turn.
		board: an instance of the Board class, maintains current state of the board.

	Returns:
		False, if the game is not over. Player object if there is a single winner.
		A list of players if there are multiple winners, in the case that all tiles are played or all remaining
		players get eliminated in the same turn.

	"""
	if len(players) == 1:
		game_over = players[0]
	elif not players:
		game_over = original_players
	elif board.num_tiles == 35:
		game_over = players
	else:
		game_over = False

	return game_over

def eliminated_player_pass_dragon_tile(players):
	"""
	If, during the turn, the player that has the dragon tile gets eliminated, the dragon tile is passed on to
	the next player with less than three tiles, going clockwise.

	Args:
		players: a list of Player objects, contains both active and eliminated players (with the eliminated flag set)

	Mutates the players list with a non-eliminated player holding the dragon tile in the end, or no one has the tile.
	"""
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

def eliminated_players_cleanup(players, eliminated, draw_pile):
	"""
	Removes eliminated players from the list of active players and adds them to the eliminated list.
	Eliminated players lose their tiles to the draw pile after they have been removed.

	Args:
		players: a list of Player objects, contains both active and eliminated players (with the eliminated flag set)
		eliminated: a list of Player objects, contains those players that were eliminated before this turn.
		draw_pile: a list of Tile objects, contains the tiles before more, if any, are added.

	Returns:
		players: a list of Player objects, all eliminated players are removed.

	eliminated is mutated in place and not returned.
	"""
	for i in range(len(players)):
		if players[i].eliminated:
			eliminated.append(players[i])
			players[i].lose_tiles(draw_pile)
			players[i].dragon_held = False

	players = [x for x in players if not x.eliminated]

	return players

def players_draw_tiles(players, draw_pile, curr_player_color):
	"""
	Completes the drawing stage of the turn.
	Drawing happens in the following order:
		- If the dragon tile is not already held, then the player who just played their turn and is not eliminated
		draws a tile if there is one available, or is given the dragon tile.
		- If the dragon tile is already held, the player holding the dragon tile draws a tile if there are any and then passes
		the dragon tile to the next player with fewer than 3 tiles. If there are no tiles in the draw pile, this player retains
		the dragon tile and game play continues.

	Args:
		players: a list of Player objects, players that are still in the game at this point
		draw_pile: a list of Tile objects, all the tiles currently in the deck
		curr_player_color: the color of the player that played the turn

	Mutates the players list and the draw_pile
	"""
	dragon_already_held = False
	for i in range(len(players)):
		if players[i].dragon_held:
			dragon_already_held = True
			break

	if not dragon_already_held:
		for j in range(len(players)):
			if players[j].color == curr_player_color:
				if not players[j].eliminated:
					if len(draw_pile) == 0:
						players[j].dragon_held = True
					else:
						players[j].draw_tile(draw_pile)

	while draw_pile and dragon_already_held:
		players[i].draw_tile(draw_pile)
		players[i].dragon_held = False
		if len(players[(i+1)%len(players)].tiles_owned) < 3:
			players[(i+1)%len(players)].dragon_held = True
		else:
			dragon_already_held = False

		i = (i+1)%len(players)

def create_draw_pile():
	"""
	Creates and returns the deck with 35 unique tile objects.
	"""
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
