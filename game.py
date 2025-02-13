#   This is the game that I coded the bots to play.  You can also play against your bot
#   To run the game you will need pygames installed.  See: https://pypi.org/project/pygame/
#   Once you have pygames, you can run the game by using the command:
#   python game.py
#   
#   the gem images used are from opengameart.org by qubodup
#   https://opengameart.org/content/rotating-crystal-animation-8-step,
#   https://creativecommons.org/licenses/by/3.0/

import pygame
pygame.mixer.quit()
import sys
import math

from a1_partd import overflow
from a1_partc import Queue
from player1 import PlayerOne
from player2 import PlayerTwo 

class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.current_option = 0

    def draw(self, window):
        # Add white background fill and black border
        pygame.draw.rect(window, WHITE, (self.x, self.y, self.width, self.height))  # White background
        pygame.draw.rect(window, BLACK, (self.x, self.y, self.width, self.height), 2)  # Black border
        
        font = pygame.font.Font(None, 36)
        text = font.render(self.options[self.current_option], True, BLACK)
        # Center the text
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        window.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if self.x < x < self.x + self.width and self.y < y < self.y + self.height:
                self.current_option = (self.current_option + 1) % len(self.options)

    def get_choice(self):
        return self.current_option

class Board:
    def __init__(self, width, height, p1_sprites, p2_sprites):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.p1_sprites = p1_sprites
        self.p2_sprites = p2_sprites
        self.board[0][0] = 1
        self.board[self.height-1][self.width-1] = -1
        self.turn = 0

    def get_board(self):
        current_board = []
        for i in range(self.height):
            current_board.append(self.board[i].copy())
        return current_board

    def valid_move(self, row, col, player):
        if row >= 0 and row < self.height and col >= 0 and col < self.width and (self.board[row][col] == 0 or self.board[row][col] / abs(self.board[row][col]) == player):
            return True
        return False

    def add_piece(self, row, col, player):
        if self.valid_move(row, col, player):
            self.board[row][col] += player
            # Check for overflow immediately
            if abs(self.board[row][col]) >= 4:
                # Get the player color
                current_color = self.board[row][col] // abs(self.board[row][col])
                # Reset the overflowing cell
                self.board[row][col] = 0
                # Spread to adjacent cells
                neighbors = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
                for nr, nc in neighbors:
                    if 0 <= nr < self.height and 0 <= nc < self.width:
                        # Add a gem of the current player's color
                        if self.board[nr][nc] == 0:
                            self.board[nr][nc] = current_color
                        else:
                            # Convert existing gems to current player's color
                            self.board[nr][nc] = current_color * (abs(self.board[nr][nc]) + 1)
            self.turn += 1
            return True
        return False

    def check_win(self):
        if self.turn > 0:
            num_p1 = 0
            num_p2 = 0
            for i in range(self.height):
                for j in range(self.width):
                    if self.board[i][j] > 0:
                        if num_p2 > 0:
                            return 0
                        num_p1 += 1
                    elif self.board[i][j] < 0:
                        if num_p1 > 0:
                            return 0
                        num_p2 += 1
            if num_p1 == 0:
                return -1
            if num_p2 == 0:
                return 1
        return 0

    def do_overflow(self, q):
        oldboard = []
        for i in range(self.height):
            oldboard.append(self.board[i].copy())
        numsteps = overflow(self.board, q)
        if numsteps != 0:
            self.set(oldboard)
        return numsteps
    
    def set(self, newboard):
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = newboard[row][col]

    def draw(self, window, frame):
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE + X_OFFSET, row * CELL_SIZE + Y_OFFSET, CELL_SIZE, CELL_SIZE)
                # Force pure white background using direct RGB values
                pygame.draw.rect(window, (255, 255, 255), rect)  # Pure white fill
                pygame.draw.rect(window, (0, 0, 0), rect, 1)  # Black border
                
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col] != 0:
                    rpos = row * CELL_SIZE + Y_OFFSET
                    cpos = col * CELL_SIZE + X_OFFSET
                    if self.board[row][col] > 0:
                        sprite = self.p1_sprites
                    else:
                        sprite = self.p2_sprites
                    if abs(self.board[row][col]) == 1:
                        cpos += CELL_SIZE //2 - 16
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 2:
                        cpos += CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2 - 16
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

                    elif abs(self.board[row][col]) == 3:
                        cpos += CELL_SIZE //2 - 16
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos = col * CELL_SIZE + X_OFFSET + CELL_SIZE //2 - 32
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                    elif abs(self.board[row][col]) == 4:
                        cpos += CELL_SIZE //2 - 32
                        rpos += 8
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos += CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        cpos += 32
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))
                        rpos -= CELL_SIZE //2
                        window.blit(sprite[math.floor(frame)], (cpos, rpos))

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False

    def draw(self, window):
        # Add white background fill and black border
        pygame.draw.rect(window, WHITE, self.rect)  # White background
        pygame.draw.rect(window, BLACK, self.rect, 2)  # Black border
        
        # Draw text
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        window.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

