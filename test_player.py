from player import Player
from board import Board
from tile import Tile
from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
import administrator
import pytest

def test_playerInitialization():
    player_1 = Player('Upasna', 'blue', (0, 1))
    player_2 = Player('Amulya', 'red', (11, 0))
    with pytest.raises(Exception):
        player_3 = Player('Amulya', 'green', (19, 8))
    with pytest.raises(Exception):
        player_4 = Player('Amulya', 'orange', (12, 0))

def test_initialize():
    player_1 = Player()
    player_1.initialize('blue', ['green', 'darkgreen'])

    assert player_1.color == 'blue'
    assert player_1.other_colors == ['green', 'darkgreen']

    player_2 = Player()
    player_2.initialize('green', ['blue', 'darkgreen'])

    assert player_2.color == 'green'
    assert player_2.other_colors == ['blue', 'darkgreen']

def test_placePawn():
    player_1 = Player()
    player_1.initialize('blue', ['green', 'darkgreen'])
    board = Board([player_1])
    assert player_1.position == None

    player_1.place_pawn(board)

    valid_positions = [i for i in range(19) if i%3!=0]
    case_1 = (player_1.position[0] == 0 or player_1.position[0] == 18) and player_1.position[1] in valid_positions
    case_2 = (player_1.position[1] == 0 or player_1.position[1] == 18) and player_1.position[0] in valid_positions
    assert case_1 or case_2
    assert player_1.position != (19,19)

def test_drawTile():
    draw_pile = administrator.create_draw_pile()
    player_1 = Player('Upasna', 'blue', (0, 1))
    player_1.draw_tile(draw_pile)
    assert len(player_1.tiles_owned) == 1
    assert len(draw_pile) == 34

    player_2 = Player('Upasna', 'green', (11, 0))
    player_2.draw_tile(draw_pile)
    assert len(player_2.tiles_owned) == 1
    assert len(draw_pile) == 33

def test_initializeHand():
    draw_pile = administrator.create_draw_pile()
    player_1 = Player('Upasna', 'blue', (0, 1))
    player_1.initialize_hand(draw_pile)
    assert len(player_1.tiles_owned) == 3
    assert len(draw_pile) == 32

    player_2 = Player('Amulya', 'green', (11, 0))
    player_2.initialize_hand(draw_pile)
    assert len(player_2.tiles_owned) == 3
    assert len(draw_pile) == 29

def test_loseTiles():
    draw_pile = administrator.create_draw_pile()
    player_1 = Player('Amulya', 'blue', (0, 1))
    player_1.initialize_hand(draw_pile)
    player_2 = Player('Amulya', 'green', (11, 0))
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
    player_1 = Player('Michael', 'blue', (0, 1))
    player_1.tiles_owned = [Tile(12, [[0, 7], [1, 2], [3, 4], [5, 6]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])]
    player_1.play_tile(tile_1)
    assert len(player_1.tiles_owned) == 2

def test_RandomPlayer_initialize():
    """
    Just checking to make sure that the derived class properly uses the base class
    """
    player_1 = RandomPlayer('Julie')
    player_1.initialize('blue', ['green', 'darkgreen'])

    assert player_1.name == 'Julie'
    assert player_1.color == 'blue'
    assert player_1.other_colors == ['green', 'darkgreen']

def test_RandomPlayer_playTurn():
    player_1 = RandomPlayer('Julie')
    player_1.initialize('blue', ['green', 'red'])
    board = Board([player_1])
    board.tiles[0][0] = Tile(0, [[0,6],[1,2],[3,4],[5,7]])
    player_1.place_pawn(board)
    player_1.position = (4, 0)
    player_1.square = (1, -1)

    # In this scenario, both these tiles cause elimination
    tile_1 = Tile(1, [[0, 1],[2,3], [4,5], [6,7]])
    tile_2 = Tile(2, [[0, 7],[1,2], [3,4], [5,6]])

    hand = [tile_1, tile_2]
    player_1.tiles_owned = hand
    assert player_1.play_turn(board, hand, 33).identifier == 1 or player_1.play_turn(board, hand, 33).identifier == 2

    # tile_3 in its current orientation will cause elimination, but after one rotation will be legal
    tile_3 = Tile(3, [[0, 7],[1,2], [3,6], [4,5]])
    hand = [tile_1, tile_2, tile_3]
    player_1.tiles_owned = hand
    tile_played = player_1.play_turn(board, hand, 33)
    assert tile_played.identifier == 3
    assert tile_played.paths == [[0,5],[1,2],[3,4],[6,7]]

    # tile_3 in its current orientation will cause elimination, but after four rotations will be legal
    tile_3 = Tile(3, [[0, 1],[2,7], [3,4], [5,6]])
    hand = [tile_1, tile_2, tile_3]
    player_1.tiles_owned = hand
    tile_played = player_1.play_turn(board, hand, 33)
    assert tile_played == tile_3
    assert tile_played.identifier == 3
    assert tile_played.paths == [[0,5],[1,2],[3,4],[6,7]]

