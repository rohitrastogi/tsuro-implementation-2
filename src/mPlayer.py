from interface import implements
from position import Position
from IPlayer import IPlayer
import random
import gameConstants as constants

class MPlayer(implements(IPlayer)):
    """ data structure that contains player metadata """

    def __init__(self, name=''):
        self.position = None #TODO
        self.color = None #TODO
        self.name = name 
        self.initialized = False
        self.placed_pawn = False
        self.played_turn = False
        self.game_ended = True

    def get_name(self):
        return self.name

    def initialize(self, color, other_colors):
        if self.initialized:
            raise RuntimeError("This player has already been initialized!")
        if not self.game_ended:
            raise RuntimeError("Do not reinitialize player without finishing the game!")
        if color not in constants.Colors:
            raise ValueError("Not a valid color for a player!")
        for c in other_colors:
            if c not in constants.Colors:
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
                x = random.choice([constants.START_WALL, constants.END_WALL])
                y = random.choice([i for i in range(constants.END_WALL + 1) if i%3!=0])
            else:
                y = random.choice([constants.START_WALL, constants.END_WALL])
                x = random.choice([i for i in range(constants.END_WALL + 1) if i%3!=0])

            for a_player in board.all_players:
                if a_player.color in self.other_colors:
                    if a_player.position:
                        if (x,y) == a_player.get_coordinates():
                            collision = True

        self.position = Position(x, y)
        self.placed_pawn = True

    def play_turn(self, board, tiles, remaining_in_pile):
        #update position field
        pass

    def end_game(self, board, colors):
        self.game_ended = True
        self.initialized = False
        self.placed_pawn = False
        self.played_turn = False
        pass

    def is_tile_owned(self, curr_tile, tiles):
        for tile in tiles:
            if tile.identifier == curr_tile.identifier:
                return True
        return False

    def legal_play(self, board, tile, tiles):
        """
        Returns whether the tile the player wants to play is a legal move or not, considering all the tiles the player has.

        Args:
            self: instance of player class, the player whose turn it is
            board: instance of Board class, current state of the board
            tile: instance of Tile class, the tile the player wants to play

        Returns:
            boolean. True, if the tile is a legal move. False, otherwise.
        """

        # First, check if there is another legal move that can be played.
        another_legal = False
        for a_tile in tiles:
            for i in range(constants.NUMBER_OF_ROTATIONS):
                a_tile.rotate_tile()
                if self.legal_play_helper(board, a_tile, tiles):
                    another_legal = True

        # If there is another legal move, just check whether this tile causes elimination or not
        # If there is not another legal move, then this tile can be played provided it belongs to the player
        if another_legal:
            return self.legal_play_helper(board, tile, tiles)
        else:
            return self.is_tile_owned(tile, tiles)
    
    def legal_play_helper(self, board, tile, tiles):
        """
        Returns whether the tile the player wants to play is a legal move or not, regardless of other tiles in the player's hand.

        Args:
            player: instance of SPlayer class, the player whose turn it is
            board: instance of Board class, current state of the board
            tile: instance of Tile class, the tile the player wants to play

        Returns:
            boolean. True, if the tile is a legal move. False, otherwise.
        """

        # Player position is returned by the move_across_board function, but is not updated.
        player_final_position, hit_a_wall = board.move_across_board(self.position, tile)

        # If player hits a wall, this tile causes elimination and is therefore, not legal.
        if hit_a_wall:
            return False
        return self.is_tile_owned(tile, tiles)

    #call in play-turn
    def update_player_position(self, board):
        for splayer in board.all_players:
            if splayer.color == self.color:
                self.position = splayer.position
	
