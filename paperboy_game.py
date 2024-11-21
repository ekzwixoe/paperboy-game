import pygame
import random
import sys
import traceback
import os
import logging

# Initialize Pygame
pygame.init()

# Enable logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
try:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Paperboy")
except pygame.error as e:
    logger.error(f"Failed to create display: {e}")
    sys.exit(1)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Game Objects
class Paperboy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed = 5
        self.score = 0
        self.lives = 3

    def move(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += self.speed

class Newspaper(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    COLORS = [RED, YELLOW, GREEN]
    
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(random.choice(self.COLORS))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class House(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

def main():
    try:
        # Game Setup
        clock = pygame.time.Clock()
        
        # Check if font is available
        available_fonts = pygame.font.get_fonts()
        logger.debug(f"Available fonts: {available_fonts}")
        
        # Use a fallback system for fonts
        try:
            font = pygame.font.SysFont('arial', 36)
            # Test font rendering
            test_render = font.render('Test', True, BLACK)
            logger.debug("Font rendering successful")
        except pygame.error as e:
            logger.error(f"Font error: {e}")
            font = pygame.font.Font(None, 36)  # Use default system font

        # Sprite Groups
        all_sprites = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        newspapers = pygame.sprite.Group()
        houses = pygame.sprite.Group()

        # Create Paperboy
        try:
            paperboy = Paperboy()
            all_sprites.add(paperboy)
            logger.debug("Paperboy created successfully")
        except Exception as e:
            logger.error(f"Failed to create Paperboy: {e}")
            raise

        # Game Loop
        running = True
        spawn_obstacle_timer = 0
        spawn_house_timer = 0

        logger.debug("Starting game loop")
        
        while running:
            try:
                # Event Handling
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    # Throw Newspaper
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        newspaper = Newspaper(paperboy.rect.right, paperboy.rect.centery)
                        all_sprites.add(newspaper)
                        newspapers.add(newspaper)

                # Key Handling
                keys = pygame.key.get_pressed()
                paperboy.move(keys)

                # Spawn Obstacles and Houses
                spawn_obstacle_timer += 1
                spawn_house_timer += 1

                if spawn_obstacle_timer > 60:
                    obstacle = Obstacle()
                    all_sprites.add(obstacle)
                    obstacles.add(obstacle)
                    spawn_obstacle_timer = 0

                if spawn_house_timer > 120:
                    house = House()
                    all_sprites.add(house)
                    houses.add(house)
                    spawn_house_timer = 0

                # Update
                all_sprites.update()

                # Collision Detection
                for newspaper in newspapers:
                    hit_houses = pygame.sprite.spritecollide(newspaper, houses, True)
                    if hit_houses:
                        paperboy.score += 1
                        newspaper.kill()

                if pygame.sprite.spritecollideany(paperboy, obstacles):
                    paperboy.lives -= 1
                    if paperboy.lives <= 0:
                        running = False

                # Clear Screen
                screen.fill(WHITE)

                # Draw Sprites
                all_sprites.draw(screen)

                # Draw Score and Lives
                score_text = font.render(f'Score: {paperboy.score}', True, BLACK)
                lives_text = font.render(f'Lives: {paperboy.lives}', True, BLACK)
                screen.blit(score_text, (10, 10))
                screen.blit(lives_text, (10, 50))

                # Update Display
                pygame.display.flip()
                clock.tick(60)

            except Exception as e:
                logger.error(f"Error in game loop: {e}")
                traceback.print_exc()
                running = False

        # Game Over Screen
        try:
            screen.fill(WHITE)
            game_over_text = font.render(f'Game Over! Score: {paperboy.score}', True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                                     SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(3000)
        except Exception as e:
            logger.error(f"Error displaying game over screen: {e}")

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        traceback.print_exc()
    finally:
        pygame.quit()
        logger.debug("Game cleaned up and closed")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Main function error: {e}")
        traceback.print_exc()
    sys.exit(0)
