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

def test_moveAcrossBoard_1():
    board = Board()
    player_1 = Player()
    player_1.initialize('blue', ['green', 'darkgreen'])
    player_1.place_pawn(board)
    player_1.position = (4,0)
    player_1.square = (1,-1)

    tile_1 = Tile(1, [[0,2],[1,5],[3,7],[4,6]])
    tile_2 = Tile(2, [[0,3],[1,6],[2,4],[5,7]])
    tile_3 = Tile(3, [[0,5],[1,4],[2,7],[3,6]])
    tile_4 = Tile(4, [[0,1],[2,6],[3,7],[4,5]])
    tile_5 = Tile(5, [[0,3],[1,2],[4,7],[5,6]])

    board.place_tile((1,0), tile_1)
    board.place_tile((1,1), tile_2)
    board.place_tile((2,1), tile_3)
    board.place_tile((3,1), tile_4)
    board.place_tile((4,1), tile_5)

    final_position, final_square, hit_a_wall_bool = board.move_across_board(player_1, tile_1)
    assert final_position == (13,3)
    assert final_square == (4,1)
    assert not hit_a_wall_bool

def test_moveAcrossBoard_2():
    board = Board()
    player_1 = Player()
    player_1.initialize('blue', ['green', 'darkgreen'])
    player_1.place_pawn(board)
    player_1.position = (4,0)
    player_1.square = (1,-1)

    tile_1 = Tile(1, [[0,2],[1,5],[3,7],[4,6]])
    tile_2 = Tile(2, [[0,3],[1,6],[2,4],[5,7]])
    tile_3 = Tile(3, [[0,5],[1,4],[2,7],[3,6]])
    tile_4 = Tile(4, [[0,1],[2,6],[3,7],[4,5]])
    tile_5 = Tile(5, [[0,3],[1,2],[4,7],[5,6]])
    tile_6 = Tile(6, [[0,2],[1,6],[3,4],[5,7]])
    tile_7 = Tile(7, [[0,3],[1,2],[4,6],[5,7]])

    board.place_tile((1,0), tile_1)
    board.place_tile((1,1), tile_2)
    board.place_tile((2,1), tile_3)
    board.place_tile((3,1), tile_4)
    board.place_tile((4,1), tile_5)
    board.place_tile((4,0), tile_6)
    board.place_tile((5,0), tile_7)

    final_position, final_square, hit_a_wall_bool = board.move_across_board(player_1, tile_1)
    assert final_position == (16,0)
    assert final_square == (5,0)
    assert hit_a_wall_bool
