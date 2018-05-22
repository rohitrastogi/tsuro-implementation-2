from interface import implements
from mPlayer import MPlayer
import gameConstants as constants
import random
import administrator

class RandomPlayer(MPlayer):
    """
    RandomPlayer is derived from Player base class
    Implements the method play_turn
    """
    def __init__(self, name):
        super().__init__(name)

    def play_turn(self, board, tiles, remaining_in_pile):
        """
        Random: This player picks randomly from all of the legal moves.
        """
        if not self.placed_pawn:
            raise RuntimeError("The pawn must be placed before the player can play a turn!")

        legal_plays = []
        for idx, tile in enumerate(tiles):
            for i in range(constants.NUMBER_OF_ROTATIONS):
                tile.rotate_tile()
                if administrator.legal_play(self, board, tile):
                    legal_plays.append((idx, i))
        
        if not legal_plays:
             tile_index = random.randint(0,len(tiles) - 1)
             rotation_index = random.randint(0, constants.NUMBER_OF_ROTATIONS - 1)
        else:
            tile_index, rotation_index = legal_plays[random.randint(0, len(legal_plays) - 1)]

        self.played_turn = True

        to_play = tiles[tile_index]
        to_play.rotate_tile_variable(rotation_index)
