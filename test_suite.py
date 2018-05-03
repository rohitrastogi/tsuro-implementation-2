from player import Player
from board import Board
from tile import Tile
from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
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
    tile_1 = Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])
    tile_2 = Tile(3, [[0, 1], [2, 7], [3, 5], [4, 6]])

    board_position = (3,2)
    start = (9,8)
    coordinates = administrator.get_coordinates(board_position)
    end = tile_1.move_along_path(start, coordinates)
    assert end == (11,9)

    board_position = (2,4)
    start = (9,13)
    coordinates = administrator.get_coordinates(board_position)
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

def test_legalPlay():

    #card causes elimination so return false
    player_1 = Player('Michael', 'blue', (0, 1))
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
    player_2 = Player('Michael', 'red', (11,0))
    player_2.position = (3,2)
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
    player_1 = Player('Jessica', 'blue', (0, 1))
    board = Board([player_1])
    player_1.tiles_owned = [Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]])]
    tile_1 = Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]])
    assert administrator.legal_play(player_1, board, tile_1)

    player_1 = Player('Jessica', 'blue', (0, 1))
    board = Board([player_1])
    player_1.tiles_owned = [Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(3, [[0, 5], [1, 4], [2, 7], [3, 6]])]
    tile_1 = Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]])
    assert not administrator.legal_play(player_1, board, tile_1)

def test_playTurn_1():
    '''
    Player one is eliminated because they play a tile that eliminates them, all player's one tiles are added back to the draw pile.
    '''
    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (11, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = administrator.create_draw_pile()

    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)
    player_4.initialize_hand(draw_pile)

    draw_pile = [Tile(35, [[0, 5], [1, 3], [2, 6], [4, 7]])]
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    tile_1 = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile_1)
    assert len(eliminated) == 1
    assert len(draw_pile) == 3
    assert len(players) == 3
    assert board.tiles[0][0] == tile_1
    assert not game_over

def test_playTurn_2():
    '''
    Test case where player one is eliminated and player three has dragon tile.
    Expected behavior is that player 3 and 4 will draw cards from the draw_pile.
    No one at the end will have a dragon tile.
    '''
    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (11, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
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
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile_1)
    assert len(eliminated) == 1
    assert len(draw_pile) == 1
    assert len(players) == 3
    assert board.tiles[0][0] == tile_1
    assert not game_over

def test_playTurn_3():
    '''
    Player one is eliminated so two tiles are added to the draw pile.
    Player three and four each get a tile and dragon tile is passed on to two.
    '''
    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (11, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = administrator.create_draw_pile()

    player_2.tiles_owned = [Tile(34, [[0, 5], [1, 6], [2, 7], [3, 4]]), Tile(31, [[0, 5], [1, 6], [2, 7], [3, 4]])]
    player_3.tiles_owned = [Tile(34, [[0, 5], [1, 6], [2, 7], [3, 4]])]
    player_4.tiles_owned = [Tile(4, [[0, 2], [1, 4], [3, 7], [5, 6]])]
    player_3.dragon_held = True

    draw_pile = []
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(35, [[0, 5], [1, 3], [2, 6], [4, 7]])]
    tile_1 = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile_1)
    assert len(eliminated) == 1
    assert len(draw_pile) == 0
    assert len(players) == 3
    assert board.tiles[0][0] == tile_1
    assert not game_over
    assert player_2.dragon_held

