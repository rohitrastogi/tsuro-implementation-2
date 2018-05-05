class Board:
    """ data structure that contains board metadata """

    def __init__(self, players = []):
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

    def is_board_space_empty(self,board_space):
        return self.tiles[board_space[0]][board_space[1]] == None

    def move_across_board(self, player, curr_tile):
        '''
        Returns a player position coordinates, board coordinates, and hit_a_wall?
        '''
        curr_position = player.position
        curr_board_position = player.board_position
        next_board_space = self.get_next_board_space(curr_position, curr_board_position)
        while True:  #functions as a do while
            coordinates = self.get_coordinates(next_board_space)
            new_position = curr_tile.move_along_path(curr_position, coordinates)
            new_board_position = next_board_space
            next_board_space = self.get_next_board_space(new_position, new_board_position)
            if self.hit_a_wall(new_position):
                return new_position, new_board_position, True 
            if self.is_board_space_empty(next_board_space):
                break
            curr_tile = self.tiles[next_board_space[0]][next_board_space[1]]
        return new_position, new_board_position, False


        # return position, board position, hit_a_wall

    def hit_a_wall(self, position):
        return position[0] == 0 or position[1] == 0 or position[0] == 18 or position[1] == 18



    def get_next_board_space(self, position, board_position):
        '''
        given a player position and current board position, find board position that player will play next tile or move through
        '''
        if position[0]%3 == 0:
            if position[0] == board_position[0]*3:
                return (board_position[0]-1, board_position[1])
            else:
                return (board_position[0]+1, board_position[1])
        else:
            if position[1] == board_position[1]*3:
                return (board_position[0], board_position[1]-1)
            else:
                return (board_position[0], board_position[1]+1)

    def get_coordinates(self, board_space):
        '''
        given a board position, returns all possible postions a player can be on starting from top-left and moving clockwise
        '''
        return [(board_space[0]*3+1, board_space[1]*3+3), \
        (board_space[0]*3+2, board_space[1]*3+3), \
        (board_space[0]*3+3, board_space[1]*3+2), \
        (board_space[0]*3+3, board_space[1]*3+1), \
        (board_space[0]*3+2, board_space[1]*3), \
        (board_space[0]*3+1, board_space[1]*3), \
        (board_space[0]*3, board_space[1]*3+1), \
        (board_space[0]*3, board_space[1]*3+2)]