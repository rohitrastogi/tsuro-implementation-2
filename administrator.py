from player import Player
from board import Board
from tile import Tile

# The admin registers players, creates the board, and initializes the pile of tiles
# starts game play

def legal_play(player, board, curr_tile):
    # TODO: write description


    # is the tile in the player's hand?
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

    for a_tile in player.owned_tiles:
        if a_tile.identifier == curr_tile.identifier:
            return True

    return legal

def play_a_turn(draw_pile, players, eliminated, board, tile):
    

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
