from interface import implements
from IPlayer import IPlayer
import gameConstants as constants
import random
import administrator
import obj2xml
import xml2obj
from state import State
from xml.etree.ElementTree import fromstring, tostring

class NetworkedPlayer(implements(IPlayer)):
    def __init__(self, socket):
        self.sock = socket
        self.state = State()
        self.name = None
        self.position = None
        self.color = None
        self.other_colors = None

    def send_and_receive(self, to_send):
        self.sock.sendall(tostring(to_send, short_empty_elements=False))
        received = self.sock.recv(8192)
        return fromstring(received)

    def get_name(self):
        to_send = obj2xml.create_get_name_xml()
        name_xml = self.send_and_receive(to_send)
        self.name = xml2obj.construct_player_name_obj(name_xml)
        return self.name

    def initialize(self, color, other_colors):
        self.state.update_state("initialize")
        to_send = obj2xml.create_initialize_xml(color, other_colors)
        void_xml = self.send_and_receive(to_send)
        self.color = color
        self.other_colors = other_colors

    def place_pawn(self, board):
        self.state.update_state("place_pawn")
        to_send = obj2xml.create_place_pawn_xml(board)
        position_xml = self.send_and_receive(to_send)
        self.position = xml2obj.create_position_obj(position_xml, board)
        return self.position

    def play_turn(self, board, tiles, remaining_in_pile):
        self.state.update_state("play_turn")
        to_send = obj2xml.create_play_turn_xml(board, tiles, remaining_in_pile)
        tile_xml = self.send_and_receive(to_send)
        return xml2obj.create_tile_obj_helper(tile_xml)

    def end_game(self, board, colors):
        self.state.update_state("end_game")
        to_send = obj2xml.create_end_game_xml(board, colors)
        void_xml = self.send_and_receive(to_send)
