import administrator
from sPlayer import SPlayer
from networkedPlayer import NetworkedPlayer
from board import Board
import gameConstants as constants
import random
import socket

class Server:
    def __init__(self, board = None, networked = True):
        self.board = Board(players = [])
        self.draw_pile = administrator.create_draw_pile()
        self.game_over = False
        self.num_players = 0
        random.shuffle(self.draw_pile)

        if networked:
            self.setup_networked_server()

    def setup_networked_server(self):
        max_connections = 3
        host = 'localhost'
        port = 9000
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(max_connections)
        self.connections = []
        while len(self.connections) < 1:
            client_socket, addr = sock.accept()
            player = NetworkedPlayer(client_socket)
            player.name = player.get_name()
            self.connections.append(player)

    def get_networked_players(self):
        return self.connections

    def play_game(self):
        self.initialize_players()
        curr_players = self.board.get_current_players()
        elim_players = self.board.get_eliminated_players()

        print ("Number of players in the game: ", len(curr_players))

        while not self.game_over:
            administrator.validate_hand(curr_players, self.draw_pile, self.board)
            acting_player = curr_players[0]
            player = acting_player.player
            current_tile = player.play_turn(self.board, acting_player.tiles_owned, len(self.draw_pile))


            print ('\n**********   State of the Game   **********')
            print ("Current player: ", acting_player.get_name())
            print ("Current player's tiles: ", [tile.identifier for tile in acting_player.tiles_owned])
            print ("Eliminated players: ", [p.get_name() for p in elim_players])
            print ("Length of draw pile: ", len(self.draw_pile))
            print ("Active players' positions: ")
            for p in curr_players:
                print("     ", p.get_name(), 'is at', p.position.x, p.position.y, 'and has', len(p.tiles_owned), 'tiles.')
            for p in curr_players:
                if p.dragon_held:
                    print (p.get_name(), 'has the dragon tile!')
            print ("Tile being played: ", current_tile.identifier, current_tile.paths)


            if not administrator.legal_play(acting_player, self.board, current_tile):
                print(acting_player.get_name() + " attempted to cheat by playing an illegal move!")
                acting_player.replace_with_random_player()
                current_tile = player.play_turn(self.board, acting_player.tiles_owned, len(self.draw_pile))
                if not administrator.legal_play(acting_player, self.board, current_tile):
                    raise RuntimeError("Received illegal move from Random Player!")
            acting_player.remove_tile_from_hand(current_tile)
            self.draw_pile, curr_players, elim_players, self.board, self.game_over = administrator.play_a_turn(self.draw_pile, curr_players, elim_players, self.board, current_tile)

            print ("Current player's tiles after turn is played: ", [tile.identifier for tile in acting_player.tiles_owned])

        return self.game_over

    def register_player(self, player):
        if self.num_players < constants.NUMBER_OF_PLAYERS:
            new_splayer = SPlayer(color = constants.Colors[self.num_players], player = player)
            self.board.add_player(new_splayer)
            self.num_players += 1
        else:
            raise RuntimeError("Tried to register too many players!")

    def initialize_players(self):
        colors = [constants.Colors[i] for i in range(self.num_players)]
        for splayer in self.board.get_current_players():
            player = splayer.player
            player.initialize(splayer.color, colors[1:])
            player.place_pawn(self.board)
            splayer.position = player.position
            splayer.initialize_hand(self.draw_pile)
            colors.append(colors.pop(0))
