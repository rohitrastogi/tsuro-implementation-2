from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from networkedPlayer import NetworkedPlayer
from server import Server

if __name__ == "__main__":
    s = Server(networked = True)
    networked_players = s.get_networked_players()
    for player in networked_players:
        s.register_player(player)
    local_player = LeastSymmetricPlayer('Obama')
    s.register_player(local_player)
    game_over = s.play_game()

    print ("Who won?: ", game_over)
