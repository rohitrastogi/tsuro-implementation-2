class Player:
    """ data structure that contains player metadata """

    def __init__(self, color, position):
        self.color = color
        self.position = position
        self.dragon_held = False
        self.tiles_owned = []
        self.eliminated = False

        if (self.position[0] + self.position[1]) % 3 == 0:
                raise Exception( 'This is not a valid starting position.')

        if self.position[0] < 0 or self.position[0] > 18 or self.position[1] < 0 or self.position[1] > 18:
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


    def lose_tiles(self, pile_of_tiles):
        for tile in self.tiles_owned:
            pile_of_tiles.append(tile)
        self.tiles_owned = []

    def draw_tile(self, pile_of_tiles):
        self.tiles_owned.append(pile_of_tiles.pop(0))

    def play_tile(self, tile):
            for i, tiles in enumerate(self.tiles_owned):
                if tile.identifier == tiles.identifier:
                    del self.tiles_owned[i]

    def initialize_hand(self, pile_of_tiles):
        for i in range(3):
            self.draw_tile(pile_of_tiles)
