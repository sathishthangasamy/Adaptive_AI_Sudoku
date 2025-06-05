class SudokuBoard:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.initial_board = [[0 for _ in range(9)] for _ in range(9)] # To keep track of fixed numbers

    def set_board(self, new_board):
        """Sets the current board and stores it as the initial board."""
        self.board = [row[:] for row in new_board]
        self.initial_board = [row[:] for row in new_board]

    def get_board(self):
        return [row[:] for row in self.board]

    def get_initial_board(self):
        return [row[:] for row in self.initial_board]

    def place_number(self, row, col, num):
        if 0 <= row < 9 and 0 <= col < 9 and 0 <= num <= 9:
            self.board[row][col] = num
            return True
        return False

    def is_valid_move(self, board_state, row, col, num):
        """Checks if placing 'num' at (row, col) is valid on the given board_state."""
        if num == 0:  # 0 is considered an empty cell, always valid to place
            return True

        # Check row
        for x in range(9):
            if board_state[row][x] == num and col != x:
                return False

        # Check column
        for x in range(9):
            if board_state[x][col] == num and row != x:
                return False

        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board_state[i + start_row][j + start_col] == num and (i + start_row != row or j + start_col != col):
                    return False
        return True

    def is_board_full(self, board_state):
        """Checks if the given board_state has any empty cells (0)."""
        for r in range(9):
            for c in range(9):
                if board_state[r][c] == 0:
                    return False
        return True

    def is_board_solved(self):
        """Checks if the current board is full and all numbers are valid."""
        temp_board = self.get_board()
        if not self.is_board_full(temp_board):
            return False

        for r in range(9):
            for c in range(9):
                num = temp_board[r][c]
                # Temporarily remove number to validate against itself
                temp_board[r][c] = 0
                if not self.is_valid_move(temp_board, r, c, num):
                    temp_board[r][c] = num # Put it back
                    return False
                temp_board[r][c] = num # Put it back
        return True

    def display(self):
        """Prints the current board to the console."""
        for r in range(9):
            if r % 3 == 0 and r != 0:
                print("- - - - - - - - - - - - ")
            for c in range(9):
                if c % 3 == 0 and c != 0:
                    print(" | ", end="")
                print(self.board[r][c] if self.board[r][c] != 0 else ".", end=" ")
            print()
        print("\n")

if __name__ == '__main__':
    # Simple test for SudokuBoard
    board = SudokuBoard()
    board.set_board([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])
    print("Initial Board:")
    board.display()
    print(f"Is board full? {board.is_board_full(board.get_board())}")
    print(f"Is board solved? {board.is_board_solved()}")

    # Test a valid move
    print(f"Is 1 valid at (0,2)? {board.is_valid_move(board.get_board(), 0, 2, 1)}") # Should be True
    # Test an invalid move
    print(f"Is 5 valid at (0,0)? {board.is_valid_move(board.get_board(), 0, 0, 5)}") # Should be False (already there)
    print(f"Is 3 valid at (0,1)? {board.is_valid_move(board.get_board(), 0, 1, 3)}") # Should be False (already there)

    # Test placing a number
    board.place_number(0, 2, 1)
    print("After placing 1 at (0,2):")
    board.display()