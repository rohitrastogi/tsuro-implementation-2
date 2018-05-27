from gameConstants import GameState

class State:
    def __init__(self):
        self.state = GameState.unitialized

    def update_state(self, method):
        if self.state == GameState.unitialized and method == "initialize":
            self.state = GameState.initialized

        elif self.state == GameState.initialized and method == "place_pawn":
            self.state = GameState.pawn_placed

        elif (self.state == GameState.pawn_placed or self.state == GameState.turn_played) and method == "play_turn":
            self.state = GameState.turn_played

        #TODO does turn_player have to occur before game_over
        elif self.state == GameState.turn_played and method == "game_over":
            self.state = GameState.game_over
        
        else:
            raise RuntimeError("Invalid Sequence Contract! State is: " + self.state.name + " and method is: " + method)
