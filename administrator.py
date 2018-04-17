from player import Player
from board import Board
from tile import Tile

# The admin registers players, creates the board, and initializes the pile of tiles
# starts game play

def legal_play(player, board, curr_tile):
    # TODO: write description
    legal = False
    new_board_position = get_next_board_position(player.position, player.board_position)
    curr_position = player.position
    start_path = -1
    end_path = -1

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
        if board.tiles[new_board_position[0]][new_board_position[1]] == None:
            break
        curr_tile = board.tiles[new_board_position[0], new_board_position[1]]

    for a_tile in player.owned_tiles:
        if a_tile.identifier == curr_tile.identifier:
            return True

    return legal

def play_a_turn(draw_pile, players, eliminated, board, place_tile):
    curr_player = players.pop(0)
    players.append(curr_player)
    original_board_position = get_next_board_position(curr_player.position, curr_player.board_position)
    board.tiles[new_board_position[0]][new_board_position[1]] = place_tile
    original_coordinates = get_coordinates(original_board_position)

    for player in players:
        if !player.eliminated:
            if player.position in original_coordinates:
                new_board_position = original_board_position
                curr_position = player.position
                while True:
                    coordinates = get_coordinates(new_board_position)
                    for i, coor in enumerate(coordinates):
                        if coor == curr_position:
                            start_path = i
                    for path in board.tiles[new_board_position[0], new_board_position[1]].paths:
                        if path[0] == start_path:
                            end_path = path[1]
                        if path[1] == start_path:
                            end_path = path[0]
                    curr_position = coordinates[end_path]
                    new_board_position = get_next_board_position(curr_position, new_board_position)
                    player.position = curr_position
                    for p in players:
                        if p.position == player.position:
                            p.eliminated = True
                            player.eliminated = True

                    if curr_position[0] == 0 or curr_position[1] == 0 or curr_position[0] == 18 or curr_position[1] == 18:
                        break
                    if board.tiles[new_board_position[0]][new_board_position[1]] == None:
                        break

    for i, player in enumerate(players):
        if player.position[0] == 0 or player.position[1] == 0 or player.position[0] == 18 or player.position[1] == 18 or player.eliminated:
            # TODO pass on this player's dragon tile
            eliminated.append(player)
            player.lose_tiles(draw_pile)
            if player.dragon_held:
            	players[(i+1)%len(players)].dragon_held = True
            del players[i]
    dragon_already_held = False
    while draw_pile:
        for i, player in enumerate(players):
            if player.dragon_held:
                player.draw_tile(draw_pile)
                player.dragon_held = False
                if len(players[(i+1)%len(players)].owned_tiles) != 3:
                    players[(i+1)%len(players)].dragon_held = True
                dragon_already_held = True
        if !dragon_already_held:
            player[len(players)-1].draw_tile(draw_pile)
            break

    if !dragon_already_held:
        player[len(players)-1].dragon_held = True

    game_over = False
    if len(players) == 1:
        game_over = players[0]

    # TODO if all tiles are done, the players on the board win 
    	# maybe do it by incrementing everytime you add a tile and flag True when it equals 35
    # TODO if the last 2 or more players get eliminated in the same turn they win

    return draw_pile, players, eliminated, board, game_over

def get_coordinates(board_position):
    return [(board_position(0)*3+1, board_position(1)*3+3), \
    (board_position(0)*3+2, board_position(1)*3+3), \
    (board_position(0)*3+3, board_position(1)*3+2), \
    (board_position(0)*3+3, board_position(1)*3+1), \
    (board_position(0)*3+2, board_position(1)*3), \
    (board_position(0)*3+1, board_position(1)*3), \
    (board_position(0)*3, board_position(1)*3+1), \
    (board_position(0)*3, board_position(1)*3+2)]

def get_next_board_position(position, board_position):

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

def game_initialization():

    draw_pile = create_draw_pile()
    # shuffle the draw_pile
    player_1 = Player('blue', (0, 1))
    player_2 = Player('red', (11, 0))
    player_3 = Player('green', (18, 8))
    players = [player_1, player_2, player_3]

    for player in players:
        for i in range(3):
            player.draw_tile(draw_pile)

    board = Board(players)



def create_draw_pile():
    draw_pile = []

    unique_tiles = [((0, 1), (2, 3), (4, 5), (6, 7)), \
                    ((0, 1), (2, 4), (3, 6), (5, 7)), \
                    ((0, 6), (1, 5), (2, 4), (3, 7)), \
                    ((0, 5), (1, 4), (2, 7), (3, 6)), \
                    ((0, 2), (1, 4), (3, 7), (5, 6)), \
                    ((0, 4), (1, 7), (2, 3), (5, 6)), \
                    ((0, 1), (2, 6), (3, 7), (4, 5)), \
                    ((0, 2), (1, 6), (3, 7), (4, 5)), \
                    ((0, 4), (1, 5), (2, 6), (3, 7)), \
                    ((0, 1), (2, 7), (3, 4), (5, 6)), \
                    ((0, 2), (1, 7), (3, 4), (5, 6)), \
                    ((0, 3), (1, 5), (2, 7), (4, 6)), \
                    ((0, 4), (1, 3), (2, 7), (5, 6)), \
                    ((0, 3), (1, 7), (2, 6), (4, 5)), \
                    ((0, 1), (2, 5), (3, 6), (4, 7)), \
                    ((0, 3), (1, 6), (2, 5), (4, 7)), \
                    ((0, 1), (2, 7), (3, 5), (4, 6)), \
                    ((0, 7), (1, 6), (2, 3), (4, 5)), \
                    ((0, 7), (1, 2), (3, 4), (5, 6)), \
                    ((0, 2), (1, 4), (3, 6), (5, 7)), \
                    ((0, 7), (1, 3), (2, 5), (4, 6)), \
                    ((0, 7), (1, 5), (2, 6), (3, 4)), \
                    ((0, 4), (1, 5), (2, 7), (3, 6)), \
                    ((0, 1), (2, 4), (3, 5), (6, 7)), \
                    ((0, 2), (1, 7), (3, 5), (4, 6)), \
                    ((0, 7), (1, 5), (2, 3), (4, 6)), \
                    ((0, 4), (1, 3), (2, 6), (5, 7)), \
                    ((0, 6), (1, 3), (2, 5), (4, 7)), \
                    ((0, 1), (2, 7), (3, 6), (4, 5)), \
                    ((0, 3), (1, 2), (4, 6), (5, 7)), \
                    ((0, 3), (1, 5), (2, 6), (4, 7)), \
                    ((0, 7), (1, 6), (2, 5), (3, 4)), \
                    ((0, 2), (1, 3), (4, 6), (5, 7)), \
                    ((0, 5), (1, 6), (2, 7), (3, 4)), \
                    ((0, 5), (1, 3), (2, 6), (4, 7))]

    for i, paths in enumerate(unique_tiles):
        draw_pile.append(Tile(i, paths))

    return draw_pile
