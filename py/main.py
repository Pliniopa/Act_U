import sys, pygame, constantes, random, asyncio

WIDTH = constantes.WIDTH
HEIGHT = constantes.HEIGHT

class Snake:
    def __init__(self):
        self.velocity = 20
        self.length = 1                    # unificado
        self.snake_body = [[220, 220]]
        self.actual_movements = random.choice(["right", "left", "down", "up"])
        self.incorrect_movements = {
            "right": ["left"],
            "left": ["right"],
            "up": ["down"],
            "down": ["up"]
        }
        self.best_score = 1
        self.temp_score = 1

    def move_snake(self, window):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # En Web: no cerrar proceso; señaliza salir
                return False

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
        return True

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
            color = constantes.YELLOW if idx == 0 else constantes.PURPLE
            pygame.draw.rect(window, color, [body[0], body[1], 20, 20])

    def check_valid_movement(self, next_mov):
        return next_mov in self.incorrect_movements[self.actual_movements]

    def check_bounds(self, value_to_check_, limit):
        # Nota: 680 asume ventana 700x700 y GRID 20.
        if limit == "max_limit":
            if value_to_check_ > 680:
                return 0
            else:
                return value_to_check_
        else:
            if value_to_check_ < 0:
                return 680
            else:
                return value_to_check_

    def get_snake_head(self):
        return self.snake_body[0]

    def grow_snake(self, value, window):
        # Crece insertando cabeza sin hacer pop()
        self.snake_body.insert(0, list(value))
        
        self.length += 1
        self.draw_snake(window)

class Food:
    def __init__(self):
        self.food_position = (0, 0)
        self.random_position()

    def random_position(self):
        self.food_position = (
            random.randrange(0, 680, 20),
            random.randrange(0, 680, 20)
        )

    def draw_food(self, window):
        pygame.draw.rect(window, constantes.RED, [self.food_position[0], self.food_position[1], 20, 20])

def check_food(snake, food, window):
    if tuple(snake.get_snake_head()) == food.food_position:
        snake.grow_snake(food.food_position, window)
        food.random_position()
        food.draw_food(window)

def draw_grid(window):
    window.fill(constantes.GREEN)
    x = 0
    y = 0
    for _ in range(WIDTH):
        x += constantes.GRID_SIZE
        y += constantes.GRID_SIZE
        pygame.draw.line(window, constantes.BLACK, (x, 0), (x, HEIGHT))
        pygame.draw.line(window, constantes.BLACK, (0, y), (WIDTH, y))

async def main():
    pygame.init()
    pygame.display.set_caption(constantes.NAME_WINDOW)

    # Crea la ventana *después* de init, en el orden correcto:
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Fuente con fallback para Web:
    game_font = pygame.font.Font(None, 28)

    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()

    running = True
    while running:
        clock.tick(11)

        draw_grid(window)
        food.draw_food(window)
        running = snake.move_snake(window)
        check_food(snake, food, window)

        score = game_font.render(f"Score {snake.length}", True, constantes.BLACK)
        window.blit(score, (5, 0))
        best_score = game_font.render("best score", True, constantes.BLACK)
        window.blit(best_score, (5, 30))

        pygame.display.update()

        # Ceder control al navegador (OBLIGATORIO en pygbag)
        await asyncio.sleep(0)  # <- no lo quites

# Entrada para pygbag (no pongas código después):
asyncio.run(main())