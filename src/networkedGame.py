from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
from networkedPlayer import NetworkedPlayer
from server import Server

if __name__ == "__main__":
    s = Server(networked = True)
    networked_players = s.get_networked_players()
    local_players = [LeastSymmetricPlayer('Obama'), MostSymmetricPlayer('Michelle')]
    for player in networked_players:
        s.register_player(player)
    for player in local_players:
        s.register_player(player)
    game_over = s.play_game()

    print ("Who won?: ", game_over)
