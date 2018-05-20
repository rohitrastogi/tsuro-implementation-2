from interface import implements
from symmetricPlayer import SymmetricPlayer
import random
import administrator

class MostSymmetricPlayer(SymmetricPlayer):
    """
    MostSymmetricPlayer is derived from SymmetricPlayer derived class
    """
    
    def __init__(self, n):
        super().__init__(n, True)
