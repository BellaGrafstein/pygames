import packaging
import packaging.version
import packaging.specifiers
import packaging.requirements
import pygame

pygame.init()

#define font
font = pygame.font.SysFont('Constantia', 30)

# CONSTANTS #
WIDTH, HEIGHT = 804, 600
FPS = 60

BLACK = (0, 0, 0)
LIGHT_GREY = (210, 210, 210)
HARD = (140, 220, 90)
MED = (230, 110, 85)
EASY = (100, 145, 245)

COLS = 12
ROWS = 6

class wall():
    def __init__(self) -> None:
        self.width = WIDTH // COLS
        self.height = HEIGHT // 2 // ROWS
    
    def create_wall(self) -> None:
        self.blocks = []
        block = []

        for row in range(ROWS):
            block_row = []
            for col in range(COLS):
                # Make x and y for each block 
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                strength = 0
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                else:
                    strength = 1

                block = [rect, strength]
                block_row.append(block)
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                block_color = EASY
                if block[1] == 2:
                    block_color = MED
                if block[1] == 1:
                    block_color = HARD

                pygame.draw.rect(SCREEN, block_color, block[0])
                pygame.draw.rect(SCREEN, LIGHT_GREY, block[0], 2)


class paddle():
    def __init__(self):
        self.width = WIDTH // COLS
        self.height = 10
        self.x = (WIDTH // 2) - (self.width // 2)
        self.y = HEIGHT - 20
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.dir = 0

    def move(self):
        self.dir = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.dir = 0
        if key[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.dir = 1

    def draw_paddle(self):
        pygame.draw.rect(SCREEN, BLACK, self.rect)


class breaker():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        game_over = 0
        collision_thresh = 5
        wall_destroyed = 1
        # Check for collision with each block
        for row in wall.blocks:
            for block in row:
                if self.rect.colliderect(block[0]):
                    # Check if collisions came from above:
                    if abs(self.rect.bottom - block[0].top) > collision_thresh:
                        self.speed_y *= -1
                    if abs(self.rect.top - block[0].bottom) > collision_thresh:
                        self.speed_y *= -1
                    if abs(self.rect.right - block[0].left) > collision_thresh:
                        self.speed_x *= -1
                    if abs(self.rect.left - block[0].right) > collision_thresh:
                        self.speed_x *= -1

                    #reduce block strength
                    if block[1] > 1:
                        block[1] -= 1
                        wall_destroyed = 0
                    else:
                        block[0] = (0,0,0,0)
                if block[0] != (0,0,0,0):
                    wall_destroyed = 0
        if wall_destroyed == 1:
            game_over = 1

        # Check for collision with the paddle
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed_x *= -1
        if self.rect.top < 0:
            self.speed_y *= -1 
        if self.rect.bottom > HEIGHT:
            game_over = -1
        if self.rect.colliderect(paddle):
            if abs(self.rect.bottom - paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += paddle.dir
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
                self.speed_x = min(self.speed_x + paddle.dir, self.speed_max)
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return game_over

    def draw(self):
        pygame.draw.circle(SCREEN, BLACK, (self.rect.x  + self.rad, self.rect.y + self.rad), self.rad)

    def reset(self, x, y):
        self.rad = 10
        self.x = x - self.rad
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.rad * 2, self.rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5

## Initialize game data
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

wall = wall()
paddle = paddle()
breaker = breaker(paddle.x + paddle.width // 2, paddle.y - paddle.height)

def draw_window():
    SCREEN.fill(LIGHT_GREY)
    
    wall.draw_wall()
    paddle.draw_paddle()
    breaker.draw()

    pygame.display.update()

def draw_text(text, x, y):
    game_text = font.render(text, True, BLACK)
    SCREEN.blit(game_text, (x, y))

def main():
    
    clock = pygame.time.Clock()

    live_game = False
    game_over = 0
    wall.create_wall()
    draw_window()
    run = True
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not live_game:
                live_game = True
                wall.create_wall()
                breaker.reset( paddle.x + ( paddle.width // 2 ), paddle.y - paddle.height)
        
        if live_game:
            paddle.move()
            game_over = breaker.move()
            draw_window()
            if game_over != 0:
                live_game = False
        
        if not live_game:
            if game_over == 0:
                draw_text('CLICK ANYWHERE TO START', 185, HEIGHT // 2 + 100)
            elif game_over == 1:
                draw_text('YOU WON!', 310, HEIGHT // 2 + 50)
                draw_text('CLICK ANYWHERE TO START', 185, HEIGHT // 2 + 100)
            if game_over == -1:
                draw_text('YOU LOST!', 310, HEIGHT // 2 + 50)
                draw_text('CLICK ANYWHERE TO START', 185, HEIGHT // 2 + 100)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()