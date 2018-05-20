from square import Square
import pytest

def test_getCoordinates():
    square_1 = Square(3,2)
    square_2 = Square(1,4)
    assert square_1.get_coordinates() == [(10,9),(11,9),(12,8),(12,7),(11,6),(10,6),(9,7),(9,8)]
    assert square_2.get_coordinates() == [(4,15),(5,15),(6,14),(6,13),(5,12),(4,12),(3,13),(3,14)]
