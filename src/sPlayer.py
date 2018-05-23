from interface import implements
from position import Position
from IPlayer import IPlayer
import random
import gameConstants as constants

class SPlayer():
    """ data structure that contains player metadata """

    def __init__(self, color='', position=None, player = None):
        self.player = player
        self.color = color
        self.position = position
        self.dragon_held = False
        self.tiles_owned = []
        self.eliminated = False
        self.other_colors = []

    def get_coordinates(self):
        return self.position.get_player_coordinates()

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
        for i in range(constants.HAND_SIZE):
            self.draw_tile(pile_of_tiles)

    def get_name(self):
        return self.player.get_name

    def is_tile_owned(self, curr_tile):
        for tile in self.tiles_owned:
            if tile.identifier == curr_tile.identifier:
                return True
        return False

    def update_position(self, new_position):
        self.position.update_position(new_position)

    def remove_tile_from_hand(self, current_tile):
        for idx, tile in enumerate(self.tiles_owned):
            if tile.identifier == current_tile.identifier:
                del self.tiles_owned[idx]

    #client check
    def validate_hand(self, board):
        """
        Checks to make sure the hand is valid.
        A valid hand does not have more than 3 tiles, has tiles that are unique from each other,
        and none of the tiles are already on the board.
        """

        if len(self.tiles_owned) == 0:
            raise RuntimeError("This player has no tiles to play!")

        if len(self.tiles_owned) > constants.HAND_SIZE:
            raise RuntimeError("A player cannot have more than 3 tiles in their hand.")

        if board.check_if_tiles_on_board(self.tiles_owned):
            raise RuntimeError("This player has a tile that is already on the board.")
