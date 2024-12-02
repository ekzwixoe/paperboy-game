import pygame
import random
import sys
import traceback
import os
import logging
from pathlib import Path

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paperboy")

# Enable logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Game Zones
TOP_LANE_Y = SCREEN_HEIGHT * 0.2
BOTTOM_LANE_Y = SCREEN_HEIGHT * 0.6
PAPERBOY_MIN_Y = SCREEN_HEIGHT * 0.15
PAPERBOY_MAX_Y = SCREEN_HEIGHT * 0.75

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Sound Effects `````````````````````````````````````````````````````
def load_sound_effects():
    try:
        sound_effects = {}
        crash_path = Path(__file__).parent / 'assets' / 'sounds' / 'crash.wav'
        if crash_path.exists():
            sound_effects['crash'] = pygame.mixer.Sound(str(crash_path))
            sound_effects['crash'].set_volume(0.7)  # Set volume (0.0 to 1.0)
            logger.info("Crash sound effect loaded successfully.")
        else:
            logger.warning("Crash sound effect file not found.")
        # Load throw sound `````````````````````````````````````````
        throw_path = Path(__file__).parent / 'assets' / 'sounds' / 'throw.wav'
        if throw_path.exists():
            sound_effects['throw'] = pygame.mixer.Sound(str(throw_path))
            sound_effects['throw'].set_volume(0.7)  # Set volume (0.0 to 1.0)
            logger.info("Throw sound effect loaded successfully.")
        else:
            logger.warning("Throw sound effect file not found.")
        # Load success sound ### 추가됨`````````````````````````````
        success_path = Path(__file__).parent / 'assets' / 'sounds' / 'success.wav'
        if success_path.exists():
            sound_effects['success'] = pygame.mixer.Sound(str(success_path))
            sound_effects['success'].set_volume(0.7)  # Set volume (0.0 to 1.0)
            logger.info("Success sound effect loaded successfully.")
        else:
            logger.warning("Success sound effect file not found.")

        return sound_effects
    except pygame.error as e:
        logger.error(f"Error loading sound effects: {e}")
        return {}

# background music'''''''''''''''''''''''''''''''''''''''''''''''``````
def play_background_music():
    try:
        music_path = Path(__file__).parent / 'assets' / 'sounds' / 'back_sounds.wav'
        if music_path.exists():
            pygame.mixer.music.load(str(music_path))  # Load the music
            pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
            pygame.mixer.music.play(-1)  # Play music in a loop (-1 for infinite)
            logger.info("Background music started successfully.")
        else:
            logger.warning("Background music file not found.")
            # Load game over sound
        game_over_path = Path(__file__).parent / 'assets' / 'sounds' / 'game_over.wav'
        if game_over_path.exists():
            sound_effects['game_over'] = pygame.mixer.Sound(str(game_over_path))
            sound_effects['game_over'].set_volume(0.7)  # Set volume
            logger.info("Game over sound effect loaded successfully.")
        else:
            logger.warning("Game over sound effect file not found.")

            
    except pygame.error as e:
        logger.error(f"Error loading or playing background music: {e}")

# Asset Loading
def load_image(path):
    try:
        image = pygame.image.load(path)
        return image.convert_alpha()
    except pygame.error as e:
        logger.error(f"Couldn't load image {path}: {e}")
        return None

