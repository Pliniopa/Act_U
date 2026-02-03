import sys, pygame, constantes, random, asyncio

WIDTH = constantes.WIDTH



HEIGHT = constantes.HEIGHT


window = pygame.display.set_mode((HEIGHT, WIDTH ))

i = 0





class Snake:
    def __init__(self):
        self.velocity = 20
        self.lengh = 1
        self.snake_body = [[220, 220], [240, 220]]
        self.actual_movements = random.choice(["right", "left", "down", "up"])
        self.incorrect_movements = {"right": ["left"],
                                    "left": ["right"],
                                    "up": ["down"],
                                    "down": ["up"]}
        self.best_score = 1
        self.temp_score = 1

    
    
    def move_snake(self, window):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_LEFT:
                    if self.check_valid_movement(pygame.key.name(event.key)):
                        continue

                    self.actual_movements = "left"

                if event.key == pygame.K_RIGHT:
                    if self.check_valid_movement(pygame.key.name(event.key)):
                        continue
                    self.actual_movements = "right"

                if event.key == pygame.K_UP:
                    if self.check_valid_movement(pygame.key.name(event.key)):
                        continue
                    self.actual_movements = "up"

                if event.key == pygame.K_DOWN:
                    if self.check_valid_movement(pygame.key.name(event.key)):
                        continue
                    self.actual_movements = "down"
        

        self.snake_movements(window)

    def snake_movements(self, window):
        if self.actual_movements == "right":
            temp = self.snake_body[0][0] + self.velocity
            x = self.check_bounds(temp, "max_limit")
            self.update_snake(x, "X", window)

        if self.actual_movements == "left":
            temp = self.snake_body[0][0] - self.velocity
            x = self.check_bounds(temp, "min_limit")
            self.update_snake(x, "X", window)

        if self.actual_movements == "up":
            temp = self.snake_body[0][1] - self.velocity
            y = self.check_bounds(temp, "min_limit")
            self.update_snake(y, "Y", window)

        if self.actual_movements == "down":
            temp = self.snake_body[0][1] + self.velocity
            y = self.check_bounds(temp, "max_limit")
            self.update_snake(y, "Y", window)


    def update_snake(self, value, key, window):
        if key == "X":
            self.snake_body.insert(0, [value, self.snake_body[0][1]])
            self.snake_body.pop()
            self.draw_snake(window)


        else:
            self.snake_body.insert(0, [self.snake_body[0][0], value])
            self.snake_body.pop()

            self.draw_snake(window)






    def draw_snake(self, window):
        for idx, body in enumerate(self.snake_body):
            if idx == 0:
                pygame.draw.rect(window, constantes.YELLOW, [body[0], body[1], 20, 20])
                continue
            pygame.draw.rect(window, constantes.PURPLE, [body[0], body[1], 20, 20])
    
    def check_valid_movement(self, next_mov):
        if next_mov in self.incorrect_movements[self.actual_movements]:
            return True
        
    def check_bounds(self, value_to_check_, limit):
        if limit == "max_limit":
            if value_to_check_ > 700:
                return 0
            else:
                return value_to_check_
        else:
            if value_to_check_ < 0:
                return 700
            else:
                return value_to_check_









def draw_grid(window):
    window.fill(constantes.GREEN)
    x = 0
    y = 0 
    for i in range(WIDTH):
        x += constantes.GRID_SIZE
        y += constantes.GRID_SIZE
        pygame.draw.line(window, constantes.BLACK, (x, 0), (x, WIDTH))
        pygame.draw.line(window, constantes.BLACK, (0., y), (HEIGHT, y))





async def main():
    pygame.init()
    pygame.display.set_caption(constantes.NAME_WINDOW)

    game_font = pygame.font.SysFont("Helvetica", 28)

    clock = pygame.time.Clock()
    snake = Snake()


    

    while True:

        clock.tick(11)

        draw_grid(window)
        snake.move_snake(window)


        score = game_font.render("Score", True, constantes.BLACK)
        window.blit(score, (5,0))
        best_score = game_font.render("best score", True, constantes.BLACK)
        window.blit(best_score, (5,30))

        pygame.display.update()
        await asyncio.sleep(0)

        
        
        
asyncio.run(main())



