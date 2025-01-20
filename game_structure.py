import pygame
import random
import pygame.mixer


# Initialize Pygame
pygame.init()

# Initialize the mixer
pygame.mixer.init()

# Load sound effects
shoot_sound = pygame.mixer.Sound('shooting_sound.mp3')
explosion_sound = pygame.mixer.Sound('explosion_sound.mp3')

shoot_sound.set_volume(0.5)
explosion_sound.set_volume(0.7)

# Load background music (optional)
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # Loop the music indefinitely


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

# Score and level settings
score = 0
level = 1


# Matrix for Player (Spaceship) and Enemy (Alien)
PLAYER_MATRIX = [
    [0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

ENEMY_MATRIX = [
    [0, 1, 1, 1, 0],
    [1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

BULLET_MATRIX = [
    [1],
    [1],
    [1]
]

# Function to draw a matrix object (player, enemy, bullet)
def draw_matrix(matrix, x, y, size=10):
    for row_index, row in enumerate(matrix):
        for col_index, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, WHITE, (x + col_index * size, y + row_index * size, size, size))


# Create enemies based on the current level
def create_enemies():
    global enemies
    enemies.clear()  # Clear existing enemies
    num_enemies = level * 5  # Increase number of enemies with each level
    for i in range(num_enemies // 2):
        for j in range(2):
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
                score += 10  # Increase score when an enemy is hit
                explosion_sound.play()
                break


# Display the score, level, and lives on the screen
def display_score_and_lives():
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))
    screen.blit(level_text, (WIDTH // 2 - 60, 10))


# Game Over screen
def game_over():
    font = pygame.font.SysFont(None, 50)
    game_over_text = font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - 150, HEIGHT // 2 + 20))
    pygame.display.flip()
    pygame.time.delay(3000)  # Show Game Over screen for 3 seconds


# Start the next level
def next_level():
    global level, enemy_speed
    level += 1
    enemy_speed += 1  # Increase enemy speed with each level
    create_enemies()


# Main game loop
def main():
    global player_x, bullets, enemies, player_lives, score, enemy_direction, level

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
                    shoot_sound.play()

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

        # If all enemies are cleared, go to next level
        if len(enemies) == 0:
            next_level()

        # Draw everything
        screen.fill(BLACK)

        # Draw player
        draw_matrix(PLAYER_MATRIX, player_x, player_y)

        # Draw bullets
        for bullet in bullets:
            draw_matrix(BULLET_MATRIX, bullet[0], bullet[1])

        # Draw enemies
        for enemy in enemies:
            draw_matrix(ENEMY_MATRIX, enemy[0], enemy[1])

        # Display score, level, and lives
        display_score_and_lives()

        # Game Over if no lives left
        if player_lives <= 0:
            game_over()
            running = False

        # Update the display
        pygame.display.flip()

    # Quit the game
    pygame.mixer.music.stop()
    pygame.quit()


# Run the game
if __name__ == "__main__":
    main()
