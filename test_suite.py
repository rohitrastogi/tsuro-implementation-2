from player import Player
from board import Board
from tile import Tile
import administrator
import pytest

def test_getCoordinates():
    assert administrator.get_coordinates((3,2)) == [(10,9),(11,9),(12,8),(12,7),(11,6),(10,6),(9,7),(9,8)]
    assert administrator.get_coordinates((1,4)) == [(4,15),(5,15),(6,14),(6,13),(5,12),(4,12),(3,13),(3,14)]

def test_getNextBoardPosition():
    assert administrator.get_next_board_position((9,7), (3,2)) == (2,2)
    assert administrator.get_next_board_position((1,0), (0,-1)) == (0,0)
    assert administrator.get_next_board_position((18,4), (6,1)) == (5,1)
    assert administrator.get_next_board_position((0,8), (-1,2)) == (0,2)
    assert administrator.get_next_board_position((11,18), (3,6)) == (3,5)

def test_gameInitialization():
    player_1 = Player('blue', (0, 1))
    player_2 = Player('red', (11, 0))
    with pytest.raises(Exception):
        player_3 = Player('green', (19, 8))
    with pytest.raises(Exception):
        player_4 = Player('orange', (12, 0))

def test_drawTile():
    draw_pile = administrator.create_draw_pile()
    player_1 = Player('blue', (0, 1))
    player_1.draw_tile(draw_pile)
    assert len(player_1.tiles_owned) == 1
    assert len(draw_pile) == 34

    player_2 = Player('green', (11, 0))
    player_2.draw_tile(draw_pile)
    assert len(player_2.tiles_owned) == 1
    assert len(draw_pile) == 33

def test_initializeHand():
    draw_pile = administrator.create_draw_pile()
    player_1 = Player('blue', (0, 1))
    player_1.initialize_hand(draw_pile)
    assert len(player_1.tiles_owned) == 3
    assert len(draw_pile) == 32

    player_2 = Player('green', (11, 0))
    player_2.initialize_hand(draw_pile)
    assert len(player_2.tiles_owned) == 3
    assert len(draw_pile) == 29

def test_loseTiles():
    draw_pile = administrator.create_draw_pile()
    player_1 = Player('blue', (0, 1))
    player_1.initialize_hand(draw_pile)
    player_2 = Player('green', (11, 0))
    player_2.initialize_hand(draw_pile)
    assert len(draw_pile) == 29
    player_1.lose_tiles(draw_pile)
    assert len(player_1.tiles_owned) == 0
    assert len(draw_pile) == 32
    player_2.lose_tiles(draw_pile)
    assert len(player_2.tiles_owned) == 0
    assert len(draw_pile) == 35

def test_playTile():
    tile_1 = Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]])
    player_1 = Player('blue', (0, 1))
    player_1.tiles_owned = [Tile(12, [[0, 7], [1, 2], [3, 4], [5, 6]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])]
    player_1.play_tile(tile_1)
    assert len(player_1.tiles_owned) == 2

def test_rotateTile():
    tile_1 = Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])
    tile_2 = Tile(3, [[0, 1], [2, 7], [3, 5], [4, 6]])

    tile_1.rotate_tile()
    assert tile_1.paths == [[2, 5], [1, 3], [0, 4], [6, 7]]
    tile_1.rotate_tile()
    assert tile_1.paths == [[4, 7], [3, 5], [2, 6], [0, 1]]
    tile_2.rotate_tile()
    assert tile_2.paths == [[2, 3], [1, 4], [5, 7], [0, 6]]
