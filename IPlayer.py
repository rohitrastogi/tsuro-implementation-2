from interface import Interface

class IPlayer(Interface):

    def get_name(self):
        pass

    def initialize(self, color, other_colors):
        pass

    def place_pawn(self, board):
        pass

    def play_turn(self, board, tiles, natural):
        pass

    def end_game(self, board, colors):
        pass

    
