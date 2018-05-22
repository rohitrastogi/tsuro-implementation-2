import administrator

class Server:
    def __init__(self):
        self.board = None
        self.tile_pile = administrator.create_draw_pile()
        self.curr_players = []
        self.elim_players = []
        
    def do_networking_stuff(self):
        #setup sockets and servers somehow
        pass

    def play_game(self):
        #main game loop
        pass

    def register_player(self, player):
        #take player and construct SPlayer and add this SPlayer to curr_players
        pass

    def initialize_players(self):
        #loop over registered SPlayers and call initialize and place-pawn, and other things?
        pass


        