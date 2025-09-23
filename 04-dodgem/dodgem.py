class GameState:
    def __init__(self,board: dict,current_player: str, parent = None):
        self.board = board
        self.current_player = current_player
        self.parent = parent

    def is_tile_free(self,coords):
        for k,v in self.board.items():
            if v == coords:
                return False
        return True

    def get_substates(self):
        substates: list = []
        next_player: str = "R" if self.current_player == "B" else "B"
        if self.current_player == "B":
            bs = ["B1","B2"]
            for b in bs: 
                b1_coords = self.board[b]
                if b1_coords[0] != -1:
                    # right
                    if b1_coords[0] == 2:
                        new_board = self.board.copy()
                        new_board[b] = (-1,-1)
                        substates.append(GameState(new_board,next_player,self))
                    elif self.is_tile_free((b1_coords[0]+1,b1_coords[1])):
                        new_board = self.board.copy()
                        new_board[b] = (b1_coords[0]+1,b1_coords[1])
                        substates.append(GameState(new_board,next_player,self))
                    # down
                    if b1_coords[1] != 2 and self.is_tile_free((b1_coords[0],b1_coords[1]+1)):
                        new_board = self.board.copy()
                        new_board[b] = (b1_coords[0],b1_coords[1]+1)
                        substates.append(GameState(new_board,next_player,self))
                    # up
                    if b1_coords[1] != 0 and self.is_tile_free((b1_coords[0],b1_coords[1]-1)):
                        new_board = self.board.copy()
                        new_board[b] = (b1_coords[0],b1_coords[1]-1)
                        substates.append(GameState(new_board,next_player,self))
        else:
            rs = ["R1","R2"]
            for r in rs:
                r_coords = self.board[r]
                if r_coords != (-1,-1):
                    # up
                    if r_coords[1] == 0:
                        new_board = self.board.copy()
                        new_board[r] = (-1,-1)
                        substates.append(GameState(new_board,next_player,self))
                    elif self.is_tile_free((r_coords[0], r_coords[1]-1)):
                        new_board = self.board.copy()
                        new_board[r] = (r_coords[0],r_coords[1]-1)
                        substates.append(GameState(new_board,next_player,self))
                    # left
                    if r_coords[0] != 0 and self.is_tile_free((r_coords[0]-1, r_coords[1])):
                        new_board = self.board.copy()
                        new_board[r] = (r_coords[0]-1,r_coords[1])
                        substates.append(GameState(new_board,next_player,self))
                    # right
                    if r_coords[0] != 2 and self.is_tile_free((r_coords[0]+1, r_coords[1])):
                        new_board = self.board.copy()
                        new_board[r] = (r_coords[0]+1,r_coords[1])
                        substates.append(GameState(new_board,next_player,self))
        return substates

    def get_valid_moves(self,car):
        valid_moves = []
        car_coords = self.board[car]
        if car[0] == "B":
            # right, up, down
            directions = [(1,0), (0,-1), (0,1)]
            for d in directions:
                new_coords = (car_coords[0]+d[0],car_coords[1]+d[1])
                if new_coords[0] < 0 or new_coords[0] > 3 or new_coords[1] < 0 or new_coords[1] > 2:
                    continue
                if not self.is_tile_free(new_coords):
                    continue
                valid_moves.append(new_coords)

                
        elif car[0] == "R":
            # left, right, up
            directions = [(-1,0), (1,0), (0,-1)]
            for d in directions:
                new_coords = (car_coords[0]+d[0],car_coords[1]+d[1])
                if new_coords[0] < -1 or new_coords[0] > 2 or new_coords[1] < 0 or new_coords[1] > 2:
                    continue
                if not self.is_tile_free(new_coords):
                    continue
                valid_moves.append(new_coords)
        else:
            print("Invalid car")
        return valid_moves

    def get_bot_move(self):
        vis_score = {}
        score, best_state = self.minimax(self, 0, 0, vis_score)
        return best_state

    def minimax(self, gs, i, d=0, vis_score=None):

        if gs in vis_score:
            return (vis_score[gs], gs)

        result = gs.is_game_over()
        if result[0]:
            score = result[1]-d if result[1] > 0 else result[1]+d
            vis_score[gs] = score
            return (score, gs)

        if d > 5:
            score = self.get_score()
            score = score-d if score > 0 else score+d
            vis_score[gs] = score
            return (score, gs)

        if gs.current_player == "B":  # maximizing
            best_score = (-999, None)
            for ss in gs.get_substates():
                candidate = self.minimax(ss, i+1, d+1, vis_score)
                if candidate[0] > best_score[0]:
                    best_score = (candidate[0], ss)
        else:  # minimizing
            best_score = (999, None)
            for ss in gs.get_substates():
                candidate = self.minimax(ss, i+1, d+1, vis_score)
                if candidate[0] < best_score[0]:
                    best_score = (candidate[0], ss)

        vis_score[gs] = best_score[0]
        return best_score

    def player_move(self, car, coord):
       new_board = self.board.copy()
       new_board[car] = coord
       next_player: str = "R" if self.current_player == "B" else "B"
       return GameState(new_board, next_player, self)

    def output(self, i=0):
        inital_board = [["  ","  ","  "],["  ","  ","  "],["  ","  ","  "]]
        for k,v in self.board.items():
            inital_board[v[1]][v[0]] = k
        separator = "--------"
        print(" "*i*4, inital_board[0][0] + "|" + inital_board[0][1] + "|" + inital_board[0][2])
        print(" "*i*4, separator)
        print(" "*i*4, inital_board[1][0] + "|" + inital_board[1][1] + "|" + inital_board[1][2])
        print(" "*i*4, separator)
        print(" "*i*4, inital_board[2][0] + "|" + inital_board[2][1] + "|" + inital_board[2][2])
        print(" "*i*4, "Player to play:", self.current_player)
        print()

    def get_score(self):
        score = 0
        if self.board["B1"] == (-1,-1):
            score += 10
        if self.board["B2"] == (-1,-1):
            score += 10
        if self.board["R1"] == (-1,-1):
            score -= 10
        if self.board["R2"] == (-1,-1):
            score -= 10
        return score

    def is_game_over(self):
        if self.board["B1"] == (-1,-1) and self.board["B2"] == (-1,-1):
            return (True, 99)
        if self.board["R1"] == (-1,-1) and self.board["R2"] == (-1,-1):
            return (True, -99)
        return (False, 0)
    def __eq__(self, other):
        return (
            isinstance(other, GameState)
            and self.current_player == other.current_player
            and self.board == other.board
        )

    def __hash__(self):
        frozen_board = tuple(sorted(self.board.items()))
        return hash((frozen_board, self.current_player))

