from player import Player
from board import Board
from tile import Tile
import copy


def legal_play(player, board, curr_tile):
	flag = False
	for tile in player.tiles_owned:
		for i in range(4):
			tile.rotate_tile()
			if legal_play_helper(player, board, tile):
				flag = True
	if flag:
		return legal_play_helper(player,board,curr_tile)
	else:
		for a_tile in player.tiles_owned:
			if a_tile.identifier == curr_tile.identifier:
				return True 
		return False

def legal_play_helper(player, board, curr_tile):
	new_board_position = get_next_board_position(player.position, player.board_position)
	curr_position = player.position
	while True:
		coordinates = get_coordinates(new_board_position)
		for i, coor in enumerate(coordinates):
			if coor == curr_position:
				start_path = i
		for path in curr_tile.paths:
			if path[0] == start_path:
				end_path = path[1]
			if path[1] == start_path:
				end_path = path[0]
		curr_position = coordinates[end_path]
		new_board_position = get_next_board_position(curr_position, new_board_position)
		if curr_position[0] == 0 or curr_position[1] == 0 or curr_position[0] == 18 or curr_position[1] == 18:
			return False
		for p in board.all_players:
			if p.color != player.color:
				if p.position == curr_position:
					return False
		if board.tiles[new_board_position[0]][new_board_position[1]] == None:
			break
		curr_tile = board.tiles[new_board_position[0], new_board_position[1]]

	for a_tile in player.tiles_owned:
		if a_tile.identifier == curr_tile.identifier:
			return True 
	return False


def play_a_turn(draw_pile, players, eliminated, board, place_tile):
	for p in eliminated:
		p.eliminated = True
	curr_player = players.pop(0)
	players.append(curr_player)
	original_board_position = get_next_board_position(curr_player.position, curr_player.board_position)
	board.tiles[original_board_position[0]][original_board_position[1]] = place_tile
	board.num_tiles += 1
	original_coordinates = get_coordinates(original_board_position)
	original_players = copy.deepcopy(players)
	for player in players:
		if not player.eliminated:
			if player.position in original_coordinates:
				new_board_position = original_board_position
				curr_position = player.position
				while True:
					coordinates = get_coordinates(new_board_position)
					for i, coor in enumerate(coordinates):
						if coor == curr_position:
							start_path = i
					for path in board.tiles[new_board_position[0]][new_board_position[1]].paths:
						if path[0] == start_path:
							end_path = path[1]
						if path[1] == start_path:
							end_path = path[0]
					curr_position = coordinates[end_path]
					new_board_position = get_next_board_position(curr_position, new_board_position)
					player.position = curr_position
					for p in players:
						if p.color != player.color:
							if p.position == player.position:
								p.eliminated = True
								player.eliminated = True
								break

					if curr_position[0] == 0 or curr_position[1] == 0 or curr_position[0] == 18 or curr_position[1] == 18:
						player.eliminated = True
						break
					if board.tiles[new_board_position[0]][new_board_position[1]] == None:
						break
	if players[len(players)-1].eliminated and players[len(players)-1].dragon_held:
		players[len(players)-1].dragon_held = False
		players[0].dragon_held = True
	for i in range(len(players)):
		if players[i].eliminated:
			eliminated.append(player)
			players[i].lose_tiles(draw_pile)
			if players[i].dragon_held:
				if len(players[(i+1)%len(players)].tiles_owned) != 3:
					players[(i+1)%len(players)].dragon_held = True
				players[i].dragon_held = False

	players = [x for x in players if not x.eliminated]
	dragon_already_held = False
	while draw_pile:
		dragon_already_held = False
		for i in range(len(players)):
			if draw_pile:
				if players[i].dragon_held:
					players[i].draw_tile(draw_pile)
					players[i].dragon_held = False
					if len(players[(i+1)%len(players)].tiles_owned) != 3:
						players[(i+1)%len(players)].dragon_held = True
					dragon_already_held = True
		if draw_pile:
			if not dragon_already_held:
				if not curr_player.eliminated:
					players[len(players)-1].draw_tile(draw_pile)
					break
				break

	if not dragon_already_held:
		if len(players)!= 0 and len(players[len(players)-1].tiles_owned) < 3:
			players[len(players)-1].dragon_held = True

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

def get_coordinates(board_position):
	'''
	given a board position, returns all possible postions a player can be on starting from top-left and moving clockwise
	'''
	return [(board_position[0]*3+1, board_position[1]*3+3), \
	(board_position[0]*3+2, board_position[1]*3+3), \
	(board_position[0]*3+3, board_position[1]*3+2), \
	(board_position[0]*3+3, board_position[1]*3+1), \
	(board_position[0]*3+2, board_position[1]*3), \
	(board_position[0]*3+1, board_position[1]*3), \
	(board_position[0]*3, board_position[1]*3+1), \
	(board_position[0]*3, board_position[1]*3+2)]

def get_next_board_position(position, board_position):
	'''
	given a player position, find board position that player will play next tile or move through
	'''

	if position[0]%3 == 0:
		if position[0] == board_position[0]*3:
			return (board_position[0]-1, board_position[1])
		else:
			return (board_position[0]+1, board_position[1])
	else:
		if position[1] == board_position[1]*3:
			return (board_position[0], board_position[1]-1)
		else:
			return (board_position[0], board_position[1]+1)

# def game_initialization(players):

# 	draw_pile = create_draw_pile()
# 	# shuffle the draw_pile
# 	for player in players:
# 		player.initialize_hand(draw_pile)

# 	board = Board(players)

# 	return board, draw_pile

# def play_game(players):
# 	board, draw_pile = game_initialization(players)
# 	curr_tile = players[0].tiles_owned[0]
# 	if legal_play(players[0], board, curr_tile):
# 		players[0].play_tile(curr_tile)
# 		eliminated = []
# 		draw_pile, players, eliminated, board, game_over = play_a_turn(draw_pile,players,eliminated,board,curr_tile)
# 		if not game_over:
# 			play_game(players)
# 		else:
# 			return game_over


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
