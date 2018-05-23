from board import Board
from tile import Tile
from position import Position
from square import Square
import administrator
import pytest

def test_constructor():
    with pytest.raises(Exception):
        tile_1 = Tile(17, [[0, 3], [1, 7], [2, 6]])

    with pytest.raises(Exception):
        tile_2 = Tile(17, [[0, 3], [1, 7], [2, 6], [2, 9]])

    with pytest.raises(Exception):
        tile_3 = Tile(17, [[1, 2], [3, 4], [5, 6], [7, 8]])

    tile_4 = Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])

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

    start_position = Position(9, 8, Square(2, 2))
    end_position = tile_1.move_along_path(start_position, Square(3, 2))
    assert end_position.get_player_coordinates() == (11,9)
    assert end_position.square.x == 3
    assert end_position.square.y == 2

    start_position = Position(9, 13, Square(3, 4))
    end_position = tile_2.move_along_path(start_position, Square(2, 4))
    assert end_position.get_player_coordinates() == (7,12)
    assert end_position.square.x == 2
    assert end_position.square.y == 4

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
