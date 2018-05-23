from src.mPlayer import MPlayer
from src.sPlayer import SPlayer
from board import Board
from tile import Tile
from position import Position
from square import Square
from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
import administrator
import pytest

def test_legalPlay():
    #tile causes elimination so return false
    player_1 = Player('Michael', 'blue', Position(0, 1))
    player_1.tiles_owned = [Tile(12, [[0, 7], [1, 2], [3, 4], [5, 6]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])]
    tile_1 = Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]])
    board = Board([player_1])

    assert not administrator.legal_play(player_1, board, tile_1)

    #card not held so return false
    player_1.tiles_owned = [Tile(12, [[0, 7], [1, 2], [3, 4], [5, 6]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]])]
    tile_2 = Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])
    assert not administrator.legal_play(player_1, board, tile_2)

    #card is a legal play
    player_1.tiles_owned = [Tile(12, [[0, 7], [1, 2], [3, 4], [5, 6]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])]
    tile_3 = Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])
    assert administrator.legal_play(player_1, board, tile_3)

    #player hits another player so not legal play
    player_2 = Player('Michael', 'red', Position(11,0))
    player_2.position = Position(3, 2, Square(1, 0))
    board.tiles[1][0] = Tile(10, [[0,3],[1,2],[4,7],[5,6]])
    board.add_player(player_2)
    assert not administrator.legal_play(player_1, board, tile_3)

    # card causes eliminatiom, testing moving across two tiles
    player_1.tiles_owned = [Tile(12, [[0, 7], [1, 2], [3, 4], [5, 6]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])]
    tile_4 = Tile(20, [[0,6], [1,2], [3,5], [4,7]])
    board.tiles[1][0] = tile_4
    assert not administrator.legal_play(player_1, board, tile_3)

def test_legalPlay_2():
    '''
    if all moves are elimination moves, allows player to play current tile

    '''
    player_1 = Player('Jessica', 'blue', Position(0, 1))
    board = Board([player_1])
    player_1.tiles_owned = [Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]])]
    tile_1 = Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]])
    assert administrator.legal_play(player_1, board, tile_1)

    player_1 = Player('Jessica', 'blue', Position(0, 1))
    board = Board([player_1])
    player_1.tiles_owned = [Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(3, [[0, 5], [1, 4], [2, 7], [3, 6]])]
    tile_1 = Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]])
    assert not administrator.legal_play(player_1, board, tile_1)
