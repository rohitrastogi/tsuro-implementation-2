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

        self.update_player_position(board)
        self.state.update_state('play_turn')
    
        legal_plays = []
        for idx, tile in enumerate(tiles):
            for i in range(constants.NUMBER_OF_ROTATIONS):
                tile.rotate_tile()
                if self.legal_play(board, tile, tiles):
                    legal_plays.append((idx, i))
        
        if legal_plays:
            random.shuffle(legal_plays)
            tile_index, rotation_index = legal_plays[0]
            to_play = tiles[tile_index]
            to_play.rotate_tile_variable(rotation_index + 1)
            return to_play

        else:
            random.shuffle(tiles)
            print("PLAYING ELIMINATION MOVE RIP")
            return tiles[0]