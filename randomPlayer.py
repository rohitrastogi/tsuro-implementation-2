from interface import implements
from player import Player
import random
import administrator

class RandomPlayer(Player):
    """
    RandomPlayer is derived from Player base class
    Implements the method play_turn
    """

    def play_turn(self, board, tiles, remaining_in_pile):
        """
        Random: This player picks randomly from all of the legal moves.
        """

        self.tiles_owned = tiles
        for tile in self.tiles_owned:
            for i in range(4):
                if administrator.legal_play(self, board, tile):
                    return tile
                tile.rotate_tile()

        return random.choice(self.tiles_owned)