class AssetLoader:
    def __init__(self):
        self.assets_dir = Path(__file__).parent / 'assets'
        self.paperboy = None
        self.houses = []
        self.obstacles = []
        self.newspaper = None
        self.background = None
        self.scenery = {
            'sky': None,
            'hills': [],
            'buildings': [],
            'grass': None
        }
        
    def load_assets(self):
        # Load paperboy sprite
        paperboy_path = self.assets_dir / 'paperboy' / 'paper-boy.png'
        if paperboy_path.exists():
            self.paperboy = load_image(str(paperboy_path))
            if self.paperboy:
                self.paperboy = pygame.transform.scale(self.paperboy, (100, 100))
        
        # Load delivery houses
        house_dir = self.assets_dir / 'delivery-houses'
        for i in range(5):
            suffix = f"-{i+1}" if i > 0 else ""
            path = house_dir / f'house{suffix}.png'
            if path.exists():
                image = load_image(str(path))
                if image:
                    image = pygame.transform.scale(image, (120, 120))
                    self.houses.append(image)
        
        # Load newspaper
        newspaper_path = self.assets_dir / 'newspapers' / 'newspaper.png'
        if newspaper_path.exists():
            self.newspaper = load_image(str(newspaper_path))
            if self.newspaper:
                self.newspaper = pygame.transform.scale(self.newspaper, (40, 40))
        
        # Load obstacles
        obstacle_sources = ['vehicles', 'animals', 'people']
        for source in obstacle_sources:
            source_dir = self.assets_dir / source
            if source_dir.exists():
                for file in source_dir.glob('*.png'):
                    image = load_image(str(file))
                    if image:
                        image = pygame.transform.scale(image, (80, 80))
                        self.obstacles.append(image)
        
        # Load background elements
        scenery_dir = self.assets_dir / 'scenery'
        
        # Load sky
        sky_path = scenery_dir / 'sky.png'
        if sky_path.exists():
            self.scenery['sky'] = load_image(str(sky_path))
            if self.scenery['sky']:
                self.scenery['sky'] = pygame.transform.scale(self.scenery['sky'], (SCREEN_WIDTH, int(SCREEN_HEIGHT * 0.4)))
        
        # Load hills and buildings
        for file in scenery_dir.glob('hill*.png'):
            image = load_image(str(file))
            if image:
                image = pygame.transform.scale(image, (300, 200))
                self.scenery['hills'].append(image)
        
        for file in scenery_dir.glob('*building*.png'):
            image = load_image(str(file))
            if image:
                image = pygame.transform.scale(image, (200, 300))
                self.scenery['buildings'].append(image)
        
        # Load grass
        grass_path = scenery_dir / 'sky-and-grass.png'
        if grass_path.exists():
            self.scenery['grass'] = load_image(str(grass_path))
            if self.scenery['grass']:
                self.scenery['grass'] = pygame.transform.scale(self.scenery['grass'], (SCREEN_WIDTH, int(SCREEN_HEIGHT * 0.3)))
        
        # Load street (main background)
        street_path = scenery_dir / 'street-3.png'
        if street_path.exists():
            self.background = load_image(str(street_path))
            if self.background:
                self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, int(SCREEN_HEIGHT * 0.5)))

