from square import Square
from position import Position
import pytest

def test_getNextBoardSquare():
    assert Position(9, 7, Square(3,2)).get_next_board_square() == Square(2,2)
    assert Position(1, 0).get_next_board_square() == Square(0,0)
    assert Position(18, 4).get_next_board_square() == Square(5,1)
    assert Position(0, 8).get_next_board_square() == Square(0,2)
    assert Position(11, 18, Square(3,6)).get_next_board_square() == Square(3,5)

def test_updatePosition():
    position_1 = Position(0, 1)
    position_2 = Position(3, 1, Square(0, 0))

    position_1.update_position(position_2)
    assert position_1 == position_2
