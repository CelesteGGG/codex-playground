"""
Simple Falling Obstacles Game (Pygame)

Run with:
    python main.py
"""

import random
import sys

import pygame


# ----------------------------
# Game configuration constants
# ----------------------------
WIDTH, HEIGHT = 600, 800
FPS = 60

PLAYER_SIZE = 50
PLAYER_SPEED = 7

OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 50
OBSTACLE_SPEED = 5
OBSTACLE_SPAWN_TIME_MS = 800  # spawn a new obstacle every 0.8 seconds

FONT_SIZE = 36


def reset_game():
    """Return a fresh game state."""
    player = pygame.Rect(
        (WIDTH - PLAYER_SIZE) // 2,
        HEIGHT - PLAYER_SIZE - 20,
        PLAYER_SIZE,
        PLAYER_SIZE,
    )
    obstacles = []
    score = 0
    game_over = False
    return player, obstacles, score, game_over


def main():
    # Initialize pygame and create the main window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Falling Obstacles")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, FONT_SIZE)

    # Create a timer event for spawning obstacles
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, OBSTACLE_SPAWN_TIME_MS)

    # Initialize game state
    player, obstacles, score, game_over = reset_game()

    running = True
    while running:
        clock.tick(FPS)

        # ----------------------------
        # Event handling
        # ----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == SPAWN_EVENT and not game_over:
                # Create a new obstacle at a random x-position
                x_pos = random.randint(0, WIDTH - OBSTACLE_WIDTH)
                obstacle = pygame.Rect(x_pos, -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
                obstacles.append(obstacle)

            if event.type == pygame.KEYDOWN and game_over:
                # Restart the game when the player presses R
                if event.key == pygame.K_r:
                    player, obstacles, score, game_over = reset_game()

        # ----------------------------
        # Player movement
        # ----------------------------
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT]:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT]:
                player.x += PLAYER_SPEED

            # Keep the player inside the window
            player.x = max(0, min(player.x, WIDTH - PLAYER_SIZE))

        # ----------------------------
        # Update obstacles
        # ----------------------------
        if not game_over:
            for obstacle in obstacles:
                obstacle.y += OBSTACLE_SPEED

            # Remove obstacles that move off-screen and increase score
            obstacles = [o for o in obstacles if o.y < HEIGHT]
            score += 1  # simple score: increase each frame the player survives

            # Check for collisions
            for obstacle in obstacles:
                if player.colliderect(obstacle):
                    game_over = True
                    break

        # ----------------------------
        # Drawing
        # ----------------------------
        screen.fill((30, 30, 30))  # dark background

        # Draw player (green square)
        pygame.draw.rect(screen, (0, 200, 0), player)

        # Draw obstacles (red squares)
        for obstacle in obstacles:
            pygame.draw.rect(screen, (200, 0, 0), obstacle)

        # Draw score text
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

        # Draw game over message
        if game_over:
            game_over_text = font.render("Game Over! Press R to Restart", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
