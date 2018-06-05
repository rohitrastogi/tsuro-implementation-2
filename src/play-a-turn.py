import xml2obj
import obj2xml
import administrator
import sys
from xml.etree.ElementTree import tostring, fromstring

argument_count = 0
arguments = []
while True:
    try:
        line = input()
        argument_count += 1
        arguments.append(line)
        if argument_count % 5 == 0:
            list_of_tile_xml, list_of_active_players_xml, list_of_elim_players_xml, board_xml, tile_xml = arguments

            list_of_tile = xml2obj.create_list_of_tile_obj(fromstring(list_of_tile_xml))
            list_of_active_players = xml2obj.create_list_of_current_splayer_obj(fromstring(list_of_active_players_xml), fromstring(board_xml))
            list_of_elim_players = xml2obj.create_list_of_eliminated_splayer_obj(fromstring(list_of_elim_players_xml), fromstring(board_xml))
            board = xml2obj.create_board_obj(fromstring(board_xml))
            tile = xml2obj.create_tile_obj_helper(fromstring(tile_xml))

            draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(list_of_tile, list_of_active_players, list_of_elim_players, board, tile)

            draw_pile_xml = obj2xml.create_list_of_tiles_xml(draw_pile)
            active_players_xml = obj2xml.create_list_of_splayers_xml(players)
            eliminated_players_xml = obj2xml.create_list_of_splayers_xml(eliminated)
            board_xml = obj2xml.create_board_xml(board)
            maybe_list_of_splayers_xml = obj2xml.create_maybe_list_of_splayers_xml(game_over)

            print (tostring(draw_pile_xml, encoding="unicode", short_empty_elements=False))
            print (tostring(active_players_xml, encoding="unicode", short_empty_elements=False))
            print (tostring(eliminated_players_xml, encoding="unicode", short_empty_elements=False))
            print (tostring(board_xml, encoding="unicode", short_empty_elements=False))
            print (tostring(maybe_list_of_splayers_xml, encoding="unicode", short_empty_elements=False))
            arguments = []
    except EOFError:
        break
