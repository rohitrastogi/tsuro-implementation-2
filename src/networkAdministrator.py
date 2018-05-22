from xml2obj import interpret

class NetworkAdministrator(imp:

    def __init__(self, player):
        self.player = player
        self.command_handler = {
            "get-name" : player.getName,
            "initialize" : player.initialize,
            "place-pawn" : player.place_pawn,
            "play-turn" : player.play_turn,
            "end-game" : player.endgame
        }

    def do_work(self):
        while True: #? or until endgame message is received?
            data_in = "" #recv from socket and convert bytes to xml
            interpreted_command = xml2obj.interpret(data_in)
            func, args = (data_in[0], data_in[1:])
            res = self.command_handler[func](*args)
            data_out = obj2xml.interpret(res) #and convert to bytes
            #send data_out to socket




