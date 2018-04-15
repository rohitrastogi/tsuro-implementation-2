class Board:
    """ data structure that contains board metadata """

    def __init__(self):
        self.all_players = []
        self.eliminated = []
        self.tiles = [[None]*6]*6
