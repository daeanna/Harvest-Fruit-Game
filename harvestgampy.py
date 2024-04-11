#! /usr/bin/env python3

import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
GRID_SIZE = 10 
GRID_WIDTH = 40
SCREEN_WIDTH = GRID_SIZE * GRID_WIDTH
SCREEN_HEIGHT = GRID_SIZE * GRID_WIDTH
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fruit Collection Game")

# Color palette
FRUIT_COLORS = {
    "blueberries": (225, 120, 197),
    "grapes": (255, 142, 143),
    "apples": (255, 179, 142),
    "oranges": (255, 253, 203)
}
BACKGROUND_COLOR = (231, 120, 197)  # Color palette background
PLAYER_COLOR = (0, 128, 255)  # Blue color for player
AI_COLOR = (255, 128, 0)  # Orange color for AI

# Game variables
player_pos = [0, 0]
ai_pos = [GRID_SIZE - 1, GRID_SIZE - 1]
player_trail = []
ai_trail = []
fruits = ["blueberries", "grapes", "apples", "oranges"]
fruit_names = ["Blueberries", "Grapes", "Apples", "Oranges"]
fruits_collected = 0
total_fruits = 0
player_score = 0
ai_score = 0
clock = pygame.time.Clock()

# Set initial fruit position
fruit_index = random.randint(0, len(fruits) - 1)
fruit_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
fruit_name = fruit_names[fruit_index]
fruit_color = FRUIT_COLORS[fruits[fruit_index]]

# Main game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos[1] > 0:
        player_pos[1] -= 1
    elif keys[pygame.K_s] and player_pos[1] < GRID_SIZE - 1:
        player_pos[1] += 1
    elif keys[pygame.K_a] and player_pos[0] > 0:
        player_pos[0] -= 1
    elif keys[pygame.K_d] and player_pos[0] < GRID_SIZE - 1:
        player_pos[0] += 1

    # AI movement towards fruit
    if ai_pos[0] < fruit_pos[0]:
        ai_pos[0] += 1
    elif ai_pos[0] > fruit_pos[0]:
        ai_pos[0] -= 1
    if ai_pos[1] < fruit_pos[1]:
        ai_pos[1] += 1
    elif ai_pos[1] > fruit_pos[1]:
        ai_pos[1] -= 1

    # Add current position to the trail
    player_trail.append(list(player_pos))
    ai_trail.append(list(ai_pos))

    # Limit the length of the trail
    if len(player_trail) > 5:
        player_trail.pop(0)
    if len(ai_trail) > 5:
        ai_trail.pop(0)

    if player_pos == ai_pos:
        player_score += 1
        ai_score += 1

    if player_pos == fruit_pos:
        player_score += 1
        fruits_collected += 1
        fruit_index = random.randint(0, len(fruits) - 1)
        fruit_name = fruit_names[fruit_index]
        fruit_color = FRUIT_COLORS[fruits[fruit_index]]
        fruit_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
    if ai_pos == fruit_pos:
        ai_score += 1
        fruits_collected += 1
        fruit_index = random.randint(0, len(fruits) - 1)
        fruit_name = fruit_names[fruit_index]
        fruit_color = FRUIT_COLORS[fruits[fruit_index]]
        fruit_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
    
    total_fruits += 2

    # Draw trail
    for pos in player_trail:
        pygame.draw.circle(screen, PLAYER_COLOR, (pos[0] * GRID_WIDTH + GRID_WIDTH // 2, pos[1] * GRID_WIDTH + GRID_WIDTH // 2), GRID_WIDTH // 4)
    for pos in ai_trail:
        pygame.draw.circle(screen, AI_COLOR, (pos[0] * GRID_WIDTH + GRID_WIDTH // 2, pos[1] * GRID_WIDTH + GRID_WIDTH // 2), GRID_WIDTH // 4)

    # Draw current positions
    pygame.draw.circle(screen, PLAYER_COLOR, (player_pos[0] * GRID_WIDTH + GRID_WIDTH // 2, player_pos[1] * GRID_WIDTH + GRID_WIDTH // 2), GRID_WIDTH // 4)
    pygame.draw.circle(screen, AI_COLOR, (ai_pos[0] * GRID_WIDTH + GRID_WIDTH // 2, ai_pos[1] * GRID_WIDTH + GRID_WIDTH // 2), GRID_WIDTH // 4)
    pygame.draw.circle(screen, fruit_color, (fruit_pos[0] * GRID_WIDTH + GRID_WIDTH // 2, fruit_pos[1] * GRID_WIDTH + GRID_WIDTH // 2), GRID_WIDTH // 4)

    # Draw fruit name
    font = pygame.font.Font(None, 24)
    text_surface = font.render(fruit_name, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 20))
    screen.blit(text_surface, text_rect)

    pygame.display.update()
    clock.tick(10)

# Game over, display scores and accuracy
screen.fill(BACKGROUND_COLOR)
font = pygame.font.Font(None, 36)
player_text = font.render(f"Player Score: {player_score}", True, PLAYER_COLOR)
ai_text = font.render(f"AI Score: {ai_score}", True, AI_COLOR)

accuracy_player = (player_score / total_fruits) * 100 if total_fruits != 0 else 0
accuracy_ai = (ai_score / total_fruits) * 100 if total_fruits != 0 else 0
accuracy_player_text = font.render(f"Player Accuracy: {accuracy_player:.2f}%", True, PLAYER_COLOR)
accuracy_ai_text = font.render(f"AI Accuracy: {accuracy_ai:.2f}%", True, AI_COLOR)

screen.blit(player_text, (SCREEN_WIDTH // 2 - player_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
screen.blit(ai_text, (SCREEN_WIDTH // 2 - ai_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
screen.blit(accuracy_player_text, (SCREEN_WIDTH // 2 - accuracy_player_text.get_width() // 2, SCREEN_HEIGHT // 2))
screen.blit(accuracy_ai_text, (SCREEN_WIDTH // 2 - accuracy_ai_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
pygame.display.update()

# Wait for a few seconds before quitting
pygame.time.wait(3000)
pygame.quit()
