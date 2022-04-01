## Thanks to Tech with Tim for the tutorial and assets! ##
import pygame
import os

pygame.font.init()

# CONSTNATS

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

FPS = 60
SHIP_WIDTH, SHIP_HEIGHT  = 55, 40
VELOCITY = 5
BULLET_SPEED = 7
BULLET_WIDTH = 10
BULLET_HEIGHT = 5
MAX_BULLETS = 5

# Players
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate( 
                        pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT )), 90)
RED_SPACESHIP_IMAGE    = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP_IMAGE    = pygame.transform.rotate(
                        pygame.transform.scale(RED_SPACESHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale( pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 40)

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

def draw_window(yellow_player, red_player, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Lives: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Lives: " + str(yellow_health), 1, WHITE)

    WIN.blit( yellow_health_text, (10, 10))
    WIN.blit( red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP_IMAGE, ( yellow_player.x, yellow_player.y))
    WIN.blit(RED_SPACESHIP_IMAGE,    ( red_player.x, red_player.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()

def handle_yellow_movement(yellow_player, keys_pressed):
    if keys_pressed[pygame.K_a] and yellow_player.x - VELOCITY > 0:          
        yellow_player.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow_player.x + yellow_player.width + VELOCITY < BORDER.x:          
        yellow_player.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow_player.y - VELOCITY > 0:          
        yellow_player.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow_player.y + yellow_player.height + VELOCITY < HEIGHT + 5:          
        yellow_player.y += VELOCITY


def handle_red_movement(red_player, keys_pressed):
    if keys_pressed[pygame.K_LEFT]  and red_player.x - VELOCITY > BORDER.x + BORDER.width:
        red_player.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red_player.x + red_player.width + VELOCITY < WIDTH: 
        red_player.x += VELOCITY
    if keys_pressed[pygame.K_UP]    and red_player.y - VELOCITY > 0:         
        red_player.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN]  and red_player.y + red_player.height + VELOCITY < HEIGHT + 5:  
        red_player.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow_player, red_player):
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED

        if red_player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x-= BULLET_SPEED

        if yellow_player.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width()//2, HEIGHT // 2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    yellow_player = pygame.Rect( 15, 250, SHIP_WIDTH, SHIP_WIDTH)
    red_player    = pygame.Rect(830, 250, SHIP_WIDTH, SHIP_WIDTH)

    clock = pygame.time.Clock()
    run = True

    yellow_bullets = []
    red_bullets = []

    yellow_health = 5
    red_health = 5

    while run:
        clock.tick(FPS)   
        for event in pygame.event.get():
            # Check event type
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) <= MAX_BULLETS:
                    yellow_bullets.append( pygame.Rect( 
                        yellow_player.x + yellow_player.width, 
                        yellow_player.y + yellow_player.height // 2 - 2,  
                        BULLET_WIDTH, BULLET_HEIGHT))

                if event.key == pygame.K_RCTRL and len(red_bullets) <= MAX_BULLETS:
                    red_bullets.append( pygame.Rect( 
                        red_player.x, 
                        red_player.y + red_player.height // 2 - 2,  
                        BULLET_WIDTH, BULLET_HEIGHT))
            
            if event.type == YELLOW_HIT:
                yellow_health -= 1

            if event.type == RED_HIT:
                red_health -= 1


        winner_text = ""
        if red_health < 0:
            winner_text = "Yellow won!"

        if yellow_health < 0:
            winner_text = "Red won!"
        
        if winner_text:
            draw_winner(winner_text)
            run = False

        keys_pressed = pygame.key.get_pressed()

        handle_bullets(yellow_bullets, red_bullets, yellow_player, red_player)
        handle_yellow_movement(yellow_player, keys_pressed)

        handle_red_movement(red_player, keys_pressed)

        draw_window(yellow_player, red_player, yellow_bullets, red_bullets, yellow_health, red_health)
        

    main()



if __name__ == "__main__":
    main()