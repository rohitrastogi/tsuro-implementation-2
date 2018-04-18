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

def test_drawTile():
    draw_pile = administrator.create_draw_pile()
    player_1 = Player('blue', (0, 1))
    player_1.draw_tile(draw_pile)
    assert len(player_1.tiles_owned) == 1
    assert len(draw_pile) == 34

    player_2 = Player('green', (11, 0))
    player_2.draw_tile(draw_pile)
    assert len(player_2.tiles_owned) == 1
    assert len(draw_pile) == 33

def test_initializeHand():
    draw_pile = administrator.create_draw_pile()
    player_1 = Player('blue', (0, 1))
    player_1.initialize_hand(draw_pile)
    assert len(player_1.tiles_owned) == 3
    assert len(draw_pile) == 32

    player_2 = Player('green', (11, 0))
    player_2.initialize_hand(draw_pile)
    assert len(player_2.tiles_owned) == 3
    assert len(draw_pile) == 29

def test_loseTiles():
    draw_pile = administrator.create_draw_pile()
    player_1 = Player('blue', (0, 1))
    player_1.initialize_hand(draw_pile)
    player_2 = Player('green', (11, 0))
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
    player_1 = Player('blue', (0, 1))
    player_1.tiles_owned = [Tile(12, [[0, 7], [1, 2], [3, 4], [5, 6]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])]
    player_1.play_tile(tile_1)
    assert len(player_1.tiles_owned) == 2

def test_rotateTile():
    tile_1 = Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])
    tile_2 = Tile(3, [[0, 1], [2, 7], [3, 5], [4, 6]])

    tile_1.rotate_tile()
    assert tile_1.paths == [[2, 5], [1, 3], [0, 4], [6, 7]]
    tile_1.rotate_tile()
    assert tile_1.paths == [[4, 7], [3, 5], [2, 6], [0, 1]]
    tile_2.rotate_tile()
    assert tile_2.paths == [[2, 3], [1, 4], [5, 7], [0, 6]]

def test_legalPlay():
    player_1 = Player('blue', (0, 1))
    player_1.tiles_owned = [Tile(12, [[0, 7], [1, 2], [3, 4], [5, 6]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])]
    tile_1 = Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]])
    board = Board([player_1])

    assert not administrator.legal_play(player_1, board, tile_1)
    player_1.tiles_owned = [Tile(12, [[0, 7], [1, 2], [3, 4], [5, 6]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]])]
    tile_2 = Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])
    assert not administrator.legal_play(player_1, board, tile_2)

    player_1.tiles_owned = [Tile(12, [[0, 7], [1, 2], [3, 4], [5, 6]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])]
    tile_3 = Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])
    assert administrator.legal_play(player_1, board, tile_3)

    player_2 = Player('red', (11,0))
    player_2.position = (3,2)
    board.add_player(player_2)
    assert not administrator.legal_play(player_1, board, tile_3)

    player_1.tiles_owned = [Tile(12, [[0, 7], [1, 2], [3, 4], [5, 6]]), Tile(3, [[0, 1], [2, 3], [4, 5], [6, 7]]), Tile(17, [[0, 3], [1, 7], [2, 6], [4, 5]])]
    tile_4 = Tile(20, [[0,6], [1,2], [3,5], [4,7]])
    board.tiles[1][0] = tile_4
    assert not administrator.legal_play(player_1, board, tile_3)

def test_playTurn():
    # Test 1
    player_1 = Player('blue', (0, 1))
    player_2 = Player('red', (11, 0))
    player_3 = Player('orange', (18, 8))
    player_4 = Player('white', (0, 5))
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

    # Test 2
    player_1 = Player('blue', (0, 1))
    player_2 = Player('red', (11, 0))
    player_3 = Player('orange', (18, 8))
    player_4 = Player('white', (0, 5))
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

    # Test 3
    player_1 = Player('blue', (0, 1))
    player_2 = Player('red', (11, 0))
    player_3 = Player('orange', (18, 8))
    player_4 = Player('white', (0, 5))
    board = Board([player_1, player_2, player_3, player_4])
    draw_pile = administrator.create_draw_pile()

    player_1.initialize_hand(draw_pile)
    player_2.tiles_owned = [Tile(34, [[0, 5], [1, 6], [2, 7], [3, 4]]), Tile(31, [[0, 5], [1, 6], [2, 7], [3, 4]])]
    player_3.tiles_owned = [Tile(34, [[0, 5], [1, 6], [2, 7], [3, 4]])]
    player_4.tiles_owned = [Tile(4, [[0, 2], [1, 4], [3, 7], [5, 6]])]
    player_3.dragon_held = True

    draw_pile = [Tile(35, [[0, 5], [1, 3], [2, 6], [4, 7]])]
    player_1.tiles_owned = [Tile(1, [[0, 1], [2, 4], [3, 6], [5, 7]])]
    tile_1 = Tile(0, [[0, 1], [2, 3], [4, 5], [6, 7]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile_1)
    assert len(eliminated) == 1
    assert len(draw_pile) == 0
    assert len(players) == 3
    assert board.tiles[0][0] == tile_1
    assert not game_over
    assert player_2.dragon_held

    # Test 4
    player_1 = Player('blue', (0, 1))
    player_2 = Player('red', (11, 0))
    player_3 = Player('orange', (18, 8))
    player_4 = Player('white', (0, 5))
    board = Board([player_4, player_2, player_3, player_1])
    draw_pile = administrator.create_draw_pile()

    player_1.initialize_hand(draw_pile)
    player_2.initialize_hand(draw_pile)
    player_3.initialize_hand(draw_pile)
    player_4.tiles_owned = [Tile(4, [[0, 2], [1, 4], [3, 7], [5, 6]]), Tile(34, [[0, 5], [1, 6], [2, 7], [3, 4]])]
    player_4.dragon_held = True

    draw_pile = []
    tile_1 = Tile(0, [[0, 5], [1, 4], [2, 7], [3, 6]])
    draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, board.all_players, [], board, tile_1)
    assert len(eliminated) == 0
    assert len(draw_pile) == 0
    assert len(players) == 4
    assert board.tiles[0][1] == tile_1
    assert not game_over
    assert player_4.dragon_held

    # Test 5
    print ("Test 5")
    player_1 = Player('blue', (0, 1))
    player_2 = Player('red', (11, 0))
    player_3 = Player('orange', (18, 8))
    player_4 = Player('white', (0, 5))
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

    # Test 6
    print ("Test 6")
    player_1 = Player('blue', (0, 1))
    player_2 = Player('red', (11, 0))
    player_3 = Player('orange', (18, 8))
    player_4 = Player('white', (0, 5))
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

    # Test 7
    print ("Test 7")
    player_1 = Player('blue', (0, 1))
    player_2 = Player('red', (11, 0))
    player_3 = Player('orange', (18, 8))
    player_4 = Player('white', (0, 5))
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

    # Test 8
    print ("Test 8")
    player_1 = Player('blue', (0, 1))
    player_2 = Player('red', (0, 2))
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

    # Test 9
    print ("Test 9")
    player_1 = Player('blue', (0, 1))
    player_2 = Player('red', (0, 8))
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
