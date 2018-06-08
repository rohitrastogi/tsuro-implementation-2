import xml2obj
import obj2xml
import socket
import sys
from randomPlayer import RandomPlayer
from mostSymmetricPlayer import MostSymmetricPlayer
from leastSymmetricPlayer import LeastSymmetricPlayer
from xml.etree.ElementTree import fromstring, tostring
import math

class NetworkAdministrator:

    def __init__(self, player, host, port):
        self.buffer_size = 512
        self.player = player
        self.command_handler = self.set_command_handler()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        print("Connecting to server at (host, port): ", host, port)


    def set_command_handler(self):
        return {
            "get-name" : self.player.get_name,
            "initialize" : self.player.initialize,
            "place-pawn" : self.player.place_pawn,
            "play-turn" : self.player.play_turn,
            "end-game" : self.player.end_game
        }

    def recv_all(self):

        def round_to_power(number):
            power = int(math.log2(number)) + 1
            return int(pow(2, power))

        received = ""
        while True:
            received += self.sock.recv(self.buffer_size).decode('utf-8')
            try:
                received_xml = fromstring(received)
                interpreted_command = xml2obj.interpret_command(received_xml)
                break
            except:
                self.buffer_size = round_to_power(len(received))
        return interpreted_command


    def listen(self):
        end_game = False
        while True:
            interpreted_command = self.recv_all() #xml2obj.interpret_command(received_xml)
            func, args = (interpreted_command[0], interpreted_command[1:])
            if func == "end-game":
                end_game = True
            to_send = self.command_handler[func](*args)
            to_send_xml = tostring(obj2xml.interpret_output(func, to_send), short_empty_elements=False) + b'\n'
            self.sock.sendall(to_send_xml)
            if end_game:
                self.resetNetworkAdmin()
                end_game = False

    def resetNetworkAdmin(self):
        self.player = RandomPlayer(sys.argv[1])
        self.command_handler = self.set_command_handler()


if __name__ == "__main__":
    #connect to server
    # arg 1 is name
    # arg 2 is localhost
    # arg 3 is port number
    n_player = LeastSymmetricPlayer(sys.argv[1])
    player_admin = NetworkAdministrator(n_player, sys.argv[2], int(sys.argv[3]))
    player_admin.listen()
