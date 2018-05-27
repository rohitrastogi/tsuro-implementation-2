from enum import Enum

# class Colors(Enum):
#     blue = 0
#     red = 1
#     green = 2
#     orange = 3
#     sienna = 4
#     hotpink = 5
#     darkgreen = 6
#     purple = 7
Colors = {0: 'blue', 1: 'red', 2: 'green', 3: 'orange', 4: 'sienna', 5: 'hotpink', 6: 'darkgreen', 7: 'purple'}

class GameState(Enum):
    unitialized = 0
    initialized = 1
    pawn_placed = 2
    turn_played = 3
    game_over = 4


START_WALL = 0
END_WALL = 18
NUMBER_OF_TILES = 35
BOARD_DIMENSION = 6
HAND_SIZE = 3
NUMBER_OF_ROTATIONS = 4
NUMBER_OF_TICKS = 8
NUMBER_OF_PLAYERS = 8
