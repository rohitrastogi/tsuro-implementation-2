import gameConstants as constants

class Square:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        if x < -1 or x > constants.BOARD_DIMENSION or y < -1 or y > constants.BOARD_DIMENSION:
            raise RuntimeError("This square does not have the right coordinates for this board!")

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_coordinates(self):
        """
        Given a square on the board, returns all coordinates of the square starting from the
        left corner of the top edge, going clockwise
        """
        return [(self.x*3+1, self.y*3+3), \
        (self.x*3+2, self.y*3+3), \
        (self.x*3+3, self.y*3+2), \
        (self.x*3+3, self.y*3+1), \
        (self.x*3+2, self.y*3), \
        (self.x*3+1, self.y*3), \
        (self.x*3, self.y*3+1), \
        (self.x*3, self.y*3+2)]
