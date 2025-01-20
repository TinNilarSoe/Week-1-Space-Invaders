import pygame
import random

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
pygame.display.set_caption('Space Invaders')

# Player settings
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 60
player_speed = 5
player_lives = 3

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
enemy_direction = 1  # 1 means moving right, -1 means moving left

# Score
score = 0

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

# Move enemies (left-right motion + down)
def move_enemies():
    global player_lives, enemy_direction
    for enemy in enemies:
        enemy[0] += enemy_speed * enemy_direction  # Move left-right
        if enemy[0] <= 0 or enemy[0] >= WIDTH - enemy_width:
            enemy_direction *= -1  # Reverse direction when hitting the edge
            for e in enemies:
                e[1] += 10  # Move all enemies down when the direction reverses
                if e[1] > HEIGHT - enemy_height:  # Check if an enemy hits the bottom
                    player_lives -= 1
                    enemies.remove(e)

# Check for collisions
def check_collisions():
    global score
    global enemies, bullets
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if enemy[0] < bullet[0] < enemy[0] + enemy_width and enemy[1] < bullet[1] < enemy[1] + enemy_height:
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 10  # Increase score when enemy is hit
                break

# Display the score and lives on the screen
def display_score_and_lives():
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))

# Game Over screen
def game_over():
    font = pygame.font.SysFont(None, 50)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 150, HEIGHT // 2 + 20))
    pygame.display.flip()
    pygame.time.delay(3000)  # Show Game Over screen for 3 seconds

# Main game loop
def main():
    global player_x, bullets, enemies, player_lives, score, enemy_direction

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
                if event.key == pygame.K_SPACE:
                    bullet = [player_x + player_width // 2 - bullet_width // 2, player_y]
                    bullets.append(bullet)

        # Get mouse position and update player's position
        mouse_x, _ = pygame.mouse.get_pos()
        player_x = mouse_x - player_width // 2  # Center player on the mouse x position

        # Limit player's movement to within screen boundaries
        if player_x < 0:
            player_x = 0
        elif player_x > WIDTH - player_width:
            player_x = WIDTH - player_width

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

        # Display score and lives
        display_score_and_lives()

        # Game Over if no lives left
        if player_lives <= 0:
            game_over()
            running = False

        # Update the display
        pygame.display.flip()

    # Quit the game
    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