# Constants
GRID_SIZE = (5, 6)
CELL_SIZE = 100
BACKGROUND_COLOR_TOP = (240, 248, 255)     # Lightest azure blue (almost white)
BACKGROUND_COLOR_BOTTOM = (208, 228, 248)   # Soft sky blue
WHITE = (255, 255, 255)  # Making sure WHITE is pure white
BLACK = (0, 0, 0)
X_OFFSET = 10
Y_OFFSET = 180  # Increased from 150 to 200 to move grid down further
FULL_DELAY = 5

def draw_background(window):
    height = window.get_height()
    width = window.get_width()
    
    # Create a vertical gradient (top to bottom)
    for y in range(height):
        # Calculate color for this line with an even smoother transition
        ratio = y / height
        # Use cubic easing for an even smoother gradient
        ratio = ratio * ratio * (3 - 2 * ratio)  # Smoothstep function
        color = (
            int(BACKGROUND_COLOR_TOP[0] * (1 - ratio) + BACKGROUND_COLOR_BOTTOM[0] * ratio),
            int(BACKGROUND_COLOR_TOP[1] * (1 - ratio) + BACKGROUND_COLOR_BOTTOM[1] * ratio),
            int(BACKGROUND_COLOR_TOP[2] * (1 - ratio) + BACKGROUND_COLOR_BOTTOM[2] * ratio)
        )
        pygame.draw.line(window, color, (0, y), (width, y))

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font(None, 36)
bigfont = pygame.font.Font(None, 108)

# Load sprite images and restart icon
try:
    p1_spritesheet = pygame.image.load('yellow.png').convert_alpha()  # Changed to yellow.png
    p2_spritesheet = pygame.image.load('blue.png').convert_alpha()    # Changed to blue.png
    restart_icon = pygame.image.load('restart-icon.png').convert_alpha()
    
    # Remove white background by setting white pixels to transparent
    for x in range(restart_icon.get_width()):
        for y in range(restart_icon.get_height()):
            color = restart_icon.get_at((x, y))
            if color[0] > 240 and color[1] > 240 and color[2] > 240:  # If pixel is white-ish
                restart_icon.set_at((x, y), (255, 255, 255, 0))  # Make it transparent
    
    # Scale the restart icon to match the gem size
    restart_icon = pygame.transform.scale(restart_icon, (32, 32))
    print("Restart icon loaded successfully!")
    
    p1_sprites = []
    p2_sprites = []
    
    # Split spritesheet into individual sprites
    for i in range(8):
        p1_sprites.append(pygame.transform.scale(p1_spritesheet.subsurface((32*i, 0, 32, 32)), (32, 32)))
        p2_sprites.append(pygame.transform.scale(p2_spritesheet.subsurface((32*i, 0, 32, 32)), (32, 32)))
except pygame.error as e:
    print(f"Warning: Could not load images. Error: {e}")
    # Fallback to colored squares if images can't be loaded
    p1_sprites = [pygame.Surface((32, 32)) for _ in range(8)]
    p2_sprites = [pygame.Surface((32, 32)) for _ in range(8)]
    
    # Update fallback colors to match the correct players
    for sprite in p1_sprites:
        sprite.fill((255, 255, 0))  # Yellow for Player 1
    for sprite in p2_sprites:
        sprite.fill((0, 0, 255))    # Blue for Player 2

# Player dropdown menus - adjusted Y positions
player1_dropdown = Dropdown(900, 225, 200, 50, ['Human', 'AI'])  # Moved down more
player2_dropdown = Dropdown(900, 285, 200, 50, ['Human', 'AI'])  # Moved down more
restart_button = Button(900, 345, 200, 50, "Restart", None)  # Moved down more

