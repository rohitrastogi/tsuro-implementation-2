class Player:
    """ data structure that contains player metadata """

    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.dragon_held = False
        self.tiles_owned = []
        self.eliminated = False

        if self.position[0]%3 == 0 or self.position[1]%3 == 0:
                raise Exception( 'This is not a valid starting position.')
                
        if self.position[0] == 0:
            self.board_position = (-1, self.position[1]//3)
        elif self.position[0] == 18:
            self.board_position = (6, self.position[1]//3)
        elif self.position[1] == 0:
            self.board_position = (self.position[0]//3, -1)
        elif self.position[1] == 18:
            self.board_position = (self.position[0]//3, 6)
        else:
            raise Exception( 'This is not a valid starting position.')


    def lose_tiles(piles_of_tiles):
        for tile in self.tiles_owned:
            piles_of_tiles.append(tile)
        self.tiles_owned = []

    def draw_tile(piles_of_tiles):
        self.tiles_owned.append(piles_of_tiles.pop(0))

    def play_tile(tile):
        for i, tiles in enumerate(self.tiles_owned):
            if tile.identifier == tiles.identifier:
                del self.tiles_owned[i]




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
