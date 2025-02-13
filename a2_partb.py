# Evaluation function
def evaluate_board(board, player):
    # Return a high score if player has won
    if check_win(board, player):
        return 1000  # Arbitrary high value for a win
    # Return a low score if player has lost
    if check_win(board, -player):
        return -1000  # Arbitrary low value for a loss

    score = 0
    for row in board:
        for cell in row:
            if cell * player > 0:  # Player's pieces
                score += abs(cell)  # Add the absolute value of the cell
            elif cell * player < 0:  # Opponent's pieces
                score -= abs(cell)  # Subtract the absolute value of the cell
    return score

# Check for a win condition
def check_win(board, player):
    # Check if all pieces on the board are of the same color (i.e., the player has won)
    for row in board:
        for cell in row:
            if cell != 0 and (cell * player < 0):  # If there's any piece not matching the player's color
                return False
    return True


from queue import Queue

class GameTree:
    class Node:
        def __init__(self, board, depth, player, tree_height=4):
            self.board = board  # The board state at this node
            self.depth = depth  # The depth of this node
            self.player = player  # The player who made the move leading to this node
            self.children = []  # List of child nodes
            self.value = None  # The minimax value of this node
            self.best_move = None  # The best move from this node
            
            if depth < tree_height:
                self.generate_children(tree_height)  # Generate the child nodes for this node

        def generate_children(self, tree_height):
            height = len(self.board)
            width = len(self.board[0])

            # First try the (0, 1) position if it's available
            if self.board[0][1] == 0 or (self.board[0][1] / abs(self.board[0][1]) == self.player):
                new_board = [r.copy() for r in self.board]
                new_board[0][1] = self.player
                self.handle_overflow(new_board, 0, 1)

                # Create a child node for the new state
                child = GameTree.Node(new_board, self.depth + 1, -self.player, tree_height)
                self.children.append((child, (0, 1)))  # Add the child node and the move to reach it
            else:
                # If (0, 1) is not available, then proceed with the rest of the board
                for row in range(height):
                    for col in range(width):
                        if self.board[row][col] == 0 or (self.board[row][col] / abs(self.board[row][col]) == self.player):
                            # Simulate a move by placing the player's gem in an empty or friendly space
                            new_board = [r.copy() for r in self.board]
                            new_board[row][col] = self.player
                            self.handle_overflow(new_board, row, col)

                            # Create a child node for the new state
                            child = GameTree.Node(new_board, self.depth + 1, -self.player, tree_height)
                            self.children.append((child, (row, col)))  # Add the child node and the move to reach it

        def handle_overflow(self, board, row, col):
            queue = Queue()
            queue.put((row, col))
            while not queue.empty():
                r, c = queue.get()
                if abs(board[r][c]) >= 4:  # Overflow condition
                    player = board[r][c] // abs(board[r][c])  # Determine whose turn it is
                    board[r][c] = 0  # Reset the current cell
                    neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]  # Neighboring cells
                    for nr, nc in neighbors:
                        if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                            board[nr][nc] += player
                            if abs(board[nr][nc]) >= 4:  # If overflow happens again
                                queue.put((nr, nc))

    def __init__(self, board, player, tree_height=4):
        self.player = player
        self.board = board
        self.tree_height = tree_height
        self.root = GameTree.Node(self.board, 0, self.player, tree_height)

    def minimax(self, node, depth, maximizing_player):
        if depth == self.tree_height or not node.children:
            return evaluate_board(node.board, self.player)

        if maximizing_player:
            max_eval = float('-inf')
            for child, move in node.children:
                eval = self.minimax(child, depth + 1, False)
                if eval > max_eval:
                    max_eval = eval
                    node.best_move = move
            node.value = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for child, move in node.children:
                eval = self.minimax(child, depth + 1, True)
                if eval < min_eval:
                    min_eval = eval
                    node.best_move = move
            node.value = min_eval
            return min_eval

    def get_move(self):
        self.minimax(self.root, 0, True)
        return self.root.best_move

    def clear_tree(self):
        self.root = None

