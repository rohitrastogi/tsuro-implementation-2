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
