from interface import implements
from position import Position
from IPlayer import IPlayer
from randomPlayer import RandomPlayer
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
        return self.player.get_name()

    def is_tile_owned(self, curr_tile):
        for tile in self.tiles_owned:
            if tile.identifier == curr_tile.identifier:
                return True
        return False

    def update_position(self, new_position):
        self.position.update_position(new_position)

    def remove_tile_from_hand(self, to_remove):
        found = False
        for idx, tile in enumerate(self.tiles_owned):
            if to_remove.identifier == tile.identifier:
                del self.tiles_owned[idx]
                found = True
        if not found:
            raise RuntimeError("Tile to remove not in hand!")
        
    def replace_with_random_player(self):
        old_player = self.player
        self.player = RandomPlayer(old_player.name)
        self.player.color = old_player.color
        self.player.other_colors = old_player.other_colors
        self.player.initialized = old_player.initialized
        self.placed_pawn = old_player.placed_pawn
        self.played_turn = old_player.played_turn
        self.game_ended = old_player.game_ended