# Initialize game state variables
current_player = 1  # 1 for Player 1, -1 for Player 2
frame = 0
status = ["It's Player 1's turn to place a gem", ""]
has_winner = False
winner = None
board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)
overflow_boards = Queue()
overflowing = False
numsteps = 0
bots = [PlayerOne(), PlayerTwo()]
grid_col = -1
grid_row = -1
choice = [None, None]

def reset_game():
    global board, current_player, has_winner, winner, status
    board = Board(GRID_SIZE[1], GRID_SIZE[0], p1_sprites, p2_sprites)
    current_player = 1
    has_winner = False
    winner = None
    status = ["It's Player 1's turn to place a gem", ""]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            row = (y - Y_OFFSET) // CELL_SIZE
            col = (x - X_OFFSET) // CELL_SIZE
            
            # Check if click is within the game board
            if (0 <= row < GRID_SIZE[0] and 0 <= col < GRID_SIZE[1]):
                # Check if move is valid and add piece
                if board.valid_move(row, col, current_player):
                    board.add_piece(row, col, current_player)
                    
                    # Check for overflow
                    q = Queue()
                    steps = board.do_overflow(q)
                    
                    # Check for winner
                    result = board.check_win()
                    if result != 0:
                        has_winner = True
                        winner = result
                        status[0] = f"Congratulations! Player {1 if result == 1 else 2} wins!"
                    else:
                        # Switch players
                        current_player = -current_player
                        status[0] = f"It's Player {1 if current_player == 1 else 2}'s turn to place a gem"
        
        # Handle restart button
        if restart_button.handle_event(event):
            reset_game()
        
        # Handle dropdown events
        player1_dropdown.handle_event(event)
        player2_dropdown.handle_event(event)
        choice[0] = player1_dropdown.get_choice()
        choice[1] = player2_dropdown.get_choice()

    # Handle AI moves if it's AI's turn
    if not has_winner:
        if (current_player == 1 and choice[0] == 1) or (current_player == -1 and choice[1] == 1):
            # Get AI move
            if current_player == 1:
                row, col = bots[0].get_play(board.get_board())
            else:
                row, col = bots[1].get_play(board.get_board())
            
            # Make AI move
            if board.valid_move(row, col, current_player):
                board.add_piece(row, col, current_player)
                
                # Check for overflow
                q = Queue()
                steps = board.do_overflow(q)
                
                # Check for winner
                result = board.check_win()
                if result != 0:
                    has_winner = True
                    winner = result
                    status[0] = f"Congratulations! Player {1 if result == 1 else 2} wins!"
                else:
                    # Switch players
                    current_player = -current_player
                    status[0] = f"It's Player {1 if current_player == 1 else 2}'s turn to place a gem"

    # Draw everything
    draw_background(window)
    board.draw(window, frame)
    
    # Draw game title centered over the game grid
    title_font = pygame.font.Font(None, 48)
    title_text = title_font.render("OVERFLOW GAME", True, (0, 46, 93))
    title_rect = title_text.get_rect(center=(580, 80))  # Moved down more
    window.blit(title_text, title_rect)
    
    # Draw player labels and icons - adjusted Y positions
    text = font.render("Player 1:", True, BLACK)
    window.blit(text, (700, 235))  # Moved down more
    text = font.render("Player 2:", True, BLACK)
    window.blit(text, (700, 295))  # Moved down more
    
    # Draw sprites and icons - adjusted Y positions
    window.blit(p1_sprites[math.floor(frame)], (850, 235))  # Moved down more
    window.blit(p2_sprites[math.floor(frame)], (850, 295))  # Moved down more
    window.blit(restart_icon, (850, 355))  # Moved down more
    
    player1_dropdown.draw(window)
    player2_dropdown.draw(window)
    restart_button.draw(window)

    # Draw status text - moved down
    if not has_winner:  
        text = font.render(status[0], True, BLACK)
        window.blit(text, (720, 500))  # Only moved this line down
        text = font.render(status[1], True, BLACK)
        window.blit(text, (720, 500))  # And this matching line
    else:
        text = bigfont.render(f"Player {winner} wins!", True, BLACK)
        text_rect = text.get_rect(center=(600, 250))  # Kept this unchanged
        window.blit(text, text_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()