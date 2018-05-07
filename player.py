from interface import implements
from IPlayer import IPlayer
from gameConstants import Colors
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
        self.square = None
        self.initialized = False
        self.placed_pawn = False
        self.played_turn = False
        self.game_ended = True
        # following statments check to make sure that position selected is valid
        if self.position:
            if (self.position[0] + self.position[1]) % 3 == 0:
                    raise Exception( 'This is not a valid starting position.')

            if self.position[0] < 0 or self.position[0] > 18 or self.position[1] < 0 or self.position[1] > 18:
                    raise Exception( 'This is not a valid starting position.')

            if self.position[0] == 0:
                self.square = (-1, self.position[1]//3)
            elif self.position[0] == 18:
                self.square = (6, self.position[1]//3)
            elif self.position[1] == 0:
                self.square = (self.position[0]//3, -1)
            elif self.position[1] == 18:
                self.square = (self.position[0]//3, 6)
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
        if self.initialized:
            raise RuntimeError("This player has already been initialized!")
        if not self.game_ended:
            raise RuntimeError("Do not reinitialize player without finishing the game!")
        if color not in Colors.__members__:
            raise ValueError("Not a valid color for a player!")
        for c in other_colors:
            if c not in Colors.__members__:
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
            self.square = (-1, self.position[1]//3)
        elif self.position[0] == 18:
            self.square = (6, self.position[1]//3)
        elif self.position[1] == 0:
            self.square = (self.position[0]//3, -1)
        elif self.position[1] == 18:
            self.square = (self.position[0]//3, 6)

        self.placed_pawn = True


    def play_turn(self, board, tiles, remaining_in_pile):
        pass

    def end_game(self, board, colors):
        self.game_ended = True
        self.initialized = False
        self.placed_pawn = False
        self.played_turn = False
        pass

    def is_tile_owned(self, curr_tile):
        for tile in self.tiles_owned:
            if tile.identifier == curr_tile.identifier:
                return True
        return False

    def update_position(self, new_position, new_square):
        self.position = new_position
        self.square = new_square

    def validate_hand(self, board):
        """
        Checks to make sure the hand is valid.
        A valid hand does not have more than 3 tiles, has tiles that are unique from each other,
        and none of the tiles are already on the board.
        """

        if len(self.tiles_owned) > 3:
            raise RuntimeError("A player cannot have more than 3 tiles in their hand.")

        if board.check_if_tiles_on_board(self.tiles_owned):
            raise RuntimeError("This player has a tile that is already on the board.")
