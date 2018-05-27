from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from networkedPlayer import NetworkedPlayer
from server import Server

if __name__ == "__main__":
    s = Server(networked = True)
    networked_players = s.getNetworkedPlayers()
    for player in networked_players:
        s.register(player)
        game_over = s.play_game()
    
    print ("Who won?: ", game_over)