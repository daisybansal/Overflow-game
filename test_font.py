import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Font Test")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load a font
font = pygame.font.SysFont("Arial", 48)

# Create a text surface
text_surface = font.render("Hello, Pygame!", True, BLACK)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with white
    screen.fill(WHITE)
    
    # Blit (copy) the text surface onto the screen
    screen.blit(text_surface, (200, 250))
    
    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

