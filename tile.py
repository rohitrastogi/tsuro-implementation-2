class Tile:
    """ data structure that contains tile metadata """

    def __init__(self, identifier, paths):
        self.identifier = identifier
        self.paths = paths
        self.position = (-1, -1)

    def rotate_tile():
        for path in self.paths:
            path[0] = (path[0] + 2)%8
            path[1] = (path[1] + 2)%8
