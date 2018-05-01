from interface import implements
from player import Player
import random
import administrator

class LeastSymmetricPlayer(Player):
    """
    LeastSymmetricPlayer is derived from Player base class
    Implements the method play_turn
    """

    def play_turn(self, board, tiles, remaining_in_pile):
        """
        LeastSymmetric: This player sorts the possible moves by how symmetric each tile is (from least symmetric to most symmetric)
        and picks the first legal one.
        """

        self.tiles_owned = tiles
        self.tiles_owned.sort(key=lambda x: x.symmetry())
        for tile in self.tiles_owned:
            for i in range(4):
                if administrator.legal_play(self, board, tile):
                    return tile
                tile.rotate_tile()

        return self.tiles_owned[0]
