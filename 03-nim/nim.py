s1 = ['I','III','IIIII','IIIIIII','H']

class game_state:
    def __init__(self, board:list, parent=None):
        self.board = board
        self.parent = parent

    def get_substates(self):
        substates = []
        for i in range(0,len(self.board)-1):
            if self.board[i] == '':
                continue
            for j in range(0,len(self.board[i])):
                new_board = self.board.copy()
                new_board[i] = "I"*j
                new_board[-1] = "C" if new_board[-1] == "H" else "H"
                substates.append(game_state(new_board,self))
        return substates

    def check_over(self):
        if self.board[0] == "" and self.board[1] == "" and self.board[2] == "" and self.board[3] == "":
            return (True,self.board[-1])
        return (False,"")

def minimax(state: game_state):
    result = state.check_over()
    if result[0]:
        return (result[1], state)
    outcomes = []
    for ss in state.get_substates():
        winner = minimax(ss)
        if winner[0] == state.board[-1]:
            return winner
        outcomes.append(winner)
    return(outcomes[0])


result = minimax(game_state(s1))
final_state = result[1]
while final_state != None:
    print(final_state.board)
    final_state = final_state.parent
