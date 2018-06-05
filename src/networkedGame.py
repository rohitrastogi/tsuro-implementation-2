from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
from networkedPlayer import NetworkedPlayer
from server import Server
import sys

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else None
    s = Server(networked = True, port = port)
    networked_players = s.get_networked_players()
    local_players = [LeastSymmetricPlayer('Obama'), MostSymmetricPlayer('Michelle')]
    for player in networked_players:
        s.register_player(player)
    for player in local_players:
        s.register_player(player)
    game_over = s.play_game()

    print ("Who won?: ", game_over)
