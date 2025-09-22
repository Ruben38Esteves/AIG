import pygame
import dodgem

selected_car = None

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Dodgem")

    initial_board = {"B1":(0,0),"B2":(0,1),"R1":(1,2),"R2":(2,2)}
    game_state = dodgem.GameState(initial_board,"B")
    
    draw_board(screen, game_state.board)
    pygame.display.flip()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected_car = handle_mouse_click(event.pos, game_state.board)
                
                draw_board(screen, game_state.board, selected_car)
                pygame.display.flip()
    pygame.quit()


def draw_board(screen, board, selected_car=None):
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


def handle_mouse_click(pos, board):
    x, y = pos
    col = x // 200
    row = y // 200
    for car, coord in board.items():
        if coord == (col, row):
            return 
    if selected_car:
        

    return None





if __name__ == "__main__":
    main()