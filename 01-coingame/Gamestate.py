import time

class Gamestate:
    def __init__(self):
        self.board: list = ["0"] + ["_" for i in range(0,6)]
        self.player: int = 1

    def play(self, amount):

        curr_pos = self.board.index("0")
        new_pos = curr_pos + amount
        if new_pos > 6:
            print("Invalid move")
            return False
        self.board[curr_pos] = "_"
        self.board[new_pos] = "0"
        return True
    
    def output(self):
        print(self.board)

    def is_game_over(self):
        if self.board[6] == "0":
            return True
        return False
    
    def play_player(self):
        amount = int(input("How many? "))
        if amount<1 or amount>2:
            print("Invalid move")
            return False
        self.play(amount)
        self.output()
        time.sleep(0.5)
        self.bot_play(amount)
        self.output()
        return True
    
    def bot_play(self, player_amount):
        print("Bot Played: ", 3-player_amount)
        self.play(3 - player_amount)
    