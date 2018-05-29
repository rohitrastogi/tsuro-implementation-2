import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom as minidom
from board import Board
from tile import Tile
from sPlayer import SPlayer
from position import Position
from square import Square
import gameConstants as constants

def prettify(element):
    rough_string = ElementTree.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def create_get_name_xml():
    top = Element('get-name')
    top.text = ' '
    return top

def create_player_name_xml(name):
    player_name = Element('player-name')
    player_name.text = name
    return player_name

def create_initialize_xml(color, list_of_colors):
    init_node = Element('initialize')
    init_node.append(create_color_xml(color))
    init_node.append(create_list_of_colors_xml(list_of_colors))
    return init_node

def create_void_xml():
    void = Element('void')
    void.text = ' '
    return void

def create_place_pawn_xml(board):
    place_pawn = Element('place-pawn')
    place_pawn.append(create_board_xml(board))
    return place_pawn

def create_pawn_loc_xml(position):
    x = position.x
    y = position.y
    # dict_mapping = {17:0, 16:1, 14:2, 13:3, 11:4, 10:5, 8:6, 7:7, 5:8, 4:9, 2:10, 1:11}
    pawn_loc = Element('pawn-loc')
    if x%3 == 0:
        pawn_loc.append(create_hv_xml('v'))
    else:
        pawn_loc.append(create_hv_xml('h'))
    pawn_loc.append(create_natural_number_xml(x//3))
    pawn_loc.append(create_natural_number_xml(12 - y + y//3))
    return pawn_loc

def create_play_turn_xml(board, tiles, number):
    play_turn = Element('play-turn')
    play_turn.append(create_board_xml(board))
    play_turn.append(create_set_of_tiles_xml(tiles))
    play_turn.append(create_natural_number_xml(number))
    return play_turn

def create_tile_xml(tile):
    tile_root = Element('tile')
    for path in tile.paths:
        tile_root.append(create_connection_xml(path[0], path[1]))
    return tile_root

def create_end_game_xml(board, winners):
    end_game_node = Element('end-game')
    end_game_node.append(create_board_xml(board))
    end_game_node.append(create_set_of_colors_xml(winners))
    return end_game_node

def create_board_xml(board):
    board_node = Element('board')
    board_node.append(create_tiles_xml(board))
    board_node.append(create_pawns_xml(board))
    return board_node

def create_splayer_xml(sPlayer):
    if sPlayer.dragon_held:
        root = Element('splayer-dragon')
    else:
        root = Element('splayer-nodragon')
    root.append(create_color_xml(sPlayer.color))
    root.append(create_set_of_tiles_xml(sPlayer.tiles_owned))
    return root

def create_list_of_splayers_xml(list_of_splayers):
    root = Element('list')
    for sPlayer in list_of_splayers:
        root.append(create_splayer_xml(sPlayer))
    return root

def create_maybe_list_of_splayers_xml(maybe_list_of_splayers):
    if maybe_list_of_splayers == False:
        root = Element('false')
        root.text = ' '
    else:
        root = create_list_of_splayers_xml(maybe_list_of_splayers)
    return root

def create_list_of_tiles_xml(list_of_tiles):
    list_node = Element('list')
    for tile in list_of_tiles:
        list_node.append(create_tile_xml(tile))
    return list_node

def create_set_of_tiles_xml(set_of_tiles):
    set_node = Element('set')
    for tile in set_of_tiles:
        set_node.append(create_tile_xml(tile))
    return set_node

def create_tiles_xml(board):
    map_node = Element('map')
    for i in range(constants.BOARD_DIMENSION):
        for j in range(constants.BOARD_DIMENSION):
            if board.tiles[i][j]:
                ent = Element('ent')
                ent.append(create_xy_xml(i, constants.BOARD_DIMENSION - j - 1))
                ent.append(create_tile_xml(board.tiles[i][j]))
                map_node.append(ent)
    return map_node

def create_pawns_xml(board):
    map_node = Element('map')
    for player in board.all_players:
        ent = Element('ent')
        ent.append(create_color_xml(player.color))
        ent.append(create_pawn_loc_xml(player.position))
        map_node.append(ent)
    return map_node

def create_hv_xml(option):
    hv = Element('hv')
    if option == 'h':
        h = SubElement(hv, 'h')
        h.text = ' '
    if option == 'v':
        v = SubElement(hv, 'v')
        v.text = ' '
    return hv

def create_xy_xml(x_num, y_num):
    xy = Element('xy')
    x = SubElement(xy, 'x')
    x.text = str(x_num)
    y = SubElement(xy, 'y')
    y.text = str(y_num)
    return xy

def create_connection_xml(start, end):
    connect = Element('connect')
    connect.append(create_natural_number_xml(start))
    connect.append(create_natural_number_xml(end))
    return connect

def create_list_of_colors_xml(list_of_colors):
    list_node = Element('list')
    for color in list_of_colors:
        list_node.append(create_color_xml(color))
    return list_node

def create_set_of_colors_xml(set_of_colors):
    set_node = Element('set')
    for color in set_of_colors:
        set_node.append(create_color_xml(color))
    return set_node

def create_color_xml(color_string):
    color = Element('color')
    color.text = color_string
    return color

def create_natural_number_xml(number):
    n = Element('n')
    n.text = str(number)
    return n

def interpret_output(func, output):
    if func == "end-game" or func == "initialize":
        return create_void_xml()
    elif func == "get-name":
        return create_player_name_xml(output)
    elif func == "place-pawn":
        return create_pawn_loc_xml(output)
    elif func == "play-turn":
        return create_tile_xml(output)
    else:
        raise RuntimeError("Invalid XML Message!")

# Tests
# n = create_natural_number_xml(3)
# print (prettify(n))
#
# connection = create_connection_xml(0, 7)
# print (prettify(connection))
#
# tile = create_tile_xml(Tile(1, [[0,1],[2,3],[4,5],[6,7]]))
# print (prettify(tile))
#
# color = create_color_xml('blue')
# print (prettify(color))
#
# get_name_message = create_get_name_xml()
# print (prettify(get_name_message))
#
# hv_1 = create_hv_xml('v')
# print (prettify(hv_1))
#
# hv_2 = create_hv_xml('h')
# print (prettify(hv_2))
#
# pawn_loc_1 = create_pawn_loc_xml(Position(3, 16, Square(0, 5)))
# print (prettify(pawn_loc_1))
#
# player_1 = Player()
# player_1.color = 'blue'
# player_1.position = Position(3, 16, Square(0, 5))
# player_2 = Player()
# player_2.color = 'green'
# player_2.position = Position(3, 1, Square(0, 0))
# board = Board([player_1, player_2])
# board.tiles[0][5] = Tile(1, [[0,1],[2,4],[3,6],[5,7]])
# # tiles_xml = create_tiles_xml(board)
# # pawns_xml = create_pawns_xml(board)
# board_xml = create_board_xml(board)
# print (prettify(board_xml))
