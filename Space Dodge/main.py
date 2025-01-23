import pygame
import time
import random

pygame.font.init()

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

BG = pygame.transform.scale(pygame.image.load("./assets/bg.jpeg"), (WIDTH, HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5
STAR_WIDTH = 10
STAR_HEIGHT = 30
STAR_VEL = 3

FONT = pygame.font.SysFont("comicsans", 30)

# Load the arrow image
ARROW_IMG = pygame.transform.scale(pygame.image.load("./assets/arrow.png"), (30, 30))


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()


def draw_game_over(selected):
    WIN.fill((0, 0, 0))  # Clear the screen before redrawing.

    game_over_text = FONT.render("You Lost!", 1, "white")
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
                if event.key == pygame.K_UP:
                    selected = 1 if selected == 0 else 0  # Toggle between 0 and 1
                if event.key == pygame.K_RETURN:
                    if selected == 0:  # Quit
                        return False
                    elif selected == 1:  # Restart
                        return True
        pygame.time.delay(100)


def game_loop():
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - 80, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0

    stars = []
    hit = False

    while True:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            if not menu():  # If quit is selected, exit the loop
                return False
            else:  # If restart is selected, break out and restart the game
                return True

        draw(player, elapsed_time, stars)


def main():
    while True:
        if not game_loop():
            break  


if __name__ == "__main__":
    main()
