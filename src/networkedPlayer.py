from interface import implements
from player import Player
import gameConstants as constants
import random
import administrator

class NetworkedPlayer(implements(IPlayer)):
    def __init__(): 
        #networking stuff
    
    def get_name(self):
        #data_out = obj2xml.create_get_name_xml()
        #socket.send(data_out.tobytes)
        #data_in = socket.recv().toxml
        #return xml2obj.construct_name_object(data_in)
        pass

    def initialize(self, color, other_colors):
        #data_out = obj2xml.create_initialize_xml(color, other_colors)
        #socket.send(data_out.tobytes)
        #data_in = socket.recv().toxml
        #return xml2obj.construct_void_obj? NOT SURE HOW TO HANDLE VOID
        pass

    def place_pawn(self, board):
        #data_out = obj2xml.create_place_pawn_xml(board)
        #socket.send(data_out.tobytes)
        #data_in = socket.recv().toxml
        #return xml2obj.create_position_obj(data_in)
        pass

    def play_turn(self, board, tiles, remaining_in_pile):
        self.update_player_position(board)
        #data_out = obj2xml.create_play_turn_xml(board, tiles, remaining_in_pile)
        #socket.send(data_out.tobytes)
        #data_in = socket.recv().toxml
        #return xml2obj.construct_tile_object(data_in)
        pass

    def end_game(self, board, colors):
        #data_out = obj2xml.create_end_game_xml(color, other_colors)
        #socket.send(data_out.tobytes)
        #data_in = socket.recv().toxml
        #return xml2obj.construct_void_obj? NOT SURE HOW TO HANDLE VOID
        pass
