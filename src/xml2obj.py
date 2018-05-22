import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom as minidom
from board import Board
from tile import Tile
from player import Player
from position import Position
from square import Square
import gameConstants as constants
import administrator

#TODO find the correct place to add paths and hashing
def create_path_hash(paths):
    path_hashes = []
    for path in paths:
        path_hashes.append(''.join(str(x) for x in path))
    return '-'.join(path_hashes)

tiles = administrator.create_draw_pile()
tile_tups = [(create_path_hash(tile.paths), tile.identifier) for tile in tiles]
path_id_map = {k:v for (k, v) in tile_tups}

def get_identifier(path_hash):
    return path_id_map[path_hash]  

def create_board_obj(board):
    board_obj = Board()

    tile_entries = [child for child in board[0]]
    pawn_entries = [child for child in board[1]]

    for tile_entry in tile_entries:
        (square_obj, tile_obj) = create_tile_obj(tile_entry)
        board_obj.place_tile(square_obj, tile_obj)

    for pawn_entry in pawn_entries:
        (color_obj, position_obj) = create_player_locs(pawn_entry)
        #TODO need to fix tile order somehow
        board_obj.add_player(Player(color_obj, position_obj))
        
    return board_obj

def create_tile_obj(tile_entry):
    xy = tile_entry[0]
    tile = tile_entry[1]
    return (create_square_obj(xy), create_tile_obj_helper(tile))

def create_square_obj(xy):
    x = xy[0].text
    y = xy[1].text
    return Square(x, convert_y_representation(y))

def convert_y_representation(y):
    return constants.NUMBER_OF_TILES - 1 - y

def create_tile_obj_helper(tile):
    connections = [child for child in tile]
    if len(connections) != 4:
        raise RuntimeError("Malformed tile XML")
    paths = []
    for connection in connections:
        paths.append(create_path_object(connection))
    paths.sort(key = lambda x: x[0])
    identifier = get_identifier(create_path_hash(paths))
    return Tile(identifier, paths)

def create_path_object(connection):
    return [int(connection[0].text), int(connection[1].text)]

def create_player_locs(pawn_entry):
    color_obj = create_color_object(pawn_entry[0])
    position_obj = create_position_obj(pawn_entry[1])
    return (color_obj, position_obj)

def create_color_object(color):
    return [c.name for cc in constants.Colors].index(color.text)

def create_position_obj(pawn_loc):
    # TODO is there a function that cna do this dynamically
    mapping = {0:17, 1:16, 2:14, 3:13, 4:11, 5:10, 6:8, 7:7, 8:5, 9:4, 10:2, 11:1}
    if pawn_loc[0].tag = "v":
        y = constants.END_WALL - pawn_loc[1]*3
        x = mapping[pawn_loc[2]]
    else:
        y = mapping[pawn_loc[2]]
        x = constants.END_WALL - pawn_loc[1] * 3 
    return Position(x, y, Square(x//3, y//3))

def create_list_of_color_obj(list_of_color):
    return [create_color_object(child) for child in list_of_color]

def create_list_of_tile_obj(list_of_tile):
    return [create_tile_object(child) for child in list_of_tile]

def interpret_command(command):
    #TODO: use enum or the like to amke this modular
    if command.tag == "get-name":
        return command.tag

    elif command.tag == "initialize":
        return command.tag, create_color_object(command[0]), create_list_of_color_obj(command[1])

    elif command.tag = "place-pawn":
        return command.tag, create_board_obj(command[0])

    elif command.tag = "play-turn":
        return command.tag, create_board_obj(command[0], create_list_of_tile_obj(command[1], int(command[2])))

    elif command.tag = "end-game":
        return command.tag, create_board_obj(command[1], create_list_of_color_obj(command[2]))

    else:
        raise RuntimeError("Invalid XML Messsage!")
    









