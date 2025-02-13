import pygame
import time
import random

# Constants
TIME_LIMIT = 10  # Time limit for each player to make a move
WIDTH, HEIGHT = 800, 600
GRID_SIZE = (8, 8)
CELL_SIZE = 70
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()

class GameTimer:
    def __init__(self):
        self.start_time = 0
        self.elapsed_time = 0

    def start(self):
        self.start_time = time.time()

    def get_time_left(self):
        self.elapsed_time = time.time() - self.start_time
        return max(TIME_LIMIT - self.elapsed_time, 0)

class PowerUp:
    def __init__(self):
        self.power_ups = {
            "skip_turn": False,
            "extra_move": False,
            "board_swap": False
        }

    def activate(self, power_up_type):
        if power_up_type in self.power_ups:
            self.power_ups[power_up_type] = True

    def use_power_up(self, power_up_type, game_state):
        if self.power_ups.get(power_up_type, False):
            if power_up_type == "skip_turn":
                game_state.skip_turn = True
            elif power_up_type == "extra_move":
                game_state.extra_move = True
            elif power_up_type == "board_swap":
                game_state.board_swap = True
            self.power_ups[power_up_type] = False

class Board:
    def __init__(self):
        self.board = [[0 for _ in range(GRID_SIZE[0])] for _ in range(GRID_SIZE[1])]
        self.valid_moves = []
        self.highlight_moves = []

    def update_valid_moves(self, player):
        self.valid_moves = []
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                if self.board[row][col] == 0:  # Empty spot
                    self.valid_moves.append((row, col))
        self.highlight_moves = self.valid_moves

    def draw(self, window):
        for row in range(GRID_SIZE[0]):
            for col in range(GRID_SIZE[1]):
                rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                color = WHITE if self.board[row][col] == 0 else BLACK
                pygame.draw.rect(window, color, rect)

        # Highlight valid moves
        for move in self.highlight_moves:
            row, col = move
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(window, GREEN, rect, 5)

class GameState:
    def __init__(self):
        self.current_player = 0  # 0 = Player 1, 1 = Player 2
        self.skip_turn = False
        self.extra_move = False
        self.board_swap = False

    def switch_turn(self):
        self.current_player = 1 - self.current_player
        self.skip_turn = False
        self.extra_move = False
        self.board_swap = False

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Gem Game")
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.timer = GameTimer()
        self.power_up = PowerUp()
        self.game_state = GameState()

    def start_turn(self):
        self.timer.start()

    def handle_move(self, row, col):
        if self.board.board[row][col] == 0:  # Valid move
            self.board.board[row][col] = 1 if self.game_state.current_player == 0 else -1
            self.board.update_valid_moves(self.game_state.current_player)
            return True
        return False

    def draw(self):
        self.window.fill(WHITE)
        self.board.draw(self.window)
        pygame.display.update()

    def check_time_limit(self):
        if self.timer.get_time_left() == 0:
            self.game_state.switch_turn()

def main():
    game = Game()
    game.start_turn()

    running = True
    while running:
        game.draw()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                row, col = y // CELL_SIZE, x // CELL_SIZE
                if game.handle_move(row, col):
                    game.game_state.switch_turn()
                    game.start_turn()

        game.check_time_limit()
        game.clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()


