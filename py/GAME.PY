import sys
import pygame
import constantes


WIDTH = constantes.WIDTH



HEIGHT = constantes.HEIGHT


window = pygame.display.set_mode((HEIGHT, WIDTH ))

i = 0



def draw_grid(window):
    window.fill(constantes.GREEN)
    x = 0
    y = 0 
    for i in range(WIDTH):
        x += constantes.GRID_SIZE
        y += constantes.GRID_SIZE
        pygame.draw.line(window, constantes.BLACK, (x, 0), (x, WIDTH))
        pygame.draw.line(window, constantes.BLACK, (0., y), (HEIGHT, y))





def main():
    pygame.init()
    pygame.display.set_caption(constantes.NAME_WINDOW)

    game_font = pygame.font.SysFont("Helvetica", 28)

    Clock = pygame.time.Clock()






    

    while True:

        Clock.tick(11)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            draw_grid(window)


            score = game_font.render("Score", True, constantes.BLACK)
            window.blit(score, (5,0))
            best_score = game_font.render("best score", True, constantes.BLACK)
            window.blit(best_score, (5,30))









            pygame.display.update()

        
main()


