class Player:
    """ data structure that contains player metadata """

    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.board_position = (-1, -1)
        self.dragon_held = False
        self.tiles_owned = []

    def lose_tiles(piles_of_tiles):
        for tile in self.tiles_owned:
            piles_of_tiles.append(tile)
        self.tiles_owned = []

    def draw_tile(piles_of_tiles):
        self.tiles_owned.append(piles_of_tiles.pop(0))

    # def get_next_board_position():
    #
    #     if position[0]%3 == 0:
    #         if position[0] == board_position[0]*3:
    #             return (board_position[0]-1, board_position[1])
    #         else:
    #             return (board_position[0]+1, board_position[1])
    #     else:
    #         if position[1] == board_position[1]*3:
    #             return (board_position[0], board_position[1]-1)
    #         else:
    #             return (board_position[0], board_position[1]+1)
