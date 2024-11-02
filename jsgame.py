import pygame
import random
import math  # Import the math module for the sin function

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Let's Play a Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 223, 0)
DARK_GRAY = (105, 105, 105)  # Dark gray for clouds

# Game variables
gravity = 0.5
jump_strength = -12
player_speed = 5
player_y_velocity = 0
score = 0
is_game_active = False
show_instructions = True
on_ground = False

# Load the background image
background_img = pygame.image.load('bg.jpg').convert()

# Load player sprite image and resize it
player_image = pygame.image.load('js.png')  # Replace 'your_image.png' with your actual image file name
player_image = pygame.transform.scale(player_image, (70, 70))  # Resize to 70x70 pixels

# Player position
player = pygame.Rect(50, SCREEN_HEIGHT - 100, 70, 70)

# Platforms as cloud-like shapes with horizontal movement
platforms = [
    pygame.Rect(100, SCREEN_HEIGHT - 150, 200, 20),
    pygame.Rect(400, SCREEN_HEIGHT - 250, 200, 20),
    pygame.Rect(150, SCREEN_HEIGHT - 350, 200, 20),
    pygame.Rect(500, SCREEN_HEIGHT - 450, 200, 20),
]

# List to hold stars
stars = []
collected_stars = []  # Track collected stars to display progress

def spawn_star():
    """Spawn a star at a random position within the game area."""
    x = random.randint(20, SCREEN_WIDTH - 40)  # Random x position
    y = random.randint(0, SCREEN_HEIGHT - 20)  # Random y position
    star = pygame.Rect(x, y, 20, 20)
    stars.append(star)

# Initial star spawning
for _ in range(6):  # Spawn initial 6 stars
    spawn_star()

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Draw the background image
    screen.blit(background_img, (0, 0))  # Draw the background at (0, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if show_instructions:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                show_instructions = False
                is_game_active = True  # Start the game when space is pressed
        elif is_game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and on_ground:
                    player_y_velocity = jump_strength
                    on_ground = False

    if show_instructions:
        # Display the instructions screen
        screen.fill(WHITE)  # Instructions screen background
        screen.blit(title_font.render("Let's Play a game", True, BLACK), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100))
        screen.blit(font.render("Collect stars to win!", True, BLACK), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))
        screen.blit(font.render("Use LEFT and RIGHT arrow keys to move.", True, BLACK), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        screen.blit(font.render("Press SPACE to jump.", True, BLACK), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
        screen.blit(font.render("Press SPACE to start the game.", True, BLACK), (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100))

    elif is_game_active:
        # Game mechanics
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < SCREEN_WIDTH:
            player.x += player_speed

        # Apply gravity and jump
        player_y_velocity += gravity
        player.y += player_y_velocity

        # Check for platform collisions
        on_ground = False
        if player.bottom >= SCREEN_HEIGHT:  # Ground level
            player.bottom = SCREEN_HEIGHT
            player_y_velocity = 0
            on_ground = True
        else:
            for platform in platforms:
                if player.colliderect(platform) and player_y_velocity >= 0:
                    player.bottom = platform.top
                    player_y_velocity = 0
                    on_ground = True

        # Check for star collection
        for star in stars[:]:  # Iterate over a copy of the list
            if player.colliderect(star):
                score += 1
                stars.remove(star)
                collected_stars.append(star)  # Add to collected stars list
                spawn_star()  # Respawn a single new star immediately

        # Move platforms
        for platform in platforms:
            platform.x += 1  # Move platform right
            if platform.x > SCREEN_WIDTH:  # If the platform moves off the right side
                platform.x = -platform.width  # Wrap it to the left side

        # Draw the player image instead of a rectangle
        screen.blit(player_image, player.topleft)  # Draw the player image at the player's position

        # Draw platforms as clouds (now in dark gray)
        for platform in platforms:
            cloud_color = DARK_GRAY
            pygame.draw.ellipse(screen, cloud_color, (platform.x, platform.y - 10, platform.width // 2, platform.height))
            pygame.draw.ellipse(screen, cloud_color, (platform.x + platform.width // 3, platform.y - 15, platform.width // 2, platform.height))
            pygame.draw.ellipse(screen, cloud_color, (platform.x + platform.width // 2, platform.y - 10, platform.width // 2, platform.height))
            pygame.draw.rect(screen, cloud_color, platform)

        # Draw stars
        for star in stars:
            pygame.draw.polygon(screen, YELLOW, [
                (star.x + 10, star.y), 
                (star.x + 20, star.y + 20), 
                (star.x, star.y + 10), 
                (star.x + 20, star.y + 10), 
                (star.x, star.y + 20)
            ])

        # Display collected stars below the score counter
        for idx, collected_star in enumerate(collected_stars):
            pygame.draw.polygon(screen, YELLOW, [
                (10 + idx * 25, 40), 
                (20 + idx * 25, 60), 
                (0 + idx * 25, 50), 
                (20 + idx * 25, 50), 
                (0 + idx * 25, 60)
            ])

        # Draw score
        score_text = font.render(f"Stars Collected: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Check if score reaches 27
        if score >= 27:
            is_game_active = False
            
            # Final message screen
            screen.blit(background_img, (0, 0))  # Draw the background again for the final screen
            
            # Display final birthday message
            game_over_text = font.render("Game Over", True, YELLOW)
            stars_collected_text = font.render(f"{score} stars collected", True, YELLOW)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(stars_collected_text, (SCREEN_WIDTH // 2 - stars_collected_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

            # Bobbing effect for the character
            bobbing_offset = int(10 * math.sin(pygame.time.get_ticks() / 300))  # Bobbing effect

            # Draw the character bobbing slightly higher above the Game Over text
            bobbing_offset = int(10 * math.sin(pygame.time.get_ticks() / 300))  # Bobbing effect
            screen.blit(player_image, (SCREEN_WIDTH // 2 - player_image.get_width() // 2, SCREEN_HEIGHT // 2 - 180 + bobbing_offset))



            # Center and draw 27 stars
            total_star_width = 27 * 25  # Calculate total width of all stars
            start_x = (SCREEN_WIDTH - total_star_width) // 2  # Starting x position to center stars

            for i in range(27):
                pygame.draw.polygon(screen, YELLOW, [
                    (start_x + i * 25, SCREEN_HEIGHT // 2), 
                    (start_x + i * 25 + 10, SCREEN_HEIGHT // 2 + 20), 
                    (start_x + i * 25 - 10, SCREEN_HEIGHT // 2 + 10), 
                    (start_x + i * 25 + 10, SCREEN_HEIGHT // 2 + 10), 
                    (start_x + i * 25 - 10, SCREEN_HEIGHT // 2 + 20)
                ])

            pygame.display.flip()
            pygame.time.delay(1500)

            # Display "Happy 27th Birthday!" and "Play Again next year?"
            birthday_text = title_font.render("Happy 27th Birthday!", True, YELLOW)
            screen.blit(birthday_text, (SCREEN_WIDTH // 2 - birthday_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
            pygame.display.flip()
            pygame.time.delay(1500)
            
            play_again_text = font.render("Play Again next year?", True, YELLOW)
            screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
            pygame.display.flip()
            pygame.time.delay(3000)  # Display for a moment before restarting

            # Reset game state
            score = 0
            stars.clear()
            collected_stars.clear()
            for _ in range(6):  # Respawn initial stars
                spawn_star()
            is_game_active = False
            show_instructions = True  # Show instructions again

    pygame.display.flip()
    clock.tick(60)  # Frame rate

pygame.quit()

