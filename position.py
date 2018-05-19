from square import Square
import gameConstants as constants

class Position:

    def __init__(self, x, y, square=None):
        self.x = x
        self.y = y
        self.square = square

        # TODO: Contract to check if the square corresponds to the position

        if not square:
            if (x + y) % 3 == 0:
                raise Exception( 'This is not a valid starting position.')

            if x < constants.START_WALL or x > constants.END_WALL or y < constants.START_WALL or y > constants.END_WALL:
                raise Exception( 'This is not a valid starting position.')

            if x == constants.START_WALL:
                self.square = Square(-1, y//3)
            elif x == constants.END_WALL:
                self.square = Square(6, y//3)
            elif y == constants.START_WALL:
                self.square = Square(x//3, -1)
            elif y == constants.END_WALL:
                self.square = Square(x//3, 6)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_player_coordinates(self):
        return (self.x, self.y)

    def update_position(self, position):
        self.x = position.x
        self.y = position.y
        self.square = position.square

    def hit_a_wall(self):
        """
        Returns boolean. True, if the player has hit a wall. False, otherwise.
        """
        return self.x == constants.START_WALL or self.y == constants.START_WALL or self.x == constants.END_WALL or self.y == constants.END_WALL

    def get_next_board_square(self):
        """
        Given a player's position and the square they are currently on returns the square they will next place the tile on.
        """
        square = self.square
        if self.x%3 == 0:
            if self.x == square.x*3:
                return Square(square.x-1, square.y)
            else:
                return Square(square.x+1, square.y)
        else:
            if self.y == square.y*3:
                return Square(square.x, square.y-1)
            else:
                return Square(square.x, square.y+1)