def test_playTurn_4():
    '''
    If there are no cards in the draw pile, and dragon tile is not currently held,
    the player who played will receive the dragon tile.
    '''

    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (11, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
    board = Board([player_4, player_2, player_3, player_1])
    draw_pile = administrator.create_draw_pile()

    player_1.initialize_hand(draw_pile)
    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)
    player_4.tiles_owned = [Tile(4, [[0, 2], [1, 4], [3, 7], [5, 6]]), Tile(34, [[0, 5], [1, 6], [2, 7], [3, 4]])]
    draw_pile = []
    tile_1 = Tile(0, [[0, 5], [1, 4], [2, 7], [3, 6]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile_1)
    assert len(eliminated) == 0
    assert len(draw_pile) == 0
    assert len(players) == 4
    assert board.tiles[0][1] == tile_1
    assert not game_over
    assert player_4.dragon_held

def test_playTurn_5():
    '''
    Player one is eliminated and Player 4 has dragon tile.
    Player 4 draws a tile and no one is given a dragon tile.
    '''
    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (11, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = administrator.create_draw_pile()

    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)

    draw_pile = [Tile(35, [[0, 5], [1, 3], [2, 6], [4, 7]])]
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.dragon_held = True
    tile_1 = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile_1)
    assert len(eliminated) == 1
    assert len(draw_pile) == 2
    assert len(players) == 3
    assert board.tiles[0][0] == tile_1
    assert not game_over
    assert len(player_4.tiles_owned) == 3
    for player in players:
        assert not player.dragon_held

def test_playTurn_6():
    '''
    Player one is eliminated.
    Since they are the last player, game_over is set to player one.
    '''
    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (11, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
    eliminated = [player_2, player_3, player_4]
    board = Board([player_1])
    draw_pile = administrator.create_draw_pile()

    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)
    player_4.initialize_hand(draw_pile)

    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    tile_1 = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, eliminated, board, tile_1)
    assert len(eliminated) == 4
    assert len(players) == 0
    assert board.tiles[0][0] == tile_1
    assert game_over[0].color == player_1.color

def test_playTurn_7():
    '''
    There is only one player in the game so game_over returns the player.
    '''
    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (11, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
    eliminated = [player_2, player_3, player_4]
    board = Board([player_1])
    draw_pile = administrator.create_draw_pile()

    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)
    player_4.initialize_hand(draw_pile)

    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    tile_1 = Tile(0, [[0, 6], [1, 5], [2, 4], [3, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, eliminated, board, tile_1)
    assert len(eliminated) == 3
    assert len(players) == 1
    assert board.tiles[0][0] == tile_1
    assert game_over.color == player_1.color

def test_playTurn_eight():
    '''
    Two players eliminated each other,
    since there are no other players game-over is True and returns these two players.
    // also tests making a move where multiple players are eliminated
    '''
    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Upasna', 'red', (0, 2))
    board = Board([player_1, player_2])
    draw_pile = administrator.create_draw_pile()
    player_2.initialize_hand(draw_pile)
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    tile_1 = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile_1)
    assert len(eliminated) == 2
    assert len(players) == 0
    assert board.tiles[0][0] == tile_1
    assert game_over[0].color == player_2.color
    assert game_over[1].color == player_1.color

def test_playTurn_nine():
    '''
    35 tiles are played on the board and there are still players alive.
    Game-over is true and returns the remaining players.
    '''
    player_1 = Player('Amulya', 'blue', (0, 1))
    player_2 = Player('Upasna', 'red', (0, 8))
    board = Board([player_1, player_2])
    draw_pile = administrator.create_draw_pile()

    tile_1 = Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])
    tile_temp = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    board.tiles = []
    for i in range(6):
        temp = []
        for j in range(6):
            temp.append(tile_temp)
        board.tiles.append(temp)
    board.tiles[0][0] = None
    board.tiles[1][0] = None
    board.num_tiles = 34
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile_1)
    assert len(eliminated) == 0
    assert len(players) == 2
    assert board.tiles[0][0] == tile_1
    assert game_over[0].color == player_2.color
    assert game_over[1].color == player_1.color


def test_playTurn_ten():
    '''
    making a move from the edge

    '''
    player_1 = Player('Upasna', 'blue', (0, 1))
    board = Board([player_1])
    draw_pile = administrator.create_draw_pile()
    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 1
    assert player_1.position == (3,2)

