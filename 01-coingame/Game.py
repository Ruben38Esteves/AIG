import Gamestate


gamestate =  Gamestate.Gamestate()
gamestate.output()
while not gamestate.is_game_over():
    if not gamestate.play_player():
        continue

print("Game Ended")