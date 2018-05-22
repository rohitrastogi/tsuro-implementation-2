from tile import Tile
from position import Position
from square import Square
from sPlayer import SPlayer
from board import Board
from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
import administrator
import random
from server import Server

if __name__ == "__main__":
    least = 0
    most = 0
    r = 0

    while True:
        s = Server()
        s.register_player(RandomPlayer('Upasna'))
        s.register_player(LeastSymmetricPlayer('Amulya'))
        s.register_player(MostSymmetricPlayer("Rohit"))
        game_over = s.play_game()
        
        if not isinstance(game_over, bool):
            for player in game_over:
                if player.get_name() == 'Upasna':
                    r += 1
                if player.get_name() == 'Amulya':
                    least += 1
                if player.get_name() == 'Rohit':
                    most += 1
        print ("Who won?: ", game_over)

    print ("Least: ", least)
    print ("Most: ", most)
    print ("Random: ", r)