def test_LeastSymmetricPlayer_playTurn():
    player_1 = LeastSymmetricPlayer('Julie')
    player_1.initialize('blue', ['green', 'red'])
    board = Board([player_1])
    player_1.place_pawn(board)

    # In the current position, this player should play tile_1 in the rotation it is given in
    # tile_1 is the least symmetric tile and will not eliminate the player
    player_1.position = (4, 0)
    player_1.square = (1, -1)
    tile_1 = Tile(1, [[0, 3], [1, 6], [2, 5], [4, 7]])
    tile_2 = Tile(2, [[0, 1], [2, 7], [3, 6], [4, 5]])
    tile_3 = Tile(3, [[0, 6], [1, 2], [3, 7], [4, 5]])

    hand = [tile_3, tile_1, tile_2]
    player_1.tiles_owned = hand
    tile_played = player_1.play_turn(board, hand, 33)
    assert tile_played == tile_1
    assert tile_played.paths == [[0, 3], [1, 6], [2, 5], [4, 7]]

    # In the current position with there being an additional tile on the board,
    # this player should play tile_2 after it has been rotated once
    # tile_1  while less symmetric than tile_2, cause elimination
    player_1.position = (2, 0)
    player_1.square = (0, -1)
    board.tiles[0][1] = Tile(4, [[0, 7], [1, 2], [3, 4], [5, 6]])
    tile_1 = Tile(1, [[0, 3], [1, 6], [2, 5], [4, 7]])
    tile_2 = Tile(2, [[0, 1], [2, 7], [3, 6], [4, 5]])
    tile_3 = Tile(3, [[0, 6], [1, 2], [3, 7], [4, 5]])

    hand = [tile_3, tile_1, tile_2]
    player_1.tiles_owned = hand
    tile_played = player_1.play_turn(board, hand, 33)
    assert tile_played == tile_2
    assert tile_played.paths == [[0, 5], [1, 4], [2, 3], [6, 7]]

def test_MostSymmetricPlayer_playTurn():
    player_1 = MostSymmetricPlayer('Julie')
    player_1.initialize('blue', ['green', 'red'])
    board = Board([player_1])
    player_1.place_pawn(board)
    # In the current position, this player should play tile_3 after rotating it once
    # tile_3 is the most symmetric tile
    player_1.position = (4, 0)
    player_1.square = (1, -1)
    tile_1 = Tile(1, [[0, 3], [1, 6], [2, 5], [4, 7]])
    tile_2 = Tile(2, [[0, 1], [2, 7], [3, 6], [4, 5]])
    tile_3 = Tile(3, [[0, 6], [1, 2], [3, 7], [4, 5]])

    hand = [tile_1, tile_3, tile_2]
    player_1.tiles_owned = hand
    tile_played = player_1.play_turn(board, hand, 33)
    assert tile_played == tile_3
    assert tile_played.paths == [[0, 2], [1, 5], [3, 4], [6, 7]]

    # In the current position with there being an additional tile on the board,
    # this player should play tile_1 in the orientation it is given in
    # tile_3 and tile_2 while more symmetric than tile_1, cause elimination and cannot be played
    player_1.position = (1, 0)
    player_1.square = (0, -1)
    board.tiles[0][1] = Tile(4, [[0, 3], [1, 2], [4, 7], [5, 6]])
    tile_1 = Tile(1, [[0, 3], [1, 6], [2, 5], [4, 7]])
    tile_2 = Tile(2, [[0, 1], [2, 7], [3, 6], [4, 5]])
    tile_3 = Tile(3, [[0, 6], [1, 2], [3, 7], [4, 5]])

    hand = [tile_2, tile_1, tile_3]
    player_1.tiles_owned = hand
    tile_played = player_1.play_turn(board, hand, 33)
    assert tile_played == tile_1
    assert tile_played.paths == [[0, 3], [1, 6], [2, 5], [4, 7]]
