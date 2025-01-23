import pygame
import os
import time
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Fighters!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('assets/Gun+Silencer.mp3')
BGM_SOUND = pygame.mixer.Sound('assets/BGM.mp3')  # Background Music
WINNER_SOUND = pygame.mixer.Sound('assets/Winner.mp3')  # Winner Music
SELECT_SOUND = pygame.mixer.Sound('assets/Select.mp3')  # Select Sound

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
FONT = pygame.font.SysFont("comicsans", 30)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))

ARROW_IMG = pygame.transform.scale(pygame.image.load("./assets/arrow.png"), (30, 30))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()  # Play hit sound
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
            BULLET_HIT_SOUND.play()  # Play hit sound
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    WINNER_SOUND.play()  # Play winner music
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_game_over(selected):
    WIN.fill((0, 0, 0))  # Clear the screen before redrawing.

    game_over_text = FONT.render("Game Over!", 1, "white")
    WIN.blit(game_over_text, (WIDTH / 2 - game_over_text.get_width() / 2, HEIGHT / 2 - game_over_text.get_height() / 2))

    quit_text = FONT.render("Quit", 1, "white")
    restart_text = FONT.render("Restart", 1, "white")

    # Draw the ">" arrow for the selected option
    if selected == 0:  # If Quit is selected, the arrow should point to Quit
        WIN.blit(ARROW_IMG, (WIDTH / 2 - quit_text.get_width() / 2 - 40, HEIGHT / 2 + 50))
    else:  # If Restart is selected, the arrow should point to Restart
        WIN.blit(ARROW_IMG, (WIDTH / 2 - restart_text.get_width() / 2 - 40, HEIGHT / 2 + 100))

    WIN.blit(quit_text, (WIDTH / 2 - quit_text.get_width() / 2, HEIGHT / 2 + 50))
    WIN.blit(restart_text, (WIDTH / 2 - restart_text.get_width() / 2, HEIGHT / 2 + 100))

    pygame.display.update()


def menu():
    selected = 0  # 0: Quit, 1: Restart
    while True:
        draw_game_over(selected)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = 1 if selected == 0 else 0  # Toggle between 0 and 1
                    SELECT_SOUND.play()  # Play select sound
                if event.key == pygame.K_UP:
                    selected = 1 if selected == 0 else 0  # Toggle between 0 and 1
                    SELECT_SOUND.play()  # Play select sound
                if event.key == pygame.K_RETURN:
                    if selected == 0:  # Quit
                        return False
                    elif selected == 1:  # Restart
                        return True
        pygame.time.delay(100)


def main():
    def reset_game():
        return pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT), pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT), [], [], 10, 10

    red, yellow, red_bullets, yellow_bullets, red_health, yellow_health = reset_game()

    # Play background music in a loop
    pygame.mixer.music.load('assets/BGM.mp3')
    pygame.mixer.music.play(-1, 0.0)  # Play in loop

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()  # Play fire sound

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()  # Play fire sound

            if event.type == RED_HIT:
                red_health -= 1

            if event.type == YELLOW_HIT:
                yellow_health -= 1

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            if not menu():  # Show game over menu
                break  # Exit if quit is selected
            else:
                red, yellow, red_bullets, yellow_bullets, red_health, yellow_health = reset_game()  # Restart the game

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    pygame.quit()
    pygame.mixer.quit()  # Make sure to quit the mixer


if __name__ == "__main__":
    main()
