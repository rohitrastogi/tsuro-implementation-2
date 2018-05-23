from randomPlayer import RandomPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
from server import Server

if __name__ == "__main__":
    least = 0
    most = 0
    r = 0

    while True:
        s = Server()
        player_1 = RandomPlayer('Upasna')
        player_2 = LeastSymmetricPlayer('Amulya')
        player_3 = MostSymmetricPlayer("Rohit")
        s.register_player(player_1)
        s.register_player(player_2)
        s.register_player(player_3)
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
