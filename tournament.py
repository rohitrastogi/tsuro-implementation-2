from player import Player
from board import Board
from tile import Tile
from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
import administrator
import random

if __name__ == "__main__":
    least = 0
    most = 0
    r = 0

    for i in range(100):
        player_1 = RandomPlayer('Navin')
        player_1.initialize('blue', ['red', 'green'])
        player_2 = LeastSymmetricPlayer('Brandon')
        player_2.initialize('red', ['green', 'blue'])
        player_3 = MostSymmetricPlayer('Samir')
        player_3.initialize('green', ['blue', 'red'])

        board = Board([player_1, player_2, player_3])

        draw_pile = administrator.create_draw_pile()
        random.shuffle(draw_pile)
        player_1.initialize_hand(draw_pile)
        player_2.initialize_hand(draw_pile)
        player_3.initialize_hand(draw_pile)

        player_1.place_pawn(board)
        player_2.place_pawn(board)
        player_3.place_pawn(board)

        game_over = False
        eliminated = []
        players = [player_1, player_2, player_3]
        # print ("player 1's position: ", player_1.position)
        # print ("player 2's position: ", player_2.position)
        # print ("player 3's position: ", player_3.position)
        while not game_over:
            # print ("Before a turn is played.")
            # print ("------------------------------------------------------")
            current_tile = players[0].play_turn(board, players[0].tiles_owned, len(draw_pile))
            # print ("Current tile: ", current_tile.identifier)
            # print ("Number of tiles on the board: ", board.num_tiles)
            # print ("Player's location: ", players[0].position)
            draw_pile, players, eliminated, board, game_over = administrator.play_a_turn(draw_pile, players, eliminated, board, current_tile)
            # print ("After a turn is played.")
            # print ("------------------------------------------------------")
            # print ("Length of draw pile: ", len(draw_pile))
            # print ("Player colors in order: ", [p.color for p in players])
            # print ("Length of eliminated: ", len(eliminated))
            # print ("player 1's position: ", player_1.position)
            # print ("player 1's board position: ", player_1.board_position)
            # print ("player 2's position: ", player_2.position)
            # print ("player 2's board position: ", player_2.board_position)
            # print ("player 3's position: ", player_3.position)
            # print ("player 3's board position: ", player_3.board_position)
            # print ("Game over: ", game_over)
            # print ("")
            # print ("")

        if isinstance(game_over, Player):
            if game_over.name == 'Navin':
                r += 1
            if game_over.name == 'Brandon':
                least += 1
            if game_over.name == 'Samir':
                most += 1
        print ("Who won?: ", game_over)
    print ("Least: ", least)
    print ("Most: ", most)
    print ("Random: ", r)
