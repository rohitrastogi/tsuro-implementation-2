import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom as minidom
from board import Board
from tile import Tile
from sPlayer import SPlayer
from position import Position
from square import Square
import gameConstants as constants
import administrator

def create_path_hash(paths):
    path_hashes = []
    for path in paths:
        path_hashes.append(''.join(str(x) for x in path))
    return '-'.join(path_hashes)

tiles = administrator.create_draw_pile()
tile_tups = []
for tile in tiles:
    for i in range(4):
        tile_tups.append((create_path_hash(tile.paths), tile.identifier))
        tile.rotate_tile()

path_id_map = {k:v for (k, v) in tile_tups}

def get_identifier(path_hash):
    return path_id_map[path_hash]

def create_board_obj(board_xml):
    board_obj = Board(players = [])

    tile_entries = [child for child in board_xml[0]]
    pawn_entries = [child for child in board_xml[1]]

    for tile_entry in tile_entries:
        (square_obj, tile_obj) = create_tiles_obj(tile_entry)
        board_obj.place_tile(square_obj, tile_obj)

    for pawn_entry in pawn_entries:
        (color_obj, position_obj) = create_player_locs(pawn_entry, board_obj)
        if position_obj.hit_a_wall() and board_obj.get_tile(position_obj.square):
            p = SPlayer(color_obj, position_obj)
            p.eliminated = True
            board_obj.add_player_to_eliminated(p)
        else:
            board_obj.add_player(SPlayer(color_obj, position_obj))

    return board_obj

def create_tiles_obj(tile_entry):
    xy = tile_entry[0]
    tile = tile_entry[1]
    return (create_square_obj(xy), create_tile_obj_helper(tile))

def create_square_obj(xy):
    x = xy[0].text
    y = xy[1].text
    return Square(int(x), convert_y_representation(int(y)))

def convert_y_representation(y):
    return constants.BOARD_DIMENSION - 1 - y

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

def create_player_locs(pawn_entry, board_obj):
    color_obj = create_color_obj(pawn_entry[0])
    position_obj = create_position_obj(pawn_entry[1], board_obj)
    return (color_obj, position_obj)

def create_color_obj(color):
    if color.text in constants.Colors.values():
        return color.text
    raise RuntimeError("Invalid Color Specified in XML!")

def create_position_obj(pawn_loc, board_obj):
    mapping = {0:17, 1:16, 2:14, 3:13, 4:11, 5:10, 6:8, 7:7, 8:5, 9:4, 10:2, 11:1}
    if pawn_loc[0].tag == "v":
        x = int(pawn_loc[1].text) * 3
        y = mapping[int(pawn_loc[2].text)]
        square = None
        if board_obj.get_tile(Square(x//3, y//3)):
            square = Square(x//3, y//3)
        if board_obj.get_tile(Square(x//3 - 1, y//3)):
            square = Square(x//3 - 1, y//3)
    else:
        x = constants.END_WALL - mapping[int(pawn_loc[2].text)]
        y = constants.END_WALL - int(pawn_loc[1].text) * 3
        square = None
        if board_obj.get_tile(Square(x//3, y//3)):
            square = Square(x//3, y//3)
        if board_obj.get_tile(Square(x//3, y//3 - 1)):
            square = Square(x//3, y//3 - 1)

    return Position(x, y, square)

def create_list_of_current_splayer_obj(list_of_splayer, board_xml):
    list_of_splayers = [create_splayer_obj(splayer) for splayer in list_of_splayer]
    board = create_board_obj(board_xml)
    color_position_dict = {player.color:player.position for player in board.current_players}
    for sp in list_of_splayers:
        sp.position = color_position_dict[sp.color]
        sp.eliminated = False
    return list_of_splayers

def create_list_of_eliminated_splayer_obj(list_of_splayer, board_xml):
    list_of_splayers = [create_splayer_obj(splayer) for splayer in list_of_splayer]
    board = create_board_obj(board_xml)
    color_position_dict = {player.color:player.position for player in board.eliminated_players}
    for sp in list_of_splayers:
        sp.position = color_position_dict[sp.color]
        sp.eliminated = True
    return list_of_splayers

def create_maybe_list_of_splayer_obj(maybe_list_of_splayers):
    if maybe_list_of_splayers.tag == 'false':
        return False
    list_of_splayers = [create_splayer_obj(splayer) for splayer in maybe_list_of_splayers]
    return list_of_splayers

def create_splayer_obj(splayer):
    sPlayer_obj = SPlayer()
    sPlayer_obj.color = create_color_obj(splayer[0])
    sPlayer_obj.tiles_owned = create_list_of_tile_obj(splayer[1])
    if splayer.tag == "splayer-dragon":
        sPlayer_obj.dragon_held = True
    else:
        sPlayer_obj.dragon_held = False

    return sPlayer_obj

def create_list_of_color_obj(list_of_color):
    return [create_color_obj(child) for child in list_of_color]

def create_list_of_tile_obj(list_of_tile):
    return [create_tile_obj_helper(child) for child in list_of_tile]

def construct_player_name_obj(player_name):
    return player_name.text

def interpret_command(command):
    #TODO: use enum or the like to make this modular
    if command.tag == "get-name":
        return [command.tag]

    elif command.tag == "initialize":
        return [command.tag, create_color_obj(command[0]), create_list_of_color_obj(command[1])]

    elif command.tag == "place-pawn":
        return [command.tag, create_board_obj(command[0])]

    elif command.tag == "play-turn":
        return [command.tag, create_board_obj(command[0]), create_list_of_tile_obj(command[1]), int(command[2].text)]

    elif command.tag == "end-game":
        return [command.tag, create_board_obj(command[0]), create_list_of_color_obj(command[1])]

    else:
        raise RuntimeError("Invalid XML Messsage!")
