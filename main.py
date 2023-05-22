import pygame
import os

# initialise pygame fonts
pygame.font.init()

# game window params
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
SEPARATOR = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

# set window name
pygame.display.set_caption("Space Game")

# frames per second
FPS = 60

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# spaceship params
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

# health font
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2 

# assets
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health):
    # background fill
    WIN.blit(BACKGROUND_IMAGE, (0, 0))

    # draw separator
    pygame.draw.rect(WIN, BLACK, SEPARATOR)

    # draw health font
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # draw spaceships
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    # draw yellow bullets
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    #draw red bullets
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    # update display window
    pygame.display.update()

def draw_winner_text(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, (WIDTH/2 - winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x > 0:    # YELLOW LEFT 
        yellow.x -= VEL

    if keys_pressed[pygame.K_d] and yellow.x < WIDTH/2 - 5 - SPACESHIP_WIDTH:    # YELLOW RIGHT 
        yellow.x += VEL

    if keys_pressed[pygame.K_w] and yellow.y > 0:    # YELLOW UP 
        yellow.y -= VEL

    if keys_pressed[pygame.K_s] and yellow.y < HEIGHT - SPACESHIP_HEIGHT - 25:    # YELLOW DOWN 
        yellow.y += VEL

def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x > WIDTH//2 + 15:    # RED LEFT 
        red.x -= VEL

    if keys_pressed[pygame.K_RIGHT] and red.x < WIDTH - SPACESHIP_WIDTH:    # RED RIGHT 
        red.x += VEL

    if keys_pressed[pygame.K_UP] and red.y > 0:    # RED UP 
        red.y -= VEL

    if keys_pressed[pygame.K_DOWN] and red.y < HEIGHT - SPACESHIP_HEIGHT - 25:    # RED DOWN 
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # move yellow bullets and check for collision with red spaceship
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL

        # check collision, register event
        if red.colliderect(bullet):
            # yellow bullet collides with red spaceship, register event, remove bullet
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        # check if bullet leaves screen
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
     
    # move red bullets and check for collision with yellow spaceship
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL

        # check collision, register event
        if yellow.colliderect(bullet):
            # red bullet collides with yellow spaceship, register event, remove bullet
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        
        # check if bullets leave screen
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def main():

    # spaceship rectangle holders
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # clock for controllin frames per second
    clock = pygame.time.Clock()

    # spaceship health
    red_health = 10
    yellow_health = 10

    # all bullets
    red_bullets = []
    yellow_bullets = []
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # listen for left and right controls to trigger bullet fire
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS: # yellow fire
                    # create bullet
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS: # red fire
                    # create bullet
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)

            # bullet hit events
            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1
            
        
        # manage health states
        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow Wins!"
        
        if yellow_health <= 0:
            winner_text = "Red Wins!"
        
        if winner_text != "":
            draw_winner_text(winner_text)
            break

        # get keys pressed for movement
        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)

        # handle bullet action
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        # draw objects on display window
        draw_window(red, yellow, yellow_bullets, red_bullets, red_health, yellow_health)
    
    pygame.quit()

if __name__ == "__main__":
    main()