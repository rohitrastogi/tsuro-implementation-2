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

    def initialize_hand(self, pile_of_tiles):
        for i in range(constants.HAND_SIZE):
            self.draw_tile(pile_of_tiles)

    def get_name(self):
        return self.player.get_name()

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

    def replace_with_random_player(self):
        from randomPlayer import RandomPlayer
        old_player = self.player
        self.player = RandomPlayer(old_player.name)
        self.player.color = old_player.color
        self.player.other_colors = old_player.other_colors
        self.player.initialized = old_player.state
 