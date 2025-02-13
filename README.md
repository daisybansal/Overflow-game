# Overflow-game

A two-player strategy game built with Pygame where players compete to control the board by placing and stacking gems.

## Game Description

Overflow is a turn-based strategy game where:
- Players take turns placing gems on a 5x6 grid
- Each cell can hold up to 3 gems
- When a fourth gem is added, the stack "overflows" spreading gems to adjacent cells
- The goal is to convert all opponent's gems to your color
- Player 1 uses yellow gems, Player 2 uses blue gems

## Features

- Human vs Human gameplay
- Human vs AI gameplay
- AI vs AI gameplay
- Interactive game board with animated gems
- Simple point-and-click interface
- Player type selection via dropdown menus
- Restart game functionality

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Clone this repository or download the source code
2. Install the required Pygame library: pip install pygame

## How to Run

Run the game using Python: python game.py


## How to Play

1. Launch the game
2. Select player types (Human/AI) using the dropdown menus
3. Click on any valid cell on the grid to place a gem
4. Take turns until one player converts all gems to their color

### Game Rules

- Players start with one gem each (Player 1 in top-left, Player 2 in bottom-right)
- Each turn, a player can place one gem in any empty cell or on their own gems
- When a cell receives a fourth gem, it overflows:
  - The gems spread to adjacent cells (up, down, left, right)
  - All gems in affected cells convert to the overflowing player's color
- Game ends when all gems on the board are the same color

## Credits

- Gem images from [OpenGameArt.org by qubodup](https://opengameart.org/content/rotating-crystal-animation-8-step)
