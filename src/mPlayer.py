from interface import implements
from position import Position
from IPlayer import IPlayer
import random
import gameConstants as constants
from state import State

class MPlayer(implements(IPlayer)):
    """ data structure that contains player metadata """

    def __init__(self, name=''):
        self.name = name
        self.state = State()
        self.position = None
        self.color = None
        self.other_colors = None

    def get_name(self):
        return self.name

    def initialize(self, color, other_colors):
        self.state.update_state("initialize")
        if color not in constants.Colors.values():
            raise ValueError("Not a valid color for a player!")
        for c in other_colors:
            if c not in constants.Colors.values():
                raise ValueError("Not a valid color for another player!")
        self.color = color
        self.other_colors = other_colors

    def place_pawn(self, board):
        """
        For now it is randomly going to pick a location not picked by another player
        """
        self.state.update_state("place_pawn")

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

            for a_player in board.current_players:
                if a_player.color in self.other_colors:
                    if a_player.position:
                        if (x,y) == a_player.get_coordinates():
                            collision = True

        self.position = Position(x, y)
        return self.position

    def update_player_position(self, board):
        for splayer in board.current_players:
            if splayer.color == self.color:
                self.position = splayer.position

    def play_turn(self, board, tiles, remaining_in_pile):
        pass

    def end_game(self, board, colors):
        self.state.update_state("end_game")

    def is_tile_owned(self, curr_tile, tiles):
        for tile in tiles:
            if tile.identifier == curr_tile.identifier:
                return True
        return False

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

        board.place_tile(self.position.get_next_board_square(), tile)
        player_final_position, hit_a_wall = board.move_across_board(self.position, tile)
        board.remove_tile(self.position.get_next_board_square())

        # If player hits a wall, this tile causes elimination and is therefore, not legal.
        if hit_a_wall:
            return False
        return self.is_tile_owned(tile, tiles)