def test_playTurn_eleven():
    '''
    making a move that causes a token to cross multiple tiles

    '''

    player_1 = Player('Amulya', 'blue', (0, 1))
    board = Board([player_1])
    draw_pile = administrator.create_draw_pile()
    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    board.tiles[1][0] = Tile(2, [[0,3],[1,4],[2,7],[5,6]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 1
    assert player_1.position == (6,2)

def test_playTurn_12():
    '''
    making a move where multiple players move at once

    '''

    player_1 = Player('Allison', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (0,2))
    board = Board([player_1, player_2])
    draw_pile = administrator.create_draw_pile()
    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    board.tiles[1][0] = Tile(2, [[0,3],[1,4],[2,7],[5,6]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 2
    assert player_1.position == (6,2)
    assert player_2.position == (2,3)
    assert game_over == False

def test_playTurn_13():
    '''
    making a move where multiple players move at once

    '''
    player_1 = Player('John', 'blue', (0, 1))
    player_2 = Player('Emma', 'red', (0,2))
    board = Board([player_1, player_2])
    draw_pile = administrator.create_draw_pile()
    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    board.tiles[1][0] = Tile(2, [[0,3],[1,4],[2,7],[5,6]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 2
    assert player_1.position == (6,2)
    assert player_2.position == (2,3)
    assert game_over == False

def test_playTurn_14():
    '''
    moving where no player has the dragon tile before or after

    '''
    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (11, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = administrator.create_draw_pile()
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)
    player_4.initialize_hand(draw_pile)

    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    for player in board.all_players:
        assert not player.dragon_held
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 4
    assert board.tiles[0][0] == tile
    assert not game_over
    for player in board.all_players:
        assert not player.dragon_held
def test_playTurn_15():
    '''
    moving where one player has the dragon tile before and no one gets any new tiles

    '''

    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (11, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = []
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])]
    player_2.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_3.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])]
    player_4.dragon_held = True

    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile)
    assert len(eliminated) == 0
    assert len(players) == 4
    assert board.tiles[0][0] == tile
    assert not game_over
    assert player_4.dragon_held
    assert len(player_1.tiles_owned) == 1
    assert len(player_2.tiles_owned) == 2
    assert len(player_3.tiles_owned) == 2
    assert len(player_4.tiles_owned) == 1


def test_playTurn_16():
    '''
    moving where one player has the dragon tile before and no one gets any new tiles

    '''

    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (2, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = []
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])]
    player_2.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_3.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_1.dragon_held = True

    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile)
    assert len(eliminated) == 1
    assert len(players) == 3
    assert board.tiles[0][0] == tile
    assert not game_over
    assert player_4.dragon_held

