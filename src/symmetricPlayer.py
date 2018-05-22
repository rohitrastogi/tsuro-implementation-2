from interface import implements
from player import Player
import gameConstants as constants
import random
import administrator

class SymmetricPlayer(Player):
    """
    MostSymmetricPlayer is derived from Player base class
    Implements the method play_turn
    """

    def __init__(self, n, reverse):
        super().__init__(name = n)
        self.reverse = reverse


    def play_turn(self, board, tiles, remaining_in_pile):
        """
        MostSymmetric: This player sorts the possible moves by how symmetric each tile is (from most symmetric to least symmetric)
        and picks the first legal one.
        """
        if not self.placed_pawn:
            raise RuntimeError("The pawn must be placed before the player can play a turn!")

        self.tiles_owned = tiles
        self.validate_hand(board)
        self.tiles_owned.sort(key=lambda x: x.symmetry(), reverse=self.reverse)
        for idx, tile in enumerate(self.tiles_owned):
            for i in range(constants.NUMBER_OF_ROTATIONS):
                if administrator.legal_play(self, board, tile):
                    del self.tiles_owned[idx]
                    return tile
                tile.rotate_tile()

        tile = self.tiles_owned[0]
        del self.tiles_owned[0]

        self.played_turn = True
        return tile