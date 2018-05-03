from interface import implements
from IPlayer import IPlayer
import random

class Player(implements(IPlayer)):
    """ data structure that contains player metadata """

    def __init__(self, name='', color='', position=None):
        self.name = name
        self.color = color
        self.position = position
        self.dragon_held = False
        self.tiles_owned = []
        self.eliminated = False
        self.other_colors = []
        self.board_position = None
        # following statments check to make sure that position selected is valid
        if self.position:
            if (self.position[0] + self.position[1]) % 3 == 0:
                    raise Exception( 'This is not a valid starting position.')

            if self.position[0] < 0 or self.position[0] > 18 or self.position[1] < 0 or self.position[1] > 18:
                    raise Exception( 'This is not a valid starting position.')

            if self.position[0] == 0:
                self.board_position = (-1, self.position[1]//3)
            elif self.position[0] == 18:
                self.board_position = (6, self.position[1]//3)
            elif self.position[1] == 0:
                self.board_position = (self.position[0]//3, -1)
            elif self.position[1] == 18:
                self.board_position = (self.position[0]//3, 6)
            else:
                raise Exception( 'This is not a valid starting position.')


    def lose_tiles(self, pile_of_tiles):
        for tile in self.tiles_owned:
            pile_of_tiles.append(tile)
        self.tiles_owned = []

    def draw_tile(self, pile_of_tiles):
        self.tiles_owned.append(pile_of_tiles.pop(0))

    def play_tile(self, tile):
            for i, tiles in enumerate(self.tiles_owned):
                if tile.identifier == tiles.identifier:
                    del self.tiles_owned[i]

    def initialize_hand(self, pile_of_tiles):
        for i in range(3):
            self.draw_tile(pile_of_tiles)

    def get_name(self):
        return self.name

    def initialize(self, color, other_colors):
        self.color = color
        self.other_colors = other_colors

    def place_pawn(self, board):
        """
        For now it is randomly going to pick a location not picked by another player
        """

        collision = True
        while collision:
            collision = False
            edge = random.choice(['x','y'])
            if edge == 'x':
                x = random.choice([0, 18])
                y = random.choice([i for i in range(19) if i%3!=0])
            else:
                y = random.choice([0, 18])
                x = random.choice([i for i in range(19) if i%3!=0])

            for a_player in board.all_players:
                if a_player.color in self.other_colors:
                    if (x,y) == a_player.position:
                        collision = True
                    else:
                        continue

        self.position = (x,y)

        if self.position[0] == 0:
            self.board_position = (-1, self.position[1]//3)
        elif self.position[0] == 18:
            self.board_position = (6, self.position[1]//3)
        elif self.position[1] == 0:
            self.board_position = (self.position[0]//3, -1)
        elif self.position[1] == 18:
            self.board_position = (self.position[0]//3, 6)


    def play_turn(self, board, tiles, remaining_in_pile):
        pass

    def end_game(self, board, colors):
        pass
