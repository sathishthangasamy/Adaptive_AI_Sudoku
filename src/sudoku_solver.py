import time

class SudokuSolver:
    def __init__(self):
        pass

    def find_empty(self, board_state):
        """Finds the next empty cell (0) in the board."""
        for r in range(9):
            for c in range(9):
                if board_state[r][c] == 0:
                    return (r, c)  # (row, col)
        return None

    def is_valid(self, board_state, row, col, num):
        """Checks if placing 'num' at (row, col) is valid on the given board_state."""
        if num == 0:
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

    def solve(self, board_state):
        """
        Solves the Sudoku board using backtracking.
        Modifies the board_state in place if a solution is found.
        Returns True if a solution exists, False otherwise.
        """
        find = self.find_empty(board_state)
        if not find:
            return True  # Board is full, solution found

        row, col = find

        for num in range(1, 10):
            if self.is_valid(board_state, row, col, num):
                board_state[row][col] = num

                if self.solve(board_state):
                    return True

                board_state[row][col] = 0  # Backtrack

        return False

    def count_solutions(self, board_state):
        """
        Counts the number of solutions for a given Sudoku board.
        Uses a non-destructive approach (creates copies of the board).
        """
        solutions = 0
        temp_board = [row[:] for row in board_state] # Create a copy to not modify original

        def _count_solutions_recursive(current_board):
            nonlocal solutions
            find = self.find_empty(current_board)
            if not find:
                solutions += 1
                return

            row, col = find
            for num in range(1, 10):
                if self.is_valid(current_board, row, col, num):
                    current_board[row][col] = num
                    _count_solutions_recursive(current_board)
                    current_board[row][col] = 0 # Backtrack

        _count_solutions_recursive(temp_board)
        return solutions

if __name__ == '__main__':
    solver = SudokuSolver()

    # Example puzzle to solve
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    print("Original Puzzle:")
    for r in puzzle:
        print(r)

    start_time = time.time()
    solved_puzzle = [row[:] for row in puzzle] # Create a copy for solving
    if solver.solve(solved_puzzle):
        end_time = time.time()
        print("\nSolved Puzzle:")
        for r in solved_puzzle:
            print(r)
        print(f"Solved in {end_time - start_time:.4f} seconds")
    else:
        print("\nNo solution exists.")

    # Test solution counting
    puzzle_with_multiple_solutions = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]
    ]
    print(f"\nSolutions for empty board: {solver.count_solutions(puzzle_with_multiple_solutions)}") # Should be > 1

    puzzle_with_one_solution = [
        [5,3,0,0,7,0,0,0,0],
        [6,0,0,1,9,5,0,0,0],
        [0,9,8,0,0,0,0,6,0],
        [8,0,0,0,6,0,0,0,3],
        [4,0,0,8,0,3,0,0,1],
        [7,0,0,0,2,0,0,0,6],
        [0,6,0,0,0,0,2,8,0],
        [0,0,0,4,1,9,0,0,5],
        [0,0,0,0,8,0,0,7,9]
    ]
    print(f"Solutions for standard puzzle: {solver.count_solutions(puzzle_with_one_solution)}") # Should be 1