from player import Player
from board import Board
from tile import Tile
from position import Position
from square import Square
import administrator
import pytest

def test_moveAcrossBoard_1():
    board = Board()
    player_1 = Player()
    player_1.initialize('blue', ['green', 'darkgreen'])
    player_1.place_pawn(board)
    player_1.position = Position(4, 0)

    tile_1 = Tile(1, [[0,2],[1,5],[3,7],[4,6]])
    tile_2 = Tile(2, [[0,3],[1,6],[2,4],[5,7]])
    tile_3 = Tile(3, [[0,5],[1,4],[2,7],[3,6]])
    tile_4 = Tile(4, [[0,1],[2,6],[3,7],[4,5]])
    tile_5 = Tile(5, [[0,3],[1,2],[4,7],[5,6]])

    board.place_tile(Square(1,0), tile_1)
    board.place_tile(Square(1,1), tile_2)
    board.place_tile(Square(2,1), tile_3)
    board.place_tile(Square(3,1), tile_4)
    board.place_tile(Square(4,1), tile_5)

    final_position, hit_a_wall_bool = board.move_across_board(player_1, tile_1)
    assert final_position.get_player_coordinates() == (13,3)
    assert final_position.square == Square(4,1)
    assert not hit_a_wall_bool

def test_moveAcrossBoard_2():
    board = Board()
    player_1 = Player()
    player_1.initialize('blue', ['green', 'darkgreen'])
    player_1.place_pawn(board)
    player_1.position = Position(4,0)

    tile_1 = Tile(1, [[0,2],[1,5],[3,7],[4,6]])
    tile_2 = Tile(2, [[0,3],[1,6],[2,4],[5,7]])
    tile_3 = Tile(3, [[0,5],[1,4],[2,7],[3,6]])
    tile_4 = Tile(4, [[0,1],[2,6],[3,7],[4,5]])
    tile_5 = Tile(5, [[0,3],[1,2],[4,7],[5,6]])
    tile_6 = Tile(6, [[0,2],[1,6],[3,4],[5,7]])
    tile_7 = Tile(7, [[0,3],[1,2],[4,6],[5,7]])

    board.place_tile(Square(1,0), tile_1)
    board.place_tile(Square(1,1), tile_2)
    board.place_tile(Square(2,1), tile_3)
    board.place_tile(Square(3,1), tile_4)
    board.place_tile(Square(4,1), tile_5)
    board.place_tile(Square(4,0), tile_6)
    board.place_tile(Square(5,0), tile_7)

    final_position, hit_a_wall_bool = board.move_across_board(player_1, tile_1)
    assert final_position.get_player_coordinates() == (16,0)
    assert final_position.square == Square(5,0)
    assert hit_a_wall_bool
