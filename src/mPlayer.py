from interface import implements
from position import Position
from IPlayer import IPlayer
import random
import gameConstants as constants

class MPlayer(implements(IPlayer)):
    """ data structure that contains player metadata """

    def __init__(self, name=''):
        self.name = name 
        self.initialized = False
        self.placed_pawn = False
        self.played_turn = False
        self.game_ended = True

    def get_name(self):
        return self.name

    def initialize(self, color, other_colors):
        print(color)
        print(other_colors)
        print(constants.Colors.__members__)
        if self.initialized:
            raise RuntimeError("This player has already been initialized!")
        if not self.game_ended:
            raise RuntimeError("Do not reinitialize player without finishing the game!")
        if color not in constants.Colors:
            raise ValueError("Not a valid color for a player!")
        for c in other_colors:
            if c not in constants.Colors:
                raise ValueError("Not a valid color for another player!")

        self.color = color
        self.other_colors = other_colors
        self.game_ended = False
        self.initialized = True

    def place_pawn(self, board):
        """
        For now it is randomly going to pick a location not picked by another player
        """
        if not self.initialized:
            raise RuntimeError("Player must be initialized first!")
        if self.placed_pawn:
            raise RuntimeError("The pawn has already been placed!")

        collision = True
        while collision:
            collision = False
            edge = random.choice(['x','y'])
            if edge == 'x':
                x = random.choice([constants.START_WALL, constants.END_WALL])
                y = random.choice([i for i in range(constants.END_WALL + 1) if i%3!=0])
            else:
                y = random.choice([constants.START_WALL, constants.END_WALL])
                x = random.choice([i for i in range(constants.END_WALL + 1) if i%3!=0])

            for a_player in board.all_players:
                if a_player.color in self.other_colors:
                    if a_player.position:
                        if (x,y) == a_player.get_coordinates():
                            collision = True

        self.position = Position(x, y)
        self.placed_pawn = True

    def play_turn(self, board, tiles, remaining_in_pile):
        pass

    def end_game(self, board, colors):
        self.game_ended = True
        self.initialized = False
        self.placed_pawn = False
        self.played_turn = False
        pass
	
