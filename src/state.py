from gameConstants import GameState

class State:
    def __init__(self):
        self.state = GameState.uninitialized

    def update_state(self, method):
        if self.state == GameState.uninitialized and method == "initialize":
            self.state = GameState.initialized

        elif self.state == GameState.initialized and method == "place_pawn":
            self.state = GameState.pawn_placed

        elif (self.state == GameState.pawn_placed or self.state == GameState.turn_played) and method == "play_turn":
            self.state = GameState.turn_played

        elif self.state == GameState.pawn_placed and method == "end_game":
            self.state = GameState.game_over

        elif self.state == GameState.turn_played and method == "end_game":
            self.state = GameState.game_over

        else:
            raise RuntimeError("Invalid Sequence Contract! State is: " + self.state.name + " and method is: " + method)
