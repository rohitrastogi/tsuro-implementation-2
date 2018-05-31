from enum import Enum

Colors = {0: 'blue', 1: 'red', 2: 'green', 3: 'orange', 4: 'sienna', 5: 'hotpink', 6: 'darkgreen', 7: 'purple'}

class GameState(Enum):
    uninitialized = 0
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
