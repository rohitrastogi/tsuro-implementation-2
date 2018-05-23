from interface import implements
from mPlayer import MPlayer
import gameConstants as constants
import random
import administrator

class SymmetricPlayer(MPlayer):
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

        self.update_player_position(board)
        if not self.placed_pawn:
            raise RuntimeError("The pawn must be placed before the player can play a turn!")

        #self.tiles_owned = tiles
        #self.validate_hand(board)
        tiles.sort(key=lambda x: x.symmetry(), reverse=self.reverse)
        for idx, tile in enumerate(tiles):
            for i in range(constants.NUMBER_OF_ROTATIONS):
                if self.legal_play(board, tile, tiles):
                    return tile
                tile.rotate_tile()

        self.played_turn = True
        random.shuffle(tiles)
        return tiles[0]
