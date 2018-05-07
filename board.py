class Board:
    """ data structure that contains board metadata """

    def __init__(self, players = []):
        self.all_players = players
        self.alive = []
        self.eliminated = []
        self.num_tiles = 0
        self.tiles = []

        for i in range(6):
            temp = []
            for j in range(6):
                temp.append(None)
            self.tiles.append(temp)

    def add_player(self, player):
        self.all_players.append(player)

    def is_square_vacant(self, square):
        return self.tiles[square[0]][square[1]] == None

    def place_tile(self, square, tile):
        self.tiles[square[0]][square[1]] = tile

    def get_tile(self, square):
        return self.tiles[square[0]][square[1]]

    def move_across_board(self, player, curr_tile):
        """
        Returns a player position coordinates, board coordinates, and hit_a_wall?
        """
        curr_position = player.position
        curr_board_position = player.square
        next_board_space = self.get_next_board_space(curr_position, curr_board_position)
        while True:
            coordinates = self.get_coordinates(next_board_space)
            curr_position = curr_tile.move_along_path(curr_position, coordinates)
            curr_board_position = next_board_space
            next_board_space = self.get_next_board_space(curr_position, curr_board_position)
            if self.hit_a_wall(curr_position):
                return curr_position, curr_board_position, True
            if self.is_square_vacant(next_board_space):
                break
            curr_tile = self.get_tile(next_board_space)
        return curr_position, curr_board_position, False

    def hit_a_wall(self, position):
        return position[0] == 0 or position[1] == 0 or position[0] == 18 or position[1] == 18

    def check_if_tiles_on_board(self, hand):
        """
        checks if any of the tiles in the hand are already on the board
        """

        tile_identifiers = []
        for tile in hand:
            tile_identifiers.append(tile.identifier)

        for i in range(6):
            for j in range(6):
                if self.tiles[i][j]:
                    if self.tiles[i][j].identifier in tile_identifiers:
                        return True

        return False


    def get_next_board_space(self, position, board_position):
        """
        given a player position and current board position, find board position that player will play next tile or move through
        """
        if position[0]%3 == 0:
            if position[0] == board_position[0]*3:
                return (board_position[0]-1, board_position[1])
            else:
                return (board_position[0]+1, board_position[1])
        else:
            if position[1] == board_position[1]*3:
                return (board_position[0], board_position[1]-1)
            else:
                return (board_position[0], board_position[1]+1)

    def get_coordinates(self, square):
        """
        given a board position, returns all possible postions a player can be on starting from top-left and moving clockwise
        """
        return [(square[0]*3+1, square[1]*3+3), \
        (square[0]*3+2, square[1]*3+3), \
        (square[0]*3+3, square[1]*3+2), \
        (square[0]*3+3, square[1]*3+1), \
        (square[0]*3+2, square[1]*3), \
        (square[0]*3+1, square[1]*3), \
        (square[0]*3, square[1]*3+1), \
        (square[0]*3, square[1]*3+2)]
