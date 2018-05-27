from interface import implements
from IPlayer import IPlayer
import gameConstants as constants
import random
import administrator
import obj2xml
import xml2obj
from xml.etree.ElementTree import fromstring

class NetworkedPlayer(implements(IPlayer)):
    def __init__(self, socket): 
        self.name = None
        self.sock = socket
        self.position = None
        self.color = None
        self.other_colors = None

    def send_and_receive(self, to_send):
        self.sock.send(bytes(to_send, 'utf-8'))
        return fromstring(self.sock.recv(4096))
    
    def get_name(self):
        to_send = obj2xml.create_get_name_xml()
        name_xml = self.send_and_receive(to_send)
        return xml2obj.construct_player_name_obj(name_xml))

    def initialize(self, color, other_colors):
        to_send = obj2xml.create_initialize_xml(color, other_colors)
        void_xml = self.send_and_receive(to_send)

    def place_pawn(self, board):
        to_send = obj2xml.create_place_pawn_xml(board)
        position_xml = self.send_and_receive(to_send)
        return xml2obj.create_position_obj(position_xml)

    def play_turn(self, board, tiles, remaining_in_pile):
        #TODO sort this update out
        #self.update_player_position(board)
        to_send = obj2xml.create_play_turn_xml(board, tiles, remaining_in_pile)
        tile_xml = self.send_and_receive(to_send)
        return xml2obj.construct_tile_object(tile_xml)

    def end_game(self, board, colors):
        to_send = obj2xml.create_end_game_xml(color, other_colors)
        void_xml = self.send_and_receive(to_send)