class SceneryElement(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.scroll_speed = 2
    
    def update(self):
        self.rect.x -= self.scroll_speed
        if self.rect.right < 0:
            self.kill()

class Background:
    def __init__(self, street_image, scenery):
        self.street = street_image
        self.scenery = scenery
        self.scroll_speed = 3
        self.street_positions = [0]
        
        # Initialize street positions for seamless scrolling
        while self.street_positions[-1] + self.street.get_width() < SCREEN_WIDTH * 2:
            self.street_positions.append(self.street_positions[-1] + self.street.get_width())
        
        # Track scenery elements
        self.scenery_elements = pygame.sprite.Group()
        self.scenery_timer = 0
    
    def add_random_scenery(self):
        if random.random() < 0.3:  
            if random.random() < 0.5:  
                image = random.choice(self.scenery['hills'] + self.scenery['buildings'])
                y = random.choice([0, SCREEN_HEIGHT - image.get_height()])
            else:  
                return  
            
            element = SceneryElement(image, SCREEN_WIDTH, y)
            self.scenery_elements.add(element)
    
    def update(self):
        # Update street positions
        for i in range(len(self.street_positions)):
            self.street_positions[i] -= self.scroll_speed
            if self.street_positions[i] + self.street.get_width() < 0:
                rightmost = max(self.street_positions)
                self.street_positions[i] = rightmost + self.street.get_width()
        
        # Update scenery
        self.scenery_timer += 1
        if self.scenery_timer > 120:  
            self.add_random_scenery()
            self.scenery_timer = 0
        
        self.scenery_elements.update()
    
    def draw(self, screen):
        # Draw sky
        if self.scenery['sky']:
            screen.blit(self.scenery['sky'], (0, 0))
        
        # Draw scenery elements
        self.scenery_elements.draw(screen)
        
        # Draw street
        street_y = (SCREEN_HEIGHT - self.street.get_height()) // 2
        for pos in self.street_positions:
            screen.blit(self.street, (pos, street_y))
        
        # Draw grass at bottom
        if self.scenery['grass']:
            screen.blit(self.scenery['grass'], (0, SCREEN_HEIGHT - self.scenery['grass'].get_height()))

class Paperboy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if asset_loader.paperboy:
            self.image = asset_loader.paperboy
        else:  
            self.image = pygame.Surface([30, 30])
            self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT // 2
        self.speed = 5
        self.score = 0
        self.lives = 3

    def move(self, keys):
        if keys[pygame.K_UP] and self.rect.top > PAPERBOY_MIN_Y:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < PAPERBOY_MAX_Y:
            self.rect.y += self.speed

class Newspaper(pygame.sprite.Sprite):
    def __init__(self, x, y, is_top_throw=True):
        super().__init__()
        if asset_loader.newspaper:
            self.image = asset_loader.newspaper
        else:  
            self.image = pygame.Surface([10, 10])
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 8
        self.speed_y = -8 if is_top_throw else 8
        self.is_top_throw = is_top_throw

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left > SCREEN_WIDTH or self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        if asset_loader.obstacles:
            self.image = random.choice(asset_loader.obstacles)
        else:  
            self.image = pygame.Surface([30, 30])
            self.image.fill(random.choice([RED, YELLOW, GREEN]))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(int(PAPERBOY_MIN_Y), int(PAPERBOY_MAX_Y))
        self.speed = random.randint(3, 7)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

class House(pygame.sprite.Sprite):
    def __init__(self, is_top_lane=True):
        super().__init__()
        if asset_loader.houses:
            self.image = random.choice(asset_loader.houses)
        else:
            self.image = pygame.Surface([40, 40])
            self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = TOP_LANE_Y if is_top_lane else BOTTOM_LANE_Y
        self.speed = 3
        self.is_top_lane = is_top_lane

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()


class VolumeControl:  # 음소거 추가``````````````````````````````````````````````````````````````````````````````
    def __init__(self, mute_icon_path, unmute_icon_path):
        self.mute_icon = pygame.transform.scale(load_image(mute_icon_path), (30, 30))  # 미니 사이즈로 조정
        self.unmute_icon = pygame.transform.scale(load_image(unmute_icon_path), (30, 30))  # 미니 사이즈로 조정
        self.icon = self.unmute_icon  # Default to unmute
        self.rect = self.icon.get_rect(topright=(SCREEN_WIDTH - 10, 10))  # 오른쪽 상단으로 위치 변경
        self.is_muted = False

    def toggle_mute(self):
        self.is_muted = not self.is_muted
        self.icon = self.mute_icon if self.is_muted else self.unmute_icon
        pygame.mixer.music.set_volume(0 if self.is_muted else 0.5)

    def draw(self, screen):
        screen.blit(self.icon, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.toggle_mute()

def main():
    try:
        # Game Setup
        clock = pygame.time.Clock()
        
        # Font setup
        available_fonts = pygame.font.get_fonts()
        logger.debug(f"Available fonts: {available_fonts}")
        
        try:
            font = pygame.font.SysFont('arial', 36)
            test_render = font.render('Test', True, BLACK)
            logger.debug("Font rendering successful")
        except pygame.error as e:
            logger.error(f"Font error: {e}")
            font = pygame.font.Font(None, 36)

        # Create background
        background = Background(asset_loader.background, asset_loader.scenery)
        
        # Sprite Groups
        all_sprites = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        newspapers = pygame.sprite.Group()
        houses = pygame.sprite.Group()

        # Create Paperboy
        paperboy = Paperboy()
        paperboy.rect.y = SCREEN_HEIGHT // 2  
        all_sprites.add(paperboy)

        # Create volume control ````````````````````````````````````````````````````````````````````
        volume_control = VolumeControl(
            mute_icon_path=str(Path(__file__).parent / 'assets' / 'sounds' / 'mute.png'),
            unmute_icon_path=str(Path(__file__).parent / 'assets' / 'sounds' / 'unmute.png')
        )
        
        # Game Loop
        running = True
        spawn_obstacle_timer = 0
        spawn_house_timer = 0
        invincible_timer = 0
        INVINCIBLE_DURATION = 120
        
        while running:
            try:
                # Event handling````````````````````````````````````````
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    
                    # Throw Newspaper
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:  
                            newspaper = Newspaper(paperboy.rect.right, paperboy.rect.centery, True)
                            all_sprites.add(newspaper)
                            newspapers.add(newspaper)
                             # Play throw sound effect````````````````````````````
                            if 'throw' in sound_effects:
                                sound_effects['throw'].play()
                            else:
                                logger.warning("Throw sound effect not loaded.")
                            
                        elif event.key == pygame.K_RIGHT:  
                            newspaper = Newspaper(paperboy.rect.right, paperboy.rect.centery, False)
                            all_sprites.add(newspaper)
                            newspapers.add(newspaper)
                            # Play throw sound effect````````````````````````````
                            if 'throw' in sound_effects:
                                sound_effects['throw'].play()
                            else:
                                logger.warning("Throw sound effect not loaded.")
                    #mute button event````````````````````````````
                    volume_control.handle_event(event)
                
                # Movement
                keys = pygame.key.get_pressed()
                paperboy.move(keys)
                
                # Spawn objects
                spawn_obstacle_timer += 1
                spawn_house_timer += 1
                
                if spawn_obstacle_timer > 120:
                    obstacle = Obstacle()
                    all_sprites.add(obstacle)
                    obstacles.add(obstacle)
                    spawn_obstacle_timer = 0
                
                if spawn_house_timer > 180:
                    is_top = random.choice([True, False])
                    house = House(is_top)
                    all_sprites.add(house)
                    houses.add(house)
                    spawn_house_timer = 0
                
                # Update
                background.update()
                all_sprites.update()
                
                # Collision detection
                for newspaper in newspapers:
                    hit_houses = pygame.sprite.spritecollide(newspaper, houses, True)
                    if hit_houses:
                        for house in hit_houses:
                            if (newspaper.is_top_throw and house.is_top_lane) or \
                               (not newspaper.is_top_throw and not house.is_top_lane):
                                paperboy.score += 1
                                # Play success sound effect ### 추가됨````````````````````
                                if 'success' in sound_effects:
                                    sound_effects['success'].play()
                                else:
                                    logger.warning("Success sound effect not loaded.")
                                
                        newspaper.kill()
                
                # Invincibility and collision handling ### 추가됨``````````````````
                if invincible_timer <= 0:
                    collided_obstacle = pygame.sprite.spritecollideany(paperboy, obstacles)
                    if collided_obstacle:
                        # Play sound effect when a collision occurs
                        if 'crash' in sound_effects:
                            sound_effects['crash'].play()  # Play the sound
                        else:
                            logger.warning("Crash sound effect not loaded or unavailable.")

                        # Handle collision logic
                        paperboy.lives -= 1
                        if paperboy.lives <= 0:
                            # Play game over sound effect ##추가됨````````````````````````````````````````````````
                            if 'game_over' in sound_effects:
                                sound_effects['game_over'].play()  # Play the game over sound
                            else:
                                logger.warning("Game over sound effect not loaded.")
                
                            running = False  # End game
                        else:
                            # Remove all obstacles upon collision
                            for obstacle in obstacles:
                                obstacle.kill()
                            invincible_timer = INVINCIBLE_DURATION
                else:
                    invincible_timer -= 1
                
                
                # Drawing
                screen.fill(WHITE)
                background.draw(screen)
                all_sprites.draw(screen)

                # Draw volume control ``````````````````````````````````````````````````````````````````````````
                volume_control.draw(screen)
                
                # UI
                score_text = font.render(f'Score: {paperboy.score}', True, BLACK)
                lives_text = font.render(f'Lives: {paperboy.lives}', True, BLACK)
                screen.blit(score_text, (10, 10))
                screen.blit(lives_text, (10, 50))
                
                pygame.display.flip()
                clock.tick(60)
                
            except Exception as e:
                logger.error(f"Error in game loop: {e}")
                traceback.print_exc()
                running = False
        
        pygame.quit()
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        traceback.print_exc()
        pygame.quit()

if __name__ == "__main__":
    try:
        # Create global asset loader
        asset_loader = AssetLoader()
        asset_loader.load_assets()  # Load all assets

        # Load sound effects`````````````````````````````````````
        sound_effects = load_sound_effects()
        
        # Start background music''''''''''''''''''''''''''''''''''
        play_background_music()
        
        main()
    except Exception as e:
        logger.error(f"Main function error: {e}")
        traceback.print_exc()
    sys.exit(0)