def test_playTurn_16():
    '''
    moving where the player that has the dragon tile makes a move that causes an elimination (of another player)
    moving where the player that has the dragon tile makes a move that causes themselves to be eliminated

    '''
    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (2, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = []
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])]
    player_2.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_3.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_1.dragon_held = True

    tile = Tile(1, [[0, 1],[2,3], [4,5], [6,7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile)
    assert len(eliminated) == 2
    assert len(players) == 2
    assert len(draw_pile) == 1
    assert board.tiles[0][0] == tile
    assert not game_over
    for player in players:
        assert not player.dragon_held

def test_playTurn_16():
    '''
    moving where a player that does not have the dragon tile makes a move and it causes an elimination of the player that has the dragon tile

    '''
    player_1 = Player('Jessica', 'blue', (0, 1))
    player_2 = Player('Michael', 'red', (2, 0))
    player_3 = Player('Upasna', 'orange', (18, 8))
    player_4 = Player('Amulya', 'white', (0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = []
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_2.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_3.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_4.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 6], [1, 5], [2, 4], [3, 7]])]
    player_2.dragon_held = True

    tile = Tile(1, [[0, 3],[1,7], [2,6], [4,5]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile)
    assert len(eliminated) == 1
    assert len(players) == 3
    assert len(draw_pile) == 0
    assert board.tiles[0][0] == tile
    assert not game_over
    assert player_1.dragon_held
    assert not player_2.dragon_held
    assert not player_3.dragon_held
    assert not player_4.dragon_held

def test_playTurn_17():
    '''
    a player plays two turns
    this is to check that all fields of the player and board are being properly updated

    '''
    player_1 = Player('Jessica', 'blue', (0, 1))
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]]), Tile(2, [[0, 7], [1, 2], [3, 4], [5, 6]])]
    board = Board([player_1])
    draw_pile = []

    tile_1 = Tile(3, [[0, 5], [1, 6], [2, 7], [3, 4]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile_1)
    assert board.tiles[0][0] == tile_1
    assert player_1.position == (2,3)
    assert player_1.board_position == (0,0)

    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])]
    tile_2 = Tile(2, [[0, 7], [1, 2], [3, 4], [5, 6]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile_2)
    assert board.tiles[0][1] == tile_2
    assert player_1.position == (3,4)
    assert player_1.board_position == (0,1)


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

    player_1.position = (4, 0)
    player_1.board_position = (1, -1)

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

    # In the current position, this player should play tile_1 in the rotation it is given in
    # tile_1 is the least symmetric tile and will not eliminate the player
    player_1.position = (4, 0)
    player_1.board_position = (1, -1)
    tile_1 = Tile(1, [[0, 3], [1, 6], [2, 5], [4, 7]])
    tile_2 = Tile(2, [[0, 1], [2, 7], [3, 6], [4, 5]])
    tile_3 = Tile(3, [[0, 6], [1, 2], [3, 7], [4, 5]])

    hand = [tile_3, tile_1, tile_2]
    player_1.tiles_owned = hand
    tile_played = player_1.play_turn(board, hand, 33)
    assert tile_played == tile_1
    assert tile_played.paths == [[0, 3], [1, 6], [2, 5], [4, 7]]

    # In the current position with there being an additional tile on the board,
    # this player should play tile_3 after it has been rotated once
    # tile_1 and tile_2 while less symmetric than tile_3, cause elimination
    player_1.position = (2, 0)
    player_1.board_position = (0, -1)
    board.tiles[0][1] = Tile(4, [[0, 7], [1, 2], [3, 4], [5, 6]])
    tile_1 = Tile(1, [[0, 3], [1, 6], [2, 5], [4, 7]])
    tile_2 = Tile(2, [[0, 1], [2, 7], [3, 6], [4, 5]])
    tile_3 = Tile(3, [[0, 6], [1, 2], [3, 7], [4, 5]])

    hand = [tile_3, tile_1, tile_2]
    player_1.tiles_owned = hand
    tile_played = player_1.play_turn(board, hand, 33)
    assert tile_played == tile_3
    assert tile_played.paths == [[0, 2], [1, 5], [3, 4], [6, 7]]

def test_MostSymmetricPlayer_playTurn():
    player_1 = MostSymmetricPlayer('Julie')
    player_1.initialize('blue', ['green', 'red'])
    board = Board([player_1])

    # In the current position, this player should play tile_3 after rotating it once
    # tile_3 is the most symmetric tile
    player_1.position = (4, 0)
    player_1.board_position = (1, -1)
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
    player_1.board_position = (0, -1)
    board.tiles[0][1] = Tile(4, [[0, 3], [1, 2], [4, 7], [5, 6]])
    tile_1 = Tile(1, [[0, 3], [1, 6], [2, 5], [4, 7]])
    tile_2 = Tile(2, [[0, 1], [2, 7], [3, 6], [4, 5]])
    tile_3 = Tile(3, [[0, 6], [1, 2], [3, 7], [4, 5]])

    hand = [tile_2, tile_1, tile_3]
    player_1.tiles_owned = hand
    tile_played = player_1.play_turn(board, hand, 33)
    assert tile_played == tile_1
    assert tile_played.paths == [[0, 3], [1, 6], [2, 5], [4, 7]]
