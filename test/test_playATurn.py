from src.mPlayer import MPlayer
from src.sPlayer import SPlayer
from board import Board
from tile import Tile
from position import Position
from square import Square
from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
import gameConstants as constants 
import administrator
import pytest

def test_playATurn_1():
    '''
    Player one is eliminated because they play a tile that eliminates them, all of player_1's tiles are added back to the draw pile.
    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(11, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = administrator.create_draw_pile()

    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)
    player_4.initialize_hand(draw_pile)

    draw_pile = [Tile(35, [[0, 5], [1, 3], [2, 6], [4, 7]])]
    player_1.tiles_owned = [Tile(15, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(16, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    tile_1 = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile_1)
    assert len(eliminated) == 1
    assert len(draw_pile) == 3
    assert len(players) == 3
    assert board.tiles[0][0] == tile_1
    assert not game_over

def test_playATurn_2():
    '''
    Test case where player one is eliminated and player three has dragon tile.
    Expected behavior is that player 3 and 4 will draw cards from the draw_pile.
    No one at the end will have a dragon tile.
    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(11, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = administrator.create_draw_pile()

    player_1.initialize_hand(draw_pile)
    player_2.initialize_hand(draw_pile)

    player_3.tiles_owned = [Tile(34, [[0, 5], [1, 6], [2, 7], [3, 4]]), Tile(33, [[0, 2], [1, 3], [4, 6], [5, 7]])]
    player_4.tiles_owned = [Tile(4, [[0, 2], [1, 4], [3, 7], [5, 6]]), Tile(5, [[0, 4], [1, 7], [2, 3], [5, 6]])]
    player_3.dragon_held = True

    draw_pile = [Tile(35, [[0, 5], [1, 3], [2, 6], [4, 7]])]
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    tile_1 = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile_1)
    assert len(eliminated) == 1
    assert len(draw_pile) == 1
    assert len(players) == 3
    assert board.tiles[0][0] == tile_1
    assert not game_over

