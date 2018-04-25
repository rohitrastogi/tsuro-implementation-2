class Board:
    """ data structure that contains board metadata """

    def __init__(self, players):
        self.all_players = players
        self.alive = []
        self.eliminated = []
        self.num_tiles = 0
        self.tiles = []
        # creates board tile spaces
        for i in range(6):
            temp = []
            for j in range(6):
                temp.append(None)
            self.tiles.append(temp)

    def add_player(self, player):
        self.all_players.append(player)
