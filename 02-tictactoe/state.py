class State:
    def __init__(self, board:List = [[".",".","."],[".",".","."],[".",".","."]], next_player: str = "X"):
        self.board: List = board
        self.next_player: str = next_player

    def get_next_states(self):
        
