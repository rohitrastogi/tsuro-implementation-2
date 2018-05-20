from interface import implements
import gameConstants as constants
from symmetricPlayer import SymmetricPlayer
import random
import administrator

class LeastSymmetricPlayer(SymmetricPlayer):
    """
    LeastSymmetricPlayer is derived from SymmetricPlayer derived class
    """
    
    def __init__(self, n):
       super().__init__(n, False)
