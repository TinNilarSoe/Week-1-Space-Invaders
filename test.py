import pygame
# import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH = 800
HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Basic Space Invaders')

# Player settings
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 60
player_speed = 5

# Bullet settings
bullet_width = 5
bullet_height = 10
bullet_speed = 7
bullets = []

# Enemy settings
enemy_width = 40
enemy_height = 40
enemy_speed = 3
enemies = []


# Function to draw player
def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, player_width, player_height))


# Function to draw a bullet
def draw_bullet(bullet):
    pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))


# Function to draw an enemy
def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, enemy_width, enemy_height))


# Create enemies
def create_enemies():
    for i in range(5):
        for j in range(4):
            enemy_x = 100 * i + 50
            enemy_y = 50 * j + 50
            enemies.append([enemy_x, enemy_y])


# Move enemies down the screen
def move_enemies():
    for enemy in enemies:
        enemy[1] += enemy_speed


# Check for collisions
def check_collisions():
    global enemies, bullets
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if enemy[0] < bullet[0] < enemy[0] + enemy_width and enemy[1] < bullet[1] < enemy[1] + enemy_height:
                enemies.remove(enemy)
                bullets.remove(bullet)
                break


# Main game loop
def main():
    global player_x, bullets, enemies

    clock = pygame.time.Clock()
    create_enemies()

    running = True
    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_x > 0:
                    player_x -= player_speed
                elif event.key == pygame.K_RIGHT and player_x < WIDTH - player_width:
                    player_x += player_speed
                elif event.key == pygame.K_SPACE:
                    bullet = [player_x + player_width // 2 - bullet_width // 2, player_y]
                    bullets.append(bullet)

        # Move bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Move enemies
        move_enemies()

        # Check for collisions
        check_collisions()

        # Draw everything
        screen.fill(BLACK)

        # Draw player
        draw_player(player_x, player_y)

        # Draw bullets
        for bullet in bullets:
            draw_bullet(bullet)

        # Draw enemies
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1])

        # Game over if enemies reach the bottom
        for enemy in enemies:
            if enemy[1] > HEIGHT - enemy_height:
                running = False

        # Update the display
        pygame.display.flip()

    # Game over screen
    print("Game Over")
    pygame.quit()


# Run the game
if __name__ == "__main__":
    main()
