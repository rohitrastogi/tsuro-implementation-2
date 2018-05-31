import xml2obj
import obj2xml
import socket
import sys
from randomPlayer import RandomPlayer
from xml.etree.ElementTree import fromstring, tostring

class NetworkAdministrator:

    def __init__(self, player, host, port):
        self.player = player
        self.command_handler = {
            "get-name" : self.player.get_name,
            "initialize" : self.player.initialize,
            "place-pawn" : self.player.place_pawn,
            "play-turn" : self.player.play_turn,
            "end-game" : self.player.end_game
        }
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        print("Connected to server at (host, port): ", host, port)

    def listen(self):
        end_game = False
        while True:
            received = self.sock.recv(8192).decode('utf-8')
            received_xml = fromstring(received)
            interpreted_command = xml2obj.interpret_command(received_xml)
            func, args = (interpreted_command[0], interpreted_command[1:])
            if func == "end-game":
                end_game = True
            to_send = self.command_handler[func](*args)
            to_send_xml = tostring(obj2xml.interpret_output(func, to_send))
            self.sock.send(to_send_xml)
            if end_game:
                self.end_connection(args)
                break

    def end_connection(self, args):
        print ("The winner(s) are: ", args[1])
        print("Game Over - Disconnecting Socket!")
        self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()


if __name__ == "__main__":
    #connect to server
    # arg 1 is name
    # arg 2 is localhost
    # arg 3 is port number
    n_player = RandomPlayer(sys.argv[1])
    player_admin = NetworkAdministrator(n_player, sys.argv[2], int(sys.argv[3]))
    player_admin.listen()
