import gameConstants as constants

class Board:
    """ data structure that contains board metadata """

    def __init__(self, players = []):
        self.all_players = players
        self.num_tiles = 0
        self.tiles = []

        for i in range(constants.BOARD_DIMENSION):
            temp = []
            for j in range(constants.BOARD_DIMENSION):
                temp.append(None)
            self.tiles.append(temp)

    def add_player(self, player):
        self.all_players.append(player)

    def is_square_vacant(self, square):
        return self.tiles[square[0]][square[1]] == None

    def place_tile(self, square, tile):
        self.tiles[square[0]][square[1]] = tile
        self.num_tiles += 1

    def get_tile(self, square):
        return self.tiles[square[0]][square[1]]

    def move_across_board(self, player, curr_tile):
        """
        Moves a player across the board after curr_tile has been places on the board.
        Returns a player position coordinates, board coordinates, and hit_a_wall?
        """
        curr_position = player.position
        curr_board_position = player.square
        next_board_space = self.get_next_board_square(curr_position, curr_board_position)
        while True:
            coordinates = self.get_coordinates(next_board_space)
            curr_position = curr_tile.move_along_path(curr_position, coordinates)
            curr_board_position = next_board_space
            next_board_space = self.get_next_board_square(curr_position, curr_board_position)
            if self.hit_a_wall(curr_position):
                return curr_position, curr_board_position, True
            if self.is_square_vacant(next_board_space):
                break
            curr_tile = self.get_tile(next_board_space)
        return curr_position, curr_board_position, False

    def hit_a_wall(self, position):
        """
        Returns boolean. True, if the player has hit a wall. False, otherwise.
        """
        return position[0] == constants.START_WALL or position[1] == constants.START_WALL or position[0] == constants.END_WALL or position[1] == constants.END_WALL

    def check_if_tiles_on_board(self, hand):
        """
        checks if any of the tiles in the hand are already on the board
        """

        tile_identifiers = []
        for tile in hand:
            tile_identifiers.append(tile.identifier)

        for i in range(constants.BOARD_DIMENSION):
            for j in range(constants.BOARD_DIMENSION):
                if self.tiles[i][j]:
                    if self.tiles[i][j].identifier in tile_identifiers:
                        return True

        return False

    def move_players(self, players, square_coordinates, curr_tile):
        """
        Moves all players affected by the placement of the curr_tile across the board.

        Args:
            players: list of Player objects, players in the game
            square_coordinates: list of tuples representing coordinates of the square the tile is being placed on
            curr_tile: an object of the Tile class, current tile being placed in this turn
        """
        for player in players:
            if not player.eliminated:
                if player.position in square_coordinates:
                    end_position, end_board_position, hit_a_wall = self.move_across_board(player, curr_tile)
                    player.update_position(end_position, end_board_position)
                    if hit_a_wall:
                        player.eliminated = True

    def get_next_board_square(self, position, square):
        """
        Given a player's position and the square they are currently on returns the square they will next place the tile on.
        """
        if position[0]%3 == 0:
            if position[0] == square[0]*3:
                return (square[0]-1, square[1])
            else:
                return (square[0]+1, square[1])
        else:
            if position[1] == square[1]*3:
                return (square[0], square[1]-1)
            else:
                return (square[0], square[1]+1)

    def get_coordinates(self, square):
        """
        Given a square on the board, returns all coordinates of the square starting from the
        left corner of the top edge, going clockwise
        """
        return [(square[0]*3+1, square[1]*3+3), \
        (square[0]*3+2, square[1]*3+3), \
        (square[0]*3+3, square[1]*3+2), \
        (square[0]*3+3, square[1]*3+1), \
        (square[0]*3+2, square[1]*3), \
        (square[0]*3+1, square[1]*3), \
        (square[0]*3, square[1]*3+1), \
        (square[0]*3, square[1]*3+2)]
