from player import Player
from board import Board
from tile import Tile
from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
import administrator
import pytest

def test_rotateTile():
    tile_1 = Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])
    tile_2 = Tile(3, [[0, 1], [2, 7], [3, 5], [4, 6]])

    tile_1.rotate_tile()
    assert tile_1.paths == [[0, 4], [1, 3], [2, 5], [6, 7]]
    tile_1.rotate_tile()
    assert tile_1.paths == [[0, 1], [2, 6], [3, 5], [4, 7]]
    tile_2.rotate_tile()
    assert tile_2.paths == [[0, 6], [1, 4], [2, 3], [5, 7]]

def test_moveAlongPath():
    board = Board()

    tile_1 = Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])
    tile_2 = Tile(3, [[0, 1], [2, 7], [3, 5], [4, 6]])

    board_position = (3,2)
    start = (9,8)
    coordinates = board.get_coordinates(board_position)
    end = tile_1.move_along_path(start, coordinates)
    assert end == (11,9)

    board_position = (2,4)
    start = (9,13)
    coordinates = board.get_coordinates(board_position)
    end = tile_2.move_along_path(start, coordinates)
    assert end == (7,12)

def test_symmetry():
    tile_1 = Tile(8, [[0, 4], [1, 5], [2, 6], [3, 7]])
    tile_2 = Tile(6, [[0, 1], [2, 6], [3, 7], [4, 5]])
    tile_3 = Tile(4, [[0, 2], [1, 4], [3, 7], [5, 6]])

    assert tile_1.symmetry() == 1
    assert tile_1.paths == [[0, 4], [1, 5], [2, 6], [3, 7]]
    assert tile_2.symmetry() == 2
    assert tile_2.paths == [[0, 1], [2, 6], [3, 7], [4, 5]]
    assert tile_3.symmetry() == 4
    assert tile_3.paths == [[0, 2], [1, 4], [3, 7], [5, 6]]
