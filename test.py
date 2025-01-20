import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game settings
WIDTH = 800
HEIGHT = 600
FPS = 120  # Increased frame rate
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders with Spaceships')

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

def draw_matrix(matrix, x, y, size=10):
    for row_index, row in enumerate(matrix):
        for col_index, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(screen, WHITE, (x + col_index * size, y + row_index * size, size, size))

class Player:
    def __init__(self):
        self.matrix = PLAYER_MATRIX
        self.x = WIDTH // 2 - len(self.matrix[0]) * 10 // 2
        self.y = HEIGHT - 60
        self.speed = 10  # Increased speed
        self.lives = 3

    def move(self, mouse_x):
        self.x = mouse_x - len(self.matrix[0]) * 10 // 2
        self.x = max(0, min(self.x, WIDTH - len(self.matrix[0]) * 10))

    def draw(self):
        draw_matrix(self.matrix, self.x, self.y)

class Bullet:
    def __init__(self, x, y):
        self.matrix = BULLET_MATRIX
        self.x = x
        self.y = y
        self.speed = 15  # Increased bullet speed

    def move(self):
        self.y -= self.speed

    def draw(self):
        draw_matrix(self.matrix, self.x, self.y)

class Enemy:
    def __init__(self, x, y):
        self.matrix = ENEMY_MATRIX
        self.x = x
        self.y = y

    def draw(self):
        draw_matrix(self.matrix, self.x, self.y)

class Game:
    def __init__(self):
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.enemy_direction = 1
        self.score = 0
        self.level = 1
        self.enemy_speed = 4  # Starting speed
        self.enemy_rows = 3  # Level 1 has 3 rows of enemies
        self.create_enemies()

    def create_enemies(self):
        self.enemies.clear()
        enemy_count = 5  # Starting with 5 columns
        for i in range(enemy_count):
            for j in range(self.enemy_rows):
                enemy_x = 100 * i + 50
                enemy_y = 50 * j + 50
                self.enemies.append(Enemy(enemy_x, enemy_y))

    def move_enemies(self):
        for enemy in self.enemies[:]:
            enemy.x += self.enemy_speed * self.enemy_direction  # Adjust speed
            if enemy.x <= 0 or enemy.x >= WIDTH - len(enemy.matrix[0]) * 10:
                self.enemy_direction *= -1
                for e in self.enemies:
                    e.y += 10
                break

    def check_collisions(self):
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                if (enemy.x < bullet.x < enemy.x + len(enemy.matrix[0]) * 10 and
                        enemy.y < bullet.y < enemy.y + len(enemy.matrix) * 10):
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    self.score += 10
                    break

    def display_score_and_lives(self):
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.player.lives}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 150, 10))
        screen.blit(level_text, (WIDTH // 2 - 50, 10))

    def check_level_up(self):
        if len(self.enemies) == 0:  # Level up if all enemies are defeated
            self.level += 1
            self.enemy_rows += 1  # Add a new row of enemies
            self.enemy_speed += 0.5  # Increase enemy speed slightly
            self.create_enemies()  # Create new enemies for the next level
            self.enemy_direction *= -1  # Change enemy movement direction for each level

    def game_over(self):
        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render(f"Final Score: {self.score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.flip()
        pygame.time.delay(3000)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            clock.tick(FPS)  # Frame rate control

            mouse_x, _ = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        bullet = Bullet(self.player.x + len(self.player.matrix[0]) * 10 // 2 - 5, self.player.y)
                        self.bullets.append(bullet)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Spacebar to shoot
                        bullet = Bullet(self.player.x + len(self.player.matrix[0]) * 10 // 2 - 5, self.player.y)
                        self.bullets.append(bullet)

            self.player.move(mouse_x)

            for bullet in self.bullets[:]:
                bullet.move()
                if bullet.y < 0:
                    self.bullets.remove(bullet)

            self.move_enemies()
            self.check_collisions()

            for enemy in self.enemies:
                if enemy.y > HEIGHT - len(enemy.matrix) * 10:
                    self.player.lives -= 1
                    self.enemies.remove(enemy)

            self.check_level_up()  # Check if level is up after clearing all enemies

            if self.player.lives <= 0:
                self.game_over()
                running = False

            screen.fill(BLACK)
            self.player.draw()

            for bullet in self.bullets:
                bullet.draw()

            for enemy in self.enemies:
                enemy.draw()

            self.display_score_and_lives()
            pygame.display.flip()

        pygame.quit()

# Make sure to use __name__ and __main__
if __name__ == "__main__":
    Game().run()
