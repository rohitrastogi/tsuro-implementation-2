import xml2obj
import obj2xml
import socket
import sys
from randomPlayer import RandomPlayer
from xml.etree.ElementTree import fromstring

class NetworkAdministrator:

    def __init__(self, player, host, port):
        self.player = player
        self.command_handler = {
            "get-name" : player.getName,
            "initialize" : player.initialize,
            "place-pawn" : player.place_pawn,
            "play-turn" : player.play_turn,
            "end-game" : player.endgame
        }
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.sock:
            self.sock.connect((host, port))
            print("Connected to server at (host, port): " + (host, port))
        

    def listen(self):
        end_game = False
        while True: 
            received = str(self.sock.recv(4096), "utf-8")
            received_xml = fromstring(received)
            print("Received XML: " + received_xml)
            interpreted_command = xml2obj.interpret_command(received_xml)
            func, args = (interpreted_command[0], interpreted_command[1:])
            if func == "end-game":
                end_game = True
            to_send = self.command_handler[func](*args)
            to_send_xml = obj2xml.interpret_output(func, to_send) 
            print("Sent XML: " + to_send_xml)
            self.sock.send(bytes(to_send_xml, "utf-8"))
            if end_game:
                self.end_connection()
                break

    def end_connection(self):
        print("Game Over - Disconnecting Socket!")
        self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()


def main():
    #connect to server
    rohit = RandomPlayer('Rohit')
    rohit_admin = NetworkAdministrator(rohit, sys.argv[0], int(sys.argv[1]))
    rohit_admin.listen()


