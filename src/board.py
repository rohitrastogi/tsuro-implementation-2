import gameConstants as constants

class Board:
    """ data structure that contains board metadata """

    def __init__(self, players = []):
        self.num_tiles = 0
        self.tiles = []
        self.current_players = players
        self.eliminated_players = []

        for i in range(constants.BOARD_DIMENSION):
            temp = []
            for j in range(constants.BOARD_DIMENSION):
                temp.append(None)
            self.tiles.append(temp)

    def add_player(self, player):
        self.current_players.append(player)

    def add_player_to_eliminated(self, player):
        player.eliminated = True
        self.eliminated_players.append(player)

    def is_square_vacant(self, square):
        return self.tiles[square.x][square.y] == None

    def place_tile(self, square, tile):
        self.tiles[square.x][square.y] = tile
        self.num_tiles += 1

    def remove_tile(self, square):
        self.tiles[square.x][square.y] = None
        self.num_tiles -= 1


    def get_tile(self, square):
        if square.x == -1 or square.x == constants.BOARD_DIMENSION or square.y == -1 or square.y == constants.BOARD_DIMENSION:
            return None
        return self.tiles[square.x][square.y]

    def move_across_board(self, position, curr_tile):
        """
        Moves a player across the board after curr_tile has been places on the board.
        Returns a player position coordinates, board coordinates, and hit_a_wall?
        """
        curr_position = position
        next_board_space = curr_position.get_next_board_square()
        while True:
            curr_position = curr_tile.move_along_path(curr_position, next_board_space)
            next_board_space = curr_position.get_next_board_square()
            if curr_position.hit_a_wall():
                return curr_position, True
            if self.is_square_vacant(next_board_space):
                break
            curr_tile = self.get_tile(next_board_space)
        return curr_position, False

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
                if player.get_coordinates() in square_coordinates:
                    end_position, hit_a_wall = self.move_across_board(player.position, curr_tile)
                    player.update_position(end_position)
                    if hit_a_wall:
                        player.eliminated = True