def test_playATurn_3():
    '''
    Player one is eliminated so two tiles are added to the draw pile.
    Player three and four each get a tile and dragon tile is passed on to two.
    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(11, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = administrator.create_draw_pile()

    player_2.tiles_owned = [Tile(34, [[0, 5], [1, 6], [2, 7], [3, 4]]), Tile(31, [[0, 5], [1, 6], [2, 7], [3, 4]])]
    player_3.tiles_owned = [Tile(34, [[0, 5], [1, 6], [2, 7], [3, 4]])]
    player_4.tiles_owned = [Tile(4, [[0, 2], [1, 4], [3, 7], [5, 6]])]
    player_3.dragon_held = True

    draw_pile = []
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(35, [[0, 5], [1, 3], [2, 6], [4, 7]])]
    tile_1 = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile_1)
    assert len(eliminated) == 1
    assert len(draw_pile) == 0
    assert len(players) == 3
    assert board.tiles[0][0] == tile_1
    assert not game_over
    assert player_2.dragon_held

def test_playATurn_4():
    '''
    If there are no cards in the draw pile, and dragon tile is not currently held,
    the player who played will receive the dragon tile.
    '''

    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(11, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    board = Board([player_4, player_2, player_3, player_1])
    draw_pile = administrator.create_draw_pile()

    player_1.initialize_hand(draw_pile)
    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)
    player_4.tiles_owned = [Tile(16, [[0, 2], [1, 4], [3, 7], [5, 6]]), Tile(18, [[0, 5], [1, 6], [2, 7], [3, 4]])]
    draw_pile = []
    tile_1 = Tile(0, [[0, 5], [1, 4], [2, 7], [3, 6]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile_1)
    assert len(eliminated) == 0
    assert len(draw_pile) == 0
    assert len(players) == 4
    assert board.tiles[0][1] == tile_1
    assert not game_over
    assert player_4.dragon_held

def test_playATurn_5():
    '''
    Player one is eliminated and Player 4 has dragon tile.
    Player 4 draws a tile and no one is given a dragon tile.
    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(11, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = administrator.create_draw_pile()

    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)

    draw_pile = [Tile(35, [[0, 5], [1, 3], [2, 6], [4, 7]])]
    player_1.tiles_owned = [Tile(12, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(13, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.tiles_owned = [Tile(14, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(15, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.dragon_held = True
    tile_1 = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile_1)
    assert len(eliminated) == 1
    assert len(draw_pile) == 2
    assert len(players) == 3
    assert board.tiles[0][0] == tile_1
    assert not game_over
    assert len(player_4.tiles_owned) == 3
    for player in players:
        assert not player.dragon_held

def test_playATurn_6():
    '''
    Player one is eliminated.
    Since they are the last player, game_over is set to player one.
    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(11, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    eliminated = [player_2, player_3, player_4]
    board = Board([player_1])
    draw_pile = administrator.create_draw_pile()

    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)
    player_4.initialize_hand(draw_pile)

    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    tile_1 = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, eliminated, board, tile_1)
    assert len(eliminated) == 4
    assert len(players) == 0
    assert board.tiles[0][0] == tile_1
    assert game_over[0].color == player_1.color

def test_playATurn_7():
    '''
    There is only one player in the game so game_over returns the player.
    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(11, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    eliminated = [player_2, player_3, player_4]
    board = Board([player_1])
    draw_pile = administrator.create_draw_pile()

    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)
    player_4.initialize_hand(draw_pile)

    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    tile_1 = Tile(0, [[0, 6], [1, 5], [2, 4], [3, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, eliminated, board, tile_1)
    assert len(eliminated) == 3
    assert len(players) == 1
    assert board.tiles[0][0] == tile_1
    assert game_over[0].color == player_1.color

def test_playATurn_8():
    '''
    Two players eliminated each other,
    since there are no other players game-over is True and returns these two players.
    // also tests making a move where multiple players are eliminated
    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(0, 2))

    board = Board([player_1, player_2])
    draw_pile = administrator.create_draw_pile()
    player_2.initialize_hand(draw_pile)
    player_1.tiles_owned = [Tile(3, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(4, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    tile_1 = Tile(7, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile[2:], board.current_players, [], board, tile_1)
    assert len(eliminated) == 2
    assert len(players) == 0
    assert board.tiles[0][0] == tile_1
    assert game_over[0].color == player_2.color
    assert game_over[1].color == player_1.color

def test_playATurn_9():
    '''
    35 tiles are played on the board and there are still players alive.
    Game-over is true and returns the remaining players.
    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(0, 8))
    board = Board([player_1, player_2])
    draw_pile = administrator.create_draw_pile()

    tile_1 = Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])
    tile_temp = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    board.tiles = []
    for i in range(constants.BOARD_DIMENSION):
        temp = []
        for j in range(constants.BOARD_DIMENSION):
            temp.append(tile_temp)
        board.tiles.append(temp)
    board.tiles[0][0] = None
    board.tiles[1][0] = None
    board.num_tiles = 34
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile_1)
    assert len(eliminated) == 0
    assert len(players) == 2
    assert board.tiles[0][0] == tile_1
    assert game_over[0].color == player_2.color
    assert game_over[1].color == player_1.color


def test_playATurn_10():
    '''
    making a move from the edge
    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    board = Board([player_1])
    draw_pile = administrator.create_draw_pile()
    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 1
    assert players[0].get_coordinates() == (3,2)

def test_playATurn_11():
    '''
    making a move that causes a token to cross multiple tiles
    '''

    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    board = Board([player_1])
    draw_pile = administrator.create_draw_pile()
    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    board.tiles[1][0] = Tile(2, [[0,3],[1,4],[2,7],[5,6]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 1
    assert players[0].get_coordinates() == (6,2)

def test_playATurn_12():
    '''
    making a move where multiple players move at once
    '''

    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(0, 2))
    board = Board([player_1, player_2])
    draw_pile = administrator.create_draw_pile()
    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    board.tiles[1][0] = Tile(2, [[0,3],[1,4],[2,7],[5,6]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 2
    assert player_1.get_coordinates() == (6,2)
    assert player_2.get_coordinates() == (2,3)
    assert game_over == False

def test_playATurn_13():
    '''
    making a move where multiple players move at once

    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(0, 2))
    board = Board([player_1, player_2])
    draw_pile = administrator.create_draw_pile()
    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    board.tiles[1][0] = Tile(2, [[0,3],[1,4],[2,7],[5,6]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 2
    assert player_1.get_coordinates() == (6,2)
    assert player_2.get_coordinates() == (2,3)
    assert game_over == False

def test_playATurn_14():
    '''
    moving where no player has the dragon tile before or after

    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(11, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = administrator.create_draw_pile()
    player_1.tiles_owned = [Tile(9, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(10, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)
    player_4.initialize_hand(draw_pile)

    tile = Tile(11, [[0, 3],[1,7], [2,6], [4,5]])
    for player in board.current_players:
        assert not player.dragon_held
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile[3:], board.current_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 4
    assert board.tiles[0][0] == tile
    assert not game_over
    for player in board.current_players:
        assert not player.dragon_held

def test_playATurn_15():
    '''
    moving where one player has the dragon tile before and no one gets any new tiles
    '''

    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(11, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = []
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])]
    player_2.tiles_owned = [Tile(2, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(3, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_3.tiles_owned = [Tile(4, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(5, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.tiles_owned = [Tile(6, [[0, 1], [2, 4], [3, 6], [5, 7]])]
    player_4.dragon_held = True

    tile = Tile(7, [[0, 3],[1,7], [2,6], [4,5]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 4
    assert board.tiles[0][0] == tile
    assert not game_over
    assert player_4.dragon_held
    assert len(player_1.tiles_owned) == 1
    assert len(player_2.tiles_owned) == 2
    assert len(player_3.tiles_owned) == 2
    assert len(player_4.tiles_owned) == 1


def test_playATurn_16():
    '''
    moving where one player has the dragon tile before and no one gets any new tiles
    '''

    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(2, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = []
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])]
    player_2.tiles_owned = [Tile(2, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(3, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_3.tiles_owned = [Tile(4, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(5, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.tiles_owned = [Tile(6, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(7, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_1.dragon_held = True

    tile = Tile(8, [[0, 3],[1,7], [2,6], [4,5]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile)
    assert len(eliminated) == 1
    assert len(players) == 3
    assert board.tiles[0][0] == tile
    assert not game_over
    assert player_4.dragon_held

def test_playATurn_17():
    '''
    moving where the player that has the dragon tile makes a move that causes themselves to be eliminated
    moving where the player that has the dragon tile makes a move that causes an elimination (of another player)

    '''

    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(2, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = []
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])]
    player_2.tiles_owned = [Tile(2, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(3, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_3.tiles_owned = [Tile(4, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(5, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.tiles_owned = [Tile(6, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(7, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_1.dragon_held = True

    tile = Tile(1, [[0, 1],[2,3], [4,5], [6,7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile)
    assert len(eliminated) == 2
    assert len(players) == 2
    assert len(draw_pile) == 1
    assert board.tiles[0][0] == tile
    assert not game_over
    for player in players:
        assert not player.dragon_held

def test_playATurn_18():
    '''
    moving where a player that does not have the dragon tile makes a move and it causes an elimination of the player that has the dragon tile

    '''

    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_2 = SPlayer(color = 'red', position = Position(2, 0))
    player_3 = SPlayer(color = 'green', position = Position(18, 8))
    player_4 = SPlayer(color = 'sienna', position = Position(0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = []
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_2.tiles_owned = [Tile(3, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(4, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_3.tiles_owned = [Tile(5, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(6, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.tiles_owned = [Tile(7, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(8, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_2.dragon_held = True

    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile)
    assert len(eliminated) == 1
    assert len(players) == 3
    assert len(draw_pile) == 0
    assert board.tiles[0][0] == tile
    assert not game_over
    assert player_1.dragon_held
    assert not player_2.dragon_held
    assert not player_3.dragon_held
    assert not player_4.dragon_held

def test_playATurn_19():
    '''
    a player plays two turns
    this is to check that all fields of the player and board are being properly updated

    '''
    player_1 = SPlayer(color = 'blue', position = Position(0, 1))
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 7], [1, 2], [3, 4], [5, 6]])]
    board = Board([player_1])
    draw_pile = []

    tile_1 = Tile(3, [[0, 5], [1, 6], [2, 7], [3, 4]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile_1)
    assert board.tiles[0][0] == tile_1
    assert player_1.get_coordinates() == (2,3)

    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])]
    tile_2 = Tile(2, [[0, 7], [1, 2], [3, 4], [5, 6]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, tile_2)
    assert board.tiles[0][1] == tile_2
    assert player_1.get_coordinates() == (3,4)
    assert player_1.position.square == Square(0,1)


# def test_validateHand_1():
#     """
#     server checks whether hand validation does not throw exception when hands are valid
#     """
#     draw_pile = administrator.create_draw_pile()
#
#     player_1 = SPlayer(color = 'blue', position = Position(0, 1))
#     player_2 = SPlayer(color = 'red', position = Position(0, 11))
#     player_3 = SPlayer(color = 'sienna', position = Position(0, 5))
#
#     player_1.tiles_owned = draw_pile[:2]
#     player_2.tiles_owned = draw_pile[2:5]
#     player_3.tiles_owned = draw_pile[5:8]
#     to_play_tile = draw_pile[8]
#
#     draw_pile = draw_pile[9:]
#
#     players = [player_1, player_2, player_3]
#     board = Board(players)
#
#     #should not throw exception
#     new_draw_pile, new_players, eliminated, new_board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, to_play_tile)
#
# def test_validateHand_2():
#     """
#     server checks whether hand validation throws exception when current player owns a tile in the draw pile
#     """
#     draw_pile = administrator.create_draw_pile()
#
#     player_1 = SPlayer(color = 'blue', position = Position(0, 1))
#     player_2 = SPlayer(color = 'red', position = Position(0, 11))
#     player_3 = SPlayer(color = 'sienna', position = Position(0, 5))
#
#     player_1.tiles_owned = draw_pile[:2]
#     dup_tile = player_1.tiles_owned[0]
#     player_2.tiles_owned = draw_pile[2:5]
#     player_3.tiles_owned = draw_pile[5:8]
#     to_play_tile = draw_pile[8]
#
#     draw_pile = draw_pile[9:].append(dup_tile)
#
#     players = [player_1, player_2, player_3]
#     board = Board(players)
#
#     with pytest.raises(Exception):
#         new_draw_pile, new_players, eliminated, new_board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, to_play_tile)
#
# def test_validateHand_3():
#     """
#     server checks whether hand validation throws exception when current player owns a tile in another player's hands
#     """
#     draw_pile = administrator.create_draw_pile()
#
#     player_1 = SPlayer(color = 'blue', position = Position(0, 1))
#     player_2 = SPlayer(color = 'red', position = Position(0, 11))
#     player_3 = SPlayer(color = 'sienna', position = Position(0, 5))
#
#     player_1.tiles_owned = draw_pile[:2]
#     player_2.tiles_owned = draw_pile[1:4]
#     player_3.tiles_owned = draw_pile[4:7]
#     to_play_tile = draw_pile[7]
#
#     draw_pile = draw_pile[8:]
#
#     players = [player_1, player_2, player_3]
#     board = Board(players)
#
#     with pytest.raises(Exception):
#         new_draw_pile, new_players, eliminated, new_board, game_over = administrator.play_a_turn(draw_pile, board.current_players, [], board, to_play_tile)
