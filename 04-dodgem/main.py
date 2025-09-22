import pygame
import dodgem

selected_car = None
initial_board = {"B1":(0,0),"B2":(0,1),"R1":(1,2),"R2":(2,2)}
game_state: dodgem.GameState = dodgem.GameState(initial_board,"B")
possible_moves = None
human_player = None


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Dodgem")

    blue_rect, red_rect = draw_menu(screen)

    chosen_color = None

    while not chosen_color:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if blue_rect.collidepoint(pos):
                    chosen_color = "B"
                    break
                elif red_rect.collidepoint(pos):
                    chosen_color = "R"
                    break

    global human_player
    human_player = chosen_color
    draw_board(screen, game_state.board, selected_car)
    

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_click(event.pos, game_state.board)
                
                draw_board(screen, game_state.board, selected_car)

    pygame.quit()


def draw_board(screen, board, selected_car=None):
    global possible_moves
    screen.fill((255, 255, 255))

    # draw horizontal lines
    pygame.draw.line(screen, (0, 0, 0), (0, 1), (600, 1), 4)
    pygame.draw.line(screen, (0, 0, 0), (0, 200), (600, 200), 4)
    pygame.draw.line(screen, (0, 0, 0), (0, 400), (600, 400), 4)
    pygame.draw.line(screen, (0, 0, 0), (0, 597), (600, 597), 4)

    # draw vertical lines
    pygame.draw.line(screen, (0, 0, 0), (0, 0), (0, 600), 4)
    pygame.draw.line(screen, (0, 0, 0), (200, 0), (200, 600), 4)
    pygame.draw.line(screen, (0, 0, 0), (400, 0), (400, 600), 4)
    pygame.draw.line(screen, (0, 0, 0), (597, 0), (597, 600), 4)

    for car, coord in board.items():
        if coord == (-1, -1):
            continue
        if car.startswith("B"):
            color = (0, 0, 255)
            x = coord[0] * 200 + 25
            y = coord[1] * 200 + 50
            rect = pygame.Rect(x, y, 150, 100)
            pygame.draw.ellipse(screen, color, rect)
        else:
            color = (255, 0, 0)
            x = coord[0] * 200 + 50
            y = coord[1] * 200 + 25
            rect = pygame.Rect(x, y, 100, 150)
            pygame.draw.ellipse(screen, color, rect)

        if car == selected_car:
            pygame.draw.ellipse(screen, (0, 255, 0), rect, 5)
    
    # Highlight possible moves for selected car
    if selected_car:
        for move in possible_moves:
            x = move[0] * 200 + 50
            y = move[1] * 200 + 50
            pygame.draw.ellipse(screen, (0, 255, 0), (x, y, 100, 100), 5)

    pygame.display.flip()


def handle_mouse_click(pos, board):
    global selected_car
    global possible_moves
    global game_state
    x, y = pos
    col = x // 200
    row = y // 200
    for car, coord in board.items():
        if car[0] == human_player:
            if coord == (col, row):
                selected_car = car
                possible_moves = game_state.get_valid_moves(selected_car)
                return
    if selected_car:
        if (col, row) in possible_moves:
            game_state = game_state.player_move(selected_car, (col,row))
            selected_car = None

    


    return None


def draw_menu(screen):
    screen.fill((255, 255, 255))
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Dodgem Game', True, (0, 0, 0))
    text_rect = text.get_rect(center=(300, 150))
    screen.blit(text, text_rect)

    blue_text = font.render('Blue Player', True, (0, 0, 255))
    blue_text_rect = blue_text.get_rect(center=(150, 400))
    screen.blit(blue_text, blue_text_rect)
    
    red_text = font.render('Red Player', True, (255, 0, 0))
    red_text_rect = red_text.get_rect(center=(450, 400))
    screen.blit(red_text, red_text_rect)
    
    pygame.display.flip()

    return blue_text_rect, red_text_rect




if __name__ == "__main__":
    main()
