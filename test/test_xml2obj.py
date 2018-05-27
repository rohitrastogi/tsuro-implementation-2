import xml2obj
from xml.etree.ElementTree import fromstring
import pytest


def test_create_square_obj():
    square_xml_1 = "<xy><x>4</x><y>1</y></xy>"
    square_parse_1 = fromstring(square_xml_1)
    square_1 = xml2obj.create_square_obj(square_parse_1)
    assert(square_1.x == 4)
    assert(square_1.y == 4)

    square_xml_2 = "<xy><x>5</x><y>3</y></xy>"
    square_parse_2 = fromstring(square_xml_2)
    square_2 = xml2obj.create_square_obj(square_parse_2)
    assert(square_2.x == 5)
    assert(square_2.y == 2)

def test_create_tile_obj_helper():
    tile_xml_1 = "<tile><connect><n>0</n><n>5</n></connect><connect><n>1</n><n>3</n></connect><connect><n>2</n><n>6</n></connect><connect><n>4</n><n>7</n></connect></tile>"
    tile_parse_1 = fromstring(tile_xml_1)
    tile_1 = xml2obj.create_tile_obj_helper(tile_parse_1)
    assert(tile_1.paths == [[0, 5], [1, 3], [2, 6], [4, 7]])
    assert(tile_1.identifier == 34)

def test_create_color_obj():
    color_xml_1 = "<color>blue</color>"
    color_parse_1 = fromstring(color_xml_1)
    color_1 = xml2obj.create_color_obj(color_parse_1)
    assert color_1 == "blue"
    with pytest.raises(Exception):
        color_xml_2 = "<color>magenta</color>"
        color_parse_2 = fromstring(color_xml_2)
        color_2 = xml2obj.create_color_obj(color_parse_2)

def test_create_pawn_loc():
    posn_xml_1 = "<pawn-loc><v></v><n>1</n><n>1</n></pawn-loc>"
    posn_parse_1 = fromstring(posn_xml_1)
    posn_1 = xml2obj.create_position_obj(posn_parse_1)
    assert(posn_1.x == 3 and posn_1.y == 16)
    
    posn_xml_2 = "<pawn-loc><h></h><n>1</n><n>1</n></pawn-loc>"
    posn_parse_2 = fromstring(posn_xml_2)
    posn_2 = xml2obj.create_position_obj(posn_parse_2)
    assert(posn_2.x == 1 and posn_2.y == 15)

def test_create_board():
    board_xml_1 = "<board><map><ent><xy><x>0</x><y>0</y></xy><tile><connect><n>0</n><n>1</n></connect><connect><n>2</n><n>4</n></connect><connect><n>3</n><n>6</n></connect><connect><n>5</n><n>7</n></connect></tile></ent></map><map><ent><color>red</color><pawn-loc><v></v><n>1</n><n>1</n></pawn-loc></ent></map></board>"
    board_parse_1 = fromstring(board_xml_1)
    board_1 = xml2obj.create_board_obj(board_parse_1)
    assert board_1.num_tiles == 1
    assert board_1.all_players[0].color == "red"
    assert board_1.tiles[0][5].identifier == 1

def test_interpret_place_pawn():
    place_pawn_xml = "<place-pawn><board><map><ent><xy><x>0</x><y>0</y></xy><tile><connect><n>0</n><n>1</n></connect><connect><n>2</n><n>4</n></connect><connect><n>3</n><n>6</n></connect><connect><n>5</n><n>7</n></connect></tile></ent></map><map><ent><color>red</color><pawn-loc><v></v><n>1</n><n>1</n></pawn-loc></ent></map></board></place-pawn>"
    place_pawn_parse = fromstring(place_pawn_xml)
    command_1 = xml2obj.interpret_command(place_pawn_parse)[0]
    board_1 = xml2obj.interpret_command(place_pawn_parse)[1]
    assert command_1 == "place-pawn" 
    assert board_1.num_tiles == 1
    assert board_1.all_players[0].color == "red"
    assert board_1.tiles[0][5].identifier == 1

def test_intepret_initialize():
    initialize_xml = "<initialize><color>blue</color><list><color>red</color><color>green</color><color>orange</color></list></initialize>"
    initialize_parse = fromstring(initialize_xml)
    command_1 = xml2obj.interpret_command(initialize_parse)[0]
    color = xml2obj.interpret_command(initialize_parse)[1]
    list_of_colors = xml2obj.interpret_command(initialize_parse)[2]
    assert command_1 == "initialize"
    assert color == "blue"
    assert list_of_colors == ["red", "green", "orange"]

def test_intepret_end_game():
    end_game_xml = "<end-game><board><map><ent><xy><x>0</x><y>0</y></xy><tile><connect><n>0</n><n>1</n></connect><connect><n>2</n><n>4</n></connect><connect><n>3</n><n>6</n></connect><connect><n>5</n><n>7</n></connect></tile></ent></map><map><ent><color>red</color><pawn-loc><v></v><n>1</n><n>1</n></pawn-loc></ent></map></board><set><color>red</color></set></end-game>"
    end_game_parse = fromstring(end_game_xml)
    command_1 = xml2obj.interpret_command(end_game_parse)[0]
    board_1 = xml2obj.interpret_command(end_game_parse)[1]
    set_of_colors = xml2obj.interpret_command(end_game_parse)[2]
    assert command_1 == "end-game" 
    assert board_1.num_tiles == 1
    assert board_1.all_players[0].color == "red"
    assert board_1.tiles[0][5].identifier == 1
    assert set_of_colors == ["red"]

def test_intepret_get_name():
    get_name_xml = "<get-name></get-name>"
    get_name_parse = fromstring(get_name_xml)
    command_1 = xml2obj.interpret_command(get_name_parse)
    assert command_1 == "get-name"

def test_interpret_play_turn():
    end_game_xml = "<play-turn><board><map><ent><xy><x>0</x><y>0</y></xy><tile><connect><n>0</n><n>1</n></connect><connect><n>2</n><n>4</n></connect><connect><n>3</n><n>6</n></connect><connect><n>5</n><n>7</n></connect></tile></ent></map><map><ent><color>red</color><pawn-loc><v></v><n>1</n><n>1</n></pawn-loc></ent></map></board><set><tile><connect><n>0</n><n>5</n></connect><connect><n>1</n><n>3</n></connect><connect><n>2</n><n>6</n></connect><connect><n>4</n><n>7</n></connect></tile></set><n>3</n></play-turn>"
    end_game_parse = fromstring(end_game_xml)
    command_1 = xml2obj.interpret_command(end_game_parse)[0]
    board_1 = xml2obj.interpret_command(end_game_parse)[1]
    set_of_tiles = xml2obj.interpret_command(end_game_parse)[2]
    num_tiles_left = xml2obj.interpret_command(end_game_parse)[3]
    assert command_1 == "play-turn"
    assert board_1.num_tiles == 1
    assert board_1.all_players[0].color == "red"
    assert board_1.tiles[0][5].identifier == 1
    assert set_of_tiles[0].identifier == 34
    assert int(num_tiles_left) == 3

def test_interpret_invalid_command():
    invalid_xml = "<move></move>"
    invalid_parse = fromstring(invalid_xml)
    with pytest.raises(Exception):
        command_1 = xml2obj.interpret_command(invalid_parse)
    





