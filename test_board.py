from player import Player
from board import Board
from tile import Tile
from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
import administrator
import pytest

def test_getCoordinates():
    board = Board()
    assert board.get_coordinates((3,2)) == [(10,9),(11,9),(12,8),(12,7),(11,6),(10,6),(9,7),(9,8)]
    assert board.get_coordinates((1,4)) == [(4,15),(5,15),(6,14),(6,13),(5,12),(4,12),(3,13),(3,14)]

def test_getNextBoardSquare():
    board = Board()
    assert board.get_next_board_square((9,7), (3,2)) == (2,2)
    assert board.get_next_board_square((1,0), (0,-1)) == (0,0)
    assert board.get_next_board_square((18,4), (6,1)) == (5,1)
    assert board.get_next_board_square((0,8), (-1,2)) == (0,2)
    assert board.get_next_board_square((11,18), (3,6)) == (3,5)
