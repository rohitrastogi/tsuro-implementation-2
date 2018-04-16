class Board:
    """ data structure that contains board metadata """

    def __init__(self, players):
        self.all_players = players
        self.eliminated = []
        self.tiles = [[None]*6]*6
