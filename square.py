import gameConstants as constants

class Square:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        if x < 0 or x > constant.BOARD_DIMENSION - 1 or y < 0 or y > constant.BOARD_DIMENSION - 1:
            raise RuntimeError("This square does not have the right coordinates for this board!")
